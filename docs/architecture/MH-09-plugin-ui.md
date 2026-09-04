# MH-09 — Plugin UI Boundary

**Status:** PROPOSED / REQUIRES VERIFICATION

Plugin-rendered UI is untrusted presentation input unless separately qualified. Plugin UI receives only declared, explicitly authorized capabilities and bounded data.

Forbidden: inherited State Authority access, raw transaction access, unrestricted filesystem/network, implicit capabilities, execution through rendering, or authority inferred from plugin registration or UI visibility. All plugin actions re-enter the normal authorization and Consumer Boundary path. MH-8 remains the plugin governance authority.
