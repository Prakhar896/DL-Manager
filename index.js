const originURL = location.origin

function checkPassword() {
    const enteredPassword = document.getElementById("passwordField").value;
    if (!enteredPassword) {
        alert("Please enter a password!")
        return
    }
    axios({
        method: 'post',
        url: `${originURL}/passwordCheck`,
        data: {
            'data': {
                'password': enteredPassword
            }
        },
        headers: {
            'Content-Type': 'application/json',
            'DLAccessCode': 'AWSDL@Prakh!6070'
        }
    })
    .then(response => {
        if (response.status == 200) {
            if (response.data.startsWith("SUCCESS")) {
                document.getElementById('updateLabel').style.visibility = "visible"
                console.log("Authorisation successful!")

                setTimeout(() => {
                    document.location = `${originURL}/session/${response.data.substring("SUCCESS: Auth token is ".length)}/home`
                }, 2000)
            } else {
                alert("Incorrect password!")
                console.log(response.data)
                document.getElementById('updateLabel').style.visibility = "hidden"
            }
        } else if (response.status == 401) {
            alert("Authorisation failed! Incorrect password!")
            console.log(response.data)
            document.getElementById('updateLabel').style.visibility = "hidden"
        } else {
            alert("Error in connecting to server and verifing password. Check logs for more information.")
            console.log("Error in connecting to server. Non-200 status code response received.")
            console.log("Response data: " + response.data)
            document.getElementById('updateLabel').style.visibility = "hidden"
        }
    })
    .catch(error => {
        if (error == "Error: Request failed with status code 401") {
            console.log("Unauthorised Response Error Occurred when checking password: " + error)
            alert("Incorrect Password. Access Denied. You are barred from access into the server due to failed authentication. Please try again.")
            return
        }
        alert("Error in connecting to server. Check logs for more information.")
        console.log("Error in connecting to server: " + error)
        document.getElementById('updateLabel').style.visibility = "hidden"
    })
}