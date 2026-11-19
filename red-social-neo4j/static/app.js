const $ = (s) => document.querySelector(s);
let editandoId = null;

async function api(ruta, opciones = {}) {
  const resp = await fetch(`/api${ruta}`, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  if (resp.status === 204) return null;
  const cuerpo = await resp.json();
  if (!resp.ok) {
    const detalle = cuerpo.detalle ? ": " + cuerpo.detalle.map((d) => d.msg).join(", ") : "";
    throw new Error(cuerpo.error + detalle);
  }
  return cuerpo;
}

function avisar(texto, esError = false) {
  const estado = $("#estado");
  estado.textContent = texto;
  estado.classList.toggle("error", esError);
}

async function intentar(accion) {
  try { await accion(); } catch (e) { avisar(e.message, true); }
}

function celda(texto) {
  const td = document.createElement("td");
  td.textContent = texto;
  return td;
}

function boton(texto, clase, onClick) {
  const b = document.createElement("button");
  b.textContent = texto;
  if (clase) b.className = clase;
  b.addEventListener("click", () => intentar(onClick));
  return b;
}

function llenarSelect(select, personas) {
  const previo = select.value;
  select.replaceChildren(...personas.map((p) => new Option(p.nombre, p.id)));
  if (personas.some((p) => p.id === previo)) select.value = previo;
}

async function cargarPersonas() {
  const personas = await api("/personas");
  const tbody = $("#tabla-personas");
  tbody.replaceChildren(...personas.map((p) => {
    const tr = document.createElement("tr");
    const acciones = document.createElement("td");
    acciones.append(
      boton("Editar", "sec", async () => editar(p)),
      boton("Eliminar", "peligro", async () => {
        if (!confirm(`¿Eliminar a ${p.nombre} y todas sus conexiones?`)) return;
        await api(`/personas/${p.id}`, { method: "DELETE" });
        avisar(`Se eliminó a ${p.nombre}`);
        await cargarPersonas();
      }),
    );
    tr.append(celda(p.nombre), celda(p.edad), celda(p.ciudad), celda(p.intereses.join(", ")), acciones);
    return tr;
  }));
  for (const sel of ["#sel-persona", "#sel-destino", "[name=persona_a_id]", "[name=persona_b_id]"]) {
    llenarSelect($(sel), personas);
  }
}

function editar(p) {
  editandoId = p.id;
  const f = $("#form-persona");
  f.nombre.value = p.nombre; f.edad.value = p.edad; f.ciudad.value = p.ciudad;
  f.intereses.value = p.intereses.join(", "); f.intereses.disabled = true;
  $("#titulo-form").textContent = "Editar persona";
  $("#btn-guardar").textContent = "Guardar";
  $("#btn-cancelar").hidden = false;
}

function salirDeEdicion() {
  editandoId = null;
  const f = $("#form-persona");
  f.reset(); f.intereses.disabled = false;
  $("#titulo-form").textContent = "Nueva persona";
  $("#btn-guardar").textContent = "Crear";
  $("#btn-cancelar").hidden = true;
}

$("#btn-cancelar").addEventListener("click", salirDeEdicion);

$("#form-persona").addEventListener("submit", (ev) => {
  ev.preventDefault();
  intentar(async () => {
    const f = ev.target;
    const datos = { nombre: f.nombre.value, edad: Number(f.edad.value), ciudad: f.ciudad.value };
    if (editandoId) {
      await api(`/personas/${editandoId}`, { method: "PUT", body: JSON.stringify(datos) });
      avisar("Persona actualizada");
    } else {
      datos.intereses = f.intereses.value.split(",").map((s) => s.trim()).filter(Boolean);
      await api("/personas", { method: "POST", body: JSON.stringify(datos) });
      avisar("Persona creada");
    }
    salirDeEdicion();
    await cargarPersonas();
  });
});

$("#form-amistad").addEventListener("submit", (ev) => {
  ev.preventDefault();
  intentar(async () => {
    const f = ev.target;
    const r = await api("/amistades", {
      method: "POST",
      body: JSON.stringify({ persona_a_id: f.persona_a_id.value, persona_b_id: f.persona_b_id.value }),
    });
    avisar(`Ahora ${r.persona_a} y ${r.persona_b} son amigos`);
  });
});

function mostrar(titulo, datos) {
  avisar(titulo);
  $("#resultado").textContent = JSON.stringify(datos, null, 2);
}

document.querySelectorAll("button[data-q]").forEach((b) => b.addEventListener("click", () => intentar(async () => {
  const id = $("#sel-persona").value;
  mostrar(b.textContent, await api(`/personas/${id}/${b.dataset.q}`));
})));

$("#btn-camino").addEventListener("click", () => intentar(async () => {
  const desde = $("#sel-persona").value, hasta = $("#sel-destino").value;
  mostrar("Camino más corto", await api(`/camino?desde=${encodeURIComponent(desde)}&hasta=${encodeURIComponent(hasta)}`));
}));

$("#btn-populares").addEventListener("click", () => intentar(async () => {
  mostrar("Más conectadas", await api("/populares"));
}));

intentar(cargarPersonas);
