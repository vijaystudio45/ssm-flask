$(document).ready(function () {
    window.first = 1;
    window.last = 4;

    window.max = 5;
    window.min = 1;

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
        $('option').each(function (index) {
            if ($(this).attr('type') === 'service_selector') {
                if ($(this).attr('id') === selected_category) {
                    $(this).show();
                }
                else {
                    $(this).hide();
                }
            }
        });
    });

    $("#service").change(function () {
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

        $("#input_fields").children('div').each(function () {
            $(this).hide();
            // console.log($(this).attr('enable_types'))
            // console.log(($(this).attr('enable_types')).search(service_type.replace(' ', '_')))
            if (($(this).attr('enable_types')).search(service_type.replace(' ', '_')) != -1) {
                $(this).show()
            }

        });
    });


    $("#next_service").click(function () {
        console.log("next")
        if (window.last == window.max) return;
        $(`#service-card-${window.first}`).attr('class', `${$(`#service-card-${window.first}`).attr('class')} d-none`);
        window.first += 1;
        window.last += 1;
        $(`#service-card-${window.last}`).attr('class', $(`#service-card-${window.last}`).attr('class').replace('d-none', ''));
        console.log("window.first", window.first)
        console.log("window.last", window.last)

    });

    $("#previous_service").click(function () {
        console.log("previous")
        if (window.first == window.min) return;
        $(`#service-card-${window.last}`).attr('class', `${$(`#service-card-${window.last}`).attr('class')} d-none`);
        window.first -= 1;
        window.last -= 1;
        $(`#service-card-${window.first}`).attr('class', $(`#service-card-${window.first}`).attr('class').replace('d-none', ''));
        console.log("window.first", window.first)
        console.log("window.last", window.last)
    });

    if (screen.width > 767) {
        $(".service").each(function () {
            if (window.counter >= 4) {
                $(this).attr('class', `${$(this).attr('class')} d-none`);
                window.counter += 1
            }
            else {
                window.counter += 1
            }
            console.log("window.max", window.max)
            window.max = window.counter;
        });
    }
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
        }
    });

    xhr.open("POST", "https://boostgram.net/submitTask");
    xhr.setRequestHeader("Content-Type", "application/json");

    //xhr.send(data);
}