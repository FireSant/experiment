# 🏋️ Web App de Registro de Entrenamiento

Este proyecto implementa una aplicación web (Web App) construida con Google Apps Script, HTML, CSS y JavaScript para facilitar el registro detallado de sesiones de entrenamiento y sus ejercicios asociados (Gimnasio o Pista). La aplicación interactúa directamente con hojas de cálculo de Google Sheets para almacenar toda la información.

## 🌟 Características Principales

*   **Interfaz de Usuario Intuitiva:** Una interfaz web moderna y responsive para ingresar datos de forma rápida y sencilla.
*   **Registro de Sesiones Generales:** Captura datos clave de la sesión como fecha, atleta, tipo de sesión, fase, horas de sueño, fatiga, RPE, limitantes y molestias.
*   **Registro Dinámico de Ejercicios:** Permite añadir múltiples ejercicios a cada sesión, diferenciando automáticamente los campos necesarios para ejercicios de `Gimnasio` (Series, Reps, Kg, RIR, Notas) y `Pista` (Serie#, Reps, Métrica, Notas).
*   **Catálogo de Ejercicios Integrado:** Sugiere ejercicios basados en un catálogo existente en tu Google Sheet, permitiendo filtrarlos por zonas (Piernas, Tren Superior, Core, Saltos).
*   **Guardado en Google Sheets:** Todos los datos se almacenan automáticamente en hojas de cálculo designadas.
*   **Generación de IDs:** Genera IDs únicos para sesiones y registros de ejercicios.

## 📁 Estructura del Proyecto

Tu repositorio debe contener los siguientes archivos:

*   `Codigo.gs`: Contiene el código de Google Apps Script (JavaScript del lado del servidor) que maneja la lógica de la aplicación, la interacción con Google Sheets y sirve la interfaz HTML.
*   `Index.html`: Define la interfaz de usuario (HTML, CSS, JavaScript del lado del cliente) de la Web App.
*   `CHANGELOG.md`: Registro de todas las versiones, funcionalidades añadidas, correcciones de errores y mejoras.
*   `README.md`: Este archivo, que proporciona una descripción general, guía de configuración y uso del proyecto.

## 🛠️ Configuración y Despliegue

Para poner en funcionamiento esta Web App, sigue los siguientes pasos:

### 1. Preparar tu Google Sheet

Asegúrate de que tu Google Sheet (la hoja de cálculo donde se almacenarán los datos) tenga las siguientes pestañas, con los nombres **exactos** (sensible a mayúsculas y minúsculas y sin espacios adicionales):

*   `Catalogo`: Contendrá tu lista de ejercicios. Se espera que tenga al menos las columnas para `Nombre_Ejercicio` (índice 1 en el script), `Tipo` (índice 2) y `Zona` (índice 4).
*   `Sesion_Entrenamiento`: Almacenará los datos generales de cada sesión. Columnas esperadas: `ID_Sesion`, `ID_Atleta`, `Fecha`, `Tipo_Sesion`, `Fase`, `Sueno`, `Fatiga`, `RPE`, `Limitante`, `Molestias`.
*   `Registros_Gimnasio`: Almacenará los ejercicios de gimnasio. Columnas esperadas: `ID_Sesion`, `ID_Registro_Gym`, `Nombre_Ejercicio`, `Series`, `Repeticiones`, `Peso_Kg`, `RIR`, `Notas_Serie`.
*   `Registros_Pista`: Almacenará los ejercicios de pista. Columnas esperadas: `ID_Sesion`, `ID_Registro_Pista`, `Nombre_Ejercicio`, `Serie_Num`, `Numero_Intento`, `Metrica_Principal`, `Notas_Serie`.

**¡Importante!** La primera fila de cada una de estas hojas debe contener los encabezados de las columnas correspondientes.

### 2. Configurar el Proyecto de Google Apps Script

1.  **Crea un nuevo proyecto de Apps Script:**
    *   Abre tu Google Sheet.
    *   Ve a `Extensiones > Apps Script`. Esto abrirá un nuevo proyecto en el editor de Apps Script.
2.  **Copia el código de `Codigo.gs`:**
    *   En el editor de Apps Script, verás un archivo `Codigo.gs`. Reemplaza todo su contenido con el código de tu `Codigo.gs`.
3.  **Copia el código de `Index.html`:**
    *   En el editor de Apps Script, haz clic en `Archivo > Nuevo > Archivo HTML`.
    *   Nombra el archivo `Index` (sin la extensión `.html`).
    *   Copia todo el contenido de tu `Index.html` en este nuevo archivo `Index.html` del editor de Apps Script.
4.  **Guarda el proyecto:** Haz clic en el icono de guardar (disquete) o `Ctrl + S / Cmd + S`.

### 3. Desplegar como Web App

1.  En el editor de Apps Script, haz clic en el botón `Desplegar` (en la parte superior derecha) y selecciona `Nueva implementación`.
2.  Haz clic en el icono de la rueda (⚙️) junto a "Tipo" y selecciona `Aplicación web`.
3.  **Configura lo siguiente:**
    *   **Ejecutar como:** `Yo` (tu dirección de correo electrónico).
    *   **Acceso:** `Cualquier persona` o `Cualquier persona que tenga una cuenta de Google` (depende de quién quieres que use la app). Para uso personal, "Cualquier persona que tenga una cuenta de Google" es una buena opción.
4.  Haz clic en `Desplegar`.
5.  **Autorización (la primera vez):** Te pedirá que autorices el script para acceder a tus hojas de Google. Revisa los permisos y otórgalos.
6.  Una vez desplegada, se te proporcionará una "URL de la aplicación web". Guarda esta URL, ya que es la que usarás para acceder a tu aplicación.

### 4. Actualizaciones Posteriores

Cada vez que realices cambios en `Codigo.gs` o `Index.html` en el editor de Apps Script:

1.  Guarda los cambios en Apps Script.
2.  Vuelve al menú `Desplegar` y selecciona `Administrar implementaciones`.
3.  Haz clic en el icono de lápiz (✏️) junto a tu implementación actual para `Editar`.
4.  En la sección "Versión", selecciona `Nueva versión`.
5.  Haz clic en `Desplegar`. **No necesitas una nueva URL**, la existente se actualizará con la nueva versión.


## 🚀 Cómo Usar la Web App

1.  Abre la "URL de la aplicación web" que obtuviste en el paso de despliegue.
2.  **En la sección "Datos de la Sesión":**
    *   Rellena la `Fecha`, el `ID Atleta` y selecciona el `Tipo Sesión` (Gimnasio o Pista).
    *   Introduce la `Fase`, `Sueño`, `Fatiga`, `RPE General`, `Limitante` y `Molestias`.
3.  **En la sección "Catálogo de Ejercicios":**
    *   Puedes usar los botones de filtro (Piernas, Tren Superior, Core, Saltos) para ver sugerencias de ejercicios de tu `Catalogo`.
    *   Haz clic en una sugerencia para añadir el ejercicio automáticamente al "Ejercicios Registrados".
4.  **En la sección "Ejercicios Registrados":**
    *   Usa el botón `+ Agregar Ejercicio` para añadir nuevas filas de ejercicio manualmente.
    *   Rellena los campos para cada ejercicio. Los campos cambiarán dinámicamente según el `Tipo Sesión` seleccionado.
    *   Puedes usar el campo "Ejercicio" con la lista de sugerencias (datalist) para autocompletar nombres de ejercicios de tu catálogo.
    *   Usa el botón `✕` para eliminar una fila de ejercicio.
5.  Una vez que todos los datos estén completos, haz clic en el botón `GUARDAR DATOS`.
6.  Verás una notificación de éxito o un mensaje de error si algo falló. La aplicación se recargará automáticamente después de un guardado exitoso.

##  Errores y Mejoras

Consulta el archivo `CHANGELOG.md` para ver el historial de versiones, errores corregidos y funcionalidades implementadas.

---
**Autor:** [FireSant]
