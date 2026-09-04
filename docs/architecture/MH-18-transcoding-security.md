# MH-18 — Transcoding Security
Status: PROPOSED / NOT ACCEPTED

Untrusted parsers/codecs are security-sensitive. Worker isolation must restrict filesystem scope, network, subprocess privileges and resource usage. No arbitrary shell or executable codec installation. Archive bombs, oversized media, malformed containers and parser crashes are treated as hostile input. Exact sandbox technology requires threat-model evidence and ADR.