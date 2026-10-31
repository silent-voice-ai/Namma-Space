Namma Space

(⁠nammaspace-3d.netlify.app⁠)
Overview
Namma Space is a custom-coded web-based 3D spatial mapping and viewing platform. Designed for indoor navigation and spatial data visualization, the project utilizes a custom data processing pipeline and a Three.js rendering engine to deliver an interactive web experience without relying on external, pre-rendered 3D Gaussian Splat assets.

Key Features:
 Custom WebGL Rendering: Powered by Three.js with a custom ⁠PLYLoader⁠ integration to parse and render local spatial coordinate datasets.
 Interactive HUD & Controls: Built-in HTML/CSS heads-up display offering real-time status indicators, mouse look, and WASD free-roaming navigation.
 
 Orthographic Minimap: Integrated secondary camera feed tracking positioning dynamically across the workspace.
 Competition Compliance: Adheres strictly to custom indoor mapping guidelines by rendering proprietary point cloud structures instead of black-box third-party assets.

Technical Architecture:
 Front-End: HTML5, CSS3, Vanilla JavaScript.
 3D Engine: Three.js (WebGL).
 Data Format: Custom processed ⁠.ply⁠ point cloud dataset (⁠points3D.ply⁠).
 Hosting Platform: Netlify Cloud Infrastructure.
 
Installation & Local Setup:
1. Clone or download the project repository to your local machine.
2. Open a terminal inside the project root folder.
3. Start a local HTTP server using Python:
Python -m http.server 8000
4. Open your web browser and navigate to ⁠http://localhost:8000⁠ to view the local application.

Live Deployment
 Live URL: [https://nammaspace-3d.netlify.app] (https://nammaspace-3d.netlify.app)
