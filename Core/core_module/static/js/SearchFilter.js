
$("#submit_button").on('click', function () {
    let operation = $("#switch")[0].checked;
    $.ajax({
        type: 'GET', url: '/dobavi_podatke',
        success: function (ret) {
            obradi_podatke(ret, operation);
        },
        error: function () {
            alert('greska');
        }
    })

})


function obradi_podatke(data, operation) {

    if (operation) {
        data = filter_data(data);
        filter_tree()
    }
    else {
        data = search_data(data);
        search_tree()
    }

    renderAll(data);

}


function filter_data(data) {
    var param = $("#search").val();
    var regex = new RegExp(param);

    if (param == "")
        return data;

    nodes = [];
    nodes_set_id = new Set();
    for (node of data.nodes) {
        if ((node.name).toUpperCase().includes(param.toUpperCase()) ||
            regex.test((node.name))) {
            nodes.push(node);
            nodes_set_id.add(node.id);
        }
    }


    links = [];
    for (link of data.links) {
        if (nodes_set_id.has(link.target_id) &&
            nodes_set_id.has(link.source_id)
        ) {
            links.push(link);
        }
    }
    data.links = links;
    data.nodes = nodes;
    return data
}


function search_data(data) {
    var param = $("#search").val();
    var regex = new RegExp(param);

    if (param == "")
        return data;

    nodes_set_id = new Set();

    for (node in data.nodes) {
        if ((data.nodes[node].name).toUpperCase().includes(param.toUpperCase()) ||
            regex.test(data.nodes[node].name)) {

            data.nodes[node].bold = true;
            nodes_set_id.add(data.nodes[node].id);
        }
        else
            data.nodes[node].bold = false;
    }


    links = [];
    for (link in data.links) {
        if (nodes_set_id.has(data.links[link].target_id) &&
            nodes_set_id.has(data.links[link].source_id)) {
            data.links[link].bold = true;
        } else
            data.links[link].bold = false;

    }
    return data


}


function filter_tree() {
    resetTree()
    let param = $("#search").val();
    $(".tree-node").each(function () {
        let node = $(this);
        if (!node.attr("id").toUpperCase().includes(param.toUpperCase())) {
            node.addClass("hide")
        }
    });

}

function search_tree() {
    resetTree()
    let param = $("#search").val();
    let first_match = "";

    $(".tree-node").each(function () {
        let node = $(this);
        if (node.attr("id").toUpperCase().includes(param.toUpperCase())) {
            // treba mi samo prvi da bih skrolao do njega
            if (!first_match) {
                first_match = node.attr("id");
            }

            node.children(".caret").addClass("selected")
        }
    });

    // skrola do prvog poklapanja
    if(first_match){
        document.getElementById(first_match).scrollIntoView();
    }

}

function resetTree() {
    $("#root-node").addClass("active");
    $(".tree-node.hide").removeClass("hide");
    $(".caret.selected").removeClass("selected")
}
