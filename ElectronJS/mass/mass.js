//Importing required modules
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const path = require('path')
const spawn = require("child_process").spawn;

//Showing opened file label
let openFilePlace = document.querySelector('#mass-open-alert')

$(document).ready(function() {
    $("#mass-open-btn").click(openFile);
    $("#massplot-btn").click(masspec);
});

let filePaths;
let openLabel;
let itemText;

function openFile(e) {

    const options = {
        title: "Open .mass file(s)",
        defaultPath: "D:",
        filters: [
            { name: 'Mass files', extensions: ['mass'] },
            { name: 'All Files', extensions: ['*'] }
        ],
        properties: ['openFile', 'multiSelections'],
    };
    filePaths = dialog.showOpenDialog(mainWindow, options);

    if (filePaths !== undefined) {
        if (openFilePlace.children.length > 0) {
            openLabel = document.querySelector('.mass-openFileLabel');
            openLabel.className = "alert alert-primary mass-openFileLabel";
            openLabel.innerHTML = filePaths
        } else {
            openLabel = document.createElement('label');
            openLabel.className = "alert alert-primary mass-openFileLabel";
            itemText = document.createTextNode(filePaths);
            openLabel.appendChild(itemText);
            openFilePlace.appendChild(openLabel);
        }
    } else {
        if (openFilePlace.children.length > 0) {
            openLabel = document.querySelector('.mass-openFileLabel');
            openLabel.remove()
        }

        openLabel = document.createElement('label');
        openLabel.className = "alert alert-danger mass-openFileLabel";
        itemText = document.createTextNode("No file selected");
        openLabel.appendChild(itemText);
        openFilePlace.appendChild(openLabel);

        setTimeout(() => openLabel.remove(), 3000)

    }
}
//python backend

function masspec(e) {
    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    const py = spawn('python', [path.join(__dirname, "./mass.py"), filePaths]);

    py.stdout.on('data', (data) => console.log(data.toString()));
    py.on('close', () => { console.log('Done') });
}