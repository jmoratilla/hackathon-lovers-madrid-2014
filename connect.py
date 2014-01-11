__author__ = 'jorge'

import requests



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

    response = requests.get(url + '/nodes/'+nodename+'/status', cookies=cookies,verify=False)

    print response.json()
