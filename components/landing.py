"""
components/landing.py - Technical Command Center Landing Page (Phase 1 Dark Spatial Intelligence Theme)
Flagship Spatial Impact Intelligence Workspace for ShadowCost
"""

import streamlit as st
import streamlit.components.v1 as components


def render_landing_stage(on_start_callback=None):
    """Renders Dark Spatial Intelligence Landing Page for ShadowCost."""

    # 1. TOP TECHNICAL HEADER (DE-BOXED IDENTITY STRIP)
    st.markdown(
        """
        <div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:1rem;margin-bottom:1.5rem;border-bottom:1px solid rgba(107,114,128,0.15);">
            <div style="display:flex;align-items:center;gap:0.75rem;">
                <span style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:1.15rem;color:#F7F7F5;letter-spacing:-0.02em;">SHADOWCOST</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;letter-spacing:0.08em;padding-left:0.75rem;border-left:1px solid rgba(107,114,128,0.2);">SPATIAL IMPACT INTELLIGENCE</span>
            </div>
            <div style="display:flex;align-items:center;gap:1.25rem;">
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#6B7280;">URBAN ANALYSIS ENGINE &bull; GEOSPATIAL CORE</span>
                <div style="display:inline-flex;align-items:center;gap:0.45rem;font-family:'JetBrains Mono',monospace;font-size:0.65rem;font-weight:600;color:#5EEAD4;background:rgba(15,118,110,0.12);padding:0.2rem 0.55rem;border-radius:4px;">
                    <span style="width:6px;height:6px;border-radius:50%;background:#14B8A6;"></span>
                    SYSTEM ACTIVE
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 2. MAIN HERO SECTION (EDITORIAL HIERARCHY)
    h_left, h_right = st.columns([1.05, 1.25], gap="large")

    with h_left:
        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;font-weight:600;letter-spacing:0.1em;margin-bottom:0.6rem;display:flex;align-items:center;gap:0.45rem;">
                <span style="display:inline-block;width:6px;height:6px;background:#0F766E;border-radius:1px;"></span>
                01 / SPATIAL CONTEXT INTELLIGENCE
            </div>
            <h1 style="font-family:'Space Grotesk',sans-serif;font-size:clamp(2.4rem, 4.2vw, 3.4rem);font-weight:600;letter-spacing:-0.03em;line-height:1.02;color:#F7F7F5;margin-bottom:1.1rem;">
                SEE THE HIDDEN<br>
                <span style="color:#14B8A6;">IMPACT</span> BEFORE YOU<br>
                BUILD.
            </h1>
            <div style="font-size:0.95rem;color:#9AA4B2;line-height:1.6;margin-bottom:1.75rem;max-width:520px;">
                Understand the social, environmental, mobility, and infrastructure consequences of urban interventions before implementation.
            </div>
            """,
            unsafe_allow_html=True
        )

        btn_c1, btn_c2 = st.columns([1.3, 1.2])
        with btn_c1:
            if st.button("BEGIN ANALYSIS →", key="hero_launch_btn", type="primary", use_container_width=True):
                if on_start_callback:
                    on_start_callback(1)
                st.rerun()

        with btn_c2:
            if st.button("EXPLORE METHODOLOGY", key="hero_method_btn", use_container_width=True):
                if on_start_callback:
                    on_start_callback(4)
                st.rerun()

        st.markdown(
            """
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;margin-top:1.5rem;">
                GEOPANDAS INTERSECTION ENGINE &bull; OPENSTREETMAP VECTOR &bull; NETWORK ANALYSIS
            </div>
            """,
            unsafe_allow_html=True
        )

    with h_right:
        # CINEMATIC URBAN SPATIAL DIGITAL TWIN CANVAS (DARK SPATIAL INTELLIGENCE THEME)
        cinematic_canvas_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 100%;
    height: 100%;
    background-color: #0B0F14;
    color: #F7F7F5;
    font-family: 'JetBrains Mono', -apple-system, monospace;
    overflow: hidden;
  }
  .card-container {
    background: #151A21;
    border: 1px solid #2A313A;
    border-radius: 8px;
    padding: 0.85rem;
    height: 375px;
    width: 100%;
    display: flex;
    flex-direction: column;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    position: relative;
  }
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    border-bottom: 1px solid #2A313A;
    padding-bottom: 0.4rem;
  }
  .title {
    font-size: 0.68rem;
    font-weight: 600;
    color: #F7F7F5;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 0.4rem;
  }
  .hud-stage {
    font-size: 0.62rem;
    color: #5EEAD4;
    background: rgba(15, 118, 110, 0.15);
    border: 1px solid rgba(15, 118, 110, 0.35);
    padding: 0.15rem 0.5rem;
    border-radius: 3px;
    font-weight: 600;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
  }
  .canvas-wrapper {
    flex: 1;
    position: relative;
    background: #11161D;
    border: 1px solid #2A313A;
    border-radius: 6px;
    overflow: hidden;
    min-height: 280px;
  }
  canvas {
    display: block;
    width: 100%;
    height: 100%;
  }
  .coord-footer {
    position: absolute;
    bottom: 6px;
    right: 8px;
    font-size: 0.55rem;
    color: #6B7280;
    pointer-events: none;
    z-index: 2;
    background: rgba(17, 22, 29, 0.85);
    padding: 2px 6px;
    border-radius: 3px;
    border: 1px solid #2A313A;
  }
  .legend-overlay {
    position: absolute;
    top: 6px;
    left: 8px;
    font-size: 0.56rem;
    color: #7C8794;
    line-height: 1.45;
    pointer-events: none;
    z-index: 2;
    background: rgba(17, 22, 29, 0.85);
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid #2A313A;
  }
