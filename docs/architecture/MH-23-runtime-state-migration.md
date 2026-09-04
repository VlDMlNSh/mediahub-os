# MH-23 Runtime State Migration

Old representation → validated migration → one canonical State Authority. During migration there must not be two competing canonical authorities. Candidate state is validated before atomic publication; stale generations fail closed; restore remains explicit.