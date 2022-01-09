function runCommand() {
    const commandField = document.getElementById("commandField")
    if (!commandField.value || commandField.value == "") {
        alert("Command textfield is empty! Please enter a command to run!")
        return
    }
    axios({
        method: 'post',
        url: `${location.origin}/api/zshCommand`,
        headers: {
            "DLAccessCode": "AWSDL@Prakh!6070",
            "Content-Type": "application/json"
        },
        data: {
            "command": commandField.value
        }
    })
    .then(response => {
        if (response.status == 200) {
            commandField.value = ""
            if (response.data.startsWith("WARNING")) {
                alert(response.data)
                const outputBoxContentContainer = document.getElementById("outputBoxContentContainer")
                outputBoxContentContainer.innerHTML = ""
                outputBoxContentContainer.innerHTML = "<p style=\"white-space: pre-line\">" + response.data.slice("WARNING: ".length) + "</p>"
                refreshCwd()
            } else {
                const outputBoxContentContainer = document.getElementById("outputBoxContentContainer")
                outputBoxContentContainer.innerHTML = ""
                outputBoxContentContainer.innerHTML = "<p style=\"white-space: pre-line\">" + response.data + "</p>"
                refreshCwd()
            }
        } else {
            alert("Failed to run command using DLM In-Browser ZSH. Could not connect to DLM API. Check console for more information.")
            console.log("Received non-200 response code from zshCommand API.")
            console.log("Response data: " + response.data)
        }
    })
    .catch(err => {
        console.log("Error in connecting to DLM zshCommand API: " + err)
        alert("An error occurred in running the command using the DLM In-Browser ZSH. Check console for information.")
    })
}

function refreshCwd() {
    const cwdLabel = document.getElementById("cwdLabel")
    axios({
        method: 'post',
        url: `${location.origin}/api/cwd`,
        headers: {
            "DLAccessCode": "AWSDL@Prakh!6070",
        },
        data: {}
    })
    .then(response => {
        if (response.status == 200) {
            cwdLabel.innerHTML = "ZSH Current Working Directory: " + response.data
        } else {
            alert("Failed to refresh current working directory status. Please check console for more information.")
            console.log("Received non-200 response code from cwd API.")
        }
    })
    .catch(err => {
        console.log("Error in connecting to DLM cwd API: " + err)
        alert("An error occurred in refreshing current working directory status. Please check console for more information.")
    })
}