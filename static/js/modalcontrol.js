$(document).ready(function () {
    $("#submit_task").click(function () {

        // inser spinner
        $("#submit_task").html(`<div class="spinner-border spinner-border-sm" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>`);


        service_id = $('#service_id_holder').text();
        link = $("#order_link").val()
        quantity = $("#quantity").val()
        username = $("#username").val()
        comments = $("#comments").val()
        drip_feed = $("#val_drip_feed").val()

        console.log(link)
        console.log(quantity)
        console.log(username)
        console.log(comments)
        console.log(drip_feed)


        var data = JSON.stringify({
            "window": window.localStorage.getItem('service_type')
        });

        console.log(data);
        
        switch (window.localStorage.getItem('service_type').toLowerCase()) {
            case "default":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "drip_feed": drip_feed
                });

                break;
            case "custom comments":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "comments": comments
                });

                break;
            case "mentions user followers":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "username": username
                });

                break;
            case "comment likes":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "username": username
                });

                break;
            case "poll":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                });
                break;
        }


        const xhr = new XMLHttpRequest();
        xhr.withCredentials = true;

        xhr.addEventListener("readystatechange", function () {
            if (this.readyState === this.DONE) {
                console.log(this.responseText);
                $("#submit_task").html('Submit Order');
                if (this.responseText.includes('successfully')) {
                    toast_green("Successfully created a new order!", this.responseText)
                }
                else {
                    toast_red("An error occured :(", this.responseText)
                }
                $("#order_modal").modal('hide')

            }
        });
        xhr.open("POST", "https://boostgram.net/submitTask");
        xhr.setRequestHeader('Content-Type', 'application/json')
        console.log("sending request");
        xhr.send(data);
    })

    $("#status_toast_close").click(function () { $(".toast").hide(); })


})

function open_modal(service_id, service_name, type, rate, min, max, dripfeed = true, refill = false, category = "") {
    console.log(service_id)
    console.log(type);
    $("#selected_value_hidden").text(rate);
    $("#payment").text('');
    window.localStorage.setItem('service_type', type);
    $('#service_id_holder').text(service_id);
    $("#order_link").val("");
    $("#quantity").val("");
    $("#username").val("");
    $("#comments").val("");
    $("#val_drip_feed").val("");

    switch (type) {
        case "default":
            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").hide();
            $("#inp_comments").hide();
            $("#inp_drip_feed").show();
            $("#inp_answer_number").hide();
            break;
        case "Custom Comments":
            $("#inp_link").show()
            $("#inp_quantity").hide();
            $("#inp_username").hide();
            $("#inp_comments").show();
            $("#inp_drip_feed").hide();
            $("#inp_answer_number").hide();

            break;
        case "Mentions User Followers":

            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").show();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();
            $("#inp_answer_number").hide();

            break;
        case "Comment Likes":

            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").show();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();
            $("#inp_answer_number").hide();
            break;
        case "Poll":

            $("#inp_link").show();
            $("#inp_quantity").show();
            $("#inp_username").hide();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();
            break;
        case "Mentions with Hashtags": 
            alert("Not yet implemented, check out soon!" + type)
            break;
        
        case "Mentions Hashtag":
            alert("Not yet implemented, check out soon!" + type)
            break;

        case "Mentions Custom List":
            alert("Not yet implemented, check out soon!" + type)
            break;
        case "Mentions Hashtag":
            alert("Not yet implemented, check out soon!" + type)
            break;
        case "Custom Comments Package":
            alert("Not yet implemented, check out soon!" + type)
            break;
        case "Comment Replies":
            alert("Not yet implemented, check out soon!" + type)
            break;
        case "Invites from Groups":
            alert("Not yet implemented, check out soon!" + type)
            break;
        case "Subscriptions":
            alert("Not yet implemented, check out soon!" + type)
            break;

    }

    $("#minmax").text(`Min ${min} - Max ${max}`)
    $("#order_modal_title").text(`Please fill in order details for ${service_name}`);

    $("#order_modal").modal("toggle");
}
