// getting current window and dialog module from electron.remote
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();

//setting default powerfile name with current date
let filename = document.querySelector('#pow-filename')

// Getting today's data
let today = new Date();
const dd = String(today.getDate()).padStart(2, '0');
const mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
const yy = today.getFullYear().toString().substr(2);
today = `${dd}_${mm}_${yy}-#`

filename.value = today

//Showing opened directory label
let dirLabelPlace = document.querySelector('.pow-dirLabel-place')
let openDirBtn = document.querySelector('.pow-opendir')
openDirBtn.addEventListener('click', openDir)

function openDir(e) {

    const options = {
        title: "Open Directory",
        properties: ['openDirectory'],
    };

    const folder = dialog.showOpenDialog(mainWindow, options);

    if (dirLabelPlace.children.length > 0) {
        dirLabel = document.querySelector('.pow-dirLabel')
        dirLabel.innerHTML = folder[0]
    } else {
        const dirLabel = document.createElement('label');
        dirLabel.className = "alert alert-primary pow-dirLabel";
        const itemText = document.createTextNode(folder);
        dirLabel.appendChild(itemText);
        dirLabelPlace.appendChild(dirLabel);
    }
}

// Showing save-alert next to save button
powSaveAlertPlace = document.querySelector('.pow-save-alert')
powSaveBtn = document.querySelector('.pow-save-btn')
powSaveBtn.addEventListener('click', saveAlert)

function saveAlert(e) {

    const alert = document.createElement('label')
    alert.className = 'alert alert-success save-alert'

    const itemText = document.createTextNode(`File saved! ${filename.value}.pow`)

    alert.appendChild(itemText)
    powSaveAlertPlace.appendChild(alert)

    // disappear after 3seconds
    setTimeout(() => alert.remove(), 3000);
}