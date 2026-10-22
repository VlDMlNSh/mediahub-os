'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const { readBoundedResponse } = require('./gemini_http_response');

function listen(server) {
  return new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.removeListener('error', reject);
      resolve(server.address().port);
    });
  });
}

function close(server) {
  return new Promise(resolve => server.close(() => resolve()));
}

function requestAndMaybeWrite(port, route, outputPath, maxBytes = 128) {
  return new Promise(resolve => {
    let finished = false;
    const finish = value => {
      if (finished) return;
      finished = true;
      resolve(value);
    };
    const req = http.get({ hostname: '127.0.0.1', port, path: route }, async res => {
      try {
        const response = await readBoundedResponse(res, req, maxBytes);
        if (response.statusCode < 200 || response.statusCode >= 300) {
          finish({ ok: false, reason: 'non_2xx' });
          return;
        }
        let parsed;
        try { parsed = JSON.parse(response.body); }
        catch { finish({ ok: false, reason: 'invalid_json' }); return; }
        const output = (parsed.candidates || [])
          .flatMap(candidate => candidate.content?.parts || [])
          .map(part => part.text || '')
          .join('\n').trim();
        if (!output || Buffer.byteLength(output, 'utf8') > 100000) {
          finish({ ok: false, reason: 'invalid_output' });
          return;
        }
        fs.writeFileSync(outputPath, output, { mode: 0o600, flag: 'wx' });
        finish({ ok: true });
      } catch (error) {
        finish({ ok: false, reason: String(error.message) });
      }
    });
    req.on('error', error => finish({ ok: false, reason: String(error.message) }));
  });
}

async function main() {
  const validBody = JSON.stringify({ candidates: [{ content: { parts: [{ text: 'audit' }, { text: 'complete' }] } }] });
  const server = http.createServer((req, res) => {
    if (req.url === '/valid') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(validBody);
    } else if (req.url === '/non-2xx') {
      res.writeHead(503, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'unavailable' }));
    } else if (req.url === '/over-limit') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end('x'.repeat(4096));
    } else if (req.url === '/truncated') {
      res.writeHead(200, { 'Content-Type': 'application/json', 'Content-Length': '100' });
      res.write('{"candidates":');
      res.socket.destroy();
    } else {
      res.writeHead(404);
      res.end();
    }
  });

  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'gemini-http-regression-'));
  const port = await listen(server);
  try {
    const validPath = path.join(tempDir, 'valid.md');
    const valid = await requestAndMaybeWrite(port, '/valid', validPath, 8192);
    assert.equal(valid.ok, true, 'complete valid response should produce an artifact');
    assert.equal(fs.readFileSync(validPath, 'utf8'), 'audit\ncomplete');

    for (const route of ['/non-2xx', '/over-limit', '/truncated']) {
      const outputPath = path.join(tempDir, route.slice(1) + '.md');
      const result = await requestAndMaybeWrite(port, route, outputPath, 128);
      assert.equal(result.ok, false, route + ' must be rejected');
      assert.equal(fs.existsSync(outputPath), false, route + ' must not produce an artifact');
    }

    console.log('PASS: complete valid response writes output; non-2xx, over-limit, and truncated responses do not.');
  } finally {
    await close(server);
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
