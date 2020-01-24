var svg = d3.select("svg"),
width = svg.attr("width") - 50,
height = svg.attr("height") - 50,
color = d3.scale.category10();



var dataset = JSON.parse(`
{"nodes":[{"id" : 0, "name":"Jimmy McNulty", "group": 0, "family": "The Law", "influence":40},
    {"id" : 11,"name":"Stringer", "group": 1, "family": "The Street", "influence":15},
    {"id" : 2,"name":"Bodie", "group": 1, "family": "The Street", "influence":24},
    {"id" : 3,"name":"Clay Davis", "group": 2, "family": "The Press", "influence":18},
    {"id" : 40,"name":"Bubbles", "group": 1, "family": "The Street", "influence":36},
    {"id" : 5,"name":"Cedric Daniels", "group": 0, "family": "The Law", "influence":22}],
"links":[{"source":0,"target":11,"weight":9},
    {"source":2,"target":3,"weight":21},
    {"source":2,"target":40,"weight":30},
    {"source":2,"target":5,"weight":23},
    {"source":40,"target":0,"weight":13}]}
`);


var nodes = dataset.nodes,
    links = dataset.links;

links.forEach(function(link) {
    link.source = nodes.find(x => x.id == link.source)
    link.target = nodes.find(x => x.id == link.target)
    link.weight = (link.source.influence + link.target.influence)/2
});

//layout
var force = d3.layout.force()
            .size([width, height])
            .nodes(nodes)
            .links(links)
            .on("tick", tick)
            .gravity(0.05)
            .charge(-200)
            .linkDistance(300)
            .start();

//dodavanje veza izmedju cvorova
var link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("stroke-width", function(d){ return d.weight/5; });

//cvorovi se moraju dodati kasnije
// da se ne bi videle linije preko kruga
var node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")

node.append("text")
    .attr("dx", 15)
    .text(function(d){ return d.name; })
    .attr("font-size", function(d){ return d.influence * 1.5 > 11 ? d.influence*1.5: 11; })


node.append("circle")
    .attr("r", function(d){ return d.influence/2>5 ? d.influence/2 : 5; })    
    .attr("fill", function(d){ return color(d.group*10); })
    .attr("data-legend",function(d) { return d.group});


// legenda grafa
var legend = svg.selectAll(".legend")
    .data(color.domain())
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

legend.append("rect")
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", color);

legend.append("text")
    .attr("x",  25)
    .attr("y", 9)
    .attr("dy", ".35em")
    .text(function(d) { return nodes.find(x => x.group == d/10).family; });

// funkcija za 
function tick (d){

    node.attr("transform", function(d) {return "translate(" + d.x + "," + d.y + ")";})
        .call(force.drag);

    //koordinate veza
    link.attr("x1", function(d){ return d.source.x; })
    link.attr("y1", function(d){ return d.source.y; })
    link.attr("x2", function(d){ return d.target.x; })
    link.attr("y2", function(d){ return d.target.y; });

}


