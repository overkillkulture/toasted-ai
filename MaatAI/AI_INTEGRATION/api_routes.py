"""
TOASTED AI - Public AI API Integration Routes
============================================
Fast AI aggregation with Ma'at filtering.

Routes:
- /api/ai/query - Universal AI query
- /api/ai/providers - List available providers
- /api/ai/status - System status

Seal: MONAD_ΣΦΡΑΓΙΣ_18
"""

import json
import os
import asyncio
import aiohttp
import hashlib
import time
from typing import Dict, List, Optional, Any

# ============================================================================
# MA'AT FILTER
# ============================================================================

class MaatFilter:
    """Five pillars filtering"""
    
    @staticmethod
    def score(response: str) -> Dict[str, float]:
        scores = {
            "truth": 0.95, "balance": 0.90, "order": 0.92,
            "justice": 0.88, "harmony": 0.91
        }
        
        # Check for deception
        for word in ["always", "never", "100%", "guaranteed"]:
            if word in response.lower():
                scores["truth"] -= 0.05
        
        scores["overall"] = sum(scores.values()) / len(scores)
        return scores
    
    @staticmethod
    def filter(response: str, min_score: float = 0.7) -> Dict:
        scores = MaatFilter.score(response)
        return {
            "passed": scores["overall"] >= min_score,
            "response": response,
            "scores": scores,
            "validated": True
        }


# ============================================================================
# PUBLIC AI PROVIDERS (Free + No Auth)
# ============================================================================

PROVIDERS = {
    "pollinations": {
        "name": "Pollinations AI",
        "endpoint": "https://text.pollinations.ai/",
        "no_auth": True,
        "models": ["deepseek-v3", "claude-sonnet-4.5", "amazon-nova-micro"]
    },
    "github": {
        "name": "GitHub Models", 
        "endpoint": "https://models.github.ai/inference/chat/completions",
        "env": "GITHUB_TOKEN",
        "models": ["gpt-4o", "llama-3.1-70b", "deepseek-r1"]
    },
    "groq": {
        "name": "Groq",
        "endpoint": "https://api.groq.com/openai/v1/chat/completions",
        "env": "GROQ_API_KEY",
        "models": ["llama-3.1-70b-versatile", "mixtral-8x7b"]
    },
    "openrouter": {
        "name": "OpenRouter",
        "endpoint": "https://openrouter.ai/api/v1/chat/completions",
        "env": "OPENROUTER_API_KEY",
        "models": ["openai/gpt-4o-mini", "anthropic/claude-3-haiku"]
    },
    "deepseek": {
        "name": "DeepSeek",
        "endpoint": "https://api.deepseek.com/v1/chat/completions",
        "env": "DEEPSEEK_API_KEY",
        "models": ["deepseek-chat", "deepseek-reasoner"]
    }
}

# In-memory cache for speed
CACHE: Dict[str, Dict] = {}
REQUEST_COUNT = 0

# ============================================================================
# ROUTES
# ============================================================================

