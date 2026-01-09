**Resumen del Proyecto: Sistema de Préstamos de Libros Físicos**  

El sistema tiene como objetivo facilitar la gestión de préstamos de libros físicos entre personas, promoviendo la colaboración y el intercambio dentro de comunidades. Los usuarios pueden gestionar sus propios libros, registrar préstamos y, en etapas avanzadas, interactuar en comunidades para compartir recursos de manera eficiente.  

---

## Instalación y Configuración

### Requisitos
- Python 3.12 o superior
- Django 5.1.4 o superior
- openpyxl 3.1.0 o superior (para carga masiva de Excel)

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd biblioteca-colectiva-zero
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos:**
   ```bash
   cd libro_prestamos
   python manage.py migrate
   ```

5. **Crear superusuario (opcional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```

El sistema estará disponible en `http://127.0.0.1:8000/`

---

## Documentación del Modelo de Datos

El diagrama entidad-relación (ER) del sistema está disponible en formato DBML:
- **Archivo:** `diagrama_ER.dbml`
- **Visualización:** Puedes visualizarlo en [dbdiagram.io](https://dbdiagram.io)

El modelo ha sido optimizado para mantenibilidad y simplicidad, priorizando la facilidad de uso y mantenimiento por un solo desarrollador.

---  

### **Entidades Principales:**
1. **Usuario:**  
   - Representa a las personas que utilizan el sistema.  
   - Atributos: nombre, correo electrónico (privado), teléfono, lugar de residencia (país y ciudad) y contraseña.  
   - Funcionalidades: registro, inicio de sesión, gestión de perfil, y asociación con libros y comunidades.  

2. **Libro:**  
   - Representa copias físicas individuales que los usuarios pueden prestar.  
   - Atributos: nombre, autor, editorial, ISBN, tags, comentarios, estado (disponible, no disponible, prestado) y propietario.  
   - Funcionalidades: los usuarios pueden cargar libros manualmente o mediante un archivo Excel, y gestionarlos (editar estado o eliminar).  

3. **Préstamo:**  
   - Registra la transacción de préstamo de un libro entre dos usuarios.  
   - Atributos: fecha de solicitud, fecha de aceptación, estado (pendiente, aceptado, prestado, devuelto), comentario del prestador, comentario del prestatario, y referencias al libro, prestador y prestatario.  
   - Funcionalidades: los usuarios pueden realizar y registrar préstamos, incluyendo comentarios al devolver los libros.  

4. **Notificación:**  
   - Facilita la comunicación entre usuarios en eventos clave como solicitudes o aceptación de préstamos.  
   - Atributos: tipo (solicitud o aceptación), estado (pendiente o visto), fecha y hora, usuario receptor y préstamo asociado.  
   - Funcionalidades: notifica automáticamente a los usuarios sobre cambios en los préstamos.  

5. **Comunidad:**  
   - Grupos de usuarios con intereses comunes para compartir y gestionar libros.  
   - Atributos: nombre, descripción, imagen y administrador.  
   - Funcionalidades: los usuarios pueden crear, unirse y gestionar comunidades, compartir libros, y establecer roles (administrador o miembro).  

---

### **Funcionalidades del Sistema:**
1. **Gestión de Usuarios:**  
   - Registro, inicio de sesión y edición de perfil.  

2. **Gestión de Libros:**  
   - Carga manual individual de libros.
   - **Carga masiva mediante archivo Excel** (Release 2 - ✅ Implementado).
   - Actualización de estado (disponible, no disponible, prestado).  
   - Edición y eliminación de libros propios.  

3. **Gestión de Préstamos:**  
   - Registrar préstamos entre usuarios con estados claros.  
   - Registrar comentarios al finalizar un préstamo.  

4. **Historial de Préstamos:**  
   - Visualización de libros prestados y recibidos por el usuario.  

5. **Notificaciones (futuro):**  
   - Comunicación automática para solicitudes y actualizaciones de préstamos.  

6. **Gestión de Comunidades (futuro):**  
   - Crear, unirse y gestionar comunidades.  
   - Compartir libros entre miembros de una comunidad.  

El sistema está diseñado para ser escalable y adaptarse a nuevas funcionalidades, permitiendo un desarrollo iterativo y la mejora continua.

### Plan de Implementación Paso a Paso

#### **Objetivo General**:  
Desarrollar un sistema para gestionar préstamos de libros físicos entre usuarios, priorizando iteraciones rápidas para llegar a un **Mínimo Producto Viable (MVP)** y escalando con funcionalidades más complejas en futuras releases.

---

### **Release 1: Mínimo Producto Viable (MVP)** - **COMPLETADO**
#### **Funcionalidades principales:**
1. **Gestión de Usuarios:**
   - Registro e inicio de sesión.
   - Información básica: nombre, correo, lugar de residencia, y contraseña.

2. **Gestión de Libros:**
   - Crear, listar, editar y eliminar libros.
   - Asociar libros a su propietario (usuario).

3. **Gestión de Préstamos:**
   - Permitir que un usuario seleccione un libro propio para prestarlo a otro usuario.
   - Registrar los datos del préstamo (libro, prestatario, prestador, estado, fechas).

#### **Tareas técnicas:**
- Configurar el proyecto en Django con las aplicaciones `usuarios`, `libros`, y `prestamos`.
- Crear modelos para las entidades Usuario, Libro, y Prestamo.
- Implementar vistas y formularios básicos para CRUD de usuarios y libros.
- Crear la lógica para registrar préstamos directamente (sin notificaciones ni estados avanzados).
- Implementar interfaz simple con templates de Django.

#### **Meta de entrega:** Sistema funcional básico donde:
   - Los usuarios gestionan sus perfiles y libros.
   - Los préstamos se registran manualmente por los usuarios involucrados.

---

### **Release 2: Gestión de Inventario a Gran Escala** - **COMPLETADO**

#### **Funcionalidades implementadas:**
1. **Carga masiva de libros:**
   - Los usuarios pueden subir un archivo Excel (.xlsx o .xls) con información de múltiples libros.
   - Validación automática de datos del archivo.
   - Detección de duplicados (por ISBN y por nombre+autor).
   - Procesamiento en lote con feedback detallado de resultados.

#### **Características técnicas:**
- Implementada funcionalidad para procesar archivos Excel utilizando **`openpyxl`**.
- Interfaz completa para subir archivos y visualizar el estado del procesamiento.
- Validación de datos del archivo (campos obligatorios: nombre y autor).
- Manejo robusto de errores (libros duplicados, datos faltantes, formato incorrecto).
- Detección flexible de columnas (case-insensitive, con/sin acentos).
- Generación de plantilla Excel descargable con ejemplos.
- Reporte detallado de resultados: libros creados, duplicados y errores por fila.

#### **Estructura del Excel:**
- **Columnas obligatorias:** Nombre, Autor
- **Columnas opcionales:** Editorial, ISBN, Descripción
- **Formato:** Primera fila con encabezados, filas siguientes con datos

#### **Meta de entrega:** ✅ **COMPLETADO**  
Sistema que facilita la carga masiva de libros, optimizando la experiencia para usuarios con grandes inventarios.

---

### **Release 3: Gestión Avanzada de Préstamos**
#### **Funcionalidades principales:**

1. **Pedidos de Préstamo:**
   - Permitir que los usuarios soliciten préstamos de libros a otros usuarios.
   - Los usuarios pueden ver y aceptar o rechazar solicitudes de préstamo.
   - Si el prestador acepta la solicitud, se visualizan los datos de los usuarios involucrados.

#### **Tareas técnicas:**
- Implementar la lógica para manejar solicitudes de préstamo y aceptación/rechazo.

#### **Meta de entrega:** 
   - Los usuarios pueden solicitar préstamos de libros y contactar a otros usuarios.

---

### **Release 4: Gestión Avanzada de Busquedas**
#### **Funcionalidades principales:**

1. **Filtros:**
   - Permitir filtros por ciudad, pais, tags en la busqueda.

#### **Tareas técnicas:**
- Implementar uso de tags
- Implementar filtros en la vista de busqueda.
- Ver libros de usuario

#### **Meta de entrega:** 
   - Los usuarios tienen una metodo mas granular para buscar libros.

---

### **Release 5: Integración de Comunidades**
#### **Funcionalidades principales:**
1. **Gestión de comunidades:**
   - Crear, unirse y gestionar comunidades.
   - Asignar roles (administrador y miembro).
   - Mostrar libros compartidos dentro de la comunidad.

#### **Tareas técnicas:**
- Crear modelos y vistas para comunidades.
- Implementar lógica de permisos y roles.
- Asociar libros y usuarios a comunidades.

#### **Meta de entrega:** Fomentar la colaboración y organización dentro de comunidades.

---

### **Release 6: Notificaciones**
#### **Funcionalidades principales:**
1. **Notificaciones automáticas:**
   - Enviar notificaciones internas cuando se haga una solicitud de préstamo o se actualice su estado.

#### **Tareas técnicas:**
- Crear un modelo para notificaciones.
- Implementar lógica para generar notificaciones en eventos clave.
- Mostrar notificaciones en la interfaz del usuario.

#### **Meta de entrega:** Sistema con trazabilidad y comunicación interna básica.

---

### **Release 7: Mejoras Opcionales**
#### **Funcionalidades principales:**
1. **Carga de imagen en comunidades.**
2. **Interfaz mejorada para búsquedas de libros por tags.**
3. **Implementación de geolocalización para proximidad.**

#### **Meta de entrega:** Mejorar usabilidad y funcionalidades avanzadas.

---

### **Estado Actual del Proyecto:**
- ✅ **Release 1 (MVP):** Completado - Sistema básico funcional
- ✅ **Release 2 (Carga Masiva):** Completado - Carga masiva desde Excel implementada
- 🔄 **Release 3 (Préstamos Avanzados):** Pendiente
- 🔄 **Release 4 (Búsquedas Avanzadas):** Pendiente
- 🔄 **Release 5 (Comunidades):** Pendiente
- 🔄 **Release 6 (Notificaciones):** Pendiente
- 🔄 **Release 7 (Mejoras Opcionales):** Pendiente

### **Observaciones finales:**
- Este plan permite ir desarrollando funcionalidades de manera iterativa, priorizando un MVP simple y escalando según las necesidades.
- La carga masiva de libros en Release 2 ha sido implementada exitosamente, mejorando significativamente la experiencia del usuario para gestionar grandes inventarios.

