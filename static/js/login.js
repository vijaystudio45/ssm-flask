console.log("login js loaded successfully")
function submitLogin() {
    username = document.getElementById('login-email').value
    password = document.getElementById('login-password').value
    const data = JSON.stringify({
        "username": username,
        "password": password
    });

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    port = document.getElementById('port').innerText
    console.log(port)
    xhr.addEventListener("readystatechange", function () {
        if (this.readyState === this.DONE) {
            console.log(this.responseText);

            if (this.status === 200) {
                location.replace(`https://boostgram.net/home`);
            }
            else if (this.status === 401) {
                toast_red("Oops!", JSON.parse(this.response)["message"]);
            }
        }

    });

    xhr.open("POST", `https://boostgram.net/login`);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("Access-Control-Allow-Credentials", "true")

    xhr.send(data);
}

function benefits() {

    $('html,body').animate({
        scrollTop: $("#benefits-anchor").offset().top
    },
        'slow');
}