</style>
</head>
<body>
  <div class="card-container">
    <div class="header">
      <div class="title">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#0F766E" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 1 10 10"/><path d="M12 12 19 5"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
        02 / CINEMATIC SPATIAL NETWORK
      </div>
      <div id="hud-stage" class="hud-stage">01 / UNORGANIZED SPATIAL DATA</div>
    </div>
    <div class="canvas-wrapper">
      <div class="legend-overlay">
        <span style="color:#14B8A6;">&#8212;</span> PROPOSED INTERVENTION<br>
        <span style="color:rgba(107,114,128,0.7);">&#8212;</span> SPATIAL NETWORK<br>
        <span style="color:#5EEAD4;">&#9679;</span> AFFECTED NODES<br>
        <span style="color:rgba(204,251,241,0.6);">&#9638;</span> GIS IMPACT FIELD
      </div>
      <canvas id="shadowcost-canvas"></canvas>
      <div class="coord-footer">
        EPSG:4326 &bull; 28.5241 N, 77.2181 E
      </div>
    </div>
  </div>

  <script>
    (function() {
      const canvas = document.getElementById('shadowcost-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const stageLabel = document.getElementById('hud-stage');
      let width = 0;
      let height = 0;
      let startTime = null;
      let animId = null;

      function resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const wrapper = canvas.parentElement;
        width = wrapper.clientWidth || wrapper.getBoundingClientRect().width || 500;
        height = wrapper.clientHeight || wrapper.getBoundingClientRect().height || 290;
        canvas.width = Math.floor(width * dpr);
        canvas.height = Math.floor(height * dpr);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);
      }

      window.addEventListener('resize', resize);
      setTimeout(resize, 50);
      resize();

      let seed = 1337;
      function rand() {
        let x = Math.sin(seed++) * 10000;
        return x - Math.floor(x);
      }

      // 1. Target Spatial Network Nodes with 3D Depth Layers (0.5: Back, 1.0: Mid, 1.5: Front)
      const targetNodes = [
        // Primary Backbone Nodes (depth 1.0 - 1.5)
        { x: 0.12, y: 0.20, depth: 1.2, isBackbone: true },
        { x: 0.28, y: 0.18, depth: 1.0, isBackbone: true },
        { x: 0.45, y: 0.15, depth: 1.5, isBackbone: true },
        { x: 0.65, y: 0.22, depth: 1.0, isBackbone: true },
        { x: 0.84, y: 0.19, depth: 1.3, isBackbone: true },
        { x: 0.18, y: 0.38, depth: 1.0, isBackbone: true },
        { x: 0.35, y: 0.35, depth: 1.4, isBackbone: true },
        { x: 0.52, y: 0.32, depth: 1.1, isBackbone: true },
        { x: 0.72, y: 0.38, depth: 1.5, isBackbone: true },
        { x: 0.88, y: 0.42, depth: 1.0, isBackbone: true },
        { x: 0.10, y: 0.58, depth: 1.3, isBackbone: true },
        { x: 0.25, y: 0.52, depth: 1.1, isBackbone: true },
        { x: 0.42, y: 0.50, depth: 1.5, isBackbone: true },

        // Secondary Spatial Nodes (depth 0.5 - 1.0)
        { x: 0.60, y: 0.55, depth: 0.8, isBackbone: false },
        { x: 0.78, y: 0.60, depth: 0.7, isBackbone: false },
        { x: 0.15, y: 0.78, depth: 0.9, isBackbone: false },
        { x: 0.32, y: 0.72, depth: 1.0, isBackbone: false },
        { x: 0.50, y: 0.75, depth: 0.6, isBackbone: false },
        { x: 0.68, y: 0.78, depth: 0.9, isBackbone: false },
        { x: 0.85, y: 0.82, depth: 0.5, isBackbone: false },
        { x: 0.22, y: 0.90, depth: 0.8, isBackbone: false },
        { x: 0.40, y: 0.88, depth: 0.7, isBackbone: false },
        { x: 0.58, y: 0.92, depth: 0.6, isBackbone: false },
        { x: 0.75, y: 0.95, depth: 0.5, isBackbone: false },
        { x: 0.55, y: 0.22, depth: 0.9, isBackbone: false },
        { x: 0.78, y: 0.28, depth: 0.7, isBackbone: false },
        { x: 0.22, y: 0.65, depth: 0.8, isBackbone: false },
        { x: 0.38, y: 0.82, depth: 0.6, isBackbone: false },
        { x: 0.62, y: 0.42, depth: 1.1, isBackbone: true }
      ];

      // 2. 3D Parallax Particle Field (Background, Midground, Foreground)
      const particles = [];
      // 30 Background Particles (depth 0.5)
      for (let i = 0; i < 30; i++) {
        particles.push({
          x: rand() * 0.92 + 0.04,
          y: rand() * 0.92 + 0.04,
          depth: 0.5,
          vx: (rand() - 0.5) * 0.0003,
          vy: (rand() - 0.5) * 0.0003,
          size: 1.0 + rand() * 0.5,
          alpha: 0.25 + rand() * 0.15,
          color: '#374151'
        });
      }
      // 25 Midground Particles (depth 1.0)
      for (let i = 0; i < 25; i++) {
        particles.push({
          x: rand() * 0.90 + 0.05,
          y: rand() * 0.90 + 0.05,
          depth: 1.0,
          vx: (rand() - 0.5) * 0.0005,
          vy: (rand() - 0.5) * 0.0005,
          size: 1.6 + rand() * 0.8,
          alpha: 0.55 + rand() * 0.20,
          color: '#6B7280'
        });
      }
      // 15 Foreground Particles (depth 1.5)
      for (let i = 0; i < 15; i++) {
        particles.push({
          x: rand() * 0.88 + 0.06,
          y: rand() * 0.88 + 0.06,
          depth: 1.5,
          vx: (rand() - 0.5) * 0.0008,
          vy: (rand() - 0.5) * 0.0008,
          size: 2.5 + rand() * 1.0,
          alpha: 0.85 + rand() * 0.15,
          color: '#9CA3AF'
        });
      }

      // 3. Network Edges with Backbone vs Secondary Classification
      const edges = [];
      for (let i = 0; i < targetNodes.length; i++) {
        for (let j = i + 1; j < targetNodes.length; j++) {
          const dx = targetNodes[i].x - targetNodes[j].x;
          const dy = targetNodes[i].y - targetNodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 0.22 && edges.length < 44) {
            const isPrimary = targetNodes[i].isBackbone && targetNodes[j].isBackbone;
            edges.push({ i, j, dist, isPrimary, idx: edges.length });
          }
        }
      }

      // 4. Proposed Intervention Corridor (5 Points)
      const interventionPath = [
        { x: 0.12, y: 0.78 },
        { x: 0.32, y: 0.62 },
        { x: 0.50, y: 0.50 },
        { x: 0.68, y: 0.38 },
        { x: 0.85, y: 0.25 }
      ];

      function distToSegment(px, py, x1, y1, x2, y2) {
        const l2 = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
        if (l2 === 0) return Math.hypot(px - x1, py - y1);
        let t = ((px - x1) * (x2 - x1) + (py - y1) * (y2 - y1)) / l2;
        t = Math.max(0, Math.min(1, t));
        return Math.hypot(px - (x1 + t * (x2 - x1)), py - (y1 + t * (y2 - y1)));
      }

      const affectedNodeIndices = [];
      targetNodes.forEach((n, idx) => {
        let minDist = 999;
        for (let k = 0; k < interventionPath.length - 1; k++) {
          const p1 = interventionPath[k];
          const p2 = interventionPath[k + 1];
          const d = distToSegment(n.x, n.y, p1.x, p1.y, p2.x, p2.y);
          if (d < minDist) minDist = d;
        }
        if (minDist < 0.14) {
          affectedNodeIndices.push({ idx, minDist });
        }
      });
      affectedNodeIndices.sort((a, b) => a.minDist - b.minDist);

      // 5. GIS Buffer Region Boundary Points
      const impactHullPoints = [
        { x: 0.08, y: 0.84 },
        { x: 0.20, y: 0.78 },
        { x: 0.30, y: 0.72 },
        { x: 0.44, y: 0.62 },
        { x: 0.58, y: 0.58 },
        { x: 0.74, y: 0.45 },
        { x: 0.90, y: 0.32 },
        { x: 0.92, y: 0.20 },
        { x: 0.80, y: 0.18 },
        { x: 0.62, y: 0.30 },
        { x: 0.46, y: 0.40 },
        { x: 0.34, y: 0.52 },
        { x: 0.22, y: 0.58 },
        { x: 0.08, y: 0.70 }
      ];

      const prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

      function draw(timestamp) {
        if (!startTime) startTime = timestamp || performance.now();
        const now = timestamp || performance.now();
        let elapsed = prefersReduced ? 20.0 : (now - startTime) / 1000;

        let stageText = '01 / UNORGANIZED SPATIAL DATA';
        let step1Prog = Math.min(1, Math.max(0, elapsed / 2.0));
        let step2Prog = Math.min(1, Math.max(0, (elapsed - 2.0) / 2.5));
        let step4Prog = Math.min(1, Math.max(0, (elapsed - 6.5) / 2.0));
        let step5Prog = Math.min(1, Math.max(0, (elapsed - 8.5) / 2.0));
        let step6Prog = Math.min(1, Math.max(0, (elapsed - 10.5) / 2.0));
        let step7Prog = Math.min(1, Math.max(0, (elapsed - 12.5) / 2.0));

        if (elapsed < 2.0) {
          stageText = '01 / UNORGANIZED SPATIAL DATA';
        } else if (elapsed < 4.5) {
          stageText = '02 / SPATIAL NETWORK FORMATION';
        } else if (elapsed < 6.5) {
          stageText = '03 / LIVING SPATIAL GRAPH';
        } else if (elapsed < 8.5) {
          stageText = '04 / PROPOSED URBAN INTERVENTION';
        } else if (elapsed < 10.5) {
          stageText = '05 / SPATIAL NODE RESPONSE';
        } else if (elapsed < 12.5) {
          stageText = '06 / GEOSPATIAL IMPACT FIELD';
        } else if (elapsed < 14.5) {
          stageText = '07 / NETWORK DATA FLOW';
        } else {
          stageText = '08 / SPATIAL INTELLIGENCE ACTIVE';
        }

        if (stageLabel && stageLabel.innerText !== stageText) {
          stageLabel.innerText = stageText;
        }

        // Deep Midnight Canvas Background
        ctx.fillStyle = '#11161D';
        ctx.fillRect(0, 0, width, height);

        // Subtle Spatial Coordinate Grid
        ctx.strokeStyle = 'rgba(26, 32, 39, 0.6)';
        ctx.lineWidth = 1;
        const gridSize = 24;
        for (let x = 0; x < width; x += gridSize) {
          ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, height); ctx.stroke();
        }
        for (let y = 0; y < height; y += gridSize) {
          ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(width, y); ctx.stroke();
        }

        // Compute Node Positions with Parallax Drift by Depth
        const currentNodes = targetNodes.map((tn, idx) => {
          let driftX = 0;
          let driftY = 0;
          if (elapsed > 2.0) {
            // Parallax drift varies by depth layer
            const depthFactor = tn.depth || 1.0;
            driftX = Math.sin(elapsed * 0.6 * depthFactor + idx * 1.1) * 0.003 * width * depthFactor;
            driftY = Math.cos(elapsed * 0.5 * depthFactor + idx * 0.9) * 0.003 * height * depthFactor;
          }

          let lerpT = Math.min(1, Math.max(0, (elapsed - 1.2) / 2.2));
          let p = particles[idx];
          let startX = p ? p.x * width : tn.x * width;
          let startY = p ? p.y * height : tn.y * height;
          let finalX = tn.x * width + driftX;
          let finalY = tn.y * height + driftY;

          return {
            x: startX + (finalX - startX) * lerpT,
            y: startY + (finalY - startY) * lerpT,
            depth: tn.depth,
            isBackbone: tn.isBackbone
          };
        });

        // 1. STEP 6: GIS Impact Field Buffer Fill & Dashed Boundary
        if (step6Prog > 0) {
          ctx.save();
          ctx.fillStyle = `rgba(204, 251, 241, ${0.08 * step6Prog})`;
          ctx.strokeStyle = `rgba(204, 251, 241, ${0.22 * step6Prog})`;
          ctx.lineWidth = 1.2;
          ctx.setLineDash([4, 4]);

          ctx.beginPath();
          const firstPt = impactHullPoints[0];
          ctx.moveTo(firstPt.x * width, firstPt.y * height);
          for (let k = 1; k < impactHullPoints.length; k++) {
            const pt = impactHullPoints[k];
            ctx.lineTo(pt.x * width, pt.y * height);
          }
          ctx.closePath();
          ctx.fill();
          ctx.stroke();
          ctx.restore();
        }

        // 2. STEP 2: Progressive Network Edge Reveal (Primary Backbone first, then Secondary)
        if (step2Prog > 0) {
          edges.forEach((e) => {
            // Backbone edges reveal early (0.0 - 0.5 step2Prog), secondary edges later (0.4 - 1.0)
            const edgeDelay = e.isPrimary ? (e.idx / edges.length) * 0.4 : 0.35 + (e.idx / edges.length) * 0.5;

            if (step2Prog >= edgeDelay) {
              const localEProg = Math.min(1, (step2Prog - edgeDelay) / 0.25);
              const n1 = currentNodes[e.i];
              const n2 = currentNodes[e.j];

              const lineX2 = n1.x + (n2.x - n1.x) * localEProg;
              const lineY2 = n1.y + (n2.y - n1.y) * localEProg;

              let baseOpacity = e.isPrimary ? 0.38 : 0.22;
              if (elapsed > 4.5) {
                baseOpacity += Math.sin(elapsed * 1.5 + e.idx * 0.4) * 0.10;
              }
              // Impact field boost
              if (step6Prog > 0 && (affectedNodeIndices.some(a => a.idx === e.i) || affectedNodeIndices.some(a => a.idx === e.j))) {
                baseOpacity += 0.15 * step6Prog;
              }

              ctx.strokeStyle = `rgba(107, 114, 128, ${Math.min(0.65, baseOpacity)})`;
              ctx.lineWidth = e.isPrimary ? 1.2 : 0.9;
              ctx.beginPath();
              ctx.moveTo(n1.x, n1.y);
              ctx.lineTo(lineX2, lineY2);
              ctx.stroke();
            }
          });
        }

        // 3. STEP 7 & Ambient: Bi-Directional Luminous Data Flow Particles
        if (step7Prog > 0 || elapsed > 12.5) {
          edges.forEach((e, idx) => {
            if (idx % 2 === 0) {
              const dir = idx % 4 === 0 ? 1 : -1;
              const flowSpeed = 0.22;
              let pFrac = ((elapsed - 12.5) * flowSpeed + idx * 0.12) % 1;
              if (dir === -1) pFrac = 1 - pFrac;

              const n1 = currentNodes[e.i];
              const n2 = currentNodes[e.j];

              const px = n1.x + (n2.x - n1.x) * pFrac;
              const py = n1.y + (n2.y - n1.y) * pFrac;

              ctx.save();
              ctx.fillStyle = idx % 4 === 0 ? '#5EEAD4' : '#14B8A6';
              ctx.shadowColor = '#14B8A6';
              ctx.shadowBlur = 4;
              ctx.beginPath();
              ctx.arc(px, py, 1.8, 0, Math.PI * 2);
              ctx.fill();
              ctx.restore();
            }
          });
        }

        // 4. STEP 1 & 2: 3D Depth Particle Field & Network Nodes
        if (elapsed < 2.0) {
          // Draw particles sorted by depth
          particles.sort((a, b) => a.depth - b.depth).forEach((p) => {
            p.x += p.vx * p.depth;
            p.y += p.vy * p.depth;
            if (p.x < 0.02 || p.x > 0.98) p.vx *= -1;
            if (p.y < 0.02 || p.y > 0.98) p.vy *= -1;

            ctx.save();
            ctx.fillStyle = p.color;
            ctx.globalAlpha = p.alpha;
            ctx.beginPath();
            ctx.arc(p.x * width, p.y * height, p.size, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
          });
        } else {
          // Draw Network Nodes with depth scaling & breathing halo
          currentNodes.sort((a, b) => a.depth - b.depth).forEach((n) => {
            const nodeIdx = targetNodes.findIndex(tn => tn.x === (n.x / width) && tn.y === (n.y / height));
            let isAffected = affectedNodeIndices.some(item => item.idx === nodeIdx);
            let isBackbone = n.isBackbone;

            let nodeColor = isBackbone ? '#9CA3AF' : '#6B7280';
            let haloColor = null;
            let radius = (isBackbone ? 2.6 : 2.0) * n.depth;

            // Breathing pulse
            radius += Math.sin(elapsed * 2.0 + (nodeIdx || 0) * 0.8) * 0.35;

            if (isAffected && step5Prog > 0) {
              const affIndex = affectedNodeIndices.findIndex(item => item.idx === nodeIdx);
              const affDelay = (affIndex / affectedNodeIndices.length) * 0.7;
              if (step5Prog >= affDelay) {
                nodeColor = '#5EEAD4';
                haloColor = '#14B8A6';
                const pulsePhase = Math.sin((step5Prog - affDelay) * Math.PI * 3);
                radius = (3.2 + Math.max(0, pulsePhase * 1.8)) * n.depth;
              }
            } else if (isBackbone) {
              haloColor = 'rgba(20, 184, 166, 0.4)';
            }

            ctx.save();
            if (haloColor) {
              ctx.shadowColor = haloColor;
              ctx.shadowBlur = 6;
            }
            ctx.fillStyle = nodeColor;
            ctx.beginPath();
            ctx.arc(n.x, n.y, Math.max(1.2, radius), 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
          });
        }

        // 5. STEP 4: Proposed Intervention Corridor (Cinematic Draw & Pulse)
        if (step4Prog > 0) {
          ctx.save();
          ctx.strokeStyle = '#14B8A6';
          ctx.lineWidth = 2.8;
          ctx.shadowColor = '#14B8A6';
          ctx.shadowBlur = 8;
          ctx.beginPath();

          const totalSegs = interventionPath.length - 1;
          const currentProgSeg = step4Prog * totalSegs;

          ctx.moveTo(interventionPath[0].x * width, interventionPath[0].y * height);

          for (let k = 1; k < interventionPath.length; k++) {
            if (currentProgSeg >= k) {
              ctx.lineTo(interventionPath[k].x * width, interventionPath[k].y * height);
            } else if (currentProgSeg > k - 1) {
              const frac = currentProgSeg - (k - 1);
              const p1 = interventionPath[k - 1];
              const p2 = interventionPath[k];
              const cx = (p1.x + (p2.x - p1.x) * frac) * width;
              const cy = (p1.y + (p2.y - p1.y) * frac) * height;
              ctx.lineTo(cx, cy);
            }
          }
          ctx.stroke();

          // Draw corridor vertex nodes
          interventionPath.forEach((pt, k) => {
            if (currentProgSeg >= k) {
              ctx.fillStyle = '#5EEAD4';
              ctx.shadowColor = '#14B8A6';
              ctx.shadowBlur = 6;
              ctx.beginPath();
              ctx.arc(pt.x * width, pt.y * height, 3.6, 0, Math.PI * 2);
              ctx.fill();
            }
          });

          // Pulse traveling along intervention corridor
          if (step4Prog >= 0.9) {
            const pulseProg = (elapsed * 0.35) % 1;
            const pProg = pulseProg * totalSegs;
            const pIdx = Math.floor(pProg);
            const pFrac = pProg - pIdx;

            if (pIdx < totalSegs) {
              const pt1 = interventionPath[pIdx];
              const pt2 = interventionPath[pIdx + 1];
              const px = (pt1.x + (pt2.x - pt1.x) * pFrac) * width;
              const py = (pt1.y + (pt2.y - pt1.y) * pFrac) * height;

              ctx.fillStyle = '#CCFBF1';
              ctx.shadowColor = '#14B8A6';
              ctx.shadowBlur = 10;
              ctx.beginPath();
              ctx.arc(px, py, 4.0, 0, Math.PI * 2);
              ctx.fill();
            }
          }
          ctx.restore();
        }

        animId = requestAnimationFrame(draw);
      }

      animId = requestAnimationFrame(draw);

      window.addEventListener('beforeunload', function() {
        if (animId) cancelAnimationFrame(animId);
      });
    })();
  </script>
