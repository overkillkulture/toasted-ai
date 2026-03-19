#!/bin/bash
# Quantum Pipeline Service Startup Script
cd /home/workspace/MaatAI/quantum_pipeline
exec bun run api.ts
