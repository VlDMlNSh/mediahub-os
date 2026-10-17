'use strict';

const DEFAULT_MAX_RESPONSE_BYTES = 2 * 1024 * 1024;

/**
 * Read a complete HTTP response while enforcing a byte limit.
 * The response body is never exposed until the end event confirms completion.
 */
function readBoundedResponse(res, req, maxBytes = DEFAULT_MAX_RESPONSE_BYTES) {
  if (!Number.isSafeInteger(maxBytes) || maxBytes < 1) {
    return Promise.reject(new TypeError('maxBytes must be a positive safe integer'));
  }

  return new Promise((resolve, reject) => {
    let settled = false;
    let receivedBytes = 0;
    const chunks = [];

    const fail = error => {
      if (settled) return;
      settled = true;
      reject(error instanceof Error ? error : new Error('HTTP response failed'));
    };

    res.on('data', chunk => {
      if (settled) return;
      const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      receivedBytes += buffer.length;
      if (receivedBytes > maxBytes) {
        const error = new Error('response byte limit exceeded');
        fail(error);
        res.destroy();
        if (req && !req.destroyed) req.destroy(error);
        return;
      }
      chunks.push(buffer);
    });

    res.on('aborted', () => fail(new Error('response aborted before completion')));
    res.on('error', error => fail(error));
    res.on('end', () => {
      if (settled) return;
      if (res.complete === false) {
        fail(new Error('response ended before HTTP message completion'));
        return;
      }
      settled = true;
      resolve({
        statusCode: res.statusCode || 0,
        headers: res.headers || {},
        body: Buffer.concat(chunks).toString('utf8'),
        receivedBytes
      });
    });
  });
}

module.exports = { DEFAULT_MAX_RESPONSE_BYTES, readBoundedResponse };
