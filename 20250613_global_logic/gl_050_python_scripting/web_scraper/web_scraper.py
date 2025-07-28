#!/usr/bin/env python3
"""
Web Scraper with Error Handling - DevOps Example

This script demonstrates web scraping techniques commonly used in DevOps:
- API endpoint monitoring
- Service health checking
- Data collection from web services
- Rate limiting and retry logic
- Concurrent requests handling

Key Python concepts demonstrated:
- HTTP requests with error handling
- Async/await for concurrent operations
- Context managers for resource management
- Custom exceptions
- Data validation and parsing
- Rate limiting implementations
"""

import asyncio
import aiohttp
import requests
import time
import json
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
import logging
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScrapingError(Exception):
    """Custom exception for scraping-related errors."""
    pass


class RateLimitError(ScrapingError):
    """Exception raised when rate limit is exceeded."""
    pass


@dataclass
class ServiceStatus:
    """Data class for service health status."""
    url: str
    status_code: int
    response_time: float
    timestamp: datetime
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RateLimiter:
    """Simple rate limiter implementation."""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    def can_proceed(self) -> bool:
        """Check if we can make another request."""
        now = time.time()
        # Remove old requests outside the time window
        self.requests = [req_time for req_time in self.requests 
                        if now - req_time < self.time_window]
        
        return len(self.requests) < self.max_requests
    
    def add_request(self):
        """Record a new request."""
        self.requests.append(time.time())
    
    def wait_time(self) -> float:
        """Calculate how long to wait before next request."""
        if not self.requests:
            return 0
        
        oldest_request = min(self.requests)
        wait_time = self.time_window - (time.time() - oldest_request)
        return max(0, wait_time)


