// B. G. L. 27/08/2025 CRUD Productos

document.addEventListener("DOMContentLoaded", () => {
    const tableBody = document.querySelector("#products-table tbody");
    const btnNewProduct = document.getElementById("btn-new-product");

    // B. G. L. 27/08/2025 Cargar productos al inicio
    async function loadProducts() {
        tableBody.innerHTML = "";
        const res = await fetch("/products");
        const products = await res.json();
        
        products.forEach(p => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${p.id}</td>
                <td>${p.name}</td>
                <td>${p.description}</td>
                <td>${p.price}</td>
                <td>${p.stock}</td>
                <td>-</td> <!-- Aquí luego ponemos el vendedor -->
                <td>
                    <button class="btn-view" data-id="${p.id}">Ver</button>
                    <button class="btn-edit" data-id="${p.id}">Editar</button>
                    <button class="btn-delete" data-id="${p.id}">Eliminar</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }

    // B. G. L. 27/08/2025 Crear producto
    async function createProduct(product) {
        await fetch("/products", {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(product)
        });
        loadProducts();
    }

    // B. G. L. 27/08/2025 Editar producto
    async function editProduct(id, product) {
        await fetch(`/products/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(product)
        });
        loadProducts();
    }

    // B. G. L. 27/08/2025 Eliminar producto
    async function deleteProduct(id) {
        await fetch(`/products/${id}`, { method: "DELETE" });
        loadProducts();
    }

    // B. G. L. 27/08/2025 Eventos de botones
    tableBody.addEventListener("click", e => {
        if (e.target.classList.contains("btn-delete")) {
            const id = e.target.dataset.id;
            if (confirm("¿Seguro que quieres eliminar este producto?")) {
                deleteProduct(id);
            }
        }

        if(e.target.classList.contains("btn-edit")) {
            const id = e.target.dataset.id;
            const name = prompt("Nuevo nombre del producto:");
            const description = prompt("Nueva descripción:");
            const price = prompt("Nuevo precio:");
            const stock = prompt("Nuevo stock:");
            if (name && price) {
                editProduct(id, {name, description, price, stock});
            }
        }

        if (e.target.classList.contains("btn-view")) {
            const id = e.target.dataset.id;
            fetch(`/products/${id}`)
                .then(res => res.json())
                .then(p => alert(`Producto:\n${p.name}\n${p.description}\nPrecio: ${p.price}\nStock: ${p.stock}`));
        }
    });

    // B. G. L. 27/08/2025 Boton nuevo producto
    btnNewProduct.addEventListener("click", () => {
        const name = prompt("Nombre del producto:");
        const description = prompt("Descripción:");
        const price = prompt("Precio:");
        const stock = prompt("Stock:");
        if (name && price) {
            createProduct({ name, description, price, stock });
        }
    });

    // B. G. L. 27/08/2025 Cargar todo al inicio
    loadProducts()
});