package components

import "context"

type SmartHomeEvent struct { EntityID string; Type string; Payload []byte }

type SmartHome interface {
	Contract
	Subscribe(ctx context.Context, entityID string) (<-chan SmartHomeEvent, error)
	Call(ctx context.Context, entityID string, service string, payload []byte) error
}

// SmartHomeAuthority explicitly separates Home Assistant Core authority from
// MediaHub State Authority. This adapter is the only permitted HA integration path.
type SmartHomeAuthority interface {
	SmartHome
	AuthorityDomain() string
}
