# MH-18 — Content Model
Status: PROPOSED / NOT ACCEPTED

Canonical entities:
- Content: logical user-visible media work.
- Asset: a concrete acquired representation of Content.
- Object/File: physical byte object belonging to an Asset.
- Metadata: attributed descriptive facts.
- Derivative: rebuildable representation such as thumbnail/transcode/index entry.
- Provenance: source and transformation history.
- Catalog: canonical read model derived from authorized state.

Invariants: Content identity != filename/path/URL/digest. Derived artifacts never become canonical truth. Runtime state remains owned by State Authority.

Minimum asset fields: content_id, asset_id, object_id, media_type, size, digest, source, lifecycle_state, provenance_ref, schema_version.
