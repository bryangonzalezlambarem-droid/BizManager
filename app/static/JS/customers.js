document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#customers-table tbody");
    const formContainer = document.getElementById("customer-form-container");
    const form = document.getElementById("customer-form");
    const formTitle = document.getElementById("form-title");
    const customerIdField = document.getElementById("customer-id");
    const nameField = document.getElementById("customer-name");
    const emailField = document.getElementById("customer-email");
    const phoneField = document.getElementById("customer-phone");
    const addressField = document.getElementById("customer-address");
    const errorContainer = document.getElementById("error-container");
    const successContainer = document.getElementById("success-container");

    // B. G. L. 29/08/2025 Funcion para mostrar mensajes
    function showMessage(container, message) {
        container.textContent = message;
        container.style.display = "block";
        setTimeout(() => {
            container.style.display = "none";
        }, 5000);
    }

    // B. G. L. 29/08/2025 Funcion para validar email
    function isValidEmail(email) {
        const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return pattern.test(email);
    }

    // B. G. L. 29/08/2025 Funcion para validar telefono
    function isValidPhone(phone) {
        if (!phone) return true; // Opcional
        const pattern = /^\+?[1-9]\d{1,14}$/;
        return pattern.test(phone);
    }

    // B. G. L. 27/08/2025 Mostrar formulario para nuevo cliente
    document.getElementById("btn-new-customer").addEventListener("click", () => {
        form.reset();
        customerIdField.value = "";
        formTitle.textContent = "Nuevo Cliente";
        formContainer.style.display = "block";
        errorContainer.style.display = "none";
        successContainer.style.display = "none";
    });

    // B. G. L. 27/08/2025 Cancelar formulario
    document.getElementById("cancel-btn").addEventListener("click", () => {
        formContainer.style.display = "none";
        errorContainer.style.display = "none";
    });

    // B. G. L. 27/08/2025 Cargar clientes desde API
    async function loadCustomers() {
        try {
            const res = await fetch("/api/customers/");
            
            if (!res.ok) {
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            
            const response = await res.json();
            const customers = response.customers || response;
            
            tableBody.innerHTML = "";
            
            if (customers.length === 0) {
                const row = document.createElement("tr");
                row.innerHTML = `<td colspan="6" style="text-align: center;">No hay clientes registrados</td>`;
                tableBody.appendChild(row);
                return;
            }
            
            customers.forEach(c => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${c.id}</td>
                    <td>${c.name}</td>
                    <td>${c.email}</td>
                    <td>${c.phone || ""}</td>
                    <td>${c.address || ""}</td>
                    <td>
                    <button class="btn-edit" data-id="${c.id}">Editar</button>
                    <button class="btn-delete" data-id="${c.id}">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // B. G. L. 29/08/2025 Conectar botones de acciones
            document.querySelectorAll(".btn-edit").forEach(btn => {
                btn.addEventListener("click", () => editCustomer(btn.dataset.id));
            });
            document.querySelectorAll(".btn-delete").forEach(btn => {
                btn.addEventListener("click", () => deleteCustomer(btn.dataset.id));
            });
            
        } catch (error) {
            console.error("Error al cargar clientes:", error);
            showMessage(errorContainer, "Error al cargar los clientes: " + error.message);
        }
    }

    // B. G. L. 27/08/2025 Editar cliente
    async function editCustomer(id) {
        try {
            const res = await fetch(`/api/customers/${id}`);
            
            if (!res.ok) {
                if (res.status === 404) {
                    throw new Error("Cliente no encontrado");
                }
                throw new Error(`Error ${res.status}: ${res.statusText}`);
            }
            
            const c = await res.json();
            customerIdField.value = c.id;
            nameField.value = c.name;
            emailField.value = c.email;
            phoneField.value = c.phone || "";
            addressField.value = c.address || "";
            formTitle.textContent = "Editar Cliente";
            formContainer.style.display = "block";
            errorContainer.style.display = "none";
            
        } catch (error) {
            console.error("Error al cargar cliente:", error);
            showMessage(errorContainer, error.message);
        }
    }

    // B. G. L. 27/08/2025 Eliminar cliente
    async function deleteCustomer(id) {
        if (!confirm("¿Seguro que quieres eliminar este cliente?")) return;
        
        try {
            const res = await fetch(`/api/customers/${id}`, { method: "DELETE" });
            
            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.error || `Error ${res.status}: ${res.statusText}`);
            }
            
            showMessage(successContainer, "Cliente eliminado correctamente");
            loadCustomers();
            
        } catch (error) {
            console.error("Error al eliminar cliente:", error);
            showMessage(errorContainer, "Error al eliminar cliente: " + error.message);
        }
    }

    // B. G. L. 27/08/2025 Guardar cliente (crear o editar)
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        // B. G. L. 29/08/2025 Validaciones del frontend
        if (!nameField.value.trim()) {
            showMessage(errorContainer, "El nombre es obligatorio");
            return;
        }
        
        if (!emailField.value.trim()) {
            showMessage(errorContainer, "El email es obligatorio");
            return;
        }
        
        if (!isValidEmail(emailField.value)) {
            showMessage(errorContainer, "El formato del email no es válido");
            return;
        }
        
        if (phoneField.value && !isValidPhone(phoneField.value)) {
            showMessage(errorContainer, "El formato del teléfono no es válido");
            return;
        }
        
        const id = customerIdField.value;
        const data = {
            name: nameField.value.trim(),
            email: emailField.value.trim(),
            phone: phoneField.value.trim() || null,
            address: addressField.value.trim() || null
        };

        let url = "/api/customers/";
        let method = "POST";

        if (id) {
            url = `/api/customers/${id}`;
            method = "PUT";
        }

        try {
            const res = await fetch(url, {
                method: method,
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            
            const responseData = await res.json();
            
            if (!res.ok) {
                throw new Error(responseData.error || `Error ${res.status}: ${res.statusText}`);
            }
            
            showMessage(successContainer, responseData.message || "Operación realizada correctamente");
            formContainer.style.display = "none";
            loadCustomers();
            
        } catch (error) {
            console.error("Error al guardar cliente:", error);
            showMessage(errorContainer, "Error al guardar cliente: " + error.message);
        }
    });

    // B. G. L. 27/08/2025 Iniciar
    loadCustomers();
});