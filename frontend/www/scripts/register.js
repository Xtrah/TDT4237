async function createNewUser(event) {
    let form = document.querySelector("#form-register-user");
    let formData = new FormData(form);

    let response = await sendRequest("POST", `${HOST}/api/v1/users/`, formData, "");
    
    if (!response.ok) {
      let data = await response.json();
      let alert = createAlert("Registration failed!", data);
      document.body.prepend(alert);
    
    } else {
      // Hide login redirect
      /*let body = {username: formData.get("username"), password: formData.get("password")};
      response = await sendRequest("POST", `${HOST}/api/v1/token/login/`, body);
      if (response.ok) {
          let data = await response.json();
          setCookie("access", data.access, 86400, "/");
          setCookie("refresh", data.refresh, 86400, "/");
          sessionStorage.setItem("username", formData.get("username"));
      } else {
        console.log("CAN'T GET JWT TOKEN ON REGISTRATION");
        let data = await response.json();
        let alert = createAlert("Registration could not complete. Try again!", data);
        document.body.prepend(alert);
      }
      form.reset();
      window.location.replace("workouts.html");*/
      let data = await response.json();
      let email = formData.get("email");
      let alert = createAlert("Registration completed! Verify your account by going to your email!", email.toString);
      form.reset();
      document.body.prepend(alert);
    }  
  }

document.querySelector("#btn-create-account").addEventListener("click", async (event) => await createNewUser(event));