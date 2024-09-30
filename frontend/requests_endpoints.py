from fake_useragent import UserAgent
import requests

local = False
if local:
    URL_MAIN = 'http://localhost:8000/'
else:
    URL_MAIN = 'http://backend:8000/'


class BackendConnection:

    def __init__(self, user, password):
        self.user = user,
        self.password = password
        self.access_token, self.refresh_token = self.login()
        self.list_tasks = self.get_list_tasks()

    def create_headers(self):
        access_token = self.access_token

        ua = UserAgent()
        user_agent = ua.random
        auth_token = f'Bearer {access_token}'

        headers = {
            'User-Agent': user_agent,
            'Authorization': auth_token,
            'Content-Type': 'application/json',
        }

        return headers

    def login(self):
        print('Login...')
        url = f'{URL_MAIN}api/auth/login/'
        user = self.user
        password = self.password

        if not user:
            user = "obidegain4"
        if not password:
            password = "ContraseñaSegura123"

        data = {
            "username": user,
            "password": password
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')

            print("Access Token:", access_token)
            print("Refresh Token:", refresh_token)

            return access_token, refresh_token
        else:
            print("Error en el login:", response.status_code, response.text)
            return None, None

    def refresh_tokens(self):
        print('Solicitando refresh token...')
        url = f'{URL_MAIN}api/auth/token/refresh/'
        refresh_token = self.refresh_token
        data = {
            "refresh": refresh_token
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token = response.json()
            access_token = token.get('access')
            self.access_token = access_token
        else:
            print("Error en el login:", response.status_code, response.text)
            return

    def get_list_tasks(self):
        print('Solicitando lista de tareas...')
        for i in range(3):
            url = f'{URL_MAIN}api/auth/get_tasks/'
            headers = self.create_headers()
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            else:
                self.refresh_tokens()
        return

    def create_task(self, title, description, deadline):
        print('Creando nueva tarea...')
        for i in range(3):
            url = f'{URL_MAIN}api/tasks/create/'
            data = {
                'title': title,
                'description': description,
                'deadline': deadline
            }
            headers = self.create_headers()
            response = requests.post(url, headers=headers, json=data)
            print(response.status_code)
            if response.status_code == 201:
                print(response.text)
                self.list_tasks = self.get_list_tasks()
                return True
            else:
                self.refresh_tokens()
        return

    def update_status_task(self, id, new_status):
        for i in range(3):
            url = f'{URL_MAIN}api/tasks/update/{id}/'
            data = {
                "status": new_status
            }
            headers = self.create_headers()
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                print(response.text)
                self.list_tasks = self.get_list_tasks()
                return True
            else:
                self.refresh_tokens()
        return

    def delete_task(self, id):
        for i in range(3):
            url = f'{URL_MAIN}api/tasks/delete/{id}/'
            headers = self.create_headers()
            response = requests.delete(url, headers=headers)
            if response.status_code == 204:
                print('Eliminada correctamente')
                self.list_tasks = self.get_list_tasks()
                return True
            else:
                self.refresh_tokens()
        return

class CreateNewUser:
    def __init__(
            self,
            username,
            password_first,
            password_second,
            email,
            first_name=None,
            last_name=None
    ):
        self.username = username
        self.password_first = password_first
        self.password_second = password_second
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.backend_conn = self.register_user()

    def register_user(self):
        url = f'{URL_MAIN}api/auth/register/'
        data = {
            "first_name": self.first_name,
            "second_name": self.last_name,
            "username": self.username,
            "password_first": self.password_first,
            "password_second": self.password_second,
            "email": self.email
        }

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                backend_conn = BackendConnection(user=self.username, password=self.password_first)
                return backend_conn
            return
        except requests.exceptions.RequestException:
            return