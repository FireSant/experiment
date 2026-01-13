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

    // Buscamos las hojas de forma segura ignorando espacios
    const hojaSesion = hojas.find(h => h.getName().trim() === "Sesion_Entrenamiento");
    const hojaGim = hojas.find(h => h.getName().trim() === "Registros_Gimnasio");
    const hojaPista = hojas.find(h => h.getName().trim() === "Registros_Pista");

    if (!hojaSesion || !hojaGim || !hojaPista) {
      throw new Error("No se encontró una pestaña. Revisa que los nombres en el Excel sean: Sesion_Entrenamiento, Registros_Gimnasio y Registros_Pista");
    }

    const idSesion = (datos.id_atleta || "S") + "_" + datos.fecha.replace(/-/g, "");

    // Guardar Cabecera
    hojaSesion.appendRow([
      idSesion, datos.id_atleta, datos.fecha, datos.tipo_sesion, 
      datos.fase, datos.sueno, datos.fatiga, datos.rpe, 
      datos.limitante, datos.molestias
    ]);

    // Guardar Detalle
    if (datos.tipo_sesion === "Gimnasio") {
      datos.ejercicios.forEach(ej => {
        if(ej.nombre) hojaGim.appendRow([idSesion, Utilities.getUuid(), ej.nombre, ej.series, ej.reps, ej.peso, ej.rir, ej.notas]);
      });
    } else {
      datos.ejercicios.forEach(ej => {
        if(ej.nombre) hojaPista.appendRow([idSesion, Utilities.getUuid(), ej.nombre, ej.serie_num, ej.reps, ej.metrica, ej.notas]);
      });
    }
    
    return "EXITO"; 
  } catch (e) {
    return "ERROR EN SERVIDOR: " + e.toString();
  }
}