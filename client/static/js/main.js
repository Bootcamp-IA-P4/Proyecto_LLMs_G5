function getToken() {
    return localStorage.getItem("access_token");
}
if (window.location.pathname === "/" && !getToken()) {
    window.location.href = "/login";
}
// Login
if (document.getElementById("loginForm")) {
    document.getElementById("loginForm").onsubmit = async function(e) {
        e.preventDefault();
        document.getElementById("loginError").innerText = "";
        try {
            const email = this.email.value;
            const password = this.password.value;
            const res = await fetch("/api/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "/";
            } else {
                document.getElementById("loginError").innerText = data.detail || "Error de login";
            }
        } catch (err) {
            document.getElementById("loginError").innerText = "Error de red";
        }
    };
}

// Registro
if (document.getElementById("registerForm")) {
    document.getElementById("registerForm").onsubmit = async function(e) {
        e.preventDefault();
        document.getElementById("registerError").innerText = "";
        try {
            const email = this.email.value;
            const password = this.password.value;
            const res = await fetch("/api/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (res.ok) {
                localStorage.setItem("access_token", data.access_token);
                window.location.href = "/";
            } else {
                document.getElementById("registerError").innerText = data.detail || "Error de registro";
            }
        } catch (err) {
            document.getElementById("registerError").innerText = "Error de red";
        }
    };
}

// Generar contenido
if (document.getElementById("contentForm")) {
    document.getElementById("contentForm").onsubmit = async function(e) {
        e.preventDefault();
        document.getElementById("result").innerHTML = "";
        try {
            const formData = new FormData(this);
            const payload = {
                topic: formData.get("topic"),
                platform: formData.get("platform"),
                audience: formData.get("audience"),
                language: formData.get("language"),
                model: formData.get("model"),
            };
            if (formData.get("company_info")) {
                payload.company_info = formData.get("company_info");
            }

            const res = await fetch("/api/content/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + getToken()
                },
                body: JSON.stringify(payload)
            });

            const data = await res.json();
            if (res.ok) {
                let content = data.text_content;
                const selectedPlatform = formData.get("platform");

                // Si es blog, formateamos mejor el contenido
                if (selectedPlatform === "blog") {
                    content = content
                        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
                        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                        .replace(/\n{2,}/g, '</p><p>')
                        .replace(/\n/g, '<br>');
                    content = `<div class="blog-content"><p>${content}</p></div>`;
                } else {
                    content = `<p>${content}</p>`;
                }

                document.getElementById("result").innerHTML = `<h3>Resultado:</h3>${content}`;
                document.getElementById("actionsBtns").style.display = "flex";
                showResetBtn(true);
            } else {
                document.getElementById("result").innerHTML = `<span class="error">${data.detail || "Error generando contenido"}</span>`;
                document.getElementById("actionsBtns").style.display = "none";
                showResetBtn(false);
            }
        } catch (err) {
            document.getElementById("result").innerHTML = `<span class="error">Error de red</span>`;
            document.getElementById("actionsBtns").style.display = "none";
            showResetBtn(false);
        }
    };
}

// Logout
if (document.getElementById("logoutBtn")) {
    document.getElementById("logoutBtn").onclick = function() {
        localStorage.removeItem("access_token");
        window.location.href = "/login";
    };
}

// Copiar contenido al portapapeles
if (document.getElementById("copyBtn")) {
    document.getElementById("copyBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
        // Extrae solo el texto, sin etiquetas HTML
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        navigator.clipboard.writeText(text)
            .then(() => alert("¡Contenido copiado al portapapeles!"))
            .catch(() => alert("No se pudo copiar el contenido."));
    };
}

// Exportar como .md
if (document.getElementById("exportMdBtn")) {
    document.getElementById("exportMdBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
        // Extrae solo el texto, sin etiquetas HTML
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        const blob = new Blob([text], { type: "text/markdown" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "contenido.md";
        link.click();
    };
}

// Exportar como .txt
if (document.getElementById("exportTxtBtn")) {
    document.getElementById("exportTxtBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
        // Extrae solo el texto, sin etiquetas HTML
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        const blob = new Blob([text], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "contenido.txt";
        link.click();
    };
}
// Mostrar el botón de reset solo cuando hay resultado
function showResetBtn(show) {
    const btn = document.getElementById("resetBtn");
    if (btn) btn.style.display = show ? "block" : "none";
}
// Botón de reset para hacer otra petición
if (document.getElementById("resetBtn")) {
    document.getElementById("resetBtn").onclick = function() {
        document.getElementById("contentForm").reset();
        document.getElementById("result").innerHTML = "";
        document.getElementById("actionsBtns").style.display = "none";
        this.style.display = "none";
    };
}

