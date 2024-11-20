import psutil
import requests
import time
import logging
from pathlib import Path

class SiteMonitor:
    def __init__(self):
        self.sites = ['hwroads.com', 'hwasphaltfl.com']
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(
            filename='monitoring.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def check_site_health(self):
        """Check if sites are responding"""
        for site in self.sites:
            try:
                response = requests.get(f'https://{site}')
                if response.status_code == 200:
                    logging.info(f'{site} is up')
                else:
                    logging.error(f'{site} returned status code {response.status_code}')
            except Exception as e:
                logging.error(f'Error checking {site}: {str(e)}')

    def monitor_resources(self):
        """Monitor system resources"""
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        logging.info(f'CPU Usage: {cpu_percent}%')
        logging.info(f'Memory Usage: {memory_percent}%')

if __name__ == "__main__":
    monitor = SiteMonitor()
    while True:
        monitor.check_site_health()
        monitor.monitor_resources()
        time.sleep(300)  # Check every 5 minutes
