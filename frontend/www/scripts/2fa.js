
async function is2faEnabled() {
  let user = await getCurrentUser();
  document.getElementById("inputUsername").value = user.username;

  if (user.is_two_factor_enabled) {
    document.getElementById("enabled2fa").classList.remove("hide");
  } else {
    document.getElementById("activate2fa").classList.remove("hide");

    let host = `${HOST}`
    response = await sendRequest("GET", host + "/api/totp/create/");
    if (!response.ok) {
      let alert = createAlert("Something is off. Try again.", {});
      document.body.prepend(alert);
    } else {
      let res = await response.json();
      new QRCode(document.getElementById("qrcode"), {
        text: res,
        // TODO: Styling
      });
    }

  }
}

window.addEventListener('load', () => {
  is2faEnabled();
});

async function enable2FA(event) {
  let user = await getCurrentUser();
  let form = document.getElementById("2fa-form");
  let formData = new FormData(form);
  let inputCode = formData.get("inputCode")
  let body = {
    "username": user.username,
    "password": formData.get("password")
  };
  let response = await sendRequest("POST", `${HOST}/api/totp/login/${inputCode}/`, body);

  if (!response.ok) {
    let alert = createAlert("Something is off. Try again.", {});
    document.body.prepend(alert);
  } else {
    let alert = createAlert("Success! You are now authenticated for 2FA-only pages!", {});
    document.body.prepend(alert);
  }
  form.reset();
  document.getElementById("inputUsername").value = user.username;
}

document.getElementById("btn-activate-2fa").addEventListener("click", async () => await enable2FA());