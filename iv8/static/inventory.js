// https://codereview.stackexchange.com/a/93367

function makeTag(openTag, closeTag){
  return function(content){
    return openTag+content+closeTag;  
  };
};
tHead=makeTag("<thead>","</thead>");
tBody=makeTag("<tbody>","</tbody>");
td=makeTag("<td>","</td>");
th=makeTag("<th>","</th>");
tr=makeTag("<tr>","</tr>");

function insertBasicTable(data,elem){
    elem.html(
        tHead(
            tr(
                th("Unit")+
                th("Inventory")
            )
        )+
        tBody(
            Object.keys(data).reduce(function(o,n){
                return o+tr(
                    td(n)+""+
                    td(data[n]+"")
                );
            },"")
        )
    );
};


$( document ).ready(function() {
  var viewer = $("#inventory");
  if(viewer) {
    var scope = viewer.data("scope");
    function refresh() {
      $.getJSON( "/api/"+scope+"/inventory", function(items) {
        for(var key in items) {
          items[key] = syntaxHighlight(JSON.stringify(items[key], null, 2))
            .replace(/[{}\n]/g, "").replace(/,/, "<br>\n");
        }
        insertBasicTable(items,viewer);
      }).always(function() {
        setTimeout(refresh, 1000);
      });
    }
    refresh();
  }
});
