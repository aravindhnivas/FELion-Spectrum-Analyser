//Importing required modules
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const { PythonShell } = require('python-shell');

//Showing opened file label
let openFilePlace = document.querySelector('#mass-open-alert')
let openFileBtn = document.querySelector('#mass-open-btn')
openFileBtn.addEventListener('click', openFile)

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

    }
}

//python backend
let massplotBtn = document.querySelector('#massplot-btn')
massplotBtn.addEventListener('click', masspec)

//Running the python script with options and arguments
function masspec(e) {

    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    let options = {
        mode: 'text',
        pythonPath: 'C:\\ProgramData\\Anaconda3\\',
        //pythonOptions: ['-u'], // get print results in real-time
        scriptPath: './',
        args: filePaths
    };

    PythonShell.run('mass.py', null, function(err, results) {
        if (err) throw err;
        // results is an array consisting of messages collected during execution
        console.log('results: %j', results);
    });

}