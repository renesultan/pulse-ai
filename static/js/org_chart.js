document.addEventListener('DOMContentLoaded', async function() {
    // Get org structure data from the page
    const orgStructureText = document.getElementById('org-structure-data').dataset.orgStructure;
    const companyName = document.getElementById('company-name').innerText;
    const departmentName = document.getElementById('department-name').dataset.departmentName;
    const reportingLine = document.getElementById('reporting-line-data')?.dataset.reportingLine || '';
    
    // Parse the organization structure
    try {
        // Show loading overlay
        showLoadingOverlay();
        
        // Send the org structure to the API for parsing
        const response = await fetch('/api/parse-org-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                org_structure: orgStructureText,
                company_name: companyName,
                department_name: departmentName,
                reporting_line: reportingLine,
                save_to_db: true // Save to database
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to parse organization data');
        }
        
        const hierarchyData = await response.json();
        
        // Initialize the org chart
        initOrgChart(hierarchyData);
        
        // Hide loading overlay
        hideLoadingOverlay();
    } catch (error) {
        console.error('Error initializing org chart:', error);
        hideLoadingOverlay();
        showError('Failed to create organization chart. Please check your data format and try again.');
    }
    
    // Initialize UI event listeners
    initUIEventListeners();
});

function initOrgChart(data) {
    // Get container dimensions
    const container = document.getElementById('chart-container');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    // Define node dimensions
    const nodeWidth = 180;
    const nodeHeight = 80;
    const nodeSpacing = 50;
    
    // Create D3 tree layout
    const root = d3.hierarchy(data);
    
    // Count descendants to determine tree dimensions
    const leaves = root.leaves();
    const depth = root.height;
    
    // Calculate dimensions based on the number of nodes
    const treeWidth = Math.max(width, leaves.length * (nodeWidth + nodeSpacing));
    const treeHeight = Math.max(height, (depth + 1) * (nodeHeight + nodeSpacing * 2));
    
    // Create the tree layout
    const treeLayout = d3.tree()
        .size([treeWidth - nodeWidth * 2, treeHeight - nodeHeight * 2])
        .nodeSize([nodeWidth + nodeSpacing, nodeHeight + nodeSpacing]);
        
    // Compute the layout
    treeLayout(root);
    
    // Create SVG element
    const svg = d3.select('#chart-container')
        .append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', [-nodeWidth, -nodeHeight, treeWidth, treeHeight].join(' '))
        .call(d3.zoom()
            .scaleExtent([0.1, 3])
            .on('zoom', function(event) {
                g.attr('transform', event.transform);
                updateMiniMap(event.transform);
            }))
        .on('dblclick.zoom', null);
    
    // Create the root group for transformation
    const g = svg.append('g')
        .attr('class', 'org-chart');
    
    // Create links between nodes
    const links = g.append('g')
        .attr('class', 'links')
        .selectAll('path')
        .data(root.links())
        .enter()
        .append('path')
        .attr('class', 'link')
        .attr('d', d => {
            return `M${d.source.x},${d.source.y + nodeHeight / 2}
                    C${d.source.x},${(d.source.y + d.target.y) / 2}
                     ${d.target.x},${(d.source.y + d.target.y) / 2}
                     ${d.target.x},${d.target.y - nodeHeight / 2}`;
        });
    
    // Create node groups
    const nodes = g.append('g')
        .attr('class', 'nodes')
        .selectAll('.node')
        .data(root.descendants())
        .enter()
        .append('g')
        .attr('class', 'node')
        .attr('transform', d => `translate(${d.x - nodeWidth / 2},${d.y - nodeHeight / 2})`)
        .on('click', function(event, d) {
            // Toggle selection
            d3.selectAll('.node').classed('selected', false);
            d3.select(this).classed('selected', true);
            
            // Show node details
            showNodeDetails(d.data);
            event.stopPropagation();
        });
    
    // Create node rectangles
    nodes.append('rect')
        .attr('width', nodeWidth)
        .attr('height', nodeHeight)
        .attr('rx', 6)
        .attr('ry', 6);
    
    // Add name text
    nodes.append('text')
        .attr('class', 'name')
        .attr('x', nodeWidth / 2)
        .attr('y', nodeHeight / 3)
        .attr('text-anchor', 'middle')
        .text(d => d.data.name);
    
    // Add title text
    nodes.append('text')
        .attr('class', 'title')
        .attr('x', nodeWidth / 2)
        .attr('y', nodeHeight / 3 + 20)
        .attr('text-anchor', 'middle')
        .text(d => d.data.title);
    
    // Hide node details when clicking on empty space
    svg.on('click', function() {
        hideNodeDetails();
        d3.selectAll('.node').classed('selected', false);
    });
    
    // Center the tree initially
    const initialTransform = d3.zoomIdentity
        .translate(width / 2, height / 3)
        .scale(0.7);
    
    svg.call(d3.zoom().transform, initialTransform);
    g.attr('transform', initialTransform);
    
    // Initialize mini-map
    initMiniMap(root, treeWidth, treeHeight, initialTransform);
    
    // Initialize zoom controls
    initZoomControls(svg);
    
    // Save references for later use
    window.orgChart = {
        svg,
        g,
        root,
        width,
        height,
        treeWidth,
        treeHeight,
        nodeWidth,
        nodeHeight
    };
}

