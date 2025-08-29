// B. G. L. 27/08/2025 CRUD Productos

document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#products-table tbody");
    const btnNewProduct = document.getElementById("btn-new-product");

    // B. G. L. 25/08/2025 Cargar productos al inicio
    async function loadProducts() {
        try {
            tableBody.innerHTML = "";
            const res = await fetch("/products");
            if (!res.ok) throw new Error("Error al cargar productos");
            const products = await res.json();
            
            products.forEach(p => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${p.id}</td>
                    <td>${p.name}</td>
                    <td>${p.description}</td>
                    <td>${p.price}</td>
                    <td>${p.stock}</td>
                    <td>-</td>
                    <td>
                        <button class="btn-view" data-id="${p.id}">Ver</button>
                        <button class="btn-edit" data-id="${p.id}">Editar</button>
                        <button class="btn-delete" data-id="${p.id}">Eliminar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } catch (err) {
            console.error(err);
            alert("No se pudieron cargar los productos.");
        }
    }

    // B. G. L. 25/08/2025 Crear producto
    async function createProduct(product) {
        try {
            const res = await fetch("/products", {
                method: "POST",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(product)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Error al crear producto");
            alert("Producto creado exitosamente");
            loadProducts();
        } catch (err) {
            console.error(err);
            alert(err.message);
        }
    }

    // B. G. L. 25/08/2025 Editar producto
    async function editProduct(id, product) {
        try {
            const res = await fetch(`/products/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json"},
                body: JSON.stringify(product)
            });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Error al actualizar producto");
            alert("Producto actualizado exitosamente");
            loadProducts();
        } catch (err) {
            console.error(err);
            alert(err.message);
        }
    }

    // B. G. L. 25/08/2025 Eliminar producto
    async function deleteProduct(id) {
        try {
            const res = await fetch(`/products/${id}`, { method: "DELETE" });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || "Error al eliminar producto");
            alert("Producto eliminado exitosamente");
            loadProducts();
        } catch (err) {
            console.error(err);
            alert(err.message);
        }
    }

    // B. G. L. 25/08/2025 Eventos de botones
    tableBody.addEventListener("click", e => {
        const id = e.target.dataset.id;

        if (e.target.classList.contains("btn-delete")) {
            if (confirm("¿Seguro que quieres eliminar este producto?")) {
                deleteProduct(id);
            }
        }

        if(e.target.classList.contains("btn-edit")) {
            const name = prompt("Nuevo nombre del producto:");
            const description = prompt("Nueva descripción:");
            const price = prompt("Nuevo precio:");
            const stock = prompt("Nuevo stock:");

            // B. G. L. 25/08/2025 Validar inputs
            const priceNum = parseFloat(price);
            const stockNum = parseInt(stock);

            if (!name || isNaN(priceNum) || priceNum < 0 || isNaN(stockNum) || stockNum < 0) {
                alert("Datos inválidos. Revisa nombre, precio y stock.");
                return;
            }

            editProduct(id, { name, description, price: priceNum, stock: stockNum });
        }

        if (e.target.classList.contains("btn-view")) {
            fetch(`/products/${id}`)
                .then(res => res.json())
                .then(p => alert(`Producto:\nNombre: ${p.name}\nDescripción: ${p.description}\nPrecio: ${p.price}\nStock: ${p.stock}`))
                .catch(err => {
                    console.error(err);
                    alert("Error al obtener producto");
                });
        }
    });

    // B. G. L. 25/08/2025 Boton nuevo producto
    btnNewProduct.addEventListener("click", () => {
        const name = prompt("Nombre del producto:");
        const description = prompt("Descripción:");
        const price = prompt("Precio:");
        const stock = prompt("Stock:");

        const priceNum = parseFloat(price);
        const stockNum = parseInt(stock);

        if (!name || isNaN(priceNum) || priceNum < 0 || isNaN(stockNum) || stockNum < 0) {
            alert("Datos inválidos. Revisa nombre, precio y stock.");
            return;
        }

        createProduct({ name, description, price: priceNum, stock: stockNum });
    });

    // B. G. L. 25/08/2025 Cargar todo al inicio
    loadProducts();
});
