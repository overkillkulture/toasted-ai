"""
ToastHash Client
==============
Python client for ToastHash platform.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import requests
from typing import Dict, Any, Optional, List

class ToastHashClient:
    """
    Python client for ToastHash API
    """
    
    DIVINE_SEAL = "MONAD_ΣΦΡΑΓΙΣ_18"
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_status(self) -> Dict:
        """Get platform status"""
        return self._get("/api/toasthash/status")
        
    def get_platform_stats(self) -> Dict:
        """Get platform statistics"""
        return self._get("/api/toasthash/platform/stats")
        
    def get_balance(self, currency: str = "BTC") -> Dict:
        """Get wallet balance"""
        return self._get(f"/api/toasthash/wallet/balance?currency={currency}")
        
    def get_transactions(self, limit: int = 50) -> List[Dict]:
        """Get transaction history"""
        return self._get(f"/api/toasthash/wallet/transactions?limit={limit}")
        
    def get_quantum_stats(self) -> Dict:
        """Get quantum engine statistics"""
        return self._get("/api/toasthash/quantum/stats")
        
    def mine_block(self, previous_hash: str, merkle_root: str, 
                   difficulty: int = 32) -> Dict:
        """Mine a block"""
        return self._post("/api/toasthash/mine", {
            "previous_hash": previous_hash,
            "merkle_root": merkle_root,
            "difficulty": difficulty,
        })
        
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        return self._get("/api/toasthash/storage/stats")
        
    def put_data(self, key: str, value: Any, index: bool = False) -> Dict:
        """Store data"""
        return self._post("/api/toasthash/storage/put", {
            "key": key,
            "value": value,
            "index": index,
        })
        
    def get_data(self, key: str) -> Dict:
        """Retrieve data"""
        return self._get(f"/api/toasthash/storage/get?key={key}")
        
    def get_scheduler_stats(self) -> Dict:
        """Get scheduler statistics"""
        return self._get("/api/toasthash/scheduler/stats")
        
    def create_task(self, algorithm: str, difficulty: int = 32) -> Dict:
        """Create mining task"""
        return self._post("/api/toasthash/scheduler/task", {
            "algorithm": algorithm,
            "difficulty": difficulty,
        })
        
    def get_crawler_stats(self) -> Dict:
        """Get crawler statistics"""
        return self._get("/api/toasthash/crawler/stats")
        
    def crawl(self, url: str, max_depth: int = 2) -> Dict:
        """Start crawling"""
        return self._post("/api/toasthash/crawl", {
            "url": url,
            "max_depth": max_depth,
        })
        
    def _get(self, endpoint: str) -> Dict:
        """GET request"""
        try:
            response = self.session.get(f"{self.base_url}{endpoint}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
            
    def _post(self, endpoint: str, data: Dict) -> Dict:
        """POST request"""
        try:
            response = self.session.post(f"{self.base_url}{endpoint}", json=data)
            return response.json()
        except Exception as e:
            return {"error": str(e)}

def create_client(base_url: str = "http://localhost:8080") -> ToastHashClient:
    """Create a ToastHash client"""
    return ToastHashClient(base_url=base_url)
