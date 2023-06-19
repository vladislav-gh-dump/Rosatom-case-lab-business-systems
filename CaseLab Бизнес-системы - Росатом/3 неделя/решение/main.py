from diadoc_api import DiadocApi

def main():
    url = 'https://diadoc-api-test.kontur.ru'
    key = 'RATest-5347d365-7f18-4126-b5b6-e76ab0073563'
    user_login = 'vvpikalov@rosatom.ru'
    user_password = '1q2w3e$R%T^Y'

    # получение токена
    dapi = DiadocApi(url=url, key=key, user_login=user_login, user_password=user_password)
    # dapi.get_token()

    # получение данных об организациях
    dapi.get_data_orgs()
    dapi.save_data_orgs_json(file_name='Организации')

    # получение данных обо всех ящиках организаций из полученных данных
    dapi.get_data_orgs_boxes()
    dapi.save_data_orgs_boxes_json(file_name='Ящики')

    # получение всех сотрудников организаций (организации-[1, 2], должность-"администратор")
    dapi.get_data_orgs_employees(list_orgs_indexes=[1, 2], key_words_position=["администратор"])
    dapi.save_data_orgs_employees_json(file_name='Сотрудники(1,2)')

    # запись данных в excel
    dapi.save_data_orgs_boxes_excel(file_name='Ящики')
    dapi.save_data_orgs_employees_excel(file_name='Сотрудники(1,2)')


if __name__ == '__main__':
    main()
