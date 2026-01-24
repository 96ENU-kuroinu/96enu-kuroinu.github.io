document.addEventListener("DOMContentLoaded", function () {
    const versionElements = document.querySelectorAll('#version-tidy-drive');
    if (versionElements) {
        versionElements.forEach((versionElement) => {
            versionElement.textContent = "Ver 1.8.1";
        })
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const versionElements = document.querySelectorAll('#version-baconjam');
    if (versionElements) {
        versionElements.forEach((versionElement) => {
            versionElement.textContent = "Ver 1.11.2";
        })
    }
});