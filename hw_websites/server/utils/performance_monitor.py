import time
from dataclasses import dataclass
from typing import Dict, List
import requests

@dataclass
class PageMetrics:
    load_time: float
    size: int
    resource_count: int
    errors: List[str]

class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, PageMetrics] = {}

    def measure_page_performance(self, url: str) -> PageMetrics:
        start_time = time.time()

        try:
            response = requests.get(url)
            load_time = time.time() - start_time

            metrics = PageMetrics(
                load_time=load_time,
                size=len(response.content),
                resource_count=len(response.links),
                errors=[]
            )

            self.metrics[url] = metrics
            return metrics

        except Exception as e:
            return PageMetrics(
                load_time=0,
                size=0,
                resource_count=0,
                errors=[str(e)]
            )
