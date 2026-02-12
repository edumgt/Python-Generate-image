async function fetchJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `요청 실패: ${url}`);
  }
  return response.json();
}

function toggleModeUI(outputType) {
  const imageFields = document.querySelectorAll('.image-only');
  const videoFields = document.querySelectorAll('.video-only');
  const isImage = outputType === 'image';

  imageFields.forEach((field) => field.classList.toggle('hidden', !isImage));
  videoFields.forEach((field) => field.classList.toggle('hidden', isImage));
}

async function initializeForm() {
  const data = await fetchJson('/api/options');
  const modelSelect = document.getElementById('model-id');

  modelSelect.innerHTML = '';
  data.models.forEach((modelId) => {
    const option = document.createElement('option');
    option.value = modelId;
    option.textContent = modelId;
    modelSelect.appendChild(option);
  });
}

function readPayload() {
  const outputType = document.getElementById('output-type').value;
  return {
    model_id: document.getElementById('model-id').value,
    output_type: outputType,
    width: Number(document.getElementById('width').value),
    height: Number(document.getElementById('height').value),
    video_size: document.getElementById('video-size').value,
    prompt: document.getElementById('prompt').value.trim(),
  };
}

async function generate(event) {
  event.preventDefault();

  const statusEl = document.getElementById('status');
  const resultImage = document.getElementById('result-image');
  const button = document.getElementById('submit-button');

  const payload = readPayload();

  if (!payload.prompt) {
    statusEl.textContent = '프롬프트를 입력해 주세요.';
    return;
  }

  button.disabled = true;
  statusEl.textContent = '생성 중...';

  try {
    const data = await fetchJson('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    resultImage.src = `${data.file_url}?t=${Date.now()}`;
    resultImage.classList.remove('hidden');
    statusEl.textContent = `완료: ${data.model_id} / ${data.width}x${data.height}`;
  } catch (error) {
    statusEl.textContent = `실패: ${error.message}`;
  } finally {
    button.disabled = false;
  }
}

async function boot() {
  const outputTypeEl = document.getElementById('output-type');
  outputTypeEl.addEventListener('change', (event) => toggleModeUI(event.target.value));

  try {
    await initializeForm();
  } catch (error) {
    const statusEl = document.getElementById('status');
    statusEl.textContent = '초기 데이터 로드 실패';
    statusEl.classList.add('muted');
  }

  toggleModeUI(outputTypeEl.value);
  document.getElementById('generate-form').addEventListener('submit', generate);
}

boot();
