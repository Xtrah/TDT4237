async function setNewPassword(event) {
    const params = (new URL(document.location)).searchParams;
    let uidValue = params.get("uid")
    let tokenValue = params.get("token")
    let form = document.querySelector("#form-set-new-password");
    let formData = new FormData(form);
    
    if(formData.get("password") != formData.get("password1")){
        let alert = createAlert("Passwords must match!", {});
        document.body.prepend(alert);
    } else {
        let body = {"uid": uidValue, "token": tokenValue, "new_password": formData.get("password")};
        let response = await sendRequest("POST", `${HOST}/api/v1/users/reset_password_confirm/`, body);
        if (!response.ok) {
            let data = await response.json();
            let alert = createAlert("Password was not reset!", data);
            document.body.prepend(alert);
        } else {
            form.reset();
            let alert = createAlert("Password reset! Try logging in with the new password.",{});
            document.body.prepend(alert);
        }  
    }
  }

document.querySelector("#btn-set-new-password").addEventListener("click", async (event) => await setNewPassword(event));   