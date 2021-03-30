// let data = document.getCookieValue("Authorization");

// fetch("https://localhost:61603/api/totp/create/", {
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
        response = await sendRequest("GET", user.is_two_factor_enabled);
        if (!response.ok) {
            let data = await response.json();
            let alert = createAlert("Could not retrieve 2FA!", data);
            document.body.prepend(alert);
        }
        let coach = await response.json();
        let input = document.querySelector("#input-coach");

        input.value = coach.username;
    } else {
        console.log("User is not 2fa enabled")
        // Print qr code
        
    }
}

is2faEnabled();
