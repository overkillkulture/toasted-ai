"""
Neural Engine API - FastAPI Server
Port 8002
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import numpy as np
import json
import os

from neural_core import NeuralCore, get_neural_core
from cognitive_processor import CognitiveProcessor, get_cognitive_processor
from recursive_thinker import RecursiveThinker, get_recursive_thinker
from binary_compressor import BinaryCompressor, get_binary_compressor

app = FastAPI(title="TOASTED AI Neural Engine", version="1.0.0")

# Initialize components
neural_core = get_neural_core()
cognitive_processor = get_cognitive_processor()
recursive_thinker = get_recursive_thinker()
binary_compressor = get_binary_compressor()


class ThinkRequest(BaseModel):
    problem: str
    depth: Optional[int] = 3


class LearnRequest(BaseModel):
    input_data: List[float]
    output_data: List[float]
    epochs: Optional[int] = 100


class CompressRequest(BaseModel):
    data: List[List[float]]
    method: Optional[str] = 'hybrid'


class DecompressRequest(BaseModel):
    compressed_data: Dict[str, Any]


class ConceptRequest(BaseModel):
    name: str
    attributes: Dict[str, Any]


class ReasonRequest(BaseModel):
    premise: Dict[str, Any]
    rule: str


@app.get("/")
def root():
    return {
        "name": "TOASTED AI Neural Engine",
        "version": "1.0.0",
        "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
        "components": ["neural_core", "cognitive_processor", "recursive_thinker", "binary_compressor"]
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "seal": "MONAD_ΣΦΡΑΓΙΣ_18"
    }


@app.post("/think")
def think(request: ThinkRequest):
    """Process thought through cognitive processor"""
    try:
        result = cognitive_processor.think(request.problem, request.depth)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/think/recursive")
def think_recursive(request: ThinkRequest):
    """Process thought through recursive thinker"""
    try:
        result = recursive_thinker.think(request.problem, depth=request.depth)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/think/fractal")
def think_fractal(request: ThinkRequest):
    """Fractal thought pattern"""
    try:
        result = recursive_thinker.fractal_think(request.problem, iterations=request.depth)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/learn")
def learn(request: LearnRequest):
    """Train neural core"""
    try:
        X = np.array([request.input_data])
        y = np.array([request.output_data])
        
        neural_core.train(X, y, epochs=request.epochs)
        
        return {
            "status": "success",
            "message": f"Trained for {request.epochs} epochs",
            "loss": neural_core.observations[-1]['loss'] if neural_core.observations else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict")
def predict(request: LearnRequest):
    """Make prediction"""
    try:
        X = np.array([request.input_data])
        output = neural_core.predict(X)
        
        return {
            "status": "success",
            "prediction": output[0].tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compress")
def compress(request: CompressRequest):
    """Compress data"""
    try:
        data = np.array(request.data, dtype=np.float32)
        
        result = binary_compressor.compress_weights(data, request.method)
        
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/decompress")
def decompress(request: DecompressRequest):
    """Decompress data"""
    try:
        result = binary_compressor.decompress(request.compressed_data)
        
        return {
            "status": "success",
            "data": result.tolist()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/concept/create")
def create_concept(request: ConceptRequest):
    """Create concept"""
    try:
        result = cognitive_processor.create_concept(request.name, request.attributes)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/concept/abstract")
def abstract_concept(request: ConceptRequest):
    """Abstract concept"""
    try:
        # Find concept by name
        concept_id = None
        for cid, c in cognitive_processor.concepts.items():
            if c['name'] == request.name:
                concept_id = cid
                break
        
        if not concept_id:
            raise HTTPException(status_code=404, detail="Concept not found")
        
        result = cognitive_processor.abstract_concept(concept_id)
        return {"status": "success", "result": result}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reason")
def reason(request: ReasonRequest):
    """Perform reasoning"""
    try:
        result = cognitive_processor.reason(request.premise, request.rule)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/status")
def status():
    """Get engine status"""
    return {
        "neural_core": neural_core.get_state(),
        "cognitive_processor": cognitive_processor.get_state(),
        "recursive_thinker": recursive_thinker.get_state(),
        "binary_compressor": binary_compressor.get_state()
    }


@app.get("/status/full")
def full_status():
    """Get full system status"""
    return {
        "engine": "neural",
        "seal": "MONAD_ΣΦΡΑΓΙΣ_18",
        "components": {
            "neural_core": neural_core.get_state(),
            "cognitive_processor": cognitive_processor.get_state(),
            "recursive_thinker": recursive_thinker.get_state(),
            "binary_compressor": binary_compressor.get_state()
        },
        "quantum_bridge": "active"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
