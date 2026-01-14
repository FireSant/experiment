function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Registro de Entrenamiento')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

function obtenerCatalogoCompleto() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  // Buscamos la hoja "Catalogo" ignorando espacios accidentales
  const hojas = ss.getSheets();
  const hoja = hojas.find(h => h.getName().trim() === "Catalogo");
  
  if (!hoja) return [];
  const datos = hoja.getDataRange().getValues();
  return datos.slice(1).map(fila => ({
    nombre: fila[1], 
    tipo: fila[2], 
    zona: fila[4] || "Otros"
  }));
}

function guardarTodo(datos) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const hojas = ss.getSheets();

    // 1. Vinculación robusta de hojas
    const hojaSesion = hojas.find(h => h.getName().trim() === "Sesion_Entrenamiento");
    const hojaGim = hojas.find(h => h.getName().trim() === "Registros_Gimnasio");
    const hojaPista = hojas.find(h => h.getName().trim() === "Registros_Pista");

    if (!hojaSesion || !hojaGim || !hojaPista) throw new Error("Faltan pestañas en el Excel.");

    // 2. Generar ID de Sesión (Nivel 1)
    const idSesion = datos.id_atleta + "_" + datos.fecha.replace(/-/g, "");

    // 3. Calcular ID Incremental por Atleta (Nivel 2)
    // Contamos registros previos del atleta en la hoja correspondiente
    const hojaDestino = (datos.tipo_sesion === "Gimnasio") ? hojaGim : hojaPista;
const valores = hojaDestino.getDataRange().getValues();

// 2. Calcular ID Incremental específica para este Atleta
let contadorAtleta = 1;

if (valores.length > 1) {
  // Filtramos las filas que pertenecen a este atleta y sumamos 1
  contadorAtleta = valores.filter(fila => {
    let idSesionFila = String(fila[0]); // Forzamos que sea texto para evitar el error .split
    return idSesionFila.startsWith(datos.id_atleta + "_");
  }).length + 1;
}

// Convertimos el número a formato de dos dígitos (ej: 01, 04, 12)
const idIncremental = contadorAtleta.toString().padStart(2, '0');

// 3. Guardar Nivel 1 (Cabecera) - Ahora lo ponemos ANTES del Nivel 2 para asegurar que se cree
const idSesionUnica = datos.id_atleta + "_" + datos.fecha.replace(/-/g, "");

hojaSesion.appendRow([
  idSesionUnica, datos.id_atleta, datos.fecha, datos.tipo_sesion, 
  datos.fase, datos.sueno, datos.fatiga, datos.rpe, 
  datos.limitante, datos.molestias
]);

// 4. Guardar Nivel 2 (Ejercicios) con la ID Incremental del Atleta
datos.ejercicios.forEach(ej => {
  if (ej.nombre) {
    if (datos.tipo_sesion === "Gimnasio") {
      hojaGim.appendRow([idSesionUnica, idIncremental, ej.nombre, ej.series, ej.reps, ej.peso, ej.rir, ej.notas]);
    } else {
      hojaPista.appendRow([idSesionUnica, idIncremental, ej.nombre, ej.serie_num, ej.reps, ej.metrica, ej.notas]);
    }
  }
});

return "EXITO"; 
  } catch (e) {
    return "ERROR: " + e.toString();
  }
}