const statusLabels = {
  foundation: "Base lista",
  reference: "Referencia",
  disconnected: "Desconectado",
  planned: "Planeado",
};

async function request(path, options) {
  const response = await fetch(path, options);
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || `HTTP ${response.status}`);
  return body;
}

function renderModules(modules) {
  const grid = document.querySelector("#module-grid");
  grid.replaceChildren(...modules.map((module, index) => {
    const card = document.createElement("article");
    card.className = "module-card";
    const icon = document.createElement("div");
    icon.className = `module-icon icon-${index % 6}`;
    icon.textContent = ["◈", "⌘", "▤", "✳", "☁", "◇"][index % 6];
    const heading = document.createElement("div");
    heading.className = "module-title-row";
    const title = document.createElement("h3");
    title.textContent = module.name;
    const badge = document.createElement("span");
    badge.className = `module-status status-${module.status}`;
    badge.textContent = statusLabels[module.status] || module.status;
    heading.append(title, badge);
    const description = document.createElement("p");
    description.textContent = module.description;
    card.append(icon, heading, description);
    return card;
  }));
}

function renderJobs(jobs) {
  const list = document.querySelector("#activity-list");
  document.querySelector("#job-count").textContent = `${jobs.length} ${jobs.length === 1 ? "ejecución" : "ejecuciones"}`;
  if (!jobs.length) {
    list.innerHTML = '<p class="empty-state">Aún no hay ejecuciones. Prueba el diagnóstico para ver el proceso y sus resultados.</p>';
    return;
  }
  list.replaceChildren(...jobs.map((job) => {
    const item = document.createElement("article");
    item.className = "job-item";
    const marker = document.createElement("span");
    marker.className = "job-marker";
    marker.textContent = "✓";
    const content = document.createElement("div");
    content.className = "job-content";
    const title = document.createElement("strong");
    title.textContent = `Diagnóstico completado · ${new Date(job.created_at).toLocaleString()}`;
    const note = document.createElement("p");
    note.textContent = job.note;
    const steps = document.createElement("ol");
    steps.className = "job-steps";
    for (const step of job.steps) {
      const li = document.createElement("li");
      li.textContent = `${step.name}: ${step.result}`;
      steps.append(li);
    }
    content.append(title, note, steps);
    item.append(marker, content);
    return item;
  }));
}

function showToast(message) {
  const toast = document.querySelector("#toast");
  toast.textContent = message;
  toast.classList.add("visible");
  window.setTimeout(() => toast.classList.remove("visible"), 2800);
}

async function refresh() {
  try {
    const [health, modules, jobs] = await Promise.all([
      request("/api/health"), request("/api/modules"), request("/api/jobs"),
    ]);
    document.querySelector("#service-status").textContent = health.status === "ok" ? "Control en línea" : "Sin conexión";
    renderModules(modules.modules);
    renderJobs(jobs.jobs);
  } catch (error) {
    document.querySelector("#service-status").textContent = "Error de conexión";
    document.querySelector("#module-grid").textContent = `No se pudieron cargar los módulos: ${error.message}`;
  }
}

document.querySelector("#run-diagnostic").addEventListener("click", async (event) => {
  const button = event.currentTarget;
  button.disabled = true;
  button.textContent = "Ejecutando flujo…";
  try {
    await request("/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "diagnostic" }),
    });
    await refresh();
    showToast("Flujo de prueba completado. No se consultaron datos externos.");
  } catch (error) {
    showToast(`No se pudo ejecutar: ${error.message}`);
  } finally {
    button.disabled = false;
    button.innerHTML = 'Ejecutar diagnóstico de prueba <span>→</span>';
  }
});

refresh();
