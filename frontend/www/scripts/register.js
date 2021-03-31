async function createNewUser(event) {
    let form = document.querySelector("#form-register-user");
    let formData = new FormData(form);

    let response = await sendRequest("POST", `${HOST}/api/v1/users/`, formData, "");
    
    if (!response.ok) {
      let data = await response.json();
      let alert = createAlert("Registration failed!", data);
      document.body.prepend(alert);
    
    } else {
      let data = await response.json();
      let email = formData.get("email");
      let alert = createAlert("Registration completed! Verify your account by going to your email!", email.toString);
      form.reset();
      document.body.prepend(alert);
    }  
  }

document.querySelector("#btn-create-account").addEventListener("click", async (event) => await createNewUser(event));