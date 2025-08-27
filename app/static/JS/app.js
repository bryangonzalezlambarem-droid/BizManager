// static/js/app.js
document.addEventListener("DOMContentLoaded", () => {
    const msgBox = document.getElementById("global-messages");
    const loader = document.getElementById("global-loader");

    // B. G. L. 27/08/2025 Mostrar mensaje global
    window.showMessage = function (text, type = "success", timeout = 3000) {
        msgBox.innerHTML = `<div class="msg ${type}">${text}</div>`;
        msgBox.style.display = "block";
        if (timeout) {
            setTimeout(() => {
                msgBox.style.display = "none";
                msgBox.innerHTML = "";
            }, timeout);
        }
    };

    // B. G. L. 27/08/2025 Mostrar loader
    window.showLoader = function () {
        loader.style.display = "flex";
    };

    // B. G. L. 27/08/2025 Ocultar loader
    window.hideLoader = function () {
        loader.style.display = "none";
    };

    // B. G. L. 27/08/2025 Confirmacion antes de eliminar
    window.confirmDelete = function (callback) {
        if (confirm("¿Seguro que deseas eliminar este registro?")) {
            callback();
        }
    };
});
