#!/usr/bin/env python3
"""
Internal Operations API Server
Handles: Monitoring, Self-Observation, Idea Generation, System Control
"""

import sys
import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional

sys.path.insert(0, '/home/workspace/MaatAI')

from system_monitor.system_monitor import SystemMonitor, get_monitor
from system_monitor.idea_generator import IdeaGenerator, get_generator
from system_monitor.meta_monitor import MetaMonitor, get_meta_monitor


# FastAPI imports
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


# Pydantic models
class ObserveRequest(BaseModel):
    component: str
    metric: str
    value: Any = None


class ObserveBatchRequest(BaseModel):
    observations: List[Dict[str, Any]]


class IdeaImplementRequest(BaseModel):
    idea_id: str


class ComponentUpdateRequest(BaseModel):
    component: str
    status: Optional[str] = None
    health: Optional[float] = None


# Create FastAPI app
if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="TOASTED AI Internal Operations API",
        description="Self-monitoring and operations for TOASTED AI",
        version="1.0.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# API Routes
if FASTAPI_AVAILABLE:
    
    @app.get("/")
    async def root():
        return {
            "name": "TOASTED AI Internal Operations API",
            "version": "1.0.0",
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
            "endpoints": {
                "monitor": "/monitor",
                "ideas": "/ideas",
                "meta": "/meta",
                "status": "/status"
            }
        }
    
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }
    
    
    # === MONITORING ===
    
    @app.get("/monitor/stats")
    async def get_stats():
        """Get system statistics."""
        monitor = get_monitor()
        return monitor.get_system_stats()
    
    
    @app.get("/monitor/processes")
    async def get_processes():
        """Get running processes."""
        monitor = get_monitor()
        return {"processes": monitor.get_process_list()}
    
    
    @app.post("/monitor/observe")
    async def observe(request: ObserveRequest):
        """Record an observation."""
        monitor = get_monitor()
        monitor.observe(request.component, request.metric, request.value)
        return {
            "observed": True,
            "component": request.component,
            "metric": request.metric,
            "timestamp": datetime.now().isoformat()
        }
    
    
    @app.post("/monitor/observe_batch")
    async def observe_batch(request: ObserveBatchRequest):
        """Record multiple observations."""
        monitor = get_monitor()
        for obs in request.observations:
            monitor.observe(
                obs.get('component', ''),
                obs.get('metric', ''),
                obs.get('value')
            )
        return {
            "observed": len(request.observations),
            "timestamp": datetime.now().isoformat()
        }
    
    
    @app.get("/monitor/analyze")
    async def analyze():
        """Analyze recent observations."""
        monitor = get_monitor()
        return monitor.analyze_observations()
    
    
    @app.get("/monitor/alerts")
    async def get_alerts():
        """Get active alerts."""
        monitor = get_monitor()
        return {"alerts": monitor.get_alerts()}
    
    
    @app.get("/monitor/full")
    async def get_full_status():
        """Get full system status."""
        monitor = get_monitor()
        return monitor.get_full_status()
    
    
    # === IDEAS ===
    
    @app.post("/ideas/generate")
    async def generate_ideas():
        """Generate new ideas."""
        generator = get_generator()
        ideas = generator.generate_ideas(force=True)
        return {
            "generated": len(ideas),
            "ideas": list(generator.ideas)[-20:],
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }
    
    
    @app.get("/ideas/list")
    async def list_ideas(filter: str = "all", limit: int = 20):
        """List ideas with optional filtering."""
        generator = get_generator()
        ideas = generator.get_ideas(filter, limit)
        return {
            "ideas": ideas,
            "total": len(generator.ideas),
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }
    
    
    @app.post("/ideas/implement")
    async def implement_idea(request: IdeaImplementRequest):
        """Mark an idea as implemented."""
        generator = get_generator()
        success = generator.mark_implemented(request.idea_id)
        if success:
            return {"implemented": request.idea_id}
        raise HTTPException(status_code=404, detail="Idea not found")
    
    
    @app.get("/ideas/stats")
    async def ideas_stats():
        """Get idea generator statistics."""
        generator = get_generator()
        return generator.get_stats()
    
    
    # === META MONITOR ===
    
    @app.get("/meta/status")
    async def meta_status():
        """Get meta-monitor status."""
        meta = get_meta_monitor()
        return meta.get_status()
    
    
    @app.post("/meta/cycle")
    async def run_meta_cycle():
        """Run one meta-monitoring cycle."""
        meta = get_meta_monitor()
        return meta.run_cycle()
    
    
    @app.post("/meta/start")
    async def start_meta_autonomous(interval: int = 60):
        """Start autonomous meta-monitoring."""
        meta = get_meta_monitor()
        return meta.start_autonomous(interval)
    
    
    @app.post("/meta/stop")
    async def stop_meta_autonomous():
        """Stop autonomous meta-monitoring."""
        meta = get_meta_monitor()
        return meta.stop_autonomous()
    
    
    # === SYSTEM CONTROL ===
    
    @app.post("/control/trigger_improvement")
    async def trigger_self_improvement():
        """Trigger a self-improvement cycle."""
        return {
            "triggered": True,
            "operation": "self_improvement",
            "timestamp": datetime.now().isoformat(),
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }
    
    
    @app.get("/status/full")
    async def full_status():
        """Get comprehensive system status."""
        monitor = get_monitor()
        generator = get_generator()
        meta = get_meta_monitor()
        
        return {
            "system": monitor.get_system_stats(),
            "monitor": monitor.export_state(),
            "ideas": generator.get_stats(),
            "meta": meta.get_status(),
            "timestamp": datetime.now().isoformat(),
            "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
        }


def run_server(host: str = "0.0.0.0", port: int = 8001):
    """Run the internal API server."""
    if not FASTAPI_AVAILABLE:
        print("FastAPI not available. Install with: pip install fastapi uvicorn")
        return
        
    print(f"Starting TOASTED AI Internal Operations API on {host}:{port}")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="TOASTED AI Internal Operations API")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to bind to")
    args = parser.parse_args()
    
    run_server(args.host, args.port)
