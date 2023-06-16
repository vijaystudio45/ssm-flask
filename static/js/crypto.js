function cryptoPay(currency) {
    amount = $(`#${currency}_input`).val();
    const data = JSON.stringify({
        "amount": amount,
    });

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText)
            resp = JSON.parse(this.responseText);

            window.open(resp['hosted_url'], '_blank');

            if (this.responseText.includes("Created")) {
                $(".toast").attr('style', '--bs-toast-bg: #2bc435;')
            }

            $("#toast_title").text(`Successful`)
            $("#toast_text").text('Please check and complete the payment on the newly opened tab. Keep in mind that transactions can take up to 10 minutes to process.')
            $(".toast").show();

        }
    });

    xhr.open("POST", "https://boostgram.net/payment/coinbase");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(data);

}