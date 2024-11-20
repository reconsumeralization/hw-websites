import time
import psutil
import logging
from datetime import datetime

class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger('system_monitor')
        self.logger.setLevel(logging.INFO)

        # Add file handler
        fh = logging.FileHandler('system_monitor.log')
        fh.setLevel(logging.INFO)
        self.logger.addHandler(fh)

    def monitor_resources(self):
        """Monitor system resources"""
        while True:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            self.logger.info(
                f"[{datetime.now()}] CPU: {cpu_percent}%, "
                f"Memory: {memory_percent}%, "
                f"Disk: {disk_percent}%"
            )

            # Alert if resources are running low
            if cpu_percent > 90 or memory_percent > 90 or disk_percent > 90:
                self.logger.warning(
                    f"[{datetime.now()}] Resource usage critical! "
                    f"CPU: {cpu_percent}%, "
                    f"Memory: {memory_percent}%, "
                    f"Disk: {disk_percent}%"
                )

            time.sleep(60)  # Check every minute
