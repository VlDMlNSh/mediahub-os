# MH-18 — Storage Abstraction
Status: PROPOSED / NOT ACCEPTED

Logical API: put/read/range/stat/delete/move/copy/verify with capability-scoped locators and bounded operations. Storage adapters expose value results, not mutable domain objects. Atomicity, durability, consistency and encryption semantics must be declared per backend. Physical paths remain implementation details.