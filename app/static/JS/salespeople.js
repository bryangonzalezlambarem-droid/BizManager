// B. G. L. 27/08/2025 static/js/salespeople.js

document.addEventListener("DOMContentLoaded", () => {
    const btnNew = document.getElementById("btn-new-salesperson");

    // B. G. L. 27/08/2025 Contenedor del formulario
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
    const mainContent = document.querySelector("main > div");
    mainContent.appendChild(formContainer);

    const form = document.getElementById("salesperson-form");
    const cancelBtn = document.getElementById("cancel-form");
    const idField = document.getElementById("salesperson_id");
    const nameField = document.getElementById("name");
    const emailField = document.getElementById("email");
    const phoneField = document.getElementById("phone");
    const formTitle = document.getElementById("form-title");

    const EMAIL_REGEX = /^[^@]+@[^@]+\.[^@]+$/;

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

        // Validaciones
        if (!nameField.value.trim()) return alert("Nombre requerido");
        if (!EMAIL_REGEX.test(emailField.value)) return alert("Email inválido");
        if (phoneField.value.length < 7 || phoneField.value.length > 15) return alert("Teléfono inválido");

        const payload = {
            name: nameField.value.trim(),
            email: emailField.value.trim(),
            phone: phoneField.value.trim()
        };

        let url = "api/salespersons";
        let method = "POST";

        if (idField.value) {
            url = `api/salespersons/${idField.value}`;
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
                alert("Error: " + (data.error || "Desconocido"));
            }
        } catch (err) {
            console.error(err);
            alert("Error en la operación");
        }
    });

    // B. G. L. 27/08/2025 Funcion para agregar eventos de ver/editar
    function attachRowEvents() {
        // Ver
        document.querySelectorAll(".btn-view").forEach(btn => {
            btn.addEventListener("click", async () => {
                try {
                    const id = btn.dataset.id;
                    const res = await fetch(`api/salespersons/${id}`);
                    if (!res.ok) throw new Error("No se pudo obtener el vendedor");
                    const sp = await res.json();
                    alert("Detalles del Vendedor:\n" + JSON.stringify(sp, null, 2));
                } catch (err) {
                    console.error(err);
                    alert(err.message);
                }
            });
        });

        //  B. G. L. 22/08/2025  Editar
        document.querySelectorAll(".btn-edit").forEach(btn => {
            btn.addEventListener("click", async () => {
                try {
                    const id = btn.dataset.id;
                    const res = await fetch(`api/salespersons/${id}`);
                    if (!res.ok) throw new Error("No se pudo obtener el vendedor");
                    const sp = await res.json();

                    idField.value = sp.salesman_id;
                    nameField.value = sp.name;
                    emailField.value = sp.email;
                    phoneField.value = sp.phone;

                    formTitle.textContent = "Editar Vendedor";
                    formContainer.style.display = "block";
                } catch (err) {
                    console.error(err);
                    alert(err.message);
                }
            });
        });

        //  B. G. L. 03/09/2025 Eliminar
        document.querySelectorAll(".btn-delete").forEach(btn => {
            btn.addEventListener("click", async () => {
                const id = btn.dataset.id;
                if (!confirm("¿Seguro que deseas eliminar este vendedor?")) return;

                try {
                    const res = await fetch(`api/salespersons/${id}`, {
                        method: "DELETE",
                        headers: { "Content-Type": "application/json" }
                    });
                    const data = await res.json();
                    if (res.ok) {
                        alert(data.message || "Vendedor eliminado");
                        location.reload();
                    } else {
                        alert("Error: " + (data.error || "Desconocido"));
                    }
                } catch (err) {
                    console.error(err);
                    alert("Error al eliminar");
                }
            });
        });
    }

    // B. G. L. 27/08/2025 Llamar al cargar
    attachRowEvents();
});
