$(document).ready(function () {
    $("#submit_task").click(function () {

        link = $("#val_link").val()
        quantity = $("#val_quantity").val()
        username = $("#val_username").val()
        comments = $("#val_comments").val()
        drip_feed = $("#val_drip_feed").val()

        console.log(link)
        console.log(quantity)
        console.log(username)
        console.log(comments)
        console.log(drip_feed)

        service_id = window.localStorage.getItem('service_id')
        var data = ""
        switch (window.localStorage.getItem('service_type')) {
            case "Default":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "drip_feed": drip_feed
                });

                break;
            case "Custom Comments":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "comments": comments
                });

                break;
            case "Mentions User Followers":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "username": username
                });

                break;
            case "Comment Likes":
                data = JSON.stringify({
                    "service_id": service_id,
                    "link": link,
                    "quantity": quantity,
                    "username": username
                });

                break;
            case "Poll":
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
            }
        });
        xhr.open("POST", "https://localhost/submitTask");
        xhr.setRequestHeader('Content-Type', 'application/json')

        xhr.send(data);
    })
})



function open_modal(service_id) {
    console.log(service_id)

    type = $(`#service_type_${service_id}`).text()

    console.log(type);

    window.localStorage.setItem('service_type', type)
    window.localStorage.setItem('service_id', service_id)

    $("#inp_link").val('')
    $("#inp_quantity").val('');
    $("#inp_username").val('');
    $("#inp_comments").val('');
    $("#inp_drip_feed").val('');

    switch (type) {
        case "Default":
            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").hide();
            $("#inp_comments").hide();
            $("#inp_drip_feed").show();
            break;
        case "Custom Comments":
            $("#inp_link").show()
            $("#inp_quantity").hide();
            $("#inp_username").hide();
            $("#inp_comments").show();
            $("#inp_drip_feed").hide();

            break;
        case "Mentions User Followers":

            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").show();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();

            break;
        case "Comment Likes":

            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").show();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();
            break;
        case "Poll":

            $("#inp_link").show()
            $("#inp_quantity").show();
            $("#inp_username").hide();
            $("#inp_comments").hide();
            $("#inp_drip_feed").hide();
            break;
    }

    $("#exampleModal").modal("toggle");


}