# -*-coding:utf-8-*-
import json

import requests

__author__ = "Allen Woo"

def api_request(url, json_params):

    url = "/api/admin/post?status=is_issued"
    headers = {"OSR-RestToken":"MDY4NTVmMDItMDA0ZS0xMWU4LWI3ZWMtMDAxYzQyNDYyOTM3",
               "OSR-ClientId": "osroomrest-8134154-0344-11e8-b7ec-001c42462937",
               "OSR-BearerToken":'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImxvZ2luX3RpbWUiOjE1MTcxMTE4NzQuOTg4OTY4NiwiY2lkIjoiNmI2NjRkYTItMDNkZi0xMWU4LWI3ZWMtMDAxYzQyNDYyOTM3IiwiaWQiOiI1YTI2OGFkNGM4OTgwNTc0NWUwMDRkNDUifSwiaXNzIjoib3Nyb29tIiwiaWF0IjoxNTE3MTExODc0LCJleHAiOjE1MTk3MDM4NzR9.F9tRHdWsBuK9prDMUUljhqjVGJcQ7fvy38wX15EGfBg'}

    url = "http://127.0.0.1:5000{}".format(url)
    custom_headers_response = requests.get(url, headers=headers,
                                           data=json_params)

    print(custom_headers_response.status_code)
    print(custom_headers_response.content.decode("utf-8"))
    print(custom_headers_response.cookies)
    print(custom_headers_response.headers)

def api_request_2(url, json_params):

    url = "/api/session/language-set"
    headers = {"OSR-RestToken":"MDY4NTVmMDItMDA0ZS0xMWU4LWI3ZWMtMDAxYzQyNDYyOTM3",
               "OSR-ClientId":"osroomrest-8134a154-0344-11e8-b7ec-001c42462937"}
    json_params = {"language":"en_US"}
    url = "http://127.0.0.1:5000{}".format(url)
    custom_headers_response = requests.put(url, headers=headers,
                                           data=json_params)

    print(custom_headers_response.status_code)
    print(custom_headers_response.content.decode("utf-8"))
    print(custom_headers_response.cookies)
    print(custom_headers_response.headers)



if __name__ == '__main__':
    api_request("", '{}')