$( document ).ready(function() {
    $(".rightSearchExtra").hide();
    $("#cmn-toggle-1").change(function() {
        if (document.getElementById('cmn-toggle-1').checked) {
            $("#label-cmn").text("Use live?");
            $(".rightSearchExtra").show();
        } else {
            $("#label-cmn").text("Use demo?");
            $(".rightSearchExtra").hide();
        }
    });
    $("#searchPad").click(function() {
        $.ajax({
            method: "GET",
            url: "/api/demo/bars/"+document.getElementById("searchBar").value+"/",
            data: {"hours": parseInt($("#hours").val()), "mins": parseInt($("#mins").val())},
            success: function(data) {
                // Remove all existing child nodes
                var results = document.getElementById("searchResults");
                while (results.firstChild) {
                    results.removeChild(results.firstChild);
                }

                var frag = document.createDocumentFragment();
                if (data.results.length > 0) {
                    // Create result list
                    data.results.forEach(function(obj) {
                        var li = document.createElement("li");
                        var a = document.createElement("a");                        
                        var h3 = document.createElement("h3");
                        h3.appendChild(document.createTextNode(obj.name));
                        var icon = document.createElement("i");
                        icon.setAttribute("aria-hidden", true);
                        if (obj.hotness === 1) {
                            icon.className = "fa fa-thumbs-o-up";
                        } else if (obj.hotness === -1) {
                            icon.className = "fa fa-thumbs-o-down";
                        } else {
                            icon.className = "fa fa-meh-o";
                        }
                        a.href = "/demo/bar/"+obj.id+"?hours="+parseInt($("#hours").val())+"&mins="+parseInt($("#mins").val());
                        li.appendChild(h3);
                        li.appendChild(icon);                        
                        a.appendChild(li);
                        frag.appendChild(a);
                    });
                } else {
                    // Display message that no bars were returned
                    var li = document.createElement("li");
                    li.appendChild(document.createTextNode("No bars with that zipcode."));
                    frag.appendChild(li);
                }
                
                results.appendChild(frag);
            },
            error: function(jqXHR, textStatus, data) {
                var results = document.getElementById("searchResults");
                while (results.firstChild) {
                    results.removeChild(results.firstChild);
                }                
                var frag = document.createDocumentFragment();
                var li = document.createElement("li");
                li.appendChild(document.createTextNode(
                    jqXHR.status === 400 ? data.errors : "You must enter a valid 5-digit zipcode."));
                frag.appendChild(li);
                results.appendChild(frag);
            }
        });
    });
    $('#searchBar').keypress(function (e) {
        var key = e.which;
        if(key == 13)  // the enter key code
        {
            $("#searchPad").trigger('click');
            return false;  
        }
    }); 
    if (window.zipcode !== "") {
        $("#searchBar").val(window.zipcode);
        $("#searchPad").trigger('click');
    }
    if (window.hours !== "" || window.mins !== "") {
        $("#label-cmn").text("Use live?");
        $(".rightSearchExtra").show();
    }
    if (window.hours !== "") {
        $("#hours").val(window.hours).trigger('change');
    }
    if (window.mins !== "") {
        $("#mins").val(window.mins).trigger('change');
    }
});