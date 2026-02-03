(function () {
    const MOBILE_MAX_WIDTH = 767;

    const isMobile = window.matchMedia(
        `(max-width: ${MOBILE_MAX_WIDTH}px)`
    ).matches;

    const script = document.createElement("script");
    script.src = isMobile
        ? "https://adm.shinobi.jp/s/86618523177f2c4a1819c7d5733ac04c"
        : "https://adm.shinobi.jp/s/d803ce14cb8127f899862ee566509aa8";

    script.async = true;


    currentScript.parentNode.appendChild(script);
})();
