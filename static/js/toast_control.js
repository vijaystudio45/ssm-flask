$(document).ready(function () {
    $("#status_toast_close").click(function () { $(".toast").hide(); })

});


function toast_green(title, message) {

    $("#toast_title").text(title);
    $("#toast_text").text(message);
    $(".toast").attr('style', '--bs-toast-bg: #2bc435;');
    $(".toast").show();
}

function toast_yellow(title, message) {
    $("#toast_title").text(title);
    $("#toast_text").text(message);
    $(".toast").attr('style', '--bs-toast-bg: #c9c922;');
    $(".toast").show();
}

function toast_red(title, message) {
    $("#toast_title").text(title);
    $("#toast_text").text(message);
    $(".toast").attr('style', '--bs-toast-bg: #cc5662;');
    $(".toast").show();
}