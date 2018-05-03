import time

import allure
import requests

from app import app

url = 'http://localhost:5000'
OK = 200
FOUND = 302
NOT_FOUND = 404
NOT_ALLOWED = 405
ERROR = 500
req_session = requests.Session()
client = app.test_client()
owner = app.test_client()


@allure.feature('API')
def test_registration():
    curr_time = str(int(time.time()))
    registration_data = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time + '@inno.ru',
                         'password': curr_time, 'password_confirmation': curr_time, 'telephone': curr_time}
    registration_data_broken_pass = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time + '11@inno.ru',
                                     'password': curr_time, 'password_confirmation': '111', 'telephone': curr_time}
    registration_data_broken_email = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time,
                                      'password': curr_time, 'password_confirmation': curr_time, 'telephone': curr_time}
    with allure.step('Registration new user'):
        register_url = f'{url}/register'
        req = client.post(register_url, data=registration_data)
        assert req.status_code == FOUND
        assert 'index' in req.location

    with allure.step('Registration with different password and confirm password'):
        req = client.post(register_url, data=registration_data_broken_pass)
        assert req.status_code == OK

    with allure.step('Registration new user with the same email'):
        req = client.post(register_url, data=registration_data)
        assert req.status_code == FOUND
        assert 'register' in req.location

    with allure.step('[NEGATIVE]: empty fields'):
        req = client.post(register_url, data={})
        assert req.status_code == OK
        assert req.location is None

    with allure.step('[NEGATIVE]: missed fields'):
        req = client.post(register_url, data={'first_name': curr_time})
        assert req.status_code == OK
        assert req.location is None

    with allure.step('[NEGATIVE]: broken email'):
        req = client.post(register_url, data=registration_data_broken_email)
        assert req.status_code == FOUND
        assert 'index' in req.location

    with allure.step('Logout'):
        logout_url = f'{url}/logout'
        req = client.post(logout_url, data=registration_data)
        assert req.status_code == NOT_ALLOWED

    with allure.step('Login'):
        login_url = f'{url}/login'
        req = client.post(login_url, data=registration_data)
        assert req.status_code == FOUND
        assert 'index' in req.location


@allure.feature('API')
def test_index_accessibility():
    with allure.step('Index page accessibility'):
        assert req_session.get(f'{url}').status_code == OK
        assert req_session.get(f'{url}/').status_code == OK
        assert req_session.get(f'{url}/index').status_code == OK
    with allure.step('[NEGATIVE]: unexisting link'):
        assert req_session.get(f'{url}/abracadabra').status_code == NOT_FOUND


@allure.feature('API')
def test_hotel_searching():
    request_data = {'destination': 'e', 'checkin': '02-05-2018', 'checkout': '03-05-2018', 'is_bathroom': False,
                    'is_tv': False, 'is_wifi': False, 'is_bathhub': False, 'is_airconditioniring': False,
                    'sleeps': 1, 'price_from': 0, 'price_to': 0, 'quantity': 1}
    with allure.step('Hotel searching'):
        search_url = f'{url}/'
        req = client.post(search_url, data=request_data)
        assert req.status_code == FOUND
        assert 'search-hotel' in req.location

    with allure.step('Search hotel'):
        search_url = f'{url}/search-hotel'
        hotel_id_data = {'hotel_id': '1'}
        req = client.post(search_url, data=hotel_id_data)
        assert req.status_code == FOUND
        assert 'more-info' in req.location

    with allure.step('Search hotel'):
        req = client.get(search_url)
        assert req.status_code == OK


# # TODO
# @allure.feature('API')
# def test_more_info():
#     request_data = {'destination': 'e', 'checkin': '02-05-2018', 'checkout': '03-05-2018', 'is_bathroom': False,
#                     'is_tv': False, 'is_wifi': False, 'is_bathhub': False, 'is_airconditioniring': False,
#                     'sleeps': 1, 'price_from': 0, 'price_to': 0, 'quantity': 1, 'hotel_id': '2'}
#
#     with allure.step('Search hotel by id'):
#         search_url = f'{url}/search-hotel/2'
#         req = client.post(search_url, data=request_data)
#         assert req.status_code == FOUND
#         assert 'login' in req.location
#
#     with allure.step('Search hotel by id'):
#         search_url = f'{url}/search-hotel/2'
#         hotel_id_data = {'hotel_id': '1'}
#         req = client.post(search_url, data=hotel_id_data)
#         assert req.status_code == FOUND
#         assert 'login' in req.location
curr_time = str(int(time.time()))
owner_data = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time + '@inno.ru',
              'password': curr_time, 'password_confirmation': curr_time, 'telephone': curr_time}
owner_data_broken_pass = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time + '@inno.ru',
                          'password': curr_time, 'password_confirmation': '11', 'telephone': curr_time}
owner_data_existing_email = {'first_name': curr_time, 'last_name': curr_time, 'email': curr_time + '@inno.ru',
                             'password': curr_time, 'password_confirmation': curr_time, 'telephone': curr_time}


@allure.feature('API')
def test_add_property():
    url_link = f'{url}/add-property'
    with allure.step('Add property with broken password'):
        req = owner.post(url_link, data=owner_data_broken_pass)
        assert req.status_code == OK

    with allure.step('Add property with same email'):
        req = owner.post(url_link, data=owner_data_existing_email)
        assert req.status_code == FOUND
        assert 'add-property' in req.location

    with allure.step('Add property success'):
        req = owner.post(url_link, data=owner_data)
        assert req.status_code == FOUND
        assert 'add-property' in req.location

    with allure.step('[NEGATIVE]'):
        pass


@allure.feature('API')
def test_get_profile():
    with allure.step('Get person`s profile'):
        profile_url = f'{url}/profile'
        req = owner.get(profile_url, data=owner_data)
        assert req.status_code == OK


@allure.feature('API')
def test_update_profile():
    with allure.step('Update person`s profile'):
        profile_url = f'{url}/profile'
        req = owner.post(profile_url, data=owner_data)
        assert req.status_code == FOUND
        assert 'index' in req.location


@allure.feature('API')
def test_my_hotels():
    with allure.step('Get owners`s hotels: POST'):
        hotel_url = f'{url}/my-hotel'
        req = owner.post(hotel_url, data=owner_data)
        assert req.status_code == FOUND

    with allure.step('Get owners`s hotels: GET'):
        hotel_url = f'{url}/my-hotel'
        req = owner.get(hotel_url, data=owner_data)
        assert req.status_code == FOUND


@allure.feature('API')
def test_add_hotel():
    with allure.step('Add hotel'):
        add_hotel_url = f'{url}/add-hotel'


@allure.feature('API')
def test_edit_hotel():
    pass


@allure.feature('API')
def test_manage_hotel():
    pass


@allure.feature('API')
def test_my_booking():
    pass


@allure.feature('API')
def test_manage_booking():
    pass


@allure.feature('API')
def test_new_booking():
    pass


@allure.feature('API')
def test_admin():
    pass
