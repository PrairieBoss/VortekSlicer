
function OnStart()
{
	window.location.href="../2/index.html"+"?"+GetGetStr();
}

let welcomeApplicationName = null;

function InitWelcome() {
    TranslatePage();
    if (welcomeApplicationName) ApplyApplicationName(welcomeApplicationName);
}

// Apply native identity regardless of whether translation or the native event runs first.
function ApplyApplicationName(appName) {
    if (typeof appName !== "string" || !appName || appName === "OrcaSlicer") return;
    welcomeApplicationName = appName;

    for (const id of ["Title", "STip"]) {
        const node = document.getElementById(id);
        if (node) {
            // The Turkish setup sentence translates "Slicer" as "Dilimleyici".
            // Only these welcome text nodes change; links and credits are untouched.
            node.textContent = node.textContent.replace(/Orca(?:\s*Slicer|\s+Dilimleyici)/g, () => appName);
        }
    }
}
