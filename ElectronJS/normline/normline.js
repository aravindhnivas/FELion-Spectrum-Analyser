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
    $("#avgPlot-btn").click(avgplot);
    $("#baseline-btn").click(basePlot);
    $(() => $('[data-toggle="tooltip"]').tooltip("show"))

    $("#help").bootstrapToggle({
        on: 'Help',
        off: 'Help'
    });

    $('#help').change(function() {
        let status = $(this).prop('checked')
        console.log(`Status: ${status}\nType: ${typeof status}`)
    });

    //END
})

/////////////////////////////////////////////////////////
//Showing opened file label
let filePaths;
let label = document.querySelector("#label")

function openFile(e) {

    const options = {
        title: "Open Felix file(s)",
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
let dataFromPython_norm;
let normlineBtn = document.querySelector("#normlinePlot-btn")

function normplot(e) {

    console.log("\n\nNormline Spectrum")
    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)

    if (filePaths === undefined) {

        label.textContent = "No files selected "
        label.className = "alert alert-danger"
        normlineBtn.className = "btn btn-danger"
        return setTimeout(() => normlineBtn.className = "btn btn-primary", 2000)
    }

    const py = spawn('python', [path.join(__dirname, "./normline.py"), [filePaths]]);

    py.stdout.on('data', (data) => {

        try {

            dataFromPython_norm = data.toString('utf8')
                //console.log("Before JSON parse (from python):\n" + dataFromPython_norm)

            dataFromPython_norm = JSON.parse(dataFromPython_norm)
            console.log("After JSON parse :" + dataFromPython_norm)

            let layout = {
                title: 'Processing Felix data',
                xaxis: {
                    domain: [0, 0.3],
                    anchor: 'y1',
                    title: 'Calibrated Wavelength'
                },
                yaxis: {
                    domain: [0, 1],
                    anchor: 'y1',
                    title: 'Intesity',
                },
                xaxis2: {
                    domain: [0.4, 1],
                    anchor: 'y2',
                    title: "Calibrated Wavelength"
                },
                yaxis2: {
                    domain: [0, 1],
                    anchor: 'x2',
                    title: "Normalised Intesity"
                },
            };

            let dataPlot = [];
            for (x in dataFromPython_norm["felix"]) {
                dataPlot.push(dataFromPython_norm["felix"][x])

            }
            for (x in dataFromPython_norm["base"]) {
                dataPlot.push(dataFromPython_norm["base"][x])
            }
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

let dataFromPython_avg;
let delta = document.querySelector("#delta")

let avgPlotBtn = document.querySelector("#avgPlot-btn")

function avgplot(e) {

    console.log("\n\nAverage Spectrum")

    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)
    console.log("--------------------------")

    if (filePaths === undefined) {
        label.textContent = "No files selected "
        label.className = "alert alert-danger"
        avgPlotBtn.className = "btn btn-danger"
        return setTimeout(() => avgPlotBtn.className = "btn btn-primary", 2000)
    }

    const py = spawn('python', [path.join(__dirname, "./avgplot.py"), [filePaths, delta.value]]);

    py.stdout.on('data', (data) => {

        try {
            dataFromPython_avg = data.toString('utf8')
                //console.log("Before JSON parse (from python):\n" + dataFromPython_avg)
            dataFromPython_avg = JSON.parse(dataFromPython_avg)
            console.log("After JSON parse :" + dataFromPython_avg)

            let layout = {
                title: `Average of Normalised Spectrum (delta=${delta.value})`,
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

let baselineBtn = document.querySelector("#baseline-btn")

function basePlot(e) {

    console.log("\n\nBaseline Correction")
    console.log("I am in javascript now!!")
    console.log(`File: ${filePaths}; ${typeof filePaths}`)
    console.log("--------------------------")

    if (filePaths === undefined) {

        label.textContent = "No files selected "
        label.className = "alert alert-danger"
        baselineBtn.className = "btn btn-danger"
        return setTimeout(() => baselineBtn.className = "btn btn-primary", 2000)
    }
    const py = spawn('python', [path.join(__dirname, "./baseline.py"), [filePaths]]);

    py.stdout.on('data', (data) => {
        try {
            let logFromPython = data.toString('utf8')
            console.log("From python:\n" + logFromPython)
        } catch (err) {
            console.log("Error Occured in javascript code: " + err.message)
        }

    });

    py.on('close', () => {
        console.log('Returned to javascript');
    });

}