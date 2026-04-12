document.addEventListener("DOMContentLoaded", function () {
    const versionElements = document.querySelectorAll('#version-tidy-drive');
    if (versionElements) {
        versionElements.forEach((versionElement) => {
            versionElement.textContent = "Ver 1.8.8";
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

document.addEventListener("DOMContentLoaded", function () {
    const versionElements = document.querySelectorAll('#version-mispla');
    if (versionElements) {
        versionElements.forEach((versionElement) => {
            versionElement.textContent = "Ver 0.1.3";
        })
    }
});