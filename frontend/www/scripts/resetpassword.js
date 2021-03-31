async function resetPassword(event) {
    let form = document.querySelector("#form-reset-password");
    let formData = new FormData(form);
    let response = await sendRequest("POST", `${HOST}/api/v1/users/reset_password/`, formData, "");
    
    if (!response.ok) {
      let data = await response.json();
      let alert = createAlert("Something is off. Try again.", data);
      document.body.prepend(alert);
    } else {
      form.reset();
      let alert = createAlert("If an active account is registered with this email, an email has been sent with a link to reset your password.",{});
      document.body.prepend(alert);
    }  
  }

document.querySelector("#btn-reset-password").addEventListener("click", async (event) => await resetPassword(event));