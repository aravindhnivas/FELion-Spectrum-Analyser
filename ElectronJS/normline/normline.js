//Importing required modules
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const path = require('path')
const spawn = require("child_process").spawn;

/////////////////////////////////////////////////////////
$(document).ready(function() {
    $("#normline-open-btn").click(openFile);
    $("#normlinePlot-btn").click(normplot);
    $("#avgPlot-btn").click(avgplot)

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
            { name: 'Felix files', extensions: ['felix', 'cfelix'] },
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
//python backend  Normline
let dataFromPython_norm;

function normplot(e) {

    console.log("\n\nNormline Spectrum")

    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    const py = spawn('python', [path.join(__dirname, "./normline.py"), [filePaths]]);

    py.stdout.on('data', (data) => {

        try {

            dataFromPython_norm = data.toString('utf8')
                //console.log("Before JSON parse (from python):\n" + dataFromPython_norm)

            dataFromPython_norm = JSON.parse(dataFromPython_norm)
            console.log("After JSON parse :" + dataFromPython_norm)

            let layout = {
                title: 'Normlised Spectrum',
                xaxis: {
                    title: 'Calibrated Wavelength'
                },
                yaxis: {
                    title: 'Normalised Intesity',
                }
            };

            let dataPlot = [];
            for (x in dataFromPython_norm) {
                dataPlot.push(dataFromPython_norm[x])
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

//python backend  AveragePlot
let dataFromPython_avg;

function avgplot(e) {

    console.log("\n\nAverage Spectrum")

    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)
    console.log("--------------------------")

    const py = spawn('python', [path.join(__dirname, "./avgplot.py"), [filePaths, 2]]);

    py.stdout.on('data', (data) => {

        try {
            dataFromPython_avg = data.toString('utf8')
                //console.log("Before JSON parse (from python):\n" + dataFromPython_avg)
            dataFromPython_avg = JSON.parse(dataFromPython_avg)
            console.log("After JSON parse :" + dataFromPython_avg)

            let layout = {
                title: 'Average of Normalised Spectrum',
                xaxis: {
                    title: 'Calibrated Wavelength'
                },
                yaxis: {
                    title: 'Normalised Intesity',
                }
            };

            let dataPlot = [];
            for (x in dataFromPython_avg) {
                dataPlot.push(dataFromPython_avg[x])
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