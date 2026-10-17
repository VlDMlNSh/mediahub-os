'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { finalizeProviderResponse, finalizeTransportError } = require('./gemini_provider_outcome');

function setup() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-provider-outcome-'));
  const manifestPath = path.join(dir, 'evidence-manifest.json');
  const outputPath = path.join(dir, 'gemini-audit.md');
  const manifest = {
    status: 'PREPARED', provider_status: 'NOT_STARTED', output_sha256: null,
    output_bytes: null, failure_class: null, finished_at: null
  };
  fs.writeFileSync(manifestPath, JSON.stringify(manifest), { mode: 0o600 });
  return { dir, manifestPath, outputPath, manifest };
}

function readManifest(testCase) {
  return JSON.parse(fs.readFileSync(testCase.manifestPath, 'utf8'));
}

function assertFailed(testCase, result, expectedProviderStatus, expectedFailureClass) {
  assert.equal(result.ok, false);
  const manifest = readManifest(testCase);
  assert.equal(manifest.status, 'FAILED');
  assert.equal(manifest.provider_status, expectedProviderStatus);
  assert.equal(manifest.failure_class, expectedFailureClass);
  assert.equal(manifest.output_sha256, null);
  assert.equal(manifest.output_bytes, null);
  assert.ok(manifest.finished_at);
  assert.equal(fs.existsSync(testCase.outputPath), false, 'failed outcome must not write model output');
}

function response(statusCode, body, headers = {}) {
  return { statusCode, body, headers };
}

function run() {
  const cases = [
    { name: 'missing HTTP status', response: response(undefined, '{"candidates":[{"content":{"parts":[{"text":"must not be accepted"}]}}]}'), provider: 'INVALID_STATUS', failure: 'invalid_status', exitCode: 32 },
    { name: 'HTTP status below range', response: response(99, '{"candidates":[]}'), provider: 'INVALID_STATUS', failure: 'invalid_status', exitCode: 32 },
    { name: 'HTTP status above range', response: response(600, '{"candidates":[]}'), provider: 'INVALID_STATUS', failure: 'invalid_status', exitCode: 32 },
    { name: 'HTTP 429', response: response(429, '{"error":"rate limited"}'), provider: 'HTTP_429', failure: 'quota_or_rate_limit', exitCode: 31 },
    { name: 'HTTP 503', response: response(503, '{"error":"unavailable"}'), provider: 'HTTP_503', failure: 'provider_http_error', exitCode: 31 },
    { name: 'invalid JSON', response: response(200, '{"candidates":'), provider: 'INVALID_JSON', failure: 'invalid_json', exitCode: 32 },
    { name: 'empty output', response: response(200, '{"candidates":[]}'), provider: 'EMPTY_OUTPUT', failure: 'empty_output', exitCode: 33 },
    { name: 'oversized output', response: response(200, JSON.stringify({ candidates: [{ content: { parts: [{ text: 'x'.repeat(101) }] } }] })), provider: 'OUTPUT_TOO_LARGE', failure: 'output_too_large', exitCode: 33, maxOutputBytes: 100 }
  ];
  for (const item of cases) {
    const testCase = setup();
    try {
      const result = finalizeProviderResponse({
        response: item.response, manifest: testCase.manifest,
        manifestPath: testCase.manifestPath, outputPath: testCase.outputPath,
        maxOutputBytes: item.maxOutputBytes || 100000,
        now: () => '2026-10-18T00:00:00.000Z'
      });
      assert.equal(result.exitCode, item.exitCode, item.name);
      assertFailed(testCase, result, item.provider, item.failure);
      console.log('PASS:', item.name, 'produces terminal FAILED manifest without output');
    } finally { fs.rmSync(testCase.dir, { recursive: true, force: true }); }
  }

  for (const item of [
    { name: 'transport failure', message: 'socket hang up', failure: 'incomplete_or_failed_response' },
    { name: 'oversized transport response', message: 'response byte limit exceeded', failure: 'response_too_large' }
  ]) {
    const testCase = setup();
    try {
      const result = finalizeTransportError({
        manifest: testCase.manifest, manifestPath: testCase.manifestPath,
        error: new Error(item.message), now: () => '2026-10-18T00:00:00.000Z'
      });
      assert.equal(result.exitCode, 34);
      assertFailed(testCase, result, 'TRANSPORT_ERROR', item.failure);
      console.log('PASS:', item.name, 'produces terminal FAILED manifest without output');
    } finally { fs.rmSync(testCase.dir, { recursive: true, force: true }); }
  }

  const testCase = setup();
  try {
    const body = JSON.stringify({ candidates: [{ content: { parts: [{ text: 'audit result' }, { text: 'second part' }] } }] });
    const result = finalizeProviderResponse({
      response: response(200, body, { 'x-goog-request-id': 'request-test-123' }),
      manifest: testCase.manifest, manifestPath: testCase.manifestPath, outputPath: testCase.outputPath,
      now: () => '2026-10-18T00:00:00.000Z'
    });
    const manifest = readManifest(testCase);
    const artifact = fs.readFileSync(testCase.outputPath);
    assert.equal(result.ok, true);
    assert.equal(manifest.status, 'COMPLETED');
    assert.equal(manifest.provider_status, 'HTTP_200');
    assert.equal(manifest.provider_request_id, 'request-test-123');
    assert.equal(manifest.output_sha256, 'sha256:' + crypto.createHash('sha256').update(artifact).digest('hex'));
    assert.equal(manifest.output_bytes, artifact.length);
    assert.equal(manifest.failure_class, null);
    assert.equal(manifest.finished_at, '2026-10-18T00:00:00.000Z');
    assert.match(artifact.toString('utf8'), /Untrusted model-generated advisory output/);
    console.log('PASS: successful response writes artifact with exact digest and byte count');
  } finally { fs.rmSync(testCase.dir, { recursive: true, force: true }); }
}

run();
