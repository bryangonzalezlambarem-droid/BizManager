// B. G. L. 27/08/2025 CRUD Productos

document.addEventListener("DOMContentLoaded", () => {
    const formContainer = document.getElementById("product-form-container");
    const form = document.getElementById("product-form");
    const formTitle = document.getElementById("product-form-title");
    const productIdField = document.getElementById("product-id");
    const nameField = document.getElementById("product-name");
    const descriptionField = document.getElementById("product-description");
    const priceField = document.getElementById("product-price");
    const stockField = document.getElementById("product-stock");
    const errorContainer = document.getElementById("product-error-container");
    const successContainer = document.getElementById("product-success-container");

    const tableBody = document.querySelector("#products-table tbody");
    const btnNewProduct = document.getElementById("btn-new-product");
    const btnCancelProduct = document.getElementById("product-cancel-btn");

    const token = localStorage.getItem("token"); // B. G. L. 05/09/2025 Recuperar token guardado en login

    // B. G. L. 25/08/2025 Cargar productos al inicio
    async function loadProducts() {
        try {
            tableBody.innerHTML = "";
            const res = await fetch("/api/products", {
                headers: { "Authorization": `Bearer ${token}` }
            });
            if (!res.ok) throw new Error("Error al cargar productos");
            const products = await res.json();
            
            products.forEach(p => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${p.product_id}</td> 
                    <td>${p.name}</td>
                    <td>${p.description}</td>
                    <td>${p.price}</td>
                    <td>${p.stock}</td>
                    <td>${p.salesman_id}</td>
                    <td>
                        <button class="btn-view" data-id="${p.product_id}">Ver</button>
                        <button class="btn-edit" data-id="${p.product_id}">Editar</button>
                        <button class="btn-delete" data-id="${p.product_id}">Eliminar</button>
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
            const res = await fetch("/api/products/", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
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

    // B. G. L. 25/08/2025 Eliminar producto
    async function deleteProduct(id) {
        try {
            const res = await fetch(`/api/products/${id}`, { 
                method: "DELETE",
                headers: { "Authorization": `Bearer ${token}` }
            });
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

        if (e.target.classList.contains("btn-edit")) {
            editProductForm(id);
        }

        if (e.target.classList.contains("btn-view")) {
            fetch(`/api/products/${id}`, {
                headers: { "Authorization": `Bearer ${token}` }
            })
                .then(res => {
                    if (!res.ok) {
                        throw new Error(`Error ${res.status}: Producto no encontrado`);
                    }
                    return res.json();
                })
                .then(p => {
                    alert(`Producto:\nNombre: ${p.name}\nDescripción: ${p.description}\nPrecio: ${p.price}\nStock: ${p.stock}`);
                })
                .catch(err => {
                    console.error(err);
                    alert(err.message);
                });
        }
    });

    // B. G. L. 25/08/2025 Boton nuevo producto
    btnNewProduct.addEventListener("click", () => {
        form.reset();
        productIdField.value = "";
        formTitle.textContent = "Nuevo Producto";
        formContainer.style.display = "block";
        errorContainer.style.display = "none";
        successContainer.style.display = "none";
    });

    btnCancelProduct.addEventListener("click", () => {
        formContainer.style.display = "none";  
        form.reset();                          
        errorContainer.style.display = "none"; 
        successContainer.style.display = "none"; 
    });

    function showMessage(container, message) {
        container.textContent = message;
        container.style.display = "block";
        setTimeout(() => container.style.display = "none", 5000);
    }

    function editProductForm(id) {
        fetch(`/api/products/${id}`, {
            headers: { "Authorization": `Bearer ${token}` }
        })
            .then(res => res.json())
            .then(p => {
                productIdField.value = p.product_id;
                nameField.value = p.name;
                descriptionField.value = p.description;
                priceField.value = p.price;
                stockField.value = p.stock;
                formTitle.textContent = "Editar Producto";
                formContainer.style.display = "block";
                errorContainer.style.display = "none";
            })
            .catch(err => showMessage(errorContainer, "Error al cargar producto: " + err.message));
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const id = productIdField.value;
        const data = {
            name: nameField.value.trim(),
            description: descriptionField.value.trim(),
            price: parseFloat(priceField.value),
            stock: parseInt(stockField.value)
        };
        const url = id ? `/api/products/${id}` : "/api/products/";
        const method = id ? "PUT" : "POST";

        try {
            console.log("DEBUG submit data:", data); // B. G. L. 05/09/2025
            console.log("DEBUG URL:", url, "Method:", method); // B. G. L. 05/09/2025
            console.log("DEBUG Token usado:", token); // B. G. L. 05/09/2025

            const res = await fetch(url, {
                method,
                headers: { 
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(data)
            });

            const resp = await res.json();
            if (!res.ok) throw new Error(resp.error || "Error interno");
            showMessage(successContainer, resp.message || "Operación realizada correctamente");
            formContainer.style.display = "none";
            loadProducts();
        } catch (err) {
            console.error("DEBUG Error en submit:", err); // 👀
            showMessage(errorContainer, err.message);
        }
    });


    // B. G. L. 25/08/2025 Cargar todo al inicio
    loadProducts();
});