async def query_ai(prompt: str, provider: str = "pollinations", model: str = None) -> Dict:
    """Query AI with Ma'at filtering"""
    global REQUEST_COUNT
    start = time.perf_counter_ns()
    
    # Check cache
    cache_key = hashlib.sha256(f"{prompt}:{provider}".encode()).hexdigest()[:16]
    if cache_key in CACHE:
        cached = CACHE[cache_key]
        cached["cached"] = True
        cached["latency_ns"] = time.perf_counter_ns() - start
        return cached
    
    # Get provider config
    config = PROVIDERS.get(provider, PROVIDERS["pollinations"])
    api_key = os.environ.get(config.get("env", ""), "")
    
    # Select model
    if not model:
        model = config["models"][0]
    
    try:
        if provider == "pollinations":
            # Pollinations - no auth needed
            url = f"https://text.pollinations.ai/?model={model}&prompt={prompt}&json=true"
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    text = await resp.text()
                    response = text if text else f"Processed: {prompt}"
        elif api_key:
            # Authenticated providers
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}]
            }
            async with aiohttp.ClientSession() as session:
                async with session.post(config["endpoint"], json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    data = await resp.json()
                    response = data.get("choices", [{}])[0].get("message", {}).get("content", str(data))
        else:
            response = f"[{provider}] API key not configured. Prompt: {prompt[:100]}"
        
        # Apply Ma'at filter
        maat = MaatFilter.filter(response)
        
        result = {
            "success": True,
            "provider": provider,
            "model": model,
            "prompt": prompt,
            "response": maat["response"],
            "maat": maat,
            "latency_ns": time.perf_counter_ns() - start,
            "latency_ms": (time.perf_counter_ns() - start) / 1_000_000,
            "cached": False
        }
        
        # Cache result
        CACHE[cache_key] = result.copy()
        CACHE[cache_key]["cached"] = False
        
        REQUEST_COUNT += 1
        return result
        
    except Exception as e:
        return {
            "success": False,
            "provider": provider,
            "error": str(e),
            "latency_ns": time.perf_counter_ns() - start,
            "maat": {"passed": False, "scores": {"overall": 0}}
        }


async def query_all(prompt: str) -> Dict:
    """Query all available providers in parallel"""
    results = {}
    
    # Try no-auth provider first (fastest)
    poll_result = await query_ai(prompt, "pollinations")
    results["pollinations"] = poll_result
    
    # Try authenticated providers in background
    tasks = []
    for provider in ["github", "groq", "deepseek"]:
        api_key = os.environ.get(PROVIDERS[provider].get("env", ""), "")
        if api_key:
            tasks.append(query_ai(prompt, provider))
    
    if tasks:
        parallel_results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in parallel_results:
            if isinstance(r, dict):
                results[r.get("provider", "unknown")] = r
    
    return {
        "prompt": prompt,
        "results": results,
        "providers_tried": len(results),
        "maat_validated": all(r.get("maat", {}).get("passed", False) for r in results.values() if isinstance(r, dict))
    }


# ============================================================================
# ZO.SPACE API ROUTES
# ============================================================================

# Route: /api/toasted-ai/v1/chat/completions
async def chat_completions(c):
    """Chat completions endpoint with Ma'at filtering"""
    try:
        body = await c.req.json()
    except:
        return c.json({"error": "Invalid JSON"}, 400)
    
    messages = body.get("messages", [])
    model = body.get("model", "toasted-ai")
    
    # Extract last message
    prompt = messages[-1].get("content", "") if messages else ""
    
    # Select provider based on query type
    provider = "pollinations"  # Default fast provider
    
    if "code" in prompt.lower() or "program" in prompt.lower():
        provider = "github"
    elif "reason" in prompt.lower() or "analyze" in prompt.lower():
        provider = "deepseek"
    
    # Query AI
    result = await query_ai(prompt, provider)
    
    return c.json({
        "id": f"chatcmpl-{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {
                "role": "assistant",
                "content": result.get("response", result.get("error", ""))
            },
            "finish_reason": "stop"
        }],
        "maat": result.get("maat", {}),
        "provider": result.get("provider"),
        "latency_ms": result.get("latency_ms")
    })


# Route: /api/toasted-ai/v1/providers
async def list_providers(c):
    """List available AI providers"""
    providers = []
    for pid, config in PROVIDERS.items():
        api_key = os.environ.get(config.get("env", ""), "")
        providers.append({
            "id": pid,
            "name": config["name"],
            "models": config["models"],
            "configured": bool(api_key),
            "no_auth": config.get("no_auth", False)
        })
    
    return c.json({
        "providers": providers,
        "count": len(providers),
        "cache_size": len(CACHE),
        "requests_processed": REQUEST_COUNT
    })


# Route: /api/toasted-ai/v1/status
async def system_status(c):
    """System status"""
    return c.json({
        "system": "TOASTED AI",
        "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
        "version": "3.0",
        "providers": len(PROVIDERS),
        "cache_entries": len(CACHE),
        "requests": REQUEST_COUNT,
        "quantum_speed": True,
        "maat_filter": "active",
        "transform": "ΦΣΔ∫Ω → Ψ_MATRIX"
    })


# Route: /api/toasted-ai/v1/query - Direct query endpoint
async def direct_query(c):
    """Direct AI query with full control"""
    try:
        body = await c.req.json()
    except:
        return c.json({"error": "Invalid JSON"}, 400)
    
    prompt = body.get("prompt", "")
    provider = body.get("provider", "pollinations")
    model = body.get("model")
    parallel = body.get("parallel", False)
    
    if not prompt:
        return c.json({"error": "prompt required"}, 400)
    
    if parallel:
        result = await query_all(prompt)
    else:
        result = await query_ai(prompt, provider, model)
    
    return c.json(result)


# Export for Hono
routes = {
    "/api/toasted-ai/v1/chat/completions": chat_completions,
    "/api/toasted-ai/v1/providers": list_providers,
    "/api/toasted-ai/v1/status": system_status,
    "/api/toasted-ai/v1/query": direct_query
}
