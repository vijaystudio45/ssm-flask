$(document).ready(function () {
    $("#quantity").keyup(function () {

        var service_cost = $("#selected_value_hidden").text()
        var quantity = $("#quantity").val();
        if (quantity == '') { quantity = 0 }
        if (quantity == " - Not Required - ") {
            quantity = $("#comments").val().split("\n");
        }
        service_cost = parseFloat(service_cost / 1000).toFixed(6);
        total = quantity * service_cost;
        total = total.toFixed(4);
        $("#payment").val(`${quantity} x $${service_cost} = ${total}`);

    });


    // See if view more button is needed

    children_count = 0
    $('.service-list').children().each(function () {
        children_count += 1
        if (children_count > 4) {
            $(this).hide();
            $("#view_more").show();
        }
    })

});

function viewmore() {

    $('.service-list').children().each(function () {
        $(this).show();
    })
    $("#view_more").hide();
}