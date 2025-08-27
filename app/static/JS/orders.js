// static/js/orders.js

document.addEventListener("DOMContentLoaded", () => {
    const btnNewOrder = document.getElementById("btn-new-order");
    const orderFormContainer = document.getElementById("order-form-container");
    const orderForm = document.getElementById("order-form");
    const cancelFormBtn = document.getElementById("cancel-form");
    const orderDetailsDiv = document.getElementById("order-details");

    // B. G. L. 27/08/2025 Obtener productos desde el div oculto
    const productsDataEl = document.getElementById("products-data");
    const PRODUCTS = JSON.parse(productsDataEl.dataset.products || "[]");

    // B. G. L. 25/08/2025 Mostrar formulario para nuevo pedido
    btnNewOrder.addEventListener("click", () => {
        orderFormContainer.style.display = "block";
        orderForm.reset();
        orderDetailsDiv.innerHTML = ""; // B. G. L. 25/08/2025 limpiar productos
        addProductRow(); // B. G. L. 25/08/2025 empezar con 1 producto
    });

    // B. G. L. 25/08/2025 Cancelar
    cancelFormBtn.addEventListener("click", () => {
        orderFormContainer.style.display = "none";
    });

    // B. G. L. 25/08/2025 Agregar producto dinamicamente
    function addProductRow() {
        const row = document.createElement("div");
        row.classList.add("order-product-row");

        row.innerHTML = `
            <select name="product_id" class="product-select">
                ${PRODUCTS.map(p => `<option value="${p.product_id}">${p.name}</option>`).join("")}
            </select>
            <input type="number" name="quantity" min="1" value="1" placeholder="Cantidad">
            <input type="number" name="unit_price" step="0.01" placeholder="Precio">
            <button type="button" class="remove-product">❌</button>
        `;

        row.querySelector(".remove-product").addEventListener("click", () => {
            row.remove();
        });

        orderDetailsDiv.appendChild(row);
    }

    // B. G. L. 25/08/2025 Enviar pedido al backend
    orderForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const customer_id = document.getElementById("customer_id").value;
        const salesperson_id = document.getElementById("salesperson_id").value;

        // B. G. L. 25/08/2025 Recoger detalles
        const details = Array.from(document.querySelectorAll(".order-product-row")).map(row => ({
            product_id: row.querySelector("select[name='product_id']").value,
            quantity: parseInt(row.querySelector("input[name='quantity']").value),
            unit_price: parseFloat(row.querySelector("input[name='unit_price']").value),
            salesman_id: salesperson_id
        }));

        const payload = {
            customer_id,
            details
        };

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
                alert("Error: " + data.error);
            }
        } catch (err) {
            console.error(err);
            alert("Error al enviar pedido");
        }
    });

    // B. G. L. 25/08/2025 Eventos para ver/editar
    document.querySelectorAll(".btn-view").forEach(btn => {
        btn.addEventListener("click", async () => {
            const id = btn.dataset.id;
            const res = await fetch(`/orders/${id}`);
            const order = await res.json();
            alert("Detalles del pedido:\n" + JSON.stringify(order, null, 2));
        });
    });

    // B. G. L. 25/08/2025 Boton para agregar mas productos
    const addBtn = document.createElement("button");
    addBtn.type = "button";
    addBtn.textContent = "➕ Agregar Producto";
    addBtn.addEventListener("click", addProductRow);
    orderDetailsDiv.parentNode.insertBefore(addBtn, orderDetailsDiv.nextSibling);
});
