package adapters

import "context"

type Inference interface {
	Component() Component
	Health(ctx context.Context) error
	Infer(ctx context.Context, request []byte) ([]byte, error)
}

type AIRouter interface {
	Route(ctx context.Context, request []byte, localAvailable bool, clusterAvailable bool) (Route, error)
}

type Route string
const (
	RouteLocal Route = "local"
	RouteCluster Route = "cluster"
	RouteCloudDevelopment Route = "cloud-development"
)

func (r Route) Valid() bool { return r == RouteLocal || r == RouteCluster || r == RouteCloudDevelopment }
