import time
from collections import defaultdict
from typing import Dict


class UsageLogger:
    """
    Tracks overall and per-client usage statistics:
    - total requests
    - total violations
    - per-client request and violation counts
    """

    def __init__(self) -> None:
        self.total_requests: int = 0
        self.total_violations: int = 0
        self.requests_per_client: Dict[str, int] = defaultdict(int)
        self.violations_per_client: Dict[str, int] = defaultdict(int)

    def log_request(self, client_id: str) -> None:
        self.total_requests += 1
        self.requests_per_client[client_id] += 1

    def log_violation(self, client_id: str) -> None:
        self.total_violations += 1
        self.violations_per_client[client_id] += 1

    def get_stats(self) -> dict:
        """
        Global statistics across all clients.
        """
        return {
            "total_requests": self.total_requests,
            "total_violations": self.total_violations,
            "clients_tracked": len(self.requests_per_client),
        }

    def get_client_stats(self, client_id: str) -> dict:
        """
        Statistics for a specific client.
        """
        return {
            "client_id": client_id,
            "requests": self.requests_per_client.get(client_id, 0),
            "violations": self.violations_per_client.get(client_id, 0),
        }
