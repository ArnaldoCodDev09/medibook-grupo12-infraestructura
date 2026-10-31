const form = document.querySelector('#appointment-form');
const statusNode = document.querySelector('#status');
const listNode = document.querySelector('#appointment-list');
const submitButton = document.querySelector('#submit-button');
let apiBaseUrl = '';

async function loadConfig() {
  const response = await fetch('./config.json', { cache: 'no-store' });
  const config = await response.json();
  apiBaseUrl = (config.apiBaseUrl || '').replace(/\/$/, '');
  if (!apiBaseUrl) throw new Error('Falta configurar la URL de la API.');
}

function showMessage(message, type = '') {
  statusNode.textContent = message;
  statusNode.className = `status ${type}`;
}

function renderAppointments(appointments) {
  listNode.replaceChildren();
  if (!appointments.length) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = 'Todavía no hay reservas de demostración.';
    listNode.append(empty);
    return;
  }
  for (const item of appointments) {
    const card = document.createElement('article');
    card.className = 'appointment';
    const name = document.createElement('strong');
    name.textContent = item.patient_name || 'Paciente de prueba';
    const specialty = document.createElement('span');
    specialty.textContent = `${item.specialty} · ${item.doctor}`;
    const time = document.createElement('time');
    time.textContent = `${item.date} · ${item.time}`;
    card.append(name, specialty, time);
    listNode.append(card);
  }
}

async function refreshAppointments() {
  if (!apiBaseUrl) return;
  listNode.innerHTML = '<p class="empty">Cargando agenda…</p>';
  try {
    const response = await fetch(`${apiBaseUrl}/appointments`);
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || 'No se pudo consultar la agenda.');
    renderAppointments(body.appointments || []);
  } catch (error) {
    listNode.innerHTML = '<p class="empty">No se pudo cargar la agenda. Revisa que la API esté disponible.</p>';
  }
}

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  submitButton.disabled = true;
  showMessage('Guardando la cita…');
  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());
  try {
    const response = await fetch(`${apiBaseUrl}/appointments`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || 'No se pudo registrar la cita.');
    form.reset();
    showMessage('Cita de prueba registrada. No uses datos reales.', 'success');
    await refreshAppointments();
  } catch (error) {
    showMessage(error.message, 'error');
  } finally {
    submitButton.disabled = false;
  }
});

document.querySelector('#refresh').addEventListener('click', refreshAppointments);
loadConfig().then(refreshAppointments).catch((error) => {
  showMessage(error.message, 'error');
  listNode.innerHTML = '<p class="empty">La página todavía no está conectada a la API.</p>';
});

