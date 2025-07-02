const API_URL = 'http://localhost:8000/actividades';

document.addEventListener('DOMContentLoaded', fetchActividades);

const form = document.getElementById('activityForm');
const tableBody = document.getElementById('tableBody');
let editingId = null;

// Crear o actualizar
form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const data = {
    cultivo: form.cultivo.value,
    tarea: form.tarea.value,
    fecha: form.fecha.value,
    estado: form.estado.value,
    descripcion: form.descripcion.value,
  };

  const method = editingId ? 'PUT' : 'POST';
  const url = editingId ? `${API_URL}/${editingId}` : API_URL;

  const res = await fetch(url, {
    method: method,
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  if (res.ok) {
    form.reset();
    closeModal();
    fetchActividades();
    editingId = null;
  }
});

// Leer y mostrar
async function fetchActividades() {
  const res = await fetch(API_URL);
  const actividades = await res.json();
  tableBody.innerHTML = '';

  actividades.forEach(act => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${act.cultivo}</td>
      <td>${act.tarea}</td>
      <td>${act.fecha}</td>
      <td><span class="status ${act.estado}">${act.estado}</span></td>
      <td>${act.descripcion}</td>
      <td class="action-buttons">
        <button class="btn btn-edit" onclick="editActividad(${act.id})">Editar</button>
        <button class="btn btn-delete" onclick="deleteActividad(${act.id})">Eliminar</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// Eliminar
async function deleteActividad(id) {
  if (confirm('¿Eliminar esta actividad?')) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    fetchActividades();
  }
}

// Editar
async function editActividad(id) {
  const res = await fetch(`${API_URL}/${id}`);
  const act = await res.json();

  form.cultivo.value = act.cultivo;
  form.tarea.value = act.tarea;
  form.fecha.value = act.fecha;
  form.estado.value = act.estado;
  form.descripcion.value = act.descripcion;

  editingId = act.id;
  openModal();
}

// Búsqueda
document.getElementById('searchInput').addEventListener('input', function () {
  const filter = this.value.toLowerCase();
  document.querySelectorAll('#tableBody tr').forEach(row => {
    const match = [...row.children].some(td => td.textContent.toLowerCase().includes(filter));
    row.style.display = match ? '' : 'none';
  });
});

// Modal
function openModal() {
  document.getElementById('modal').style.display = 'block';
}
function closeModal() {
  document.getElementById('modal').style.display = 'none';
}

