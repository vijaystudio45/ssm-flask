$(document).ready(function () {
    $("#status_toast_close").click(function () { $(".toast").hide(); })
});

function getStatus(task_id, order_id, order_name, order_link_short, order_issued_at, order_quantity, order_cost) {

    /// check_status/<int:order_id>
    $(`#spinner_${task_id}`).attr('class', $(`#spinner_${task_id}`).attr('class').replace('d-none', ''))
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            $(`#spinner_${task_id}`).attr('class', $(`#spinner_${task_id}`).attr('class') + 'd-none')
            if (screen.width < 950) {
                displayData(task_id, order_id, order_name, order_link_short, order_issued_at, order_quantity, order_cost, this.responseText);
            }
            else if(this.responseText.includes("Log in")){
                window.location.href = "https://boostgram.net"
            }
            else if (this.responseText.includes("Completed")) {
                toast_green(`Task (id: ${task_id}) status`, this.responseText);
            }
            else if (this.responseText.includes("In progress")) {
                toast_yellow(`Task (id: ${task_id}) status`, this.responseText);
            }
            else {
                toast_red(`Task (id: ${task_id}) status`, this.responseText);
            }
        }
    });

    xhr.open("GET", `https://boostgram.net/check_status/${task_id}`);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
}

function displayData(task_id, order_id, order_name, order_link_short, order_issued_at, order_quantity, order_cost, status_response) {
    $("#status_modal").modal('show');
    $("#holder_response").text(status_response);
    $("#holder_task_id").text(task_id);
    $("#holder_order_id").text(order_id);
    $("#holder_order_name").text(order_name);
    $("#holder_link_short").attr('href', `https://${order_link_short}`);
    $("#holder_issued_at").text(order_issued_at);
    $("#holder_quantity").text(order_quantity);
    $("#holder_cost").text(`$ ${order_cost}`);
}