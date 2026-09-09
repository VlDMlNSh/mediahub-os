class AIAdapter:
    def __init__(self):
        self.is_denied = True
        self.authorized = False
        self.data_minimized = False
        self.egress_policy = None
        self.residency_policy = None
        self.timeout_retry = None
        self.response_provenance = None
        self.audit_events = None
