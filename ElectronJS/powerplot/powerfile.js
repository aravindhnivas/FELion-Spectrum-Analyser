// getting current window and dialog module from electron.remote
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const fs = require('fs');
const path = require('path');

//setting default powerfile name with current date
let filename = document.querySelector('#pow-filename')

// Getting today's data to set the filename
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

let folder;
let dirLabel;

function openDir(e) {

    const options = {
        title: "Open Directory",
        properties: ['openDirectory'],
    };

    folder = dialog.showOpenDialog(mainWindow, options);

    if (folder !== undefined) {
        if (dirLabelPlace.children.length > 0) {
            dirLabel = document.querySelector('.pow-dirLabel')
            dirLabel.innerHTML = folder[0]
        } else {
            dirLabel = document.createElement('label');
            dirLabel.className = "alert alert-primary pow-dirLabel";
            let itemText = document.createTextNode(folder);
            dirLabel.appendChild(itemText);
            dirLabelPlace.appendChild(dirLabel);
        }
    } else {

        if (dirLabelPlace.children.length > 0) {
            dirLabel.remove()

        }
    }
}

// Showing save-alert next to save button
powSaveAlertPlace = document.querySelector('.pow-save-alert')
powSaveBtn = document.querySelector('.pow-save-btn')
powSaveBtn.addEventListener('click', saveAlert)

function saveAlert(e) {

    //creating alert label
    const alert = document.createElement('label')
    let itemText;

    //Getting the filecontents
    contents = document.querySelector('#pow-filecontents').value
    console.log(`Filecontents ${contents}; ${typeof contents}`)

    if (folder === undefined) {

        alert.className = 'alert alert-danger save-alert'
        itemText = document.createTextNode('ERROR: Please open a directory to save!')
        dirLabel.remove()

    } else {

        alert.className = 'alert alert-success save-alert'
        itemText = document.createTextNode(`File saved! ${filename.value}.pow`)

        let fullname = path.join(folder[0], filename.value + '.pow')
        console.log(`Filename: ${fullname}`)

        fs.writeFile(fullname, contents, (err) => {
            if (err) {
                alert.className = 'alert alert-danger save-alert'
                let itemText = document.createTextNode(`Error: ${err}`)
            }
        })
    }
    // Placing the alert label
    alert.appendChild(itemText)
    powSaveAlertPlace.appendChild(alert)

    // disappear after 3seconds
    setTimeout(() => alert.remove(), 3000);
}