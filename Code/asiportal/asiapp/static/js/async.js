var TOTAL_FORMS = $("#id_form-TOTAL_FORMS")
var NEXT_FORM = parseInt(TOTAL_FORMS.val())
var BASE_ROW = $("tbody>tr").last().clone()
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var ws_path = ws_scheme + "://" + window.location.host + window.location.pathname + "stream/";
console.log("Attempting to connect to : " + ws_path);
var socket = new ReconnectingWebSocket(ws_path);

$(document).ready(function() {
    $("#postem").click(function(){
        socket.send(JSON.stringify({'formdata' : $('form').serialize()}));
    });

socket.onmessage = function(e) { console.log(e.data); }
  $("#addrow").on("click", function(){
    var clone = prepareClone();
    console.log($(clone).attr('id'));
    $("tbody").append(clone);
    updateTotalForms();
    reFormat();

      socket.onmessage = function(message)
      {
          console.log("Got message : " + message);
      }


      $("tr#" + $(clone).attr('id') + ">td>button[id$=-DELETE]").on(
          "click", function() { 
              console.log("got a click on : " + this);
              delForms(this); 
        });

        function delForms(form){
            console.log(form);
            var formNum = form.name.split('-DELETE')[0];
            console.log("no problem yet");
            $("tr#"+formNum).remove();
            decTotalForms();
            reIndexForms();
    }});

});

function prepareClone(){
    var re = /form-[0-9]+/gi
    var next_form_prefix = function() { return "form-" + NEXT_FORM; };
    return "<tr id=" + next_form_prefix() +">" + BASE_ROW.html().replace(re, next_form_prefix()) + "</tr>";
}

function updateTotalForms(){
TOTAL_FORMS.prop("value", function() { return ++NEXT_FORM; });
}

function decTotalForms(){
  TOTAL_FORMS.prop("value", function() {
      if(NEXT_FORM - 1 < 0)
      {
          console.log("uh oh");
          NEXT_FORM = 0
      }
    else
      {
        return --NEXT_FORM;
      }
  });
}

function reIndexForms()
{
  $("tr[id^=form]").each(function(i) {
    var newform = 'form-' + i;
    var new_id = this.id.replace(/form-[0-9]+/i, newform);
    console.log("new id name : " + new_id);
    $(this).prop('id', new_id)
    $(this).children().each(function() {
        $(this).children().each(function() { 
          var new_id = this.id.replace(/id_form-[0-9]+/i, 'id_form-' + i);
          $(this).prop('id', new_id);
          var new_name = this.name.replace(/form-[0-9]+/i, newform);
          $(this).prop('name', new_name);
        })
      })
    })
}
function reFormat()
{
    $("input").addClass("form-control");
    $("select").addClass("form-control");
    $("button").addClass("btn btn-outline-primary");
}
