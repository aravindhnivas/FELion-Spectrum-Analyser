const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();

//Showing opened file label
let openFilePlace = document.querySelector('#normline-open-alert')
let openFileBtn = document.querySelector('#normline-open-btn')
openFileBtn.addEventListener('click', openFile)

let filePaths;
let openLabel;
let itemText;

function openFile(e) {

    const options = {
        title: "Open .felix or .cfelic file(s)",
        defaultPath: "D:",
        filters: [
            { name: 'FELIX files', extensions: ['felix', 'cfelix'] },
            { name: 'All Files', extensions: ['*'] }
        ],
        properties: ['openFile', 'multiSelections'],
    };
    filePaths = dialog.showOpenDialog(mainWindow, options);

    if (filePaths !== undefined) {
        if (openFilePlace.children.length > 0) {
            openLabel = document.querySelector('.normline-openFileLabel');
            openLabel.className = "alert alert-primary normline-openFileLabel";
            openLabel.innerHTML = filePaths
        } else {
            openLabel = document.createElement('label');
            openLabel.className = "alert alert-primary normline-openFileLabel";
            itemText = document.createTextNode(filePaths);
            openLabel.appendChild(itemText);
            openFilePlace.appendChild(openLabel);
        }
    } else {
        if (openFilePlace.children.length > 0) {
            openLabel = document.querySelector('.normline-openFileLabel');
            openLabel.remove()
        }

        openLabel = document.createElement('label');
        openLabel.className = "alert alert-danger normline-openFileLabel";
        itemText = document.createTextNode("No file selected");
        openLabel.appendChild(itemText);
        openFilePlace.appendChild(openLabel);

    }
}