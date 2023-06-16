$(document).ready(function () {
    window.first = 0;
    window.last = 3;

    window.max = 5;
    window.min = 0;

    window.counter = 0;

    $('.service_quantity').each(function (index) {
        $(this).hide();
    });

    $("#category").change(function () {
        var selected_category = $(this).val();

        $("#service").val('');
        $("#order_link").val('');
        $("#quantity").val('');
        $('#comments').val('');
        $('#username').val('');
        $('#answer_number').val('');
        selected_category = selected_category.replace('  ', ' ');
        $('option').each(function (index) {
            if ($(this).attr('type') === 'service_selector') {
                //console.log($(this).attr('id').replace('  ', ' '), selected_category)
                if ($(this).attr('id').replace('  ', ' ') === selected_category) {
                    $(this).show();
                }
                else {
                    $(this).hide();
                }
            }
        });
    });

    $("#service").change(function () {
        var service_cost = ($("#service").find(":selected").attr("cost"));
        var quantity = $("#quantity").val();
        if (quantity == '') { quantity = 0 }
        service_cost = parseFloat(service_cost / 1000).toFixed(4);
        total = quantity * service_cost
        total = total.toFixed(4)
        $("#payment").val(`${quantity} x $${service_cost} = ${total}`);


        var selected_service = $(this).val();
        $('.service_quantity').each(function (index) {

            if ($(this).attr('id') == selected_service) {
                $(this).show();
            }
            else {
                $(this).hide();
            }
        });

        var service_type = ($("#service").find(":selected").attr("service_type"));
        var service_id = ($("#service").find(":selected").attr("service_id"));
        window.localStorage.setItem('service_id', service_id)
        console.log(service_id)
        //enable_types="Default Custom_Comments Mentions_User_Followers Comment_Likes Poll">

        $("input").each(function () {
            if ($(this).attr('enable_types') != undefined) {
                console.log("searching:", service_type.replace(' ', '_').toLowerCase())
                console.log(($(this).attr('enable_types')).toLowerCase())
                $(this).prop('disabled', true);
                $(this).val(' - Not Required - ');
                if (($(this).attr('enable_types')).toLowerCase().search(service_type.replace(' ', '_').toLowerCase()) != -1) {
                    $(this).prop('disabled', false);
                    $(this).val('');
                }
            }
        });
        $("textarea").each(function () {
            if ($(this).attr('enable_types') != undefined) {
                $(this).prop('disabled', true);
                $(this).val(' - Not Required - ');
                if (($(this).attr('enable_types')).search(service_type.replace(' ', '_')) != -1) {
                    $(this).prop('disabled', false);
                    $(this).val('');
                }
            }
        });
        $("#input_fields").children('input').each(function () {
            $(this).prop('disabled', true);
        });

    });


    $("#next_service").click(function () {
        if (window.last == window.max) return;
        $(`#service-card-${window.first}`).attr('class', `${$(`#service-card-${window.first}`).attr('class')} d-none`);
        window.first += 1;
        window.last += 1;
        $(`#service-card-${window.last}`).attr('class', $(`#service-card-${window.last}`).attr('class').replace('d-none', ''));
        console.log(window.first)
        console.log(window.last)

    });

    $("#previous_service").click(function () {
        if (window.first == window.min) return;
        $(`#service-card-${window.last}`).attr('class', `${$(`#service-card-${window.last}`).attr('class')} d-none`);
        window.first -= 1;
        window.last -= 1;
        $(`#service-card-${window.first}`).attr('class', $(`#service-card-${window.first}`).attr('class').replace('d-none', ''));
        console.log(window.first)
        console.log(window.last)
    });


    $("#quantity").keyup(function () {

        var service_cost = ($("#service").find(":selected").attr("cost"));
        var quantity = $("#quantity").val();
        if (quantity == '') { quantity = 0 }
        service_cost = parseFloat(service_cost / 1000).toFixed(4);
        total = quantity * service_cost
        total = total.toFixed(4)
        $("#payment").val(`${quantity} x $${service_cost} = ${total}`);
    });

});

function submitTask() {

    service_id = window.localStorage.getItem('service_id');
    order_link = $("#order_link").val();
    quantity = $("#quantity").val();
    comments = $('#comments').val();
    username = $('#username').val();
    answer_number = $('#answer_number').val();

    const data = JSON.stringify({
        "service_id": service_id,
        "link": order_link,
        "quantity": quantity,
        "comments": comments,
        "username": username,
        "answer_number": answer_number
    });
    console.log(data)

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            $("#submit_task").html('Submit Order');
            if (this.responseText.includes('successfully')) {
                toast_green("Successfully created a new order!", this.responseText);
            }
            else {
                toast_red("An error occured :(", this.responseText);
            }
            $("#order_modal").modal('hide')

        }
    });

    xhr.open("POST", "https://boostgram.net/submitTask");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(data);
}