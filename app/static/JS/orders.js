// static/js/orders.js

document.addEventListener("DOMContentLoaded", () => {
    const btnNewOrder = document.getElementById("btn-new-order");
    const orderFormContainer = document.getElementById("order-form-container");
    const orderForm = document.getElementById("order-form");
    const cancelFormBtn = document.getElementById("cancel-form");
    const orderDetailsDiv = document.getElementById("order-details");

    // B. G. L. 29/08/2025 Obtener productos desde el div oculto
    const productsDataEl = document.getElementById("products-data");
    const PRODUCTS = JSON.parse(productsDataEl.dataset.products || "[]");

    // B. G. L. 29/08/2025 Mostrar formulario para nuevo pedido
    btnNewOrder.addEventListener("click", () => {
        orderFormContainer.style.display = "block";
        orderForm.reset();
        orderDetailsDiv.innerHTML = "";
        addProductRow();
    });

    // B. G. L. 29/08/2025 Cancelar formulario
    cancelFormBtn.addEventListener("click", () => {
        orderFormContainer.style.display = "none";
    });

    //  B. G. L. 29/08/2025 Agregar fila de producto dinamicamente
    function addProductRow() {
        const row = document.createElement("div");
        row.classList.add("order-product-row");

        row.innerHTML = `
            <select name="product_id" class="product-select">
                <option value="">--Selecciona un producto--</option>
                ${PRODUCTS.map(p => `<option value="${p.product_id}">${p.name}</option>`).join("")}
            </select>
            <input type="number" name="quantity" min="1" value="1" placeholder="Cantidad" required>
            <button type="button" class="remove-product">❌</button>
        `;

        row.querySelector(".remove-product").addEventListener("click", () => row.remove());
        orderDetailsDiv.appendChild(row);
    }

    // B. G. L. 29/08/2025 Boton para agregar mas productos
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "➕ Agregar Producto";
    addBtn.addEventListener("click", addProductRow);
    orderDetailsDiv.parentNode.insertBefore(addBtn, orderDetailsDiv.nextSibling);

    //  B. G. L. 29/08/2025 Enviar pedido al backend
    orderForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const customer_id = document.getElementById("customer_id").value;
        const salesperson_id = document.getElementById("salesperson_id").value;

        if (!customer_id) {
            alert("Debe seleccionar un cliente");
            return;
        }

        const rows = document.querySelectorAll(".order-product-row");
        if (rows.length === 0) {
            alert("Agrega al menos un producto");
            return;
        }

        const details = [];
        for (let row of rows) {
            const product_id = row.querySelector("select[name='product_id']").value;
            const quantity = parseInt(row.querySelector("input[name='quantity']").value);

            if (!product_id) {
                alert("Selecciona un producto en todas las filas");
                return;
            }
            if (!quantity || quantity < 1) {
                alert("Ingresa una cantidad válida");
                return;
            }

            details.push({
                product_id,
                quantity,
                salesman_id: salesperson_id
            });
        }

        const payload = { customer_id, details };

        try {
            const res = await fetch("/orders", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (res.ok) {
                alert("Pedido creado con éxito (ID: " + data.order_id + ")");
                location.reload();
            } else {
                alert("Error: " + (data.error || "Desconocido"));
            }
        } catch (err) {
            console.error(err);
            alert("Error al enviar pedido");
        }
    });

    // B. G. L. 29/08/2025 Ver detalles del pedido
    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            try {
                const res = await fetch(`/orders/${id}`);
                if (!res.ok) throw new Error("Pedido no encontrado");
                const order = await res.json();
                alert("Detalles del pedido:\n" + JSON.stringify(order, null, 2));
            } catch (err) {
                console.error(err);
                alert("Error al obtener el pedido: " + err.message);
            }
        });
    });
});
