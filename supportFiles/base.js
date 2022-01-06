const originURL = location.origin
const authToken = document.location.pathname.split("/")[2]

document.getElementById('zshLinkNavBar').href = `${origin}/session/${authToken}/zsh`
document.getElementById('logoutLinkNavBar').href = `${origin}/session/${authToken}/sessionAdmin/logout`
document.getElementById('homeLinkNavBar').href = `${origin}/session/${authToken}/home`