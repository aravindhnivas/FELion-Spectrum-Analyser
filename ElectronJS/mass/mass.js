//Importing required modules
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const path = require('path')
const spawn = require("child_process").spawn;


/////////////////////////////////////////////////////////
$(document).ready(function() {
    $("#mass-open-btn").click(openFile);
    $("#massplot-btn").click(masspec);

});

/////////////////////////////////////////////////////////

//Showing opened file label
let filePaths;
let label = document.querySelector("#label")

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

    let baseName = [];
    for (x in filePaths) {
        baseName.push(`: ${path.basename(filePaths[x])}`)
    }

    if (filePaths == undefined) {
        label.textContent = "No files selected "
        label.className = "alert alert-danger"

    } else {
        label.textContent = `${path.dirname(filePaths[0])} ${baseName}`;
        label.className = "alert alert-success"
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