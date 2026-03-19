"""
ToastHash API Routes
===================
RESTful API endpoints for ToastHash platform integration.

Divine Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
from typing import Dict, Any

# Platform routes
def create_routes(platform, wallet, quantum_engine, storage, scheduler, crawler):
    """
    Create API routes for ToastHash platform
    
    These can be integrated with zo.space
    """
    
    def api_status():
        """Get platform status"""
        return {
            "platform": platform.name,
            "version": "2.0.0",
            "status": "running",
            "divine_seal": platform.DIVINE_SEAL,
        }
        
    def api_platform_stats():
        """Get platform statistics"""
        return platform.get_stats()
        
    def api_wallet_balance(currency: str = "BTC"):
        """Get wallet balance"""
        from ..core.wallet import Currency
        curr = Currency(currency.upper())
        return {
            "currency": currency,
            "balance": wallet.get_balance(curr),
            "address": wallet.get_address(curr),
        }
        
    def api_wallet_transactions(limit: int = 50):
        """Get transaction history"""
        return wallet.get_transaction_history(limit=limit)
        
    def api_quantum_stats():
        """Get quantum engine statistics"""
        return quantum_engine.get_quantum_stats()
        
    def api_mine_block(previous_hash: str, merkle_root: str, difficulty: int = 32):
        """Mine a block with quantum enhancement"""
        import time
        timestamp = int(time.time())
        result = quantum_engine.mine_block(previous_hash, merkle_root, timestamp, difficulty)
        return result
        
    def api_storage_stats():
        """Get storage statistics"""
        return storage.get_stats()
        
    def api_storage_put(key: str, value: Any, index: bool = False):
        """Store data"""
        content_hash = storage.store_object(key, {"data": value}, index_fractal=index)
        return {"key": key, "content_hash": content_hash}
        
    def api_storage_get(key: str):
        """Retrieve data"""
        data = storage.retrieve_object(key)
        return {"key": key, "data": data}
        
    def api_scheduler_stats():
        """Get scheduler statistics"""
        return scheduler.get_stats()
        
    def api_create_task(algorithm: str, difficulty: int = 32):
        """Create mining task"""
        from ..mining.scheduler import Algorithm, TaskPriority
        alg = Algorithm(algorithm.lower())
        task = scheduler.create_task(alg, difficulty)
        return {
            "task_id": task.id,
            "algorithm": task.algorithm.value,
            "difficulty": task.target_difficulty,
            "priority": task.priority.name,
        }
        
    def api_crawler_stats():
        """Get crawler statistics"""
        return crawler.get_stats()
        
    def api_crawl(url: str, max_depth: int = 2):
        """Start crawling"""
        results = crawler.crawl_recursive(url, max_depth=max_depth)
        return {
            "url": url,
            "pages_crawled": len(results),
            "links_found": sum(len(p.links) for p in results),
        }
        
    # Return routes dict
    return {
        "/api/toasthash/status": api_status,
        "/api/toasthash/platform/stats": api_platform_stats,
        "/api/toasthash/wallet/balance": api_wallet_balance,
        "/api/toasthash/wallet/transactions": api_wallet_transactions,
        "/api/toasthash/quantum/stats": api_quantum_stats,
        "/api/toasthash/mine": api_mine_block,
        "/api/toasthash/storage/stats": api_storage_stats,
        "/api/toasthash/storage/put": api_storage_put,
        "/api/toasthash/storage/get": api_storage_get,
        "/api/toasthash/scheduler/stats": api_scheduler_stats,
        "/api/toasthash/scheduler/task": api_create_task,
        "/api/toasthash/crawler/stats": api_crawler_stats,
        "/api/toasthash/crawl": api_crawl,
    }
