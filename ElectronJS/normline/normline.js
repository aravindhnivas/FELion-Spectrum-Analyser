const { remote } = require('electron');
const dialog = remote.dialog;
const mainWindow = remote.getCurrentWindow();

const options = {
    title: "Open .felix or .cfelic file(s)",
    defaultPath: "D:",
    filters: [
        { name: 'FELIX filees', extensions: ['felix', 'cfelix'] },
        { name: 'All Files', extensions: ['*'] }
    ],
    properties: ['openFile', 'multiSelections'],
};

function openFile() {
    const filePaths = dialog.showOpenDialog(mainWindow, options);
    console.log(filePaths);
}