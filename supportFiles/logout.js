const statusLabel = document.getElementById("statusLabel")

setTimeout(() => {
    statusLabel.innerHTML = "Removing authentication certificate and token..."
}, 2000)

setTimeout(() => {
    statusLabel.innerHTML = "Cleaning up session metadata..."
}, 3000)

setTimeout(() => {
    statusLabel.innerHTML = "Finishing up log out..."
}, 4000)

setTimeout(() => {
    statusLabel.innerHTML = "You have been successfully logged out! You will be redirected to the homepage in 2 seconds..."
}, 6000)

setTimeout(() => {
    location = location.origin
}, 8000)