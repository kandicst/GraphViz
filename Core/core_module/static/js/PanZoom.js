/**
* Funkcija koja omogucava pan i zoom funkcionalnosti
* nad trenutnim prikazom iz plugina
*/
function panZoom(){

    let zoom = d3.behavior.zoom();
    var svg = d3.select("#canvas")
    .call(zoom.on("zoom", function (d, i) {
        svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")");
    }))
    .select("g");
    return zoom;
}