class WebScraper:
    """Web scraper with comprehensive error handling and rate limiting."""
    
    def __init__(self, base_url: str = "", rate_limit: tuple = (10, 60)):
        self.base_url = base_url
        self.session = requests.Session()
        self.rate_limiter = RateLimiter(rate_limit[0], rate_limit[1])
        
        # Set user agent and headers
        self.session.headers.update({
            'User-Agent': 'DevOps-Monitor/1.0 (Python Scraper)',
            'Accept': 'application/json, text/html, */*',
            'Accept-Language': 'en-US,en;q=0.9'
        })
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _respect_rate_limit(self):
        """Enforce rate limiting."""
        if not self.rate_limiter.can_proceed():
            wait_time = self.rate_limiter.wait_time()
            if wait_time > 0:
                logger.info(f"Rate limit reached, waiting {wait_time:.2f} seconds...")
                time.sleep(wait_time)
        
        self.rate_limiter.add_request()
    
    def get_with_retry(self, url: str, max_retries: int = 3, 
                      backoff_factor: float = 1.0, **kwargs) -> requests.Response:
        """Make HTTP GET request with retry logic."""
        self._respect_rate_limit()
        
        full_url = urljoin(self.base_url, url) if self.base_url else url
        
        for attempt in range(max_retries + 1):
            try:
                response = self.session.get(full_url, timeout=10, **kwargs)
                
                if response.status_code == 429:  # Too Many Requests
                    retry_after = int(response.headers.get('Retry-After', 60))
                    raise RateLimitError(f"Rate limited, retry after {retry_after}s")
                
                response.raise_for_status()
                return response
                
            except (requests.RequestException, RateLimitError) as e:
                if attempt == max_retries:
                    logger.error(f"Failed to fetch {full_url} after {max_retries + 1} attempts: {e}")
                    raise ScrapingError(f"Request failed: {e}")
                
                wait_time = backoff_factor * (2 ** attempt)
                logger.warning(f"Attempt {attempt + 1} failed for {full_url}, retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
    
    def check_service_health(self, urls: List[str]) -> List[ServiceStatus]:
        """Check health status of multiple services."""
        results = []
        
        for url in urls:
            start_time = time.time()
            timestamp = datetime.now()
            
            try:
                response = self.get_with_retry(url)
                response_time = time.time() - start_time
                
                status = ServiceStatus(
                    url=url,
                    status_code=response.status_code,
                    response_time=response_time,
                    timestamp=timestamp
                )
                
                logger.info(f"✓ {url} - {response.status_code} ({response_time:.3f}s)")
                
            except ScrapingError as e:
                status = ServiceStatus(
                    url=url,
                    status_code=0,
                    response_time=time.time() - start_time,
                    timestamp=timestamp,
                    error=str(e)
                )
                
                logger.error(f"✗ {url} - {e}")
            
            results.append(status)
        
        return results
    
    def scrape_api_data(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """Scrape data from API endpoint with proper error handling."""
        try:
            response = self.get_with_retry(endpoint, params=params)
            
            # Try to parse as JSON
            try:
                data = response.json()
                return {
                    'success': True,
                    'data': data,
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                # Fallback to text content
                return {
                    'success': True,
                    'data': response.text,
                    'status_code': response.status_code,
                    'timestamp': datetime.now().isoformat(),
                    'content_type': response.headers.get('content-type', 'unknown')
                }
                
        except ScrapingError as e:
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def monitor_endpoints(self, endpoints: Dict[str, str], 
                         output_file: str = "monitoring_results.csv"):
        """Monitor multiple endpoints and save results to CSV."""
        results = []
        
        for name, url in endpoints.items():
            logger.info(f"Monitoring {name}: {url}")
            
            status_list = self.check_service_health([url])
            status = status_list[0] if status_list else None
            
            if status:
                result = {
                    'service_name': name,
                    'url': status.url,
                    'status_code': status.status_code,
                    'response_time': status.response_time,
                    'timestamp': status.timestamp.isoformat(),
                    'error': status.error or ''
                }
                results.append(result)
        
        # Save to CSV
        if results:
            self._save_to_csv(results, output_file)
            logger.info(f"Monitoring results saved to {output_file}")
        
        return results
    
    def _save_to_csv(self, data: List[Dict], filename: str):
        """Save data to CSV file."""
        if not data:
            return
        
        fieldnames = data[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)


class AsyncWebScraper:
    """Asynchronous web scraper for high-performance concurrent requests."""
    
    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def fetch(self, session: aiohttp.ClientSession, url: str) -> Dict[str, Any]:
        """Fetch a single URL asynchronously."""
        async with self.semaphore:
            start_time = time.time()
            
            try:
                async with session.get(url) as response:
                    response_time = time.time() - start_time
                    content = await response.text()
                    
                    return {
                        'url': url,
                        'status_code': response.status,
                        'response_time': response_time,
                        'content_length': len(content),
                        'success': True,
                        'timestamp': datetime.now().isoformat()
                    }
                    
            except Exception as e:
                return {
                    'url': url,
                    'status_code': 0,
                    'response_time': time.time() - start_time,
                    'error': str(e),
                    'success': False,
                    'timestamp': datetime.now().isoformat()
                }
    
    async def fetch_multiple(self, urls: List[str], timeout: int = 30) -> List[Dict[str, Any]]:
        """Fetch multiple URLs concurrently."""
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        timeout_config = aiohttp.ClientTimeout(total=timeout)
        
        async with aiohttp.ClientSession(
            connector=connector, 
            timeout=timeout_config
        ) as session:
            tasks = [self.fetch(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle exceptions that might have been returned
            processed_results = []
            for result in results:
                if isinstance(result, Exception):
                    processed_results.append({
                        'url': 'unknown',
                        'error': str(result),
                        'success': False,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    processed_results.append(result)
            
            return processed_results


def demo_web_scraper():
    """Demonstrate the web scraper functionality."""
    print("=== Web Scraper Demo ===\n")
    
    # Example endpoints to monitor (using public APIs)
    test_endpoints = {
        'JSONPlaceholder': 'https://jsonplaceholder.typicode.com/posts/1',
        'HTTPBin Status': 'https://httpbin.org/status/200',
        'HTTPBin Headers': 'https://httpbin.org/headers',
        'GitHub API': 'https://api.github.com/repos/python/cpython',
        'Invalid URL': 'https://this-definitely-does-not-exist.invalid'
    }
    
    # Synchronous scraping demo
    print("1. Synchronous Service Health Monitoring:")
    with WebScraper(rate_limit=(5, 10)) as scraper:
        results = scraper.monitor_endpoints(test_endpoints)
        
        print(f"\nMonitored {len(results)} endpoints:")
        for result in results:
            status = "✓" if result['status_code'] == 200 else "✗"
            print(f"  {status} {result['service_name']}: {result['status_code']} "
                  f"({result['response_time']:.3f}s)")
    
    # Asynchronous scraping demo
    print("\n2. Asynchronous Concurrent Requests:")
    
    async def async_demo():
        async_scraper = AsyncWebScraper(max_concurrent=5)
        urls = list(test_endpoints.values())
        
        start_time = time.time()
        results = await async_scraper.fetch_multiple(urls)
        total_time = time.time() - start_time
        
        print(f"Fetched {len(urls)} URLs in {total_time:.2f}s:")
        for result in results:
            status = "✓" if result.get('success') else "✗"
            status_code = result.get('status_code', 'N/A')
            response_time = result.get('response_time', 0)
            url = result.get('url', 'unknown')
            
            print(f"  {status} {urlparse(url).netloc}: {status_code} ({response_time:.3f}s)")
    
    # Run async demo
    asyncio.run(async_demo())
    
    # API data scraping demo
    print("\n3. API Data Scraping:")
    with WebScraper() as scraper:
        api_data = scraper.scrape_api_data('https://jsonplaceholder.typicode.com/users/1')
        
        if api_data['success']:
            user_data = api_data['data']
            print(f"  User: {user_data.get('name', 'Unknown')}")
            print(f"  Email: {user_data.get('email', 'Unknown')}")
            print(f"  Company: {user_data.get('company', {}).get('name', 'Unknown')}")
        else:
            print(f"  Failed to fetch user data: {api_data['error']}")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo_web_scraper()