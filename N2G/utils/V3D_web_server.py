graph_browser = """
<head>
  <style> body { margin: 0; } </style>
  
  <script src="//unpkg.com/dat.gui"></script>
  <script src="//unpkg.com/three"></script>
  <script src="//unpkg.com/three/examples/js/renderers/CSS2DRenderer.js"></script>
  <script src="//unpkg.com/3d-force-graph"></script>

  <style>
    .node-label {
      font-size: 12px;
      padding: 1px 4px;
      border-radius: 4px;
      background-color: white;
      user-select: none;
    }
  </style>  
</head>

<body>
  <div id="3d-graph"></div>
 
  <script type="module">  
    import { UnrealBloomPass } from '//cdn.skypack.dev/three/examples/jsm/postprocessing/UnrealBloomPass.js';  
    
    const elem = document.getElementById("3d-graph");
    const json_data = {{ json_data | json }};
    var gData = JSON.parse(json_data);
    
    // create graph
    const Graph = ForceGraph3D({
      extraRenderers: [new THREE.CSS2DRenderer()]
    })(elem)
        .enableNodeDrag(true)
        .nodeLabel(node => node.label)
        .graphData(gData)
        .onNodeDragEnd(node => {
          node.fx = node.x;
          node.fy = node.y;
          node.fz = node.z;
        })
	    .nodeThreeObject(node => {
          const nodeEl = document.createElement('div');
          nodeEl.textContent = node.label;
          nodeEl.style.color = "black";
          nodeEl.className = 'node-label';
          return new THREE.CSS2DObject(nodeEl);
        })
        .nodeThreeObjectExtend(true);
        
    // add bloom
    const bloomPass = new UnrealBloomPass();
    bloomPass.strength = 3;
    bloomPass.radius = 1;
    bloomPass.threshold = 0.1;
    Graph.postProcessingComposer().addPass(bloomPass);
    
    //Define GUI
    const Settings = function() {
      this.Distance = 20;
      this.isAnimationActive = true;
      this.isRotating = false;
    };
    var settings = new Settings();
    const gui = new dat.GUI();

    // link distance:
    const linkForce = Graph
      .d3Force('link')
      .distance(settings.Distance);

    const controllerOne = gui.add(settings, 'Distance', 0, 100);
    controllerOne.onChange(updateLinkDistance);
    function updateLinkDistance() {
      linkForce.distance(settings.Distance);
      Graph.numDimensions(3); // Re-heat simulation
    }
    
    // pause / resume animation
    const controllerAnim = gui.add(settings, 'isAnimationActive');
    controllerAnim.onChange(updateAnimation);
    function updateAnimation() {
      Settings.isAnimationActive ? Graph.resumeAnimation() : Graph.pauseAnimation() ;
      Settings.isAnimationActive = !Settings.isAnimationActive;
    }    

  </script>
</body>     
"""
