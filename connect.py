__author__ = 'jorge'

import requests
import time


class Configuration(object):
    username = 'root'
    password = 'cangetin'
    realm    = 'pam'
    url      = 'https://192.168.253.110:8006/api2/json'
    nodename = 'pve-1'
    storage  = 'local'

    auth = {'username': username, 'realm': realm, 'password': password}
    response = requests.post(url + '/access/ticket',data=auth,verify=False)

    data = response.json()
    token = data['data']['ticket']
    cookies = {'PVEAuthCookie': token.replace(':','%3A').replace('=','%3D')}
    csrf_prevention_token = data['data']['CSRFPreventionToken']
    print 'cookie: ',cookies

    #auth_params = { 'CSRFPreventionToken': csrf_prevention_token, 'cookie': cookie}

    time_array = []
    samples = 10
    interval = 1
    for i in range(samples):
        response = requests.get(url + '/nodes/'+nodename+'/openvz/102/status/current', cookies=cookies,verify=False)
        data = response.json()
        time_array.append(data['data']['cpu'])
        time.sleep(interval)

    print time_array