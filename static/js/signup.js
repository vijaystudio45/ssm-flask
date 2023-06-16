
function submitRegister() {
    $("#status_toast_close").click(function () { $(".toast").hide(); });
    
    email = document.getElementById("email").value
    username = document.getElementById("username").value
    password = document.getElementById("password").value
    repeat_password = document.getElementById("password2").value
    console.log(email);
    console.log(username);
    console.log(password);
    console.log(repeat_password);

    if (!($('#terms-and-conditions').is(':checked'))) {
        toast_red("OOPS!", "Terms of service aren't accepted.")
        return
    }
    if (email === "" || username === "" || password === "") {
        toast_red("OOPS!", "Please fill in all the fields")
        return
    }
    if (password !== repeat_password) {
        toast_red("OOPS!", "Passwords do not match!")
        return
    }
    const data = JSON.stringify({
        "email": email,
        "username": username,
        "password": password
    });

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {
        alert("Hello123");
        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            console.log(this.status);

            if (this.status === 200) {
                alert("Success");
                // location.replace(`https://boostgram.net/home`);
                location.replace(`http://127.0.0.1:5000/home`);
            }
            else if (this.status === 401) {
                toast_red("OOPS!", this.responseText)
            }
        }

    });

    // xhr.open("POST", "https://boostgram.net/register");
    xhr.open("POST", "http://127.0.0.1:5000/register");
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.send(data);
}