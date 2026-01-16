/**Lógica del Servidor - Registro de Entrenamientos y Atletas*/
function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Registro de Entrenamiento')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// Mantenemos esta función para que el autocompletado en el HTML funcione
function obtenerCatalogoCompleto() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const hoja = ss.getSheets().find(h => h.getName().trim() === "Catalogo");
  if (!hoja) return [];
  const datos = hoja.getDataRange().getValues();
  return datos.slice(1).map(fila => ({
    nombre: fila[1], 
    tipo: fila[2]
  }));
}

function guardarTodo(datos) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const hojas = ss.getSheets();
    const hojaSesion = hojas.find(h => h.getName().trim() === "Sesion_Entrenamiento");
    const hojaGim = hojas.find(h => h.getName().trim() === "Registros_Gimnasio");
    const hojaPista = hojas.find(h => h.getName().trim() === "Registros_Pista");

    if (!hojaSesion || !hojaGim || !hojaPista) throw new Error("Faltan pestañas en el Spreadsheet.");

    const sufijo = (datos.tipo_sesion === "Gimnasio") ? "_G" : "_P";
    const idSesionConSufijo = datos.id_atleta + "_" + datos.fecha.replace(/-/g, "") + sufijo;

    // 1. Guardar Cabecera de Sesión
    hojaSesion.appendRow([
      idSesionConSufijo, datos.id_atleta, datos.fecha, datos.tipo_sesion, 
      datos.fase, datos.sueno, datos.fatiga, datos.intensidad, 
      datos.limitante
    ]);

    // 2. Guardar Detalle de Ejercicios
    datos.ejercicios.forEach(ej => {
      if (ej.nombre) {
        if (datos.tipo_sesion === "Gimnasio") {
          hojaGim.appendRow([idSesionConSufijo, ej.nombre, ej.series, ej.reps, ej.peso, ej.rir, ej.descanso, ej.notas]);
        } else {
          hojaPista.appendRow([idSesionConSufijo, ej.nombre, ej.serie_num, ej.reps, ej.metrica, ej.descanso, ej.notas]);
        }
      }
    });
    return "EXITO"; 
  } catch (e) {
    return "ERROR: " + e.toString();
  }
}

function registrarNuevoAtleta(obj) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let hoja = ss.getSheetByName("Atletas");
    if (!hoja) {
      hoja = ss.insertSheet("Atletas");
      hoja.appendRow(["ID_Atleta", "Nombre Completo", "Fecha Nacimiento", "Sexo", "Área", "Mejor Marca", "Fecha Marca", "Objetivo"]);
    }
    const nuevoId = (hoja.getLastRow()).toString().padStart(2, '0');
    hoja.appendRow(["'"+nuevoId, obj.nombre, obj.nacimiento, obj.sexo, obj.perfil, obj.marca, obj.fechaMarca, obj.objetivo]);
    return "EXITO_ATLETA_" + nuevoId;
  } catch (e) {
    return "ERROR: " + e.toString();
  }
}