//Importing required modules

const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const path = require('path')
const spawn = require("child_process").spawn;


/////////////////////////////////////////////////////////

//Showing opened file label
let openFilePlace = document.querySelector('#mass-open-alert')

$(document).ready(function() {
    $("#mass-open-btn").click(openFile);
    $("#massplot-btn").click(masspec);
});

let filePaths;
let openLabel;
let itemText;

/////////////////////////////////////////////////////////

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
/////////////////////////////////////////////////////////

let dataFromPython;
//python backend

function masspec(e) {

    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    const py = spawn('python', [path.join(__dirname, "./mass.py"), filePaths]);

    py.stdout.on('data', (data) => {

        dataFromPython = data.toString('utf8')
        dataFromPython = JSON.parse(dataFromPython)
        console.log(dataFromPython)

        /*

        let trace1 = {
            x: dataFromPython["mass"][0],
            y: dataFromPython["counts"][0],
            mode: 'lines',
            name: dataFromPython["filename"]
        };

        let layout = {
            title: 'Mass spectrum',
            xaxis: {
                title: 'Mass [u]'
            },
            yaxis: {
                title: 'Counts'
            }
        };

        let dataPlot = [trace1];
        Plotly.newPlot('plot', dataPlot, layout);

        */
    });

    py.on('close', () => {
        console.log('Returned to javascript');
    });
}
/////////////////////////////////////////////////////////