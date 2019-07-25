//Importing required modules
const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();
const path = require('path')
const spawn = require("child_process").spawn;
const fs = require('fs')

/////////////////////////////////////////////////////////
$(document).ready(function() {

    $("#timescan-btn").click(openFile);

    $(() => $('[data-toggle="tooltip"]').tooltip("disable"))

    // Info  display toggle
    $("#help").bootstrapToggle({
        on: 'Help',
        off: 'Help'
    });

    $('#help').change(function() {
        let info = $(this).prop('checked')
        console.log(`Status: ${info}\nType: ${typeof info}`)
        info_status(info)
    });

    //END
})

function info_status(info) {
    if (info) {
        $(() => $('[data-toggle="tooltip"]').tooltip("enable"))
        $(() => $('[data-toggle="tooltip"]').tooltip("show"))
    } else {
        $(() => $('[data-toggle="tooltip"]').tooltip("hide"))
        $(() => $('[data-toggle="tooltip"]').tooltip("disable"))
    }
}

/////////////////////////////////////////////////////////

//Showing opened file label

let filePaths;
let label = document.querySelector("#timescan-label")
let fileLocation;
let baseName = [];

function openFile(e) {

    const options = {
        title: "Open file(s)",
        defaultPath: "D:",
        filters: [
            { name: 'Timescan', extensions: ['scan'] },
            { name: 'DAT', extensions: ['dat'] },
            { name: 'Powerfile', extensions: ['pow'] },
            { name: 'txt', extensions: ['txt'] },
            { name: 'All Files', extensions: ['*'] }
        ],
        properties: ['openFile', 'multiSelections'],
    };
    filePaths = dialog.showOpenDialog(mainWindow, options);

    if (filePaths == undefined) {

        label.textContent = "No files selected "
        label.className = "alert alert-danger"

    } else {

        baseName = [];
        for (x in filePaths) {
            baseName.push(`| ${path.basename(filePaths[x])}`)
        }

        fileLocation = path.dirname(filePaths[0])

        label.textContent = `${fileLocation} ${baseName}`;
        label.className = "alert alert-success"
    }
}
/////////////////////////////////////////////////////////