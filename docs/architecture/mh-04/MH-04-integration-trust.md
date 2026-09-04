# MH-04 Integration Trust

Integration Boundary is a trust boundary, not a trust grant.

External protocol adapters must normalize identity, validate input and establish the principal/context before command authorization.

Device/protocol reachability does not imply capability. Invalid, unknown or malformed integration input is rejected; unknown external principals/devices may be quarantined.

Integration cannot write canonical state outside the inherited Consumer Contract and State Authority path.