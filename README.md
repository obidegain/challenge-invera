# Challenge Invera

Este proyecto es una aplicación de gestión de tareas construida con Django y Streamlit, utilizando Docker para la ejecución.

## Requisitos

- Docker
- Docker Compose

## Instalación

1. **Clonar el repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd challenge-invera
   ```

2. **Levantar contenedores**
    ```bash
    docker-compose up
     ```
4. **Acceder a la aplicación:**

- Backend (Django): http://0.0.0.0:8000
- Frontend (Streamlit): http://0.0.0.0:8501

## Endpoints
### Usuarios
1. POST /api/auth/register/

Registra un nuevo usuario. Requiere un payload JSON con los campos necesarios para la creación de un usuario (ej. nombre de usuario, contraseña).

2. POST /api/auth/login/

Inicia sesión y obtiene un token de acceso y de refresco. Requiere un payload JSON con nombre de usuario y contraseña.

3. POST /api/auth/token/refresh/

Refresca el token de acceso utilizando el token de refresco. Requiere el token de refresco en el payload.

4. GET /api/auth/get_tasks/

Obtiene la lista de tareas del usuario autenticado. Requiere el token de acceso en los headers.

### Tareas
1. POST /api/tasks/create/

Crea una nueva tarea. Requiere un payload JSON con la información de la tarea (title, description, deadline). Requiere el token de acceso en los headers.

2. DELETE /api/tasks/delete/<int:pk>/

Elimina una tarea específica identificada por su ID. Devuelve un mensaje de éxito tras la eliminación. Requiere el token de acceso en los headers.

3. PATCH /api/tasks/update/<int:pk>/

Actualiza el estado de una tarea específica identificada por su ID. Requiere un payload JSON con el nuevo estado (PROGRESS, DONE, CANCELLED, POSTPONED, EXPIRED). Requiere el token de acceso en los headers.
