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
            payload.include_image = document.getElementById("include_image").checked;
            const imagePromptValue = document.getElementById("image_prompt").value;
            if (imagePromptValue) {
                payload.image_prompt = imagePromptValue;
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

                // Formateamos mejor el contenido para las generaciones de blog
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
                // Mostrar la imagen 
                const imageDiv = document.getElementById('image-result');
                if (data.image_url) {
                    imageDiv.innerHTML = `<img src="${data.image_url}" alt="Imagen generada" class="generated-image">`;
                } else {
                    imageDiv.innerHTML = ""; 
                }
                document.getElementById("actionsBtns").style.display = "flex";
                showResetBtn(true);
            } else {
                document.getElementById("result").innerHTML = `<span class="error">${data.detail || "Error generando contenido"}</span>`;
                document.getElementById("actionsBtns").style.display = "none";
                showResetBtn(false);
            }
        } catch (err) {
            document.getElementById("loader").style.display = "none";
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

// Podemos copiar contenido al portapapeles
if (document.getElementById("copyBtn")) {
    document.getElementById("copyBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        navigator.clipboard.writeText(text)
            .then(() => alert("¡Contenido copiado al portapapeles!"))
            .catch(() => alert("No se pudo copiar el contenido."));
    };
}

// Podemos exportar como .md
if (document.getElementById("exportMdBtn")) {
    document.getElementById("exportMdBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
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

// Podemos exportar como .txt
if (document.getElementById("exportTxtBtn")) {
    document.getElementById("exportTxtBtn").onclick = function() {
        const resultDiv = document.getElementById("result");
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

if (document.getElementById("fetchLogsBtn")) {
    document.getElementById("fetchLogsBtn").onclick = async function() {
        const output = document.getElementById("logsOutput");
        output.innerHTML = "Cargando logs...";

        try {
            const res = await fetch("/api/content/langsmith", {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + getToken(),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ limit: 10 })
            });

            const data = await res.json();
            if (res.ok && data.runs && data.runs.length > 0) {
                let html = `<table>
                    <thead>
                        <tr>
                            <th>Fecha</th>
                            <th>Modelo</th>
                            <th>Tipo</th>
                            <th>Topic</th>
                            <th>Input (prompt)</th>
                            <th>Output (respuesta generada)</th>
                            <th>Estado</th>
                            <th>Error</th>
                        </tr>
                    </thead>
                    <tbody>`;
                data.runs.forEach(run => {
                    let model = run.extra?.invocation_params?.ls_model_name || run.extra?.invocation_params?.model || "-";
                    let topic = run.inputs?.messages?.[0]?.[0]?.kwargs?.content?.match(/about: '([^']+)'/)?.[1]
                        || run.inputs?.topic
                        || "-";
                    let prompt = run.inputs?.messages?.[0]?.[0]?.kwargs?.content
                        || run.inputs?.topic
                        || JSON.stringify(run.inputs || {}, null, 2);
                    let output = "";
                    if (run.outputs?.generations?.[0]?.[0]?.text) {
                        output = run.outputs.generations[0][0].text;
                    } else if (run.outputs?.output?.content) {
                        output = run.outputs.output.content;
                    } else if (run.outputs?.output) {
                        output = JSON.stringify(run.outputs.output);
                    } else {
                        output = "-";
                    }
                    function truncate(str, n = 100) {
                        return (str && str.length > n) ? str.slice(0, n) + "..." : str;
                    }
                    html += `<tr>
                        <td>${run.start_time ? new Date(run.start_time).toLocaleString() : "-"}</td>
                        <td>${model}</td>
                        <td>${run.run_type || "-"}</td>
                        <td>${topic}</td>
                        <td class="log-prompt">${truncate(prompt, 100)}</td>
                        <td class="log-output">${truncate(output, 100)}</td>
                        <td class="${run.status === 'success' ? 'log-success' : 'log-error'}">${run.status || "-"}</td>
                        <td class="log-error">${run.error ? run.error.split('\n')[0].slice(0, 80) + "..." : ""}</td>
                    </tr>`;
                });
                html += "</tbody></table>";
                output.innerHTML = html;
            } else if (res.ok) {
                output.innerHTML = "<em>No hay logs recientes.</em>";
            } else {
                output.innerHTML = `<span class="log-error">Error: ${data.detail || res.status}</span>`;
            }
        } catch (err) {
            output.innerHTML = "<span class='log-error'>Error de red al cargar los logs.</span>";
        }
    };
}
if (document.getElementById("logsNavBtn")) {
    document.getElementById("logsNavBtn").onclick = function() {
        window.location.href = "/langsmith";
    };
}

const includeImageCheckbox = document.getElementById('include_image');
if (includeImageCheckbox) {
    includeImageCheckbox.addEventListener('change', function() {
        document.getElementById('imagePromptDiv').style.display = this.checked ? 'block' : 'none';
    });
}


// Generar artículo científico

if (document.getElementById("scienceNavBtn")) {
    document.getElementById("scienceNavBtn").onclick = function() {
        window.location.href = "/science";
    };
}

if (document.getElementById("scienceForm")) {
    document.getElementById("scienceForm").onsubmit = async function(e) {
        e.preventDefault();
        document.getElementById("scienceResult").innerHTML = "Generando...";
        const formData = new FormData(this);
        const payload = {
            topic: formData.get("topic"),
            audience: formData.get("audience"),
            language: formData.get("language"),
            model: formData.get("model"),
            max_docs: Number(formData.get("max_docs")) || 3
        };
        try {
            const res = await fetch("/api/science/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + getToken()
                },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            if (res.ok) {
                let html = `<div class="science-result"><h3>Artículo generado:</h3><div class="blog-content"><p>${data.text_content.replace(/\n/g, "<br>")}</p></div>`;
                html += `<div class="science-sources"><h4>Fuentes utilizadas:</h4><ul>`;
                data.sources.forEach(src => {
                    html += `<li>
                        <strong>${src.title}</strong> (${src.authors || "Sin autores"})<br>
                        <a href="${src.url}" target="_blank">Ver paper</a>
                        <br>Relevancia: ${src.relevance_score ? src.relevance_score.toFixed(2) : "-"}
                    </li>`;
                });
                html += `</ul></div></div>`;
                document.getElementById("scienceResult").innerHTML = html;
                document.getElementById("scienceActions").style.display = "flex";
            } else {
                document.getElementById("scienceResult").innerHTML = `<span class="error">${data.detail || "Error generando artículo"}</span>`;
                document.getElementById("scienceActions").style.display = "none";
            }
        } catch (err) {
            document.getElementById("scienceResult").innerHTML = `<span class="error">Error de red</span>`;
        }
    };
}
// Copiar contenido científico
if (document.getElementById("copyScienceBtn")) {
    document.getElementById("copyScienceBtn").onclick = function() {
        const resultDiv = document.getElementById("scienceResult");
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        navigator.clipboard.writeText(text)
            .then(() => alert("¡Contenido copiado al portapapeles!"))
            .catch(() => alert("No se pudo copiar el contenido."));
    };
}

// Exportar como .md
if (document.getElementById("exportScienceMdBtn")) {
    document.getElementById("exportScienceMdBtn").onclick = function() {
        const resultDiv = document.getElementById("scienceResult");
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        const blob = new Blob([text], { type: "text/markdown" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "articulo_cientifico.md";
        link.click();
    };
}

// Exportar como .txt
if (document.getElementById("exportScienceTxtBtn")) {
    document.getElementById("exportScienceTxtBtn").onclick = function() {
        const resultDiv = document.getElementById("scienceResult");
        const tempElement = document.createElement("div");
        tempElement.innerHTML = resultDiv.innerHTML;
        const text = tempElement.innerText;
        const blob = new Blob([text], { type: "text/plain" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "articulo_cientifico.txt";
        link.click();
    };
}