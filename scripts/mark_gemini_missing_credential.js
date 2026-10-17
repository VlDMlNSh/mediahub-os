'use strict';

const fs = require('node:fs');
const path = require('node:path');

function markMissingCredential(manifestPath) {
  if (!manifestPath) throw new TypeError('manifestPath is required');
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  if (manifest.status !== 'PREPARED' || manifest.provider_status !== 'NOT_STARTED') {
    throw new Error('only a PREPARED/NOT_STARTED manifest can be blocked for missing credentials');
  }

  manifest.status = 'BLOCKED_MISSING_CREDENTIAL';
  manifest.provider_status = 'MISSING_CREDENTIAL';
  manifest.failure_class = 'missing_credential';
  manifest.output_sha256 = null;
  manifest.output_bytes = null;
  manifest.finished_at = new Date().toISOString();

  const directory = path.dirname(manifestPath);
  const temporaryPath = path.join(directory, '.evidence-manifest-' + process.pid + '.tmp');
  fs.writeFileSync(temporaryPath, JSON.stringify(manifest, null, 2) + '\n', { mode: 0o600, flag: 'wx' });
  fs.renameSync(temporaryPath, manifestPath);
  return manifest;
}

if (require.main === module) {
  try {
    if (process.argv.length !== 3) throw new Error('usage: node mark_gemini_missing_credential.js <manifest-path>');
    markMissingCredential(process.argv[2]);
  } catch (error) {
    console.error('Unable to finalize missing-credential manifest: ' + String(error.message || error).slice(0, 200));
    process.exitCode = 1;
  }
}

module.exports = { markMissingCredential };
