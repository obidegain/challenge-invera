import streamlit as st
from requests_endpoints import BackendConnection, CreateNewUser


def register_user():
    st.title('Registro de nuevo usuario')
    st.subheader("Por favor, complete los siguientes datos para registrarse")
    first_name = st.text_input("Nombre")
    last_name = st.text_input("Apellido")
    username = st.text_input("Nombre de usuario")
    password_first = st.text_input("Contraseña", type='password')
    password_second = st.text_input("Repita la contraseña", type='password')
    email = st.text_input("Email")

    if st.button("Registrar"):
        if not username or not password_first or not password_second or not email:
            st.error("Por favor, complete todos los campos.")
            if password_first != password_second:
                st.error("Las contraseñas no coinciden.")
        else:
            new_user_instance = CreateNewUser(
                username=username,
                password_first=password_first,
                password_second=password_second,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            backend_conn = new_user_instance.backend_conn
            if backend_conn.access_token:
                st.session_state['backend_conn'] = backend_conn
                st.success("Registro exitoso")
            else:
                st.error("Error en el registro")


# Definir las páginas
def login_page():
    st.title('Login')
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button('Login'):
        backend_conn = BackendConnection(username, password)
        if backend_conn.access_token:
            st.session_state['backend_conn'] = backend_conn
            st.success("Login exitoso")
        else:
            st.error("Error en el login")


def view_tasks_page():
    st.title('Tus Tareas')
    backend_conn = st.session_state.get('backend_conn')
    if not backend_conn:
        st.warning("Por favor, inicia sesión primero")
        return

    tasks = backend_conn.list_tasks
    if tasks:
        task_data = [
            {
                'ID': task['id'],
                'Título': task['title'],
                'Descripción': task['description'],
                'Estado': task['status'],
                'Fecha límite': task['deadline']
            }
            for task in tasks
        ]

        st.dataframe(task_data)
    else:
        st.write("No se encontraron tareas.")


def create_task_page():
    st.title('Crear Nueva Tarea')
    backend_conn = st.session_state.get('backend_conn')
    if not backend_conn:
        st.warning("Por favor, inicia sesión primero")
        return

    title = st.text_input("Título")
    description = st.text_area("Descripción")
    deadline = st.date_input("Fecha límite")

    if st.button('Crear'):
        success = backend_conn.create_task(title, description, str(deadline))
        if success:
            st.success("Tarea creada exitosamente")
        else:
            st.error("Error al crear la tarea")


def update_task_status_page():
    st.title('Modificar Estado de una Tarea')
    backend_conn = st.session_state.get('backend_conn')
    if not backend_conn:
        st.warning("Por favor, inicia sesión primero")
        return

    tasks = backend_conn.list_tasks
    task_options = [f"{task['id']} - {task['title']}" for task in tasks]
    selected_task = st.selectbox("Selecciona una tarea para actualizar:", task_options)
    task_id = selected_task.split(" - ")[0]

    new_status = st.selectbox("Nuevo estado", ['progress', 'done', 'cancelled', 'postponed', 'expired'])

    if st.button('Modificar Estado'):
        success = backend_conn.update_status_task(task_id, new_status)
        if success:
            st.success("Estado de la tarea actualizado exitosamente")
        else:
            st.error("Error al actualizar el estado de la tarea")


def delete_task_page():
    st.title('Eliminar Tarea')
    backend_conn = st.session_state.get('backend_conn')
    if not backend_conn:
        st.warning("Por favor, inicia sesión primero")
        return

    tasks = backend_conn.list_tasks
    task_options = [f"{task['id']} - {task['title']}" for task in tasks]
    selected_task = st.selectbox("Selecciona una tarea para actualizar:", task_options)
    task_id = selected_task.split(" - ")[0]

    if st.button('Eliminar'):
        success = backend_conn.delete_task(task_id)
        if success:
            st.success(f"Tarea {task_id} eliminada exitosamente")
        else:
            st.error(f"Error al eliminar la tarea {task_id}")


def main():
    st.sidebar.title("Menú")
    page = st.sidebar.radio(
        "Selecciona una página",
        ("Login", "Ver Tareas", "Crear Tarea", "Modificar Estado", "Eliminar Tarea", "Registrar Nuevo Usuario")
    )

    if page == "Login":
        login_page()
    elif page == "Ver Tareas":
        view_tasks_page()
    elif page == "Crear Tarea":
        create_task_page()
    elif page == "Modificar Estado":
        update_task_status_page()
    elif page == "Eliminar Tarea":
        delete_task_page()
    elif page == "Registrar Nuevo Usuario":
        register_user()


if __name__ == "__main__":
    main()
