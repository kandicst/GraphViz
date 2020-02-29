var svg, container;

var birdsvg;
var birdg;

var zoom = null;

$(document).ready(function() {

    zoom = panZoom();
    get_data();

})

/**
* Dobavlja ucitane podatke i poziva njihov prikaz
* od strane trenutnog plugina za prikaz (ako postoji)
*/
function get_data() {
    $.ajax( {
        type : 'GET', url : '/dobavi_podatke',
        success : function (ret) {
            renderAll(ret);
        }
    })
}
function fit() {
    var bounds = container.node().getBBox();
    var parent = svg.node();
    var fullWidth = parent.clientWidth,
        fullHeight = parent.clientHeight;
    var width = bounds.width,
        height = bounds.height;
    var midX = bounds.x + width / 2,
        midY = bounds.y + height / 2;
    if (width == 0 || height == 0) return; // nothing to fit
    var scale = (0.75) / Math.max(width / fullWidth, height / fullHeight);
    lastScale = scale;
    var t = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];
    container
        .transition()
        .duration(3000)
		.call(zoom.translate(t).scale(scale).event);
}
function birdViewRefresh() {
    birdsvg.html("");
    let group = $("#group");
    let el = group.clone().attr("id","birdg");
    let domel = group[0];
    birdg = birdsvg.select("#birdg");
    
    var bounds = domel.getBBox();
    var parent = birdsvg.node();
    var fullWidth = parent.clientWidth,
        fullHeight = parent.clientHeight;
    var width = bounds.width,
        height = bounds.height;
    var midX = bounds.x + width / 2,
        midY = bounds.y + height / 2;
    if (width == 0 || height == 0) return; // nothing to fit
    var scale = (0.75) / Math.max(width / fullWidth, height / fullHeight);
    lastScale = scale;
    var t = [fullWidth / 2 - scale * midX, fullHeight / 2 - scale * midY];
    el.attr("transform","translate("+t[0]+","+t[1]+") scale("+scale+")");
    parent.appendChild(el[0]);
}


/**
* Funkcija koja predstavlja "interfejs" core modula
* za graficki prikaz ucitanih elemenata, i koju plugin za prikaz mora da implementira
* @param  {JSON} data  ucitani podaci u obliku grafa {nodes : {}, links : {}}
* @param  {SVGElement} svg Kontejner za graficke elemente
* @param  {SVGElement} container <g> element unutar <svg> koji grupise kreirane elemente
*/
function draw(data, svg, container) {

}


function renderAll(data) {

    svg = d3.select("#canvas");
    container = d3.select("#canvas").select("#group").html("");
    birdsvg = d3.select("#birdsvg");
    birdg = birdsvg.select("#birdg").html("");

    draw(data, svg, container);
    setTimeout(fit, 100);
    birdViewRefresh();
    setInterval(birdViewRefresh,100);

}