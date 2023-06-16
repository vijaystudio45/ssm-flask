$(document).ready(function () { $("#status_toast_close").click(function () { $(".toast").hide(); }) })

function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
    if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

var CREATE_PAYMENT_URL = "https://boostgram.net/payment/paypal/create/";
var EXECUTE_PAYMENT_URL = "https://boostgram.net/payment/paypal/execute";
paypal.Button.render({
    env: 'sandbox', // Or 'production'
    // Set up the payment:
    // 1. Add a payment callback
    payment: function (data, actions) {

        amount = $(`#Amount`).val();
        // 2. Make a request to your server
        return actions.request.post(`${CREATE_PAYMENT_URL}${amount}`)
            .then(function (res) {
                // 3. Return res.paymentIDswea/+ yujkupo000000+from the response
                return res.paymentID;
            });
    },
    // Execute the payment:
    // 1. Add an onAuthorize callback
    onAuthorize: function (data, actions) {
        console.log(getCookie('_user_id'))
        // 2. Make a request to your server
        return actions.request.post(EXECUTE_PAYMENT_URL, {
            paymentID: data.paymentID,
            payerID: data.payerID,
            _user_id: getCookie('_user_id')
        })
            .then(function (res) {
                console.log(res.success)
                // 3. Show the buyer a confirmation message.
                if (res.success == true) {
                    toast_green("Success!", "You've successfully added funds to your account!")

                }
            });
    }
}, '#paypal-button');