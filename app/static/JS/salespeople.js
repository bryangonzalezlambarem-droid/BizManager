// static/js/salespeople.js

document.addEventListener("DOMContentLoaded", () => {
    const btnNew = document.getElementById("btn-new-salesperson");

    // B. G. L. 27/08/2025 Crear un contenedor para el formulario
    let formContainer = document.createElement("div");
    formContainer.id = "salesperson-form-container";
    formContainer.style.display = "none";
    formContainer.innerHTML = `
        <form id="salesperson-form">
            <h3 id="form-title">Nuevo Vendedor</h3>
            <input type="hidden" id="salesperson_id">

            <label>Nombre:</label>
            <input type="text" id="name" required>

            <label>Email:</label>
            <input type="email" id="email" required>

            <label>Teléfono:</label>
            <input type="text" id="phone" required>

            <button type="submit">Guardar</button>
            <button type="button" id="cancel-form">Cancelar</button>
        </form>
    `;
    document.body.appendChild(formContainer);

    const form = document.getElementById("salesperson-form");
    const cancelBtn = document.getElementById("cancel-form");
    const idField = document.getElementById("salesperson_id");
    const nameField = document.getElementById("name");
    const emailField = document.getElementById("email");
    const phoneField = document.getElementById("phone");
    const formTitle = document.getElementById("form-title");

    // B. G. L. 27/08/2025 Abrir formulario para nuevo vendedor
    btnNew.addEventListener("click", () => {
        idField.value = "";
        nameField.value = "";
        emailField.value = "";
        phoneField.value = "";
        formTitle.textContent = "Nuevo Vendedor";
        formContainer.style.display = "block";
    });

    // B. G. L. 27/08/2025 Cancelar
    cancelBtn.addEventListener("click", () => {
        formContainer.style.display = "none";
    });

    // B. G. L. 27/08/2025 Guardar vendedor (nuevo o editado)
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            name: nameField.value,
            email: emailField.value,
            phone: phoneField.value
        };

        let url = "/salespersons";
        let method = "POST";

        if (idField.value) {
            // B. G. L. 27/08/2025 modo edicion
            url = `/salespersons/${idField.value}`;
            method = "PUT";
        }

        try {
            const res = await fetch(url, {
                method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (res.ok) {
                alert(data.message || "Operación exitosa");
                location.reload();
            } else {
                alert("Error: " + data.error);
            }
        } catch (err) {
            console.error(err);
            alert("Error en la operación");
        }
    });

    // B. G. L. 27/08/2025 Ver vendedor
    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            const res = await fetch(`/salespersons/${id}`);
            const sp = await res.json();
            alert("Detalles del Vendedor:\n" + JSON.stringify(sp, null, 2));
        });
    });

    // B. G. L. 27/08/2025 Editar vendedor
    document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            const res = await fetch(`/salespersons/${id}`);
            const sp = await res.json();

            idField.value = sp.id || sp.salesman_id;
            nameField.value = sp.name;
            emailField.value = sp.email;
            phoneField.value = sp.phone;

            formTitle.textContent = "Editar Vendedor";
            formContainer.style.display = "block";
        });
    });
});