function initMiniMap(root, treeWidth, treeHeight, initialTransform) {
    const miniMap = d3.select('.mini-map-content');
    const miniMapWidth = 150;
    const miniMapHeight = 100;
    
    // Calculate scale factor for mini-map
    const scaleX = miniMapWidth / treeWidth;
    const scaleY = miniMapHeight / treeHeight;
    const scale = Math.min(scaleX, scaleY);
    
    // Create mini-map SVG
    const miniSvg = miniMap.append('svg')
        .attr('width', '100%')
        .attr('height', '100%')
        .attr('viewBox', [0, 0, treeWidth, treeHeight].join(' '));
    
    // Draw simplified tree representation
    const miniG = miniSvg.append('g')
        .attr('transform', `scale(${scale})`);
    
    // Add nodes to mini-map as simple dots
    root.descendants().forEach(node => {
        miniG.append('circle')
            .attr('cx', node.x)
            .attr('cy', node.y)
            .attr('r', 2 / scale)
            .attr('fill', '#f64277');
    });
    
    // Add links between nodes
    root.links().forEach(link => {
        miniG.append('line')
            .attr('x1', link.source.x)
            .attr('y1', link.source.y)
            .attr('x2', link.target.x)
            .attr('y2', link.target.y)
            .attr('stroke', '#ccc')
            .attr('stroke-width', 1 / scale);
    });
    
    // Add viewport indicator
    const viewport = d3.select('.mini-map')
        .append('div')
        .attr('class', 'mini-map-viewport');
    
    // Update viewport size and position based on zoom transform
    updateMiniMap(initialTransform);
}

function updateMiniMap(transform) {
    if (!window.orgChart) return;
    
    const { width, height, treeWidth, treeHeight } = window.orgChart;
    const miniMapWidth = 150;
    const miniMapHeight = 100;
    
    // Calculate scale factor for mini-map
    const scaleX = miniMapWidth / treeWidth;
    const scaleY = miniMapHeight / treeHeight;
    const scale = Math.min(scaleX, scaleY);
    
    // Calculate viewport dimensions and position
    const viewWidth = width / transform.k * scale;
    const viewHeight = height / transform.k * scale;
    
    // Calculate viewport position based on transform
    const centerX = treeWidth / 2 - transform.x / transform.k;
    const centerY = treeHeight / 2 - transform.y / transform.k;
    
    const viewX = (centerX - width / (2 * transform.k)) * scale;
    const viewY = (centerY - height / (2 * transform.k)) * scale;
    
    // Update viewport indicator
    d3.select('.mini-map-viewport')
        .style('width', `${viewWidth}px`)
        .style('height', `${viewHeight}px`)
        .style('left', `${Math.max(0, viewX)}px`)
        .style('top', `${Math.max(0, viewY)}px`);
}

