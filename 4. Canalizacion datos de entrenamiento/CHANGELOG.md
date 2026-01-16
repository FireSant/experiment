# Registro de versiones y novedades

Flujo de trabajo: Revisar correcciones y mejoras, desarrollar la tarea, probar mejora, registrar mejoras o errores capturados, subir a git.
        Se registrara lo siguiente: Primero la version y fecha. Luego: `Funcionalidades`, `Problemas conocidos`, `Correcciones y merjoras`, `Sugerencias`


 
## v0.0.1  - 2026-01-12 🛠️
### Funcionalidades o features
*   Interfaz Web App: Migración de macros de Excel a una aplicación web completa con HTML/CSS/JS.
*   Catálogo Dinámico: Implementación de filtros por zona (Piernas, Tren Superior, etc.) para selección rápida de ejercicios.
*   Soporte Multimodal: Lógica diferenciada para ingresos de Gimnasio y Pista en un solo formulario.

### Problemas conocidos
*   Falla en Cascada: Solo se está guardando el registro de nivel 2 (detalles de ejercicios) pero no el nivel 1 (cabecera de la sesión).
*   UX Post-Guardado: La página se queda en blanco tras presionar guardar.
*   Complejidad de IDs: Los IDs actuales para Gimnasio y Pista son demasiado complejos y dificultan la lectura manual en la base de datos.
*   Filtros por zona: No esta funcionando. Se evaluara la practicidad de la funcionalidad y su posible retiro.

### Correcciones y mejoras


### Sugerencias
* Probar happy paths y edge cases
* Cronometrar el tiempo de uso de la app para la tarea 
* Cambio en la logica de base de datos de atletas y Userflow:
    - Opcion A: Que el usuario cuando se registre conozca su Numero id unico para colocarlo durante el userflow
    - Opcion B. Que al inicio de la ejecucion de la app, se obtengan todos los nombres de usuarios y sus ID. que el usuario pueda consultar su id segun su nombre. Seria un poco sin sentido pues seria mejor que solo haga el registro con su nombre y como se obtuvieron todos los usuarios de la bbdd, el autocompletar ayude a evitar errores     
* Agregar tiempo de descanso entre series de un ejercicio
  

## v0.0.2  - 2026-01-13 🛠️
### Funcionalidades
*   Interfaz Web App: Formulario completo web completa con HTML/CSS/JS.
*   Catálogo Dinámico: Implementación de filtros por zona (Piernas, Tren Superior, etc.) para selección rápida de ejercicios.
*   Soporte Multimodal: Lógica diferenciada para ingresos de Gimnasio y Pista en un solo formulario.

### Problemas conocidos
*   Filtros por zona: No esta funcionando. Se evaluara la practicidad de la funcionalidad y su posible retiro.


### Correcciones y mejoras
*   Falla en Cascada: Se envian todos los datos
*   UX Post-Guardado: Se corrigio la función  enviar() del archivo Index.html que use un mensaje de confirmación que no fuerce la recarga inmediata, permitiendo ver que los datos se procesaron.
*   Complejidad de IDs: Se carga un id dependiendo si ya ha habido uno anterior para ese atleta

### Sugerencias
* Probar happy paths y edge cases
* Cronometrar el tiempo de uso de la app para la tarea 
* Cambio en la logica de base de datos de atletas y Userflow:
    - Opcion A: Que el usuario cuando se registre conozca su Numero id unico para colocarlo durante el userflow
    - Opcion B. Que al inicio de la ejecucion de la app, se obtengan todos los nombres de usuarios y sus ID. que el usuario pueda consultar su id segun su nombre. Seria un poco sin sentido pues seria mejor que solo haga el registro con su nombre y como se obtuvieron todos los usuarios de la bbdd, el autocompletar ayude a evitar errores     
* Agregar box de tiempo de descanso entre series de un ejercicio
  
## v0.0.3  - 2026-01-14 🛠️
### Funcionalidades
*   Interfaz Web App: Formulario completo web completa con HTML/CSS/JS.
*   Catálogo Dinámico: Implementación de filtros por zona (Piernas, Tren Superior, etc.) para selección rápida de ejercicios.
*   Soporte Multimodal: Lógica diferenciada para ingresos de Gimnasio y Pista en un solo formulario.
*   Módulo de Registro de Atletas con ID autoincremental

### Problemas conocidos
*   Filtros por zona: No esta funcionando. Se evaluara la practicidad de la funcionalidad y su posible retiro.
### Correcciones y mejoras
*   Refactor: Simplificación de IDs de nivel 2. Se elimina el uso de UUIDs y se adopta un sistema de ID de Sesión compuesto (Atleta_Fecha_TipoSesion) que actúa como clave relacional, permitiendo sesiones múltiples por día y mejorando la legibilidad de la base de datos
*   Feature: Implementación de módulo de Registro de Atletas con ID autoincremental (01, 02...). 
*   Feature: Inclusión de campo 'Descanso' en registros de Nivel 2 (Gimnasio y Pista) posicionado antes de las notas de serie para mejorar la trazabilidad del entrenamiento.

### Sugerencias
* Probar happy paths y edge cases
* Cronometrar el tiempo de uso de la app para la tarea 
* Evaluar si el usuario debe ingresar su nombre o ID unico de la app para registrar sus entrenamientos.

## v0.0.4  - 2026-01-15 🛠️
### Funcionalidades
*   Interfaz Web App: Formulario completo web completa con HTML/CSS/JS.
*   Catálogo Dinámico: Implementación de filtros por zona (Piernas, Tren Superior, etc.) para selección rápida de ejercicios.
*   Soporte Multimodal: Lógica diferenciada para ingresos de Gimnasio y Pista en un solo formulario.
*   Pestaña: Módulo de Registro de Atletas con ID autoincremental

### Problemas conocidos

### Correcciones y mejoras
*   Se quito el bloque de categorias de ejercicios 
*   Unificación logica de IDs  
*   Se agregaron bordes a botones de pestañas
*   Cambio en ubicación de placeholders y unificacion de casillero limitante y molestias


### Sugerencias
* Probar happy paths y edge cases
* Cronometrar el tiempo de uso de la app para la tarea 
* Evaluar si el usuario debe ingresar su nombre o ID unico de la app para registrar sus entrenamientos.