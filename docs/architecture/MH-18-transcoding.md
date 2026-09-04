# MH-18 — Transcoding
Status: PROPOSED / NOT ACCEPTED

Transcoding is an isolated derived-artifact job: input asset → bounded worker → output derivative → integrity/validation → registration. Jobs require queue identity, resource quota, cancellation, timeout, retry budget and observable status. It cannot mutate canonical metadata directly. FFmpeg/GStreamer/VLC remain CANDIDATE only.