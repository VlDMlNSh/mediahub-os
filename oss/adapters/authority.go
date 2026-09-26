package adapters

// AuthorityDomain declares the only domain in which an upstream component may
// be authoritative. An empty value means the component has no authority.
type AuthorityDomain string

const (
	NoAuthority      AuthorityDomain = ""
	SmartHomeDomain  AuthorityDomain = "smart-home"
	MediaHubState    AuthorityDomain = "mediahub-state-authority"
)

// ValidateAuthority prevents accidental authority escalation.
func ValidateAuthority(componentID string, domain AuthorityDomain) error {
	switch componentID {
	case "home-assistant-core":
		if domain != SmartHomeDomain {
			return ErrForbiddenAuthority
		}
	default:
		if domain != NoAuthority {
			return ErrForbiddenAuthority
		}
	}
	return nil
}
