document.addEventListener("DOMContentLoaded", function() {
    // ...todo tu código JS aquí...
//const { Debug } = require("@prisma/client/runtime/library");

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
            alert("Voy a imprimir el token");
            console.log("Token enviado:", getToken());
            console.log("Cabeceras:", {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + getToken()
            });
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
                document.getElementById("result").innerHTML = `<h3>Resultado:</h3><p>${data.text_content}</p>`;
                document.getElementById("imagen").src = data.image_url;
            } else {
                document.getElementById("result").innerHTML = `<span class="error">${data.detail || "Error generando contenido"}</span>`;
            }
        } catch (err) {
            document.getElementById("result").innerHTML = `<span class="error">Error de red</span>`;
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

});