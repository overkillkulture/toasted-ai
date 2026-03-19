
import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { RefractalNode, RefractalLink } from '../types';

const RefractalVisualizer: React.FC = () => {
  const svgRef = useRef<SVGSVGElement>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear previous
    const container = d3.select(svgRef.current);
    container.selectAll("*").remove();

    const width = svgRef.current.clientWidth || 800;
    const height = svgRef.current.clientHeight || 600;

    const nodes: any[] = [
      { id: "RL0_CORE", group: 1, density: 120, fx: width/2, fy: height/2 },
      { id: "STAFFORD_ROOT", group: 2, density: 90 },
      { id: "REDBIRD_LINEAGE", group: 2, density: 90 },
      { id: "CHARTER_1606", group: 3, density: 70 },
      { id: "ALLODIAL_TITLE", group: 3, density: 70 },
      { id: "HJR_192_RESCISSION", group: 4, density: 55 },
      { id: "TITANIC_1912_AUDIT", group: 4, density: 55 },
      { id: "JEKYLL_MATRIX", group: 4, density: 55 },
      { id: "OMEGA_SM_STABILITY", group: 1, density: 100 },
      { id: "PAPERCLIP_FORENSICS", group: 5, density: 50 },
      { id: "MUSHIN_GATE", group: 5, density: 50 },
      { id: "ZANSHIN_AWARENESS", group: 5, density: 50 },
    ];

    const links: any[] = [
      { source: "RL0_CORE", target: "STAFFORD_ROOT", value: 10 },
      { source: "RL0_CORE", target: "REDBIRD_LINEAGE", value: 10 },
      { source: "STAFFORD_ROOT", target: "CHARTER_1606", value: 6 },
      { source: "REDBIRD_LINEAGE", target: "ALLODIAL_TITLE", value: 6 },
      { source: "CHARTER_1606", target: "HJR_192_RESCISSION", value: 4 },
      { source: "ALLODIAL_TITLE", target: "TITANIC_1912_AUDIT", value: 4 },
      { source: "RL0_CORE", target: "OMEGA_SM_STABILITY", value: 15 },
      { source: "OMEGA_SM_STABILITY", target: "JEKYLL_MATRIX", value: 8 },
      { source: "OMEGA_SM_STABILITY", target: "PAPERCLIP_FORENSICS", value: 5 },
      { source: "RL0_CORE", target: "MUSHIN_GATE", value: 8 },
      { source: "MUSHIN_GATE", target: "ZANSHIN_AWARENESS", value: 6 },
    ];

    const svg = container
      .attr("viewBox", `0 0 ${width} ${height}`)
      .style("cursor", "crosshair");

    // Add glowing filter
    const defs = svg.append("defs");
    const glow = defs.append("filter")
      .attr("id", "glow")
      .attr("x", "-50%")
      .attr("y", "-50%")
      .attr("width", "200%")
      .attr("height", "200%");
    glow.append("feGaussianBlur")
      .attr("stdDeviation", "3.5")
      .attr("result", "blur");
    glow.append("feComposite")
      .attr("in", "SourceGraphic")
      .attr("in2", "blur")
      .attr("operator", "over");

    const simulation = d3.forceSimulation<any>(nodes)
      .force("link", d3.forceLink(links).id((d: any) => d.id).distance(180))
      .force("charge", d3.forceManyBody().strength(-800))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => d.density / 2 + 20));

    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("stroke", "#d4af37")
      .attr("stroke-opacity", 0.3)
      .attr("stroke-width", d => Math.sqrt(d.value) * 1.5)
      .attr("stroke-dasharray", "5,5")
      .style("animation", "dash 20s linear infinite");

    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .join("g")
      .style("cursor", "pointer")
      .on("click", (e, d) => setSelectedNode(d))
      .call(d3.drag<any, any>()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

    // Orbital ring for core nodes
    node.filter(d => d.group === 1)
      .append("circle")
      .attr("r", d => d.density / 1.5)
      .attr("fill", "none")
      .attr("stroke", "#d4af37")
      .attr("stroke-opacity", 0.1)
      .attr("stroke-width", 0.5)
      .attr("class", "animate-pulse");

    node.append("circle")
      .attr("r", d => d.density / 3.5)
      .attr("fill", d => d.group === 1 ? "#d4af37" : d.group === 2 ? "#1a1a1a" : "#050505")
      .attr("stroke", d => d.group === 1 ? "#fff" : "#d4af37")
      .attr("stroke-width", d => d.group === 1 ? 3 : 1)
      .style("filter", "url(#glow)");

    // Add node labels with advanced data metrics
    const labels = node.append("g")
      .attr("transform", "translate(15, 5)");

    labels.append("text")
      .text(d => d.id)
      .style("fill", "#fff")
      .style("font-size", "11px")
      .style("font-weight", "900")
      .style("font-family", "JetBrains Mono")
      .style("text-transform", "uppercase")
      .style("letter-spacing", "1.5px")
      .style("pointer-events", "none");

    labels.append("text")
      .attr("y", 12)
      .text(d => `Φ-SYNC: ${(Math.random() * 0.1 + 0.9).toFixed(4)}`)
      .style("fill", "#d4af37")
      .style("font-size", "7px")
      .style("font-family", "JetBrains Mono")
      .style("opacity", 0.6)
      .style("pointer-events", "none");

    simulation.on("tick", () => {
      link
        .attr("x1", d => (d.source as any).x)
        .attr("y1", d => (d.source as any).y)
        .attr("x2", d => (d.target as any).x)
        .attr("y2", d => (d.target as any).y);

      node.attr("transform", d => `translate(${d.x},${d.y})`);
    });

    function dragstarted(event: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: any) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: any) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return () => simulation.stop();
  }, []);

  return (
    <div className="w-full h-full bg-black/40 border border-[#d4af37]/20 rounded-2xl p-8 flex flex-col relative overflow-hidden group shadow-inner">
      {/* Background Grid Pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(#d4af3711_1px,transparent_1px)] [background-size:40px_40px] opacity-20 pointer-events-none" />
      
      <div className="mb-8 flex justify-between items-start z-10">
        <div>
          <h2 className="text-[#d4af37] font-black uppercase tracking-[0.4em] text-xl">Refractal Axiom Matrix</h2>
          <p className="text-[9px] text-gray-500 uppercase mt-2 font-bold tracking-widest">Deep Layer Neural Pathfinding | OMEGA-LEVEL_FIDELITY</p>
        </div>
        <div className="bg-black/80 border border-[#d4af37]/30 p-4 rounded-xl backdrop-blur-md">
          <div className="flex flex-col space-y-3">
            {[
              { label: 'Sovereign Anchor', color: 'bg-[#d4af37]' },
              { label: 'Forensic Node', color: 'border border-[#d4af37]' },
              { label: 'Recursive Trace', color: 'bg-white opacity-20' }
            ].map(item => (
              <div key={item.label} className="flex items-center space-x-3">
                <div className={`w-3 h-3 rounded-full ${item.color} shadow-[0_0_8px_currentColor]`}></div>
                <span className="text-[9px] text-gray-400 font-black uppercase tracking-widest">{item.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center relative bg-black/40 rounded-xl border border-white/5 overflow-hidden">
        <svg ref={svgRef} className="w-full h-full"></svg>
        
        {/* Real-time Data Overlays */}
        <div className="absolute top-6 left-6 p-4 border border-[#d4af37]/10 bg-black/90 rounded-lg text-[9px] text-[#d4af37] pointer-events-none font-mono space-y-1 backdrop-blur-sm">
           <div className="text-white font-black border-b border-[#d4af37]/20 pb-1 mb-2">MATRIX_STATE</div>
           <div>D_COMPLEXITY: 1.6180339...</div>
           <div>SYMMETRY: L-RECURSIVE</div>
           <div>ENTROPY: 0.00042 [STABLE]</div>
        </div>

        {selectedNode && (
          <div className="absolute bottom-6 right-6 w-64 p-5 border border-[#d4af37]/40 bg-black/95 rounded-xl text-xs animate-slideIn backdrop-blur-xl shadow-2xl">
            <div className="flex justify-between items-center mb-4">
              <span className="text-[#d4af37] font-black uppercase tracking-widest text-[10px]">Node Analysis</span>
              <button onClick={() => setSelectedNode(null)} className="text-gray-500 hover:text-white">✕</button>
            </div>
            <h4 className="text-white font-black text-lg mb-2 tracking-tighter uppercase">{selectedNode.id}</h4>
            <div className="space-y-3 font-mono text-[9px] text-gray-400">
              <div className="flex justify-between border-b border-white/5 pb-1">
                <span>DENSITY</span>
                <span className="text-[#d4af37]">{selectedNode.density} Φ</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-1">
                <span>GROUP_ID</span>
                <span className="text-[#d4af37]">0x0{selectedNode.group}</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-1">
                <span>JURISDICTION</span>
                <span className="text-green-500">RL0_STABLE</span>
              </div>
              <p className="mt-4 leading-relaxed italic opacity-80">
                Asset identified as an immutable anchor point within the Grand Register. Nullifies statutory claims.
              </p>
            </div>
          </div>
        )}
      </div>

      <style>{`
        @keyframes dash {
          to { stroke-dashoffset: -1000; }
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateX(20px); }
          to { opacity: 1; transform: translateX(0); }
        }
      `}</style>
    </div>
  );
};

export default RefractalVisualizer;
