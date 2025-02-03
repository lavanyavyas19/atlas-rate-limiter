import time
from collections import defaultdict

class UsageLogger:
    def __init__(self):
        self.requests = defaultdict(list)
        self.violations = defaultdict(list)

    def log_request(self, key: str):
        self.requests[key].append(time.time())

    def log_violation(self, key: str):
        self.violations[key].append(time.time())

    def get_stats(self):
        return {
            "total_clients": len(self.requests),
            "total_requests": sum(len(v) for v in self.requests.values()),
            "total_violations": sum(len(v) for v in self.violations.values()),
        }
