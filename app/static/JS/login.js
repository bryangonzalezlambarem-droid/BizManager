document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const errorDiv = document.getElementById("login-error");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const data = {
        email: document.getElementById("email").value.trim(),
        password: document.getElementById("password").value.trim()
        };

        try {
        const res = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "same-origin",
            body: JSON.stringify(data)
        });

        const resp = await res.json();
        if (!res.ok) throw new Error(resp.error || "Error al iniciar sesión");

        // # B. G. L. 04/09/2025 Cookie HttpOnly ya quedo guardada -> podemos navegar
        window.location.href = "/";
        } catch (err) {
        errorDiv.textContent = err.message;
        errorDiv.style.display = "block";
        }
    });
});
