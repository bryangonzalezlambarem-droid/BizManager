// static/js/orders.js

document.addEventListener("DOMContentLoaded", () => {
    const btnNewOrder = document.getElementById("btn-new-order");
    const orderFormContainer = document.getElementById("order-form-container");
    const orderForm = document.getElementById("order-form");
    const cancelFormBtn = document.getElementById("cancel-form");
    const orderDetailsDiv = document.getElementById("order-details");
    const ordersTableBody = document.querySelector("#orders-table tbody");

    // B. G. L. 03/09/2025 Productos desde el div oculto
    const productsDataEl = document.getElementById("products-data");
    const PRODUCTS = JSON.parse(productsDataEl.dataset.products || "[]");

    // ----- B. G. L. 03/09/2025 Funciones -----
    function addProductRow(productId = "", quantity = 1) {
        const row = document.createElement("div");
        row.classList.add("order-product-row");
        row.innerHTML = `
            <select name="product_id" class="product-select">
                <option value="">--Selecciona un producto--</option>
                ${PRODUCTS.map(p => `<option value="${p.product_id}" ${p.product_id == productId ? "selected" : ""}>${p.name}</option>`).join("")}
            </select>
            <input type="number" name="quantity" min="1" value="${quantity}" placeholder="Cantidad" required>
            <button type="button" class="remove-product">❌</button>
        `;
        row.querySelector(".remove-product").addEventListener("click", () => row.remove());
        orderDetailsDiv.appendChild(row);
    }

    function resetForm() {
        orderForm.reset();
        orderDetailsDiv.innerHTML = "";
        addProductRow();
    }

    function showForm() {
        orderFormContainer.style.display = "block";
    }

    function hideForm() {
        orderFormContainer.style.display = "none";
    }

    async function loadOrders() {
        try {
            const res = await fetch("/api/orders/");
            if (!res.ok) throw new Error("No se pudieron cargar los pedidos");
            const orders = await res.json();
            ordersTableBody.innerHTML = "";

            orders.forEach(o => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${o.order_id}</td>
                    <td>${o.customer_id}</td>
                    <td>${o.details.length > 0 ? o.details[0].salesman_id : ""}</td>
                    <td>${new Date(o.order_date).toLocaleString()}</td>
                    <td>${o.status}</td>
                    <td>${o.total_amount.toFixed(2)}</td>
                    <td>
                        <button class="btn-view" data-id="${o.order_id}">Ver</button>
                        <button class="btn-edit" data-id="${o.order_id}">Editar</button>
                        <button class="btn-delete" data-id="${o.order_id}">Eliminar</button>
                    </td>
                `;
                ordersTableBody.appendChild(row);
            });
        } catch (err) {
            console.error(err);
            alert(err.message);
        }
    }

    // ----- B. G. L. 03/09/2025 Eventos -----

    btnNewOrder.addEventListener("click", () => {
        resetForm();
        showForm();
    });

    cancelFormBtn.addEventListener("click", hideForm);

    // B. G. L. 03/09/2025 Enviar pedido (crear)
    orderForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const customer_id = document.getElementById("customer_id").value;
        const salesperson_id = document.getElementById("salesperson_id").value;
        const rows = document.querySelectorAll(".order-product-row");

        if (!customer_id || rows.length === 0) {
            alert("Selecciona cliente y agrega al menos un producto");
            return;
        }

        const details = [];
        rows.forEach(row => {
            const product_id = row.querySelector("select[name='product_id']").value;
            const quantity = parseInt(row.querySelector("input[name='quantity']").value);
            if (!product_id || !quantity || quantity < 1) throw new Error("Revisa los productos y cantidades");
            details.push({ product_id, quantity, salesman_id: salesperson_id });
        });

        try {
            const res = await fetch("/api/orders/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ customer_id, details })
            });
            const data = await res.json();
            if (res.ok) {
                alert(`Pedido creado con éxito (ID: ${data.order_id})`);
                hideForm();
                loadOrders();
            } else {
                alert(data.error || "Error desconocido");
            }
        } catch (err) {
            console.error(err);
            alert("Error al enviar pedido");
        }
    });

    // B. G. L. 03/09/2025 Delegacion de eventos en la tabla para Ver, Editar, Eliminar
    ordersTableBody.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        if (!id) return;

        // Ver
        if (e.target.classList.contains("btn-view")) {
            try {
                const res = await fetch(`/api/orders/${id}`);
                if (!res.ok) throw new Error("Pedido no encontrado");
                const order = await res.json();
                alert(JSON.stringify(order, null, 2));
            } catch (err) {
                console.error(err);
                alert("Error al obtener el pedido: " + err.message);
            }
        }

        // B. G. L. 03/09/2025 Editar
        if (e.target.classList.contains("btn-edit")) {
            try {
                const res = await fetch(`/api/orders/${id}`);
                if (!res.ok) throw new Error("Pedido no encontrado");
                const order = await res.json();
                resetForm();
                document.getElementById("customer_id").value = order.customer_id;
                document.getElementById("salesperson_id").value = order.details[0]?.salesman_id || "";
                order.details.forEach(d => addProductRow(d.product_id, d.quantity));
                showForm();
            } catch (err) {
                console.error(err);
                alert("Error al editar el pedido: " + err.message);
            }
        }

        // B. G. L. 03/09/2025 Eliminar
        if (e.target.classList.contains("btn-delete")) {
            if (!confirm("¿Seguro que quieres eliminar este pedido?")) return;
            try {
                const res = await fetch(`/api/orders/${id}`, { method: "DELETE" });
                const data = await res.json();
                if (res.ok) {
                    alert(data.message);
                    loadOrders();
                } else {
                    alert(data.error || "Error desconocido");
                }
            } catch (err) {
                console.error(err);
                alert("Error al eliminar el pedido");
            }
        }
    });

    // B. G. L. 03/09/2025 Boton para agregar mas productos
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "➕ Agregar Producto";
    addBtn.addEventListener("click", () => addProductRow());
    orderDetailsDiv.parentNode.insertBefore(addBtn, orderDetailsDiv.nextSibling);

    // B. G. L. 03/09/2025 Carga inicial de pedidos
    loadOrders();
});
