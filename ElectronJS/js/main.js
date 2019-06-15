const { app, BrowserWindow, dialog } = require('electron')
const path = require('path')
let mainWindow

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
    })

    mainWindow.loadFile('html/index.html')
    mainWindow.on('closed', function() {
        mainWindow = null
    })
}
app.on('ready', createWindow)

app.on('window-all-closed', function() {
    app.quit()
})

app.on('activate', function() {
    if (mainWindow === null) createWindow()
})