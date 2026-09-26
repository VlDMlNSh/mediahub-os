package components

import "context"

type Message struct { Subject string; Key string; Data []byte; Schema string }
type Transport interface { Contract; Publish(context.Context, Message) error; Subscribe(context.Context, string, func(Message) error) error }

type Coordination interface { Contract; Acquire(ctx context.Context, key string) (release func() error, err error) }

// Transport and coordination are future-gated. They cannot become implicit state authorities.