function initZoomControls(svg) {
    const zoomIn = document.querySelector('.zoom-in');
    const zoomOut = document.querySelector('.zoom-out');
    
    // Get D3 zoom behavior
    const zoom = d3.zoom().on('zoom', function(event) {
        window.orgChart.g.attr('transform', event.transform);
        updateMiniMap(event.transform);
    });
    
    // Zoom in button
    zoomIn.addEventListener('click', function() {
        svg.transition().duration(300).call(
            zoom.scaleBy, 1.3
        );
    });
    
    // Zoom out button
    zoomOut.addEventListener('click', function() {
        svg.transition().duration(300).call(
            zoom.scaleBy, 0.7
        );
    });
}

function showNodeDetails(nodeData) {
    const nodeDetails = document.querySelector('.node-details');
    const nameElem = document.getElementById('detail-name');
    const titleElem = document.getElementById('detail-title');
    const reportsToElem = document.getElementById('detail-reports-to');
    
    // Set details content
    nameElem.textContent = nodeData.name;
    titleElem.textContent = nodeData.title;
    
    // Check if this node has a parent (reports to someone)
    const parent = d3.select('.node.selected').datum().parent;
    if (parent && parent.data.name) {
        reportsToElem.textContent = parent.data.name;
        document.querySelector('.detail-reports-to').style.display = 'block';
    } else {
        document.querySelector('.detail-reports-to').style.display = 'none';
    }
    
    // Show direct reports if any
    const directReports = nodeData.children || [];
    const reportsElem = document.getElementById('detail-direct-reports');
    
    if (directReports.length > 0) {
        const reportsList = directReports.map(report => report.name).join(', ');
        reportsElem.textContent = reportsList;
        document.querySelector('.detail-direct-reports').style.display = 'block';
    } else {
        document.querySelector('.detail-direct-reports').style.display = 'none';
    }
    
    // Show the details panel
    nodeDetails.classList.add('visible');
}

function hideNodeDetails() {
    const nodeDetails = document.querySelector('.node-details');
    nodeDetails.classList.remove('visible');
}

function initUIEventListeners() {
    // Close details button
    document.querySelector('.close-details').addEventListener('click', function() {
        hideNodeDetails();
        d3.selectAll('.node').classed('selected', false);
    });
    
    // Export chart button
    document.querySelector('.export-btn').addEventListener('click', function() {
        document.querySelector('.export-panel').classList.add('visible');
    });
    
    // Cancel export button
    document.querySelector('.cancel-export').addEventListener('click', function() {
        document.querySelector('.export-panel').classList.remove('visible');
    });
    
    // Confirm export button
    document.querySelector('.confirm-export').addEventListener('click', function() {
        const selectedFormat = document.querySelector('input[name="export-format"]:checked').value;
        exportChart(selectedFormat);
        document.querySelector('.export-panel').classList.remove('visible');
    });
}

function exportChart(format) {
    if (!window.orgChart) return;
    
    // Get the SVG element
    const svg = window.orgChart.svg.node();
    
    if (format === 'png') {
        // For PNG export
        try {
            const svgData = new XMLSerializer().serializeToString(svg);
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            
            // Set canvas dimensions
            canvas.width = window.orgChart.treeWidth;
            canvas.height = window.orgChart.treeHeight;
            
            // Create image
            const img = new Image();
            const svgBlob = new Blob([svgData], {type: 'image/svg+xml'});
            const url = URL.createObjectURL(svgBlob);
            
            img.onload = function() {
                ctx.fillStyle = '#f9f9f9';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.drawImage(img, 0, 0);
                URL.revokeObjectURL(url);
                
                // Trigger download
                const a = document.createElement('a');
                a.download = `${document.getElementById('company-name').innerText}-org-chart.png`;
                a.href = canvas.toDataURL('image/png');
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            };
            
            img.src = url;
        } catch (error) {
            console.error('Error exporting as PNG:', error);
            showError('Failed to export as PNG. Please try again.');
        }
    } else if (format === 'pdf') {
        // For future PDF implementation
        alert('PDF export will be implemented in a future update.');
    }
}

function showLoadingOverlay() {
    const overlay = document.querySelector('.loading-overlay');
    overlay.style.display = 'flex';
}

function hideLoadingOverlay() {
    const overlay = document.querySelector('.loading-overlay');
    overlay.style.display = 'none';
}

function showError(message) {
    alert(message);
}