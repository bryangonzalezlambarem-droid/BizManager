document.addEventListener("DOMContentLoaded", () => {
    const btnNew = document.getElementById("btn-new-order");
    const formContainer = document.getElementById("order-form-container");
    const cancelBtn = document.getElementById("cancel-form");

    btnNew.addEventListener("click", () => {
        formContainer.style.display = "block";
    });

    cancelBtn.addEventListener("click", () => {
        formContainer.style.display = "none";
    });
});
