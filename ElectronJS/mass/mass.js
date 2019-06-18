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
let labelName;
let baseName = []

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

    //create an alert label
    if (openFilePlace.children.length > 0) { //Check if the alert label is already created under openFileLabel class
        openLabel = document.querySelector('.mass-openFileLabel');
    } else { // if not then create one
        openLabel = document.createElement('label');
        openLabel.className = "alert alert-primary mass-openFileLabel";
    }

    if (filePaths !== undefined) { // The file is defined

        // defining the basename of the file
        for (let i = 0; i < filePaths.length; i++) {
            baseName.push(path.basename(filePaths[i]))
        }

        labelName = `${path.dirname(filePaths[0])}; \n${baseName}`

        if (openFilePlace.children.length > 0) { // We have already created a label, so let's just replace the name with this new filepaths
            openLabel.innerHTML = labelName
        } else { // The label is empty hence first create a label
            itemText = document.createTextNode(labelName);
            openLabel.appendChild(itemText);
            openFilePlace.appendChild(openLabel);
        }
    } else { // The file is undefined
        if (openFilePlace.children.length > 0) { // we already have the file label so remove it.
            openLabel.remove()
        }

        //Alret that no-file is selected
        openLabel.className = "alert alert-danger mass-openFileLabel";
        openLabel.innerHTML = "No file selected"
        openFilePlace.appendChild(openLabel);
        setTimeout(() => openLabel.remove(), 2000)
    }
}
/////////////////////////////////////////////////////////
//python backend
let dataFromPython;

function masspec(e) {

    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    const py = spawn('python', [path.join(__dirname, "./mass.py"), filePaths]);

    py.stdout.on('data', (data) => {

        try {

            dataFromPython = data.toString('utf8')
                //console.log("Before JSON parse :" + dataFromPython)
            dataFromPython = JSON.parse(dataFromPython)
            console.log("After JSON parse :" + dataFromPython)

            let layout = {
                title: 'Mass spectrum',
                xaxis: {
                    title: 'Mass [u]'
                },
                yaxis: {
                    title: 'Counts',
                    type: "log"
                }
            };

            let dataPlot = [];
            for (x in dataFromPython) {
                dataPlot.push(dataFromPython[x])
            }

            console.log(dataPlot)
            Plotly.newPlot('plot', dataPlot, layout);

        } catch (err) {
            console.log("Error Occured in javascript code: " + err.message)
        }

    });

    py.on('close', () => {
        console.log('Returned to javascript');
    });
}
/////////////////////////////////////////////////////////