# Guía de Uso y Preguntas Frecuentes

## Introducción
¡Bienvenid@ al sistema de préstamos colaborativos! Esta guía te ayudará a entender cómo usar la plataforma y responderá a preguntas comunes para que tu experiencia sea lo más sencilla y clara posible. Si tienes dudas adicionales, ¡no dudes en consultarnos!

---

## Tabla de Contenidos
1. [Cómo Registrarse](#cómo-registrarse)
2. [Cómo Añadir Libros](#cómo-añadir-libros)
3. [Carga Masiva de Libros desde Excel](#carga-masiva-de-libros-desde-excel)
4. [Cómo Pedir un Libro en Préstamo](#cómo-pedir-un-libro-en-préstamo)
5. [Preguntas Frecuentes](#preguntas-frecuentes)
6. [Actualización de la Guía](#actualización-de-la-guía)

---

## Cómo Registrarse
1. Ve a la página principal y haz clic en **Registrarme**.
2. Completa el formulario con tus datos: 
   - Nombre de usuario
   - Contraseña
   - Email
   - Información adicional (ciudad, país, teléfono, etc.)
3. Haz clic en **Enviar** para completar tu registro.
4. Te lleva a la pagina de inicio apra iniciar sesion.

---

## Cómo Añadir Libros

### Carga Individual de Libros
1. Inicia sesión en tu cuenta.
2. Ve al menú **Libros** y selecciona **Cargar Libro**.
3. Completa la información del libro, como:
   - Nombre (obligatorio)
   - Autor (obligatorio)
   - Editorial (opcional)
   - ISBN (opcional)
   - Descripción (opcional)
4. Haz clic en **Guardar** para agregar el libro a tu biblioteca personal.

### Carga Masiva de Libros desde Excel
Para agregar múltiples libros de una vez, puedes usar la funcionalidad de carga masiva:

1. Inicia sesión en tu cuenta.
2. Ve al menú **Libros** y selecciona **Carga Masiva (Excel)**.
3. Descarga la plantilla Excel de ejemplo haciendo clic en el botón **"Descargar Plantilla Excel"**.
4. Completa la plantilla con tus libros:
   - **Columnas obligatorias:** Nombre, Autor
   - **Columnas opcionales:** Editorial, ISBN, Descripción
   - La primera fila debe contener los encabezados
   - Cada fila siguiente representa un libro
5. Guarda el archivo Excel (.xlsx o .xls).
6. En la página de carga masiva, haz clic en **"Elegir archivo"** y selecciona tu archivo Excel.
7. Haz clic en **"Procesar Archivo"**.
8. Revisa los resultados:
   - **Libros creados:** Se mostrarán los libros que se agregaron exitosamente
   - **Duplicados:** Se mostrarán los libros que ya existen (no se crearán)
   - **Errores:** Se mostrarán los problemas encontrados en el archivo con el número de fila

**Nota:** El sistema detecta automáticamente las columnas, incluso si tienen nombres ligeramente diferentes (con o sin acentos, mayúsculas/minúsculas).

---

## Cómo Prestar un Libro en Préstamo
1. Inicia sesión en tu cuenta.
2. Ve al menú **Prestamos** y selecciona **Prestar Libro**.
3. Selecciona el libro que deseas prestar.
4. Selecciona el usuario al que deseas prestar el libro.
5. Haz click en **Confirmmar Prestamo** para confirmar.

## **Mis Préstamos y Gestionar Devolución de Libros**
- En el menú, selecciona **"Mis Préstamos"** para ver los libros que has solicitado y que tienes prestados actualmente.
- Para devolver un libro, ve al detalle del préstamo y utiliza la opción **"Marcar como devuelto"**.

---

## **Historial de Préstamos**
- Consulta el historial de préstamos realizados o recibidos desde la sección **"Historial de Préstamos"**.
- Aquí se mostrarán todos los préstamos completados o cancelados.

---

## Preguntas Frecuentes

### ¿Qué pasa si olvidé mi contraseña?
Por Ahora no esta implementada la recuperación de contraseña, contacta al administrador del sistema.

### ¿Puedo editar la información de un libro?
Sí, ve a **Mis Libros**, selecciona el libro que deseas editar y actualiza la información.

### ¿Cómo pido un libro prestado?
Por ahora no está implementada la funcionalidad de pedidos, si conoces al anfitrión del libro pídeselo y que él gestione el préstamo en la plataforma.

### ¿Puedo cargar muchos libros a la vez?
Sí, puedes usar la funcionalidad de **Carga Masiva (Excel)** desde el menú de Libros. Descarga la plantilla, completa tus libros en Excel y súbelos todos de una vez. El sistema te mostrará cuántos se crearon, cuáles son duplicados y si hubo algún error.

### ¿Qué pasa si tengo libros duplicados en mi archivo Excel?
El sistema detecta automáticamente los duplicados y no los creará. Te mostrará qué libros son duplicados y por qué (por ISBN o por nombre+autor). Los duplicados no se crearán, pero el resto de los libros válidos sí se procesarán.

### ¿Qué formato debe tener el archivo Excel?
El archivo debe ser .xlsx o .xls. La primera fila debe contener los encabezados de las columnas. Las columnas obligatorias son "Nombre" y "Autor". Las opcionales son "Editorial", "ISBN" y "Descripción". Puedes descargar una plantilla de ejemplo desde la página de carga masiva.

### ¿Qué pasa si mi archivo Excel tiene errores?
El sistema procesará todas las filas válidas y te mostrará un reporte detallado de:
- Los libros que se crearon exitosamente
- Los libros duplicados (que no se crearon)
- Los errores encontrados, indicando el número de fila y el motivo del error

Puedes corregir los errores en tu archivo Excel y volver a subirlo.

---

## Actualización de la Guía
Esta guía puede actualizarse con frecuencia para reflejar nuevas funcionalidades o resolver dudas recurrentes. Si encuentras algún error o tienes sugerencias, contáctanos.

---

## Cuestionario de Feedback para Betatesters

1. **Experiencia General:**
   - ¿Qué te pareció la plataforma? ¿Fue fácil de usar?

2. **Funcionalidades:**
   - ¿Pudiste registrarte, añadir libros y realizar pedidos sin problemas?
   - ¿Qué funcionalidad agregarías o cambiarías?

3. **Interfaz de Usuario:**
   - ¿Te resultó claro el diseño de la interfaz?
   - ¿Algún elemento te resultó confuso o difícil de encontrar?

4. **Sugerencias y Comentarios Adicionales:**
   - ¿Algo más que quieras compartir para mejorar la plataforma?

> **Nota:** Por favor, envía tus respuestas a nuestro correo o utiliza el formulario de contacto incluido en la plataforma. ¡Gracias por tu colaboración!

---
