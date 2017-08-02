var formatInputs = $(document).ready( function () {
    $("input").addClass("form-control");
    $("button").addClass("btn btn-outline-primary");
    $("#id_session_canceled").removeClass("form-control");
    $("#id_tutee_absent").removeClass("form-control");
    $("#id_session_canceled").addClass("checkbox");
    $("#id_tutee_absent").addClass("checkbox");
    $("select").addClass("form-control");
	$("#panel-one").toggle();
	$("#panel-two").toggle();
	$("#clickable-two").click(function () {
		$("#panel-two").toggle("slow");
	});
	$("#clickable-one").click(function () {
		$("#panel-one").toggle("slow");
	});
    if ($(window).innerWidth() < 420) {
        $('td').each( function () {
            if($(this).html().slice(-3) == "day"){
                    $(this).html($(this).html().slice(0,3))
                }
            });
        }
});

$(".poll-button").click( function () {
	if($(this).prev().css("display") == "none") {
		$(this).prev().show("slow");
		$(this).text("-");
	}
	else {
		$(this).prev().hide("slow");
		$(this).text("+");
	}
});
