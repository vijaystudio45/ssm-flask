function logout() {
    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

    xhr.addEventListener("readystatechange", function () {

        if (this.readyState === this.DONE) {
            console.log(this.responseText);
            location.reload(true);
            console.log(this.responseText);
            window.location.href = window.location.href; // if first reload fails
        }
    }
    );
    xhr.open("POST", "https://boostgram.net/logout");
    xhr.setRequestHeader('Content-Type', 'application/json')

    xhr.send();
}