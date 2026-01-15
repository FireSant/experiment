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

    const hojaSesion = hojas.find(h => h.getName().trim() === "Sesion_Entrenamiento");
    const hojaGim = hojas.find(h => h.getName().trim() === "Registros_Gimnasio");
    const hojaPista = hojas.find(h => h.getName().trim() === "Registros_Pista");

    if (!hojaSesion || !hojaGim || !hojaPista) throw new Error("Faltan pestañas.");

    // --- REFACTOR DE ID ---
    // Creamos el sufijo según el tipo de sesión
    const sufijo = (datos.tipo_sesion === "Gimnasio") ? "_G" : "_P";
    
    // La nueva ID de sesión ahora incluye el sufijo (Ej: A01_20260112_G)
    const idSesionConSufijo = datos.id_atleta + "_" + datos.fecha.replace(/-/g, "") + sufijo;

    // 1. Guardar Nivel 1 (Cabecera) con la nueva ID
    hojaSesion.appendRow([
      idSesionConSufijo, datos.id_atleta, datos.fecha, datos.tipo_sesion, 
      datos.fase, datos.sueno, datos.fatiga, datos.rpe, 
      datos.limitante, datos.molestias
    ]);

    // 2. Guardar Nivel 2 (Ejercicios)
    // Ya NO necesitamos calcular 'idIncremental', usamos 'idSesionConSufijo' directamente
    if (datos.tipo_sesion === "Gimnasio") {
      datos.ejercicios.forEach(ej => {
        if (ej.nombre) {
          // Eliminamos la columna de ID Nivel 2, ahora el primer dato es la ID con sufijo
          hojaGim.appendRow([idSesionConSufijo, ej.nombre, ej.series, ej.reps, ej.peso, ej.rir, ej.notas]);
        }
      });
    } else {
      datos.ejercicios.forEach(ej => {
        if (ej.nombre) {
          hojaPista.appendRow([idSesionConSufijo, ej.nombre, ej.serie_num, ej.reps, ej.metrica, ej.notas]);
        }
      });
    }
    
    return "EXITO"; 
  } catch (e) {
    return "ERROR: " + e.toString();
  }
}


function registrarNuevoAtleta(obj) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let hoja = ss.getSheetByName("Atletas");
    
    // Si la hoja no existe, la crea con encabezados
    if (!hoja) {
      hoja = ss.insertSheet("Atletas");
      hoja.appendRow(["ID_Atleta", "Nombre Completo", "Fecha Nacimiento", "Sexo", "Área", "Mejor Marca", "Fecha Marca", "Objetivo"]);
    }
    
    const ultimoRegistro = hoja.getLastRow();
    // Generar ID: 01, 02, 03... basado en la fila actual
    const nuevoId = (ultimoRegistro).toString().padStart(2, '0');
    
    hoja.appendRow([
      nuevoId,
      obj.nombre,
      obj.nacimiento,
      obj.sexo,
      obj.perfil,
      obj.marca,
      obj.fechaMarca,
      obj.objetivo
    ]);
    
    return "EXITO_ATLETA_" + nuevoId;
  } catch (e) {
    return "ERROR: " + e.toString();
  }
}