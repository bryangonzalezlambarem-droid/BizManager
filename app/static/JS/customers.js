document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#customers-table tbody");
    const formContainer = document.getElementById("customer-form-container");
    const form = document.getElementById("customer-form");
    const formTitle = document.getElementById("form-title");
    const customerIdField = document.getElementById("customer-id");
    const nameField = document.getElementById("customer-name");
    const emailField = document.getElementById("customer-email");
    const phoneField = document.getElementById("customer-phone");
    const adressField = document.getElementById("customer-adress");

    // B. G. L. 27/08/2025 Mostrar formulario para nuevo cliente
    document.getElementById("btn-new-customer").addEventListener("click", () => {
        form.reset();
        customerIdField.value = "";
        formTitle.textContent = "Nuevo Cliente";
        formContainer.style.display = "block";
    });

    // B. G. L. 27/08/2025 Cancelar formulario
    document.getElementById("cancel-btn").addEventListener("click", () => {
        formContainer.style.display = "none";
    });

    // B. G. L. 27/08/2025 Cargar clientes desde API
    async function loadCustomers() {
        const res = await fetch("/customers/");
        const customers = await res.json();
        tableBody.innerHTML = "";
        customers.forEach(c => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.email}</td>
            <td>${c.phone || ""}</td>
            <td>${c.adress || ""}</td>
            <td>
            <button class="btn-edit" data-id="${c.id}">Editar</button>
            <button class="btn-delete" data-id="${c.id}">Eliminar</button>
            </td>
        `;
        tableBody.appendChild(row);
        });

        // Conectar botones de acciones
        document.querySelectorAll(".btn-edit").forEach(btn => {
        btn.addEventListener("click", () => editCustomer(btn.dataset.id));
        });
        document.querySelectorAll(".btn-delete").forEach(btn => {
        btn.addEventListener("click", () => deleteCustomer(btn.dataset.id));
        });
    }

    // B. G. L. 27/08/2025 Editar cliente
    async function editCustomer(id) {
        const res = await fetch(`/customers/${id}`);
        const c = await res.json();
        customerIdField.value = c.id;
        nameField.value = c.name;
        emailField.value = c.email;
        phoneField.value = c.phone || "";
        adressField.value = c.adress || "";
        formTitle.textContent = "Editar Cliente";
        formContainer.style.display = "block";
    }

    // B. G. L. 27/08/2025 Eliminar cliente
    async function deleteCustomer(id) {
        if (!confirm("¿Seguro que quieres eliminar este cliente?")) return;
        await fetch(`/customers/${id}`, { method: "DELETE" });
        loadCustomers();
    }

    // B. G. L. 27/08/2025 Guardar cliente (crear o editar)
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = customerIdField.value;
        const data = {
        name: nameField.value,
        email: emailField.value,
        phone: phoneField.value,
        adress: adressField.value
        };

        let url = "/customers/";
        let method = "POST";

        if (id) {
        url = `/customers/${id}`;
        method = "PUT";
        }

        await fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
        });

        formContainer.style.display = "none";
        loadCustomers();
    });

    // B. G. L. 27/08/2025 Iniciar
    loadCustomers();
    });
