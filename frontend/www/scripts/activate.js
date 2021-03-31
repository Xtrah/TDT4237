async function activateUser(event) {
    let activationText = document.querySelector("#activation-text");
    let activationIcon = document.querySelector("#activation-icon");
    let spinner = document.querySelector("#activation-spinner");
    // Get token and uid from url
    const params = (new URL(document.location)).searchParams;
    let uidValue = params.get("uid")
    let tokenValue = params.get("token")
    let body = {"uid": uidValue, "token": tokenValue};
    let response = await sendRequest("POST", `${HOST}/api/v1/users/activation/`, body);

    if (!response.ok) {
      spinner.classList.add("hide")
      activationText.innerHTML ="Activation failed, try again."
      activationIcon.classList.add("fa-exclamation-triangle")
      let data = await response.json();
      let alert = createAlert("Activation failed, try again!", data);
      document.body.prepend(alert);
    } else {
      spinner.classList.add("hide")
      activationText.innerHTML = "Activated!"
      let alert = createAlert("Activation finished. Now you can log in!",{});
      document.body.prepend(alert);
    }  
}

window.addEventListener('load', (event) => {
  activateUser()
});