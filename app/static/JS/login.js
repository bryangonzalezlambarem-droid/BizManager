document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const errorDiv = document.getElementById("login-error");
    const submitBtn = form.querySelector('button[type="submit"]');
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const originalBtnText = submitBtn.textContent;

    //  B. G. L 03/09/2025 Deshabilitar boton inicialmente
    submitBtn.disabled = true;
    submitBtn.style.opacity = "0.7";
    submitBtn.style.cursor = "not-allowed";

    // B. G. L 03/09/2025 Funcion para validar email en tiempo real (solo verifica @)
    function validateEmailRealTime(email) {
        return email.includes('@') && email.length > 3;
    }

    // B. G. L 03/09/2025 Funcion para validar formulario en tiempo real
    function validateFormRealTime() {
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        
        const isEmailValid = validateEmailRealTime(email);
        const isPasswordValid = password.length >= 1; // B. G. L 03/09/2025 Al menos 1 caracter

        if (isEmailValid && isPasswordValid) {
            submitBtn.disabled = false;
            submitBtn.style.opacity = "1";
            submitBtn.style.cursor = "pointer";
        } else {
            submitBtn.disabled = true;
            submitBtn.style.opacity = "0.7";
            submitBtn.style.cursor = "not-allowed";
        }
    }

    // B. G. L 03/09/2025 Event listeners para validacion en tiempo real
    emailInput.addEventListener('input', validateFormRealTime);
    passwordInput.addEventListener('input', validateFormRealTime);

    // B. G. L 03/09/2025 Validar al cargar la pagina (por si hay valores autocompletados)
    validateFormRealTime();

    // B. G. L 03/09/2025 Funcion para mostrar errores
    function showError(message) {
        console.log("Mostrando error:", message);
        errorDiv.textContent = message;
        errorDiv.style.display = "block";
        errorDiv.classList.add("alert", "alert-danger");
        
        // B. G. L 03/09/2025 Ocultar error despues de 5 segundos
        setTimeout(() => {
            errorDiv.style.display = "none";
        }, 5000);
    }

    // B. G. L 03/09/2025 Funcion para mostrar carga
    function setLoading(isLoading) {
        if (isLoading) {
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Iniciando sesión...';
        } else {
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
            // B. G. L 03/09/2025 Restaurar el estado del boton segun validacion
            validateFormRealTime();
        }
    }

    // B. G. L 03/09/2025 Validacion completa del formulario (mas estricta)
    function validateForm(email, password) {
        email = email.trim();
        password = password.trim();

        if (!email) {
            showError("Por favor, ingresa tu email");
            return false;
        }
        
        if (!password) {
            showError("Por favor, ingresa tu contraseña");
            return false;
        }

        // B. G. L 03/09/2025 Validacion mas robusta de email
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        
        if (!emailRegex.test(email)) {
            showError("Por favor, ingresa un email válido (ej: usuario@dominio.com)");
            return false;
        }

        return true;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // B. G. L 03/09/2025 Limpiar error anterior
        errorDiv.style.display = "none";

        // B. G. L 03/09/2025 Validar formulario (validacion completa)
        if (!validateForm(email, password)) {
            return;
        }

        setLoading(true);

        try {
            const res = await fetch("/auth/login", {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                credentials: "same-origin",
                body: JSON.stringify({ email, password })
            });

            const data = await res.json();
            localStorage.setItem("token", data.token); // 🔑 guardar token

            if (!res.ok) {
                throw new Error(data.error || "Error al iniciar sesión");
            }

            // B. G. L 03/09/2025 Login exitoso - redirigir al dashboard
            errorDiv.textContent = "¡Login exitoso! Redirigiendo...";
            errorDiv.style.display = "block";
            errorDiv.classList.remove("alert-danger");
            errorDiv.classList.add("alert-success");
            
            setTimeout(() => {
                window.location.href = "/";
            }, 1000);

        } catch (err) {
            // B. G. L 03/09/2025 Manejar diferentes tipos de errores
            if (err.name === 'TypeError' || err.message.includes('Failed to fetch')) {
                showError("Error de conexión. Verifica tu internet.");
            } else {
                showError(err.message);
            }
        } finally {
            setLoading(false);
        }
    });

    // B. G. L 03/09/2025 Limpiar error cuando el usuario empiece a escribir
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            errorDiv.style.display = 'none';
            // B. G. L 03/09/2025 Mantener la validacion en tiempo real
            validateFormRealTime();
        });
    });

    // B. G. L 03/09/2025 Tambien validar cuando se pierde el foco (blur)
    emailInput.addEventListener('blur', validateFormRealTime);
    passwordInput.addEventListener('blur', validateFormRealTime);
});