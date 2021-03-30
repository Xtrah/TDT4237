// send(host + "/api/totp/create/", {
//     method: "POST",
//     body: JSON.stringify(data)
// }).then(res => {
//     console.log("Request complete! response:", res);
//     new QRCode(document.getElementById("qrcode"), "res");
// });

async function is2faEnabled() {
    let user = await getCurrentUser();
    let enabled = false;

    if (user.is_two_factor_enabled) {
        document.querySelector("#enabled2fa").classList.remove("hide");
        console.log("User is 2FA enabled :D")

    } else {
        document.querySelector("#activate2fa").classList.remove("hide");
        console.log("User is not 2FA enabled :(")

        let data = getCookieValue("access");
        let host = `${HOST}`
        response = await sendRequest("GET", host + "/api/totp/create/");
        let res = await response.json();
        console.log(res)
        // TODO: Create QR code from res
        // Create POST request from input field and button
        // If POST returns true, set user.is_two_factor_enabled = true
    }
}

is2faEnabled();