</body>
</html>"""

        components.html(cinematic_canvas_html, height=380, scrolling=False)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

    # 3. PRE-LOADED SPATIAL PRESETS (DE-BOXED)
    st.markdown(
        """
        <div style="margin-bottom:0.75rem;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;font-weight:700;color:#6B7280;letter-spacing:0.08em;display:flex;align-items:center;gap:0.5rem;">
                <span style="display:inline-block;width:6px;height:6px;background:#0F766E;border-radius:1px;"></span>
                PRE-LOADED SPATIAL PRESETS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        if st.button("01  Road Alignment — Saket, Delhi", key="preset_saket", use_container_width=True):
            st.session_state["current_city_query"] = "Saket, New Delhi"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    with d_col2:
        if st.button("02  Building Footprint — Bandra West, Mumbai", key="preset_bandra", use_container_width=True):
            st.session_state["current_city_query"] = "Bandra West, Mumbai"
            st.session_state["radius_km"] = 1.2
            st.session_state["active_tab_idx"] = 1
            st.session_state["scenario_substep"] = 1
            st.rerun()

    st.markdown("<div style='height:1.75rem;'></div>", unsafe_allow_html=True)

    # 4. FOUR SPATIAL LENSES (DE-BOXED EDITORIAL COLUMNS)
    st.markdown(
        """
        <div style="margin-bottom:1.25rem;">
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;">
                03 / EVALUATION FRAMEWORK
            </div>
            <h2 style="font-family:'Space Grotesk',sans-serif;font-size:1.35rem;font-weight:600;color:#F7F7F5;margin-top:0.2rem;letter-spacing:-0.02em;">
                Four Spatial Lenses for Pre-Implementation Intelligence
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    l1, l2, l3, l4 = st.columns(4)

    with l1:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    SOCIAL EXPOSURE
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Quantifies displaced residents, housing complex intersections, school/clinic proximity, and community route disruption.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l2:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    ENVIRONMENT
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Measures tree canopy removal (ha), green cover percentage loss, and urban heat island micro-climate exposure.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l3:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    MOBILITY NETWORK
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Calculates average added travel distance, network detour factors, daily trip rerouting, and peak-hour congestion multipliers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with l4:
        st.markdown(
            """
            <div style="border-left:2px solid #0F766E;padding-left:0.75rem;min-height:120px;">
                <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#F7F7F5;font-size:0.82rem;margin-bottom:0.4rem;letter-spacing:0.02em;">
                    INFRASTRUCTURE
                </div>
                <div style="font-size:0.78rem;color:#9AA4B2;line-height:1.5;">
                    Computes composite Shadow Impact Index (0-100), asset displacement counts, and rights-of-way cost tradeoffs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:1.75rem;'></div>", unsafe_allow_html=True)

    # 5. TECHNICAL STATUS STRIP & FOOTER (DE-BOXED)
    st.markdown(
        """
        <div style="border-top:1px solid rgba(107,114,128,0.15);padding-top:1rem;margin-top:1rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;font-family:'JetBrains Mono',monospace;font-size:0.68rem;color:#6B7280;">
            <div style="display:flex;gap:1.5rem;">
                <span>SYSTEM STATUS: <b style="color:#14B8A6;font-weight:600;">ACTIVE</b></span>
                <span>SPATIAL ENGINE: <b style="color:#9AA4B2;font-weight:500;">READY</b></span>
                <span>NETWORK MODEL: <b style="color:#9AA4B2;font-weight:500;">READY</b></span>
                <span>IMPACT ENGINE: <b style="color:#9AA4B2;font-weight:500;">READY</b></span>
            </div>
            <div style="color:#6B7280;">
                SHADOWCOST v2.5 &bull; URBAN SPATIAL INTELLIGENCE
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
