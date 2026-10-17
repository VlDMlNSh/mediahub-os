'use strict';

const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');

const OUTPUT_PREFIX = '<!-- Untrusted model-generated advisory output; not execution authority -->\n';
const MAX_OUTPUT_BYTES = 100000;

function persistManifest(manifestPath, manifest) {
  const tempPath = path.join(path.dirname(manifestPath), `.evidence-manifest.${process.pid}.${crypto.randomBytes(6).toString('hex')}.tmp`);
  fs.writeFileSync(tempPath, JSON.stringify(manifest, null, 2) + '\n', { mode: 0o600, flag: 'wx' });
  try {
    fs.renameSync(tempPath, manifestPath);
  } catch (error) {
    try { fs.unlinkSync(tempPath); } catch {}
    throw error;
  }
}

function finalizeTransportError({ manifest, manifestPath, error, now = () => new Date().toISOString(), providerStatus = 'TRANSPORT_ERROR', failureClass = null }) {
  const message = String(error && error.message || 'transport error').slice(0, 160);
  manifest.status = 'FAILED';
  manifest.provider_status = providerStatus;
  manifest.failure_class = failureClass || (message.includes('byte limit') ? 'response_too_large' : 'incomplete_or_failed_response');
  manifest.output_sha256 = null;
  manifest.output_bytes = null;
  manifest.finished_at = now();
  persistManifest(manifestPath, manifest);
  return { ok: false, exitCode: 34, message };
}

function finalizeProviderResponse({ response, manifest, manifestPath, outputPath, now = () => new Date().toISOString(), maxOutputBytes = MAX_OUTPUT_BYTES }) {
  const statusCode = response?.statusCode;
  manifest.provider_request_id = response?.requestId || response?.headers?.['x-goog-request-id'] || response?.headers?.['x-request-id'] || null;
  manifest.finished_at = now();

  if (!Number.isInteger(statusCode) || statusCode < 100 || statusCode > 599) {
    manifest.status = 'FAILED';
    manifest.provider_status = 'INVALID_STATUS';
    manifest.failure_class = 'invalid_status';
    manifest.output_sha256 = null;
    manifest.output_bytes = null;
    persistManifest(manifestPath, manifest);
    return { ok: false, exitCode: 32, reason: 'invalid_status' };
  }

  manifest.provider_status = `HTTP_${statusCode}`;
  if (statusCode < 200 || statusCode >= 300) {
    manifest.status = 'FAILED';
    manifest.failure_class = statusCode === 429 ? 'quota_or_rate_limit' : 'provider_http_error';
    manifest.output_sha256 = null;
    manifest.output_bytes = null;
    persistManifest(manifestPath, manifest);
    return { ok: false, exitCode: 31, reason: 'non_2xx' };
  }

  let parsed;
  try {
    parsed = JSON.parse(response.body);
  } catch {
    manifest.status = 'FAILED';
    manifest.provider_status = 'INVALID_JSON';
    manifest.failure_class = 'invalid_json';
    manifest.output_sha256 = null;
    manifest.output_bytes = null;
    persistManifest(manifestPath, manifest);
    return { ok: false, exitCode: 32, reason: 'invalid_json' };
  }

  const output = (parsed.candidates || [])
    .flatMap(candidate => candidate.content?.parts || [])
    .map(part => part.text || '')
    .join('\n').trim();
  const outputBytes = Buffer.byteLength(output, 'utf8');
  if (!output || outputBytes > maxOutputBytes) {
    const tooLarge = Boolean(output);
    manifest.status = 'FAILED';
    manifest.provider_status = tooLarge ? 'OUTPUT_TOO_LARGE' : 'EMPTY_OUTPUT';
    manifest.failure_class = tooLarge ? 'output_too_large' : 'empty_output';
    manifest.output_sha256 = null;
    manifest.output_bytes = null;
    persistManifest(manifestPath, manifest);
    return { ok: false, exitCode: 33, reason: tooLarge ? 'output_too_large' : 'empty_output' };
  }

  const artifact = OUTPUT_PREFIX + output + '\n';
  const artifactBytes = Buffer.from(artifact, 'utf8');
  fs.writeFileSync(outputPath, artifactBytes, { mode: 0o600, flag: 'wx' });
  manifest.status = 'COMPLETED';
  manifest.failure_class = null;
  manifest.output_sha256 = `sha256:${crypto.createHash('sha256').update(artifactBytes).digest('hex')}`;
  manifest.output_bytes = artifactBytes.length;
  persistManifest(manifestPath, manifest);
  return { ok: true, exitCode: 0, output, outputSha256: manifest.output_sha256, outputBytes: artifactBytes.length };
}

module.exports = { MAX_OUTPUT_BYTES, finalizeProviderResponse, finalizeTransportError };
