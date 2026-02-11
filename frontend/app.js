async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`요청 실패: ${url}`);
  }
  return response.json();
}

function renderList(elementId, items, formatter) {
  const el = document.getElementById(elementId);
  el.innerHTML = "";

  if (!items.length) {
    const li = document.createElement("li");
    li.className = "muted";
    li.textContent = "데이터가 없습니다.";
    el.appendChild(li);
    return;
  }

  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = formatter(item);
    el.appendChild(li);
  });
}

async function loadDashboard() {
  const healthEl = document.getElementById("health");

  try {
    const [health, stack, files] = await Promise.all([
      fetchJson("/api/health"),
      fetchJson("/api/stack"),
      fetchJson("/api/files"),
    ]);

    healthEl.textContent = `상태: ${health.status}`;

    renderList(
      "stack-list",
      stack,
      (item) => `[${item.category}] ${item.name} - ${item.description}`,
    );

    renderList("files-list", files.python_files, (name) => name);
  } catch (error) {
    healthEl.textContent = "상태 확인 실패";
    healthEl.classList.add("muted");
  }
}

loadDashboard();
