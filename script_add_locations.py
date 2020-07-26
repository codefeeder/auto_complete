import requests
import argparse


def get_token():
    url = 'http://127.0.0.1:8000/api/login'
    request_data = {'username': 'siddharth',
                    'password': '12345'}
    response = requests.post(url, data=request_data)
    return response.text


def add_locations(filename, url='http://127.0.0.1:8000/add'):
    file = open(filename, "r+")
    locations = file.readlines()
    file.close()
    token = get_token().split(':')[-1][1:-2]
    headers = {'authorization': 'token ' + token}
    for location in locations:
        location_name = location.split(' ')[-1][:-1].replace('_', ' ')
        request_data = {'location': location_name,
                        'popularity': location.split(' ')[0]}
        response = requests.post(url, data=request_data, headers=headers)
        print(location_name + '-' + response.text)


parser = argparse.ArgumentParser()
parser.add_argument('--file', default='location_cnt.txt', type=str, help='Input locations file')
args = parser.parse_args()
add_locations(filename=args.file)

