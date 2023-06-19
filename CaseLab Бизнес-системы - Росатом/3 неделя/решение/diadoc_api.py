# 1 - получить токен
# 2 - получить ящики
# 3 - получить список всех сотрудников

import requests
import json
import difflib
from openpyexcel import Workbook


class DiadocApi:
    ''' класс для взаимодействия с Диадок при помощи api '''

    # список команд
    commands = {
        'auth': '/V3/Authenticate',
        'get_data_orgs': '/GetMyOrganizations',
        'get_data_orgs_employees': '/GetEmployees'
    }

    def __init__(self, url: str = '', key: str = '', user_login: str = '', user_password: str = ''):

        self.url = url

        # ссылка запроса для авторизации пользователя
        url_auth = self.url + DiadocApi.commands['auth']

        # заголовок для авторизации пользователя
        user_auth = f'DiadocAuth ddauth_api_client_id={key}'

        # заголовки запроса
        headers = {
            "Authorization": user_auth,
            "Content-Length": "1252",
            "Connection": "Keep-Alive",
            "Content-Type": "application/json; charset=utf-8"
        }

        # данные пользователя
        data_user = {
            'login': user_login,
            'password': user_password
        }
        # преобразование данных пользователя в json для передачи в запросе
        self.data_user_json = json.dumps(data_user)

        # параметры запроса
        params = {
            "type": "password"
        }

        # запрос на получение токена
        try:
            response = requests.request(
                method='POST',
                url=url_auth,
                headers=headers,
                params=params,
                data=self.data_user_json
            )
            print(f"[INFO] STATUS CODE: {response.status_code}")

            # токен получен
            self.token = response.text
            self.is_get_token = True
            print("[INFO] TOKEN WAS GOT")

            # заголовок для идентификации пользователя по токену
            self.auth_token = user_auth + f",ddauth_token={self.token}"
        except Exception:
            raise "[ERROR] TOKEN WAS NOT GOT"

        # данные о всех организациях
        self.data_orgs = []

        # данные о ящиках всех организаций
        self.data_orgs_boxes = {}

        # данные о всех сотрудниках организаций
        self.data_orgs_employees = []

    @staticmethod
    def compare_words(words_in = [], string = ''):
        ''' сравнение слов со строками '''

        for w in words_in:
            res = difflib.SequenceMatcher(a=w.lower(), b=string.lower()).ratio()
            print(res)
            if (res > 0.51):
                return True
        return False

    def get_token(self):
        ''' получить токен пользователя '''

        if (self.is_get_token):
            return self.token
        return None

    def get_data_orgs(self):
        ''' получить данные о всех организациях '''

        if (self.is_get_token):

            # ссылка запроса для получения данных о всех организациях
            url_get_data_orgs = self.url + DiadocApi.commands['get_data_orgs']

            # заголовки запроса
            headers = {
                "Authorization": self.auth_token,
                "Content-Length": "1252",
                "Connection": "Keep-Alive",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # параметры запроса
            params = {
                "type": "password"
            }

            # отправка запроса
            try:
                response = requests.request(
                    method='GET',
                    url=url_get_data_orgs,
                    headers=headers,
                    params=params,
                    data=self.data_user_json
                )
                print(f"[INFO] STATUS CODE: {response.status_code}")

                # данные получены
                data_orgs_json = response.json()
                self.data_orgs = data_orgs_json["Organizations"]
                print("[INFO] DATA ORGS WAS GOT")

                return self.data_orgs
            except Exception:
                raise "[ERROR] DATA ORGS DO NOT EXIST"
        return None

    def get_data_orgs_boxes(self):
        ''' получить данные о ящиках всех организаций\n
            return {orgs_ids: [{boxes}]}
        '''

        if (self.data_orgs != []):
            index = 1
            for org in self.data_orgs:
                data_org = {}
                org_id = org['OrgId']
                full_name = org['FullName']
                boxes = org["Boxes"]

                self.data_orgs_boxes[index] = [full_name, org_id, boxes]
                index += 1
            print("[INFO] DATA ORGS BOXES WAS GOT")

            return self.data_orgs_boxes
        print("[WARNING] DATA ORGS DO NOT EXIST")

    def get_data_orgs_employees(self, list_orgs_indexes: list = [1], key_words_position: list = ["сотрудник"]):
        ''' получить данные о всех сотрудниках организаций
            list_orgs_indexes - список индексов организаций
            key_words_position - должности в качестве ключевых слов (по ним будут отбираться сотрудники)
        '''

        if (self.data_orgs_boxes != []):
            for i in list_orgs_indexes:
                if (i <= 0):
                    print('[WARNING] LIST ORGS INDEXES CONTAIN INVALID NUMS')
                    return

            # ссылка запроса для получения данных о всех организациях
            url_get_data_orgs_employees = self.url + DiadocApi.commands['get_data_orgs_employees']

            # заголовки запроса
            headers = {
                "Authorization": self.auth_token,
                "Content-Length": "1252",
                "Connection": "Keep-Alive",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            # получение данных по индексам
            data_orgs_employees = {}
            for org_index in set(list_orgs_indexes):
                data_org = {
                    "org_name": self.data_orgs_boxes[org_index][0],
                    "org_id": self.data_orgs_boxes[org_index][1]
                }
                for box in self.data_orgs_boxes[org_index][2]:
                    box_id = box["BoxId"]
                    box_title = box["Title"]

                    # параметры запроса
                    params = {
                        "boxId": box_id
                    }

                    # отправка запроса
                    try:
                        response = requests.request(
                            method='GET',
                            url=url_get_data_orgs_employees,
                            headers=headers,
                            params=params,
                            data=self.data_user_json
                        )
                        print(f"[INFO] STATUS CODE: {response.status_code}")

                        data_user_and_position = []
                        for empl in response.json()['Employees']:
                            data_user = empl["User"]
                            data_position = empl["Position"]
                            if (DiadocApi.compare_words(words_in=key_words_position, string=data_position)):
                                data_user_and_position.append({
                                    "position": data_position,
                                    "user": data_user
                                })

                        data_org["boxes"] = [{
                            'box_title': box_title,
                            'box_id': box_id,
                            'employees': data_user_and_position
                        }]

                        print("[INFO] DATA ORGS EMPLOYEES  WAS GOT")

                    except Exception:
                        raise "[ERROR] DATA ORGS EMPLOYEES  DO NOT EXIST"
                # запись полученных данных
                data_orgs_employees[org_index] = [data_org]

            # все данные получены
            self.data_orgs_employees = data_orgs_employees
            return self.data_orgs_employees
        print("[WARNING] DATA ORGS BOXES DO NOT EXIST")

    def save_data_orgs_json(self, dir: str = '', file_name: str = 'data_orgs'):
        ''' сохранение списка организаций в формате json '''

        if (self.data_orgs != []):

            # запись данных в json
            with open(dir+file_name+'.json', 'w', encoding='utf-8') as file:
                json.dump(self.data_orgs, file, ensure_ascii=False, indent=4)
                print("[INFO] DATA ORGS WAS SAVED\n"
                      f" ----- DIR: {dir}\n"
                      f" ----- FILE NAME: {file_name}")
            return
        print("[WARNING] DATA ORGS DO NOT EXIST")

    def save_data_orgs_boxes_json(self, dir: str = '', file_name: str = 'data_orgs_boxes'):
        ''' сохранение данные о ящиках всех организаций в формате json '''

        if (self.data_orgs != []):

            # запись данных в json
            with open(dir+file_name+'.json', 'w', encoding='utf-8') as file:
                json.dump(self.data_orgs_boxes, file, ensure_ascii=False, indent=4)
                print("[INFO] DATA ORGS BOXES WAS SAVED\n"
                      f" ----- DIR: {dir}\n"
                      f" ----- FILE NAME: {file_name}")
            return
        print("[WARNING] DATA ORGS DO NOT EXIST")

    def save_data_orgs_employees_json(self, dir: str = '', file_name: str = 'data_orgs_employees'):
        ''' сохранение данные о всех сотрудниках относящихся к ящику организации в формате json '''

        if (self.data_orgs_employees != []):

            # запись данных в json
            with open(dir+file_name+'.json', 'w', encoding='utf-8') as file:
                json.dump(self.data_orgs_employees , file, ensure_ascii=False, indent=4)
                print("[INFO] DATA ORGS EMPLOYEES  WAS SAVED\n"
                      f" ----- DIR: {dir}\n"
                      f" ----- FILE NAME: {file_name}")
            return
        print("[WARNING] DATA ORGS EMPLOYEES  DO NOT EXIST")

    def save_data_orgs_boxes_excel(self, dir: str = '', file_name: str = 'data_orgs_boxes'):
        ''' сохранение данные о ящиках всех организаций в формате excel '''

        if (self.data_orgs_boxes != []):
            # запись данных в excel
            workbook = Workbook()
            sheet = workbook.active
            sheet.append(['Название ящика'])

            for org_index in self.data_orgs_boxes:
                for box in self.data_orgs_boxes[org_index][2]:
                    sheet.append([box['Title']])

            sheet.title = file_name
            workbook.save(dir+file_name+'.xlsx')
            print("[INFO] DATA ORGS BOXES WAS SAVED\n"
                  f" ----- DIR: {dir}\n"
                  f" ----- FILE NAME: {file_name}")
            return
        print("[WARNING] DATA ORGS BOXES DO NOT EXIST")
        
    def save_data_orgs_employees_excel(self, dir: str = '', file_name: str = 'data_orgs_employees'):
        ''' сохранение данные о всех сотрудниках относящихся к ящику организации в формате excel '''

        if (self.data_orgs_employees != []):
            # запись данных в excel
            workbook = Workbook()
            del workbook['Sheet']
            for org_index in self.data_orgs_employees:
                for org_data in self.data_orgs_employees[org_index]:
                    sheet = workbook.create_sheet(org_data['boxes'][0]['box_title'])
                    sheet.append(['Фамилия', 'Имя', 'Отчество', 'Должность'])

                    employees = org_data['boxes'][0]['employees']
                    for empl in employees:
                        sheet.append([
                            empl['user']['FullName']['LastName'],
                            empl['user']['FullName']['FirstName'],
                            empl['user']['FullName']['MiddleName'],
                            empl['position']
                        ])

            workbook.save(dir+file_name+'.xlsx')
            print("[INFO] DATA ORGS EMPLOYEES WAS SAVED\n"
                  f" ----- DIR: {dir}\n"
                  f" ----- FILE NAME: {file_name}")
            return
        print("[WARNING] DATA ORGS EMPLOYEES DO NOT EXIST")


# if __name__ == '__main__':
#
#     url = 'https://diadoc-api-test.kontur.ru'
#     key = 'RATest-5347d365-7f18-4126-b5b6-e76ab0073563'
#     user_login = 'vvpikalov@rosatom.ru'
#     user_password = '1q2w3e$R%T^Y'
#
#     dapi = DiadocApi(url=url, key=key, user_login=user_login, user_password=user_password)
#     dapi.get_token()
#     dapi.get_data_orgs()
#     dapi.save_data_orgs_json(file_name='Организации')
#     dapi.get_data_orgs_boxes()
#     dapi.save_data_orgs_boxes_json(file_name='Ящики')
#     dapi.get_data_orgs_employees(list_orgs_indexes=[1,2])
#     dapi.save_data_orgs_employees_json(file_name='Сотрудники(1,2)')
#     dapi.save_data_orgs_boxes_excel(file_name='Ящики')
#     dapi.save_data_orgs_employees_excel(file_name='Сотрудники(1,2)')