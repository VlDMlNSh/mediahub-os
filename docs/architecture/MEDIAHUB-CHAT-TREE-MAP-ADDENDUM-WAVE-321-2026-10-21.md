# Map addendum — Wave 321 post-merge regression

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)

- Evidence: [Wave 321 post-merge verification and HMAC test regression](../checkpoints/MEDIAHUB-MERGE-AND-CI-REGRESSION-WAVE-321-2026-10-21.md).
- PR #432 merged as `1a6e5a16ef9950b72dda04abd69a27f019922489`; final PR head `33ae44f3ca77337553b97819f5190d57d157fe5e`. Controller and child workflow changes are now on main.
- Post-merge CI failed: compileall run [39648761007](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761007) and transport contract run [39648761390](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648761390), both caused by a missing closing parenthesis in the new HMAC contract test at line 140.
- Minimal one-character syntax correction proposed in [Draft PR #434](https://github.com/VlDMlNSh/mediahub-os/pull/434), head `04442fe0aac243499231b1233e0a84eff0a33ede`, test blob `785618fad51ecf898b35132f6e43b196a18f7eae`. Exact-head CI was in progress at report creation.
- Formal review API for PR #432 returns zero submitted reviews. Merge does not prove independent review acceptance.
- Gemini 1–3 and Claude/agent-browser on Alamo remain NOT RUN. Only `Voktors-Mini.Dlink` is operational in SentinelX; Alamo identity/route remains unverified.
- Next: verify exact-head CI for PR #434, then retain fail-closed agent dispatch until governance, independent review and executor identity gates are proven.
