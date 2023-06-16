$(document).ready(function () {
    window.localStorage.setItem("status_sort", '0')
    $("#status_toast_close").click(function () { $(".toast").hide(); });

    $(".tab-control").each(function () {
        $(this).click(function () {
            target = $(this).attr('data-toggle');
            $("#users_tab").hide();
            $("#dashboard_tab").hide();
            $("#services_tab").hide();

            $(".nav-tab").each(function () { $(this).attr("class", "nav-tab nav-link") });

            $(`#${target}`).show();
            $(this).children('a').attr("class", "nav-tab nav-link active");

        });
    })

    $("#status_filter").click(displayStatusChange);
});

function mass_update(){
    let option = "spiderpanel";
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            if (this.responseText.includes("Completed")) {
                toast_green("Success", this.responseText);
            }
            else if (this.responseText.includes("Pending")) {
                toast_yellow("Failure", this.responseText);
            }
        }
    });

    xhr.open("POST", `https://boostgram.net/mass_update/${option}}`);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
    console.log("Sent out mass update request.. Awaiting response....");
}
function displayStatusChange(){
    function _displayStatusChangeDriver(s){
        let sk = window.localStorage.getItem('status_sort');
        window.localStorage.setItem('status_sort', s);
        $('tr').each(function(){
            console.log($(this).find('.enabled_status').text());
            if($(this).attr('class') == 'subtable-label')
                return
            if(sk == '1'){
                if($(this).find('.enabled_status').text()==='✔️')
                    $(this).show();
                else
                    $(this).hide();
            }
            else {
                if($(this).find('.enabled_status').text()==='✔️')
                    $(this).hide();
                else
                    $(this).show();
            }

        })
    }
    if(window.localStorage.getItem('status_sort') == '0'){
        _displayStatusChangeDriver('1');
    }
    else{
        _displayStatusChangeDriver('0');
    }
}


function getStatus(task_id) {
    /// check_status/<int:order_id>
    $(`#spinner_${task_id}`).attr('class', $(`#spinner_${task_id}`).attr('class').replace('d-none', ''))
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            $(`#spinner_${task_id}`).attr('class', $(`#spinner_${task_id}`).attr('class') + 'd-none')
            if (this.responseText.includes("Completed")) {
                toast_green('Task (id: ${task_id}) status', this.responseText);
            }
            else if (this.responseText.includes("Pending")) {
                toast_yellow('Task (id: ${task_id}) status', this.responseText);
            }
        }
    });

    xhr.open("GET", `https://boostgram.net/check_status/${task_id}`);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
}

function updateService(task_id) {
    ///updateService/<int:service_id>/<string:new_name>/<float:new_rate>

    new_rate = $(`#new_rate_${task_id}`).val();
    new_name = $(`#new_name_${task_id}`).val();

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            $(`#new_rate_${task_id}`).attr("style", $(`#new_rate_${task_id}`).attr("style") + " background-color:#90ee90")
            $(`#new_name_${task_id}`).attr("style", $(`#new_name_${task_id}`).attr("style") + " background-color:#90ee90")
        }
    });

    xhr.open("PUT", `https://boostgram.net/updateService/${task_id}/${new_name}/${new_rate}`);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
}

function change_service_status(task_id) {
    ///updateServiceRate/<int:service_id>/<float:new_rate>

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    let status = false

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            if (status) {
                $(`#e_${task_id}`).text('✔️');
            }
            else {
                $(`#e_${task_id}`).text('❌')
            }
        }
    });

    if ($(`#e_${task_id}`).text().includes('❌')) {
        status = true
        xhr.open("POST", `https://boostgram.net/updateServiceStatus/${task_id}/True`);
    }
    else {
        status = false
        xhr.open("POST", `https://boostgram.net/updateServiceStatus/${task_id}/False`);
    }

    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
}

function adminAddFunds(id, factor) {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    var num = prompt("Topup amount (in USD):");
    amount = parseFloat(num)
    if (amount == NaN) { return; }
    xhr.addEventListener("readystatechange", function () {
        console.log(this.responseText)
        if (this.readyState === this.DONE) {
            toast_green('Status', this.responseText)
        }
        else {
            toast_red('Status', this.responseText)
        }
    });
    console.log(factor * amount)
    xhr.open("POST", `https://boostgram.net/adminAddFunds/${id}/${factor * amount}`);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send();
}