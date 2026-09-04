# MH-12 Plugin Security

Plugin is an extension, not an authority. It cannot self-authorize, self-grant, use wildcard capabilities, inherit another plugin's authority, directly mutate State Authority, bypass Consumer Boundary, or gain unrestricted filesystem/network/subprocess access.

Signature establishes integrity/provenance evidence only; installation does not establish runtime trust. Plugin path: identity → capability → authorization → Consumer Boundary → State Authority.
