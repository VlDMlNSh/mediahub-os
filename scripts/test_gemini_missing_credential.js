'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { markMissingCredential } = require('./mark_gemini_missing_credential');

const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-manifest-finalizer-'));
try {
  const manifestPath = path.join(directory, 'evidence-manifest.json');
  const initial = {
    schema_version: 'mediahub.gemini-readonly-evidence.v1',
    status: 'PREPARED',
    provider_status: 'NOT_STARTED',
    output_sha256: null,
    output_bytes: null,
    finished_at: null
  };
  fs.writeFileSync(manifestPath, JSON.stringify(initial), { mode: 0o600 });

  const result = markMissingCredential(manifestPath);
  assert.equal(result.status, 'BLOCKED_MISSING_CREDENTIAL');
  assert.equal(result.provider_status, 'MISSING_CREDENTIAL');
  assert.equal(result.failure_class, 'missing_credential');
  assert.equal(result.output_sha256, null);
  assert.equal(result.output_bytes, null);
  assert.ok(Number.isFinite(Date.parse(result.finished_at)));
  assert.deepEqual(JSON.parse(fs.readFileSync(manifestPath, 'utf8')), result);
  assert.equal(fs.readdirSync(directory).some(name => name.endsWith('.tmp')), false);

  assert.throws(() => markMissingCredential(manifestPath), /only a PREPARED\/NOT_STARTED manifest/);
  console.log('PASS: missing credential writes a terminal manifest atomically; non-prepared states are rejected.');
} finally {
  fs.rmSync(directory, { recursive: true, force: true });
}
