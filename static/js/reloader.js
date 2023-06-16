// window.onload = function () {
//     var images = document.images;
//     for (var i = 0; i < images.length; i++) {
//         images[i].src = images[i].src.replace(/\btime=[^&]*/, 'time=' + new Date().getTime());
//     }
// }

function imageRetry(e) {
    console.log("imageRetry")
    reloadImg(e);
    setTimeout(reloadImg, 1000, e);
}
function reloadImg(e) {

    var source = (e.src).split('/static')[1];
    e.src = '/static' + source;
}

function show() { $("#contact_modal").modal("show") };
function show_bot() { $("#bot_modal").modal("show") };
function show_faq() { $("#faq_modal").modal("show"); hide_all() };
function show_ans(btn, a_id) {
    $(`#a_${a_id}`).toggle();
}
function hide_all(num = 32) {
    $('#faq_content').children('span').each(function () { $(this).hide(); })
}