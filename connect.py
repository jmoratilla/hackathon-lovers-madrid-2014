__author__ = 'jorge'

import requests
import time
import plotly

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
x_dim = []
samples = 60
interval = 0.5

vm_info=[]
host_info=[]

# py = plotly.plotly(username='username', key='api_key')
py = plotly.plotly('jmoratilla','111slefsy7')

def get_info_vm(nodename,vmid):
    response = requests.get(url + '/nodes/'+nodename+'/openvz/'+str(vmid)+'/status/current', cookies=cookies,verify=False)
    data = response.json()
    vm_info.append(data['data']['cpu'])

def get_info_host(nodename):
    response = requests.get(url + '/nodes/'+nodename+'/status', cookies=cookies,verify=False)
    data = response.json()
    host_info.append(data['data']['cpu'])


for i in range(samples):
    get_info_host(nodename)
    get_info_vm(nodename,102)
    x_dim.append(i)
    time.sleep(interval)

x_dim = [e*interval for e in x_dim]

line1 = {'x':x_dim,'y':host_info,"type":"scatter", "name":"host",
         "line":{"color":"rgb(3,78,123)", "width":6, "dash":"dot"},
         "marker":{"opacity":1.0,"symbol":"square", "size":12,"color":"rgb(54,144,192)",
                   "line":{"width":3, "color":"darkblue"}}}

line2 = {'x':x_dim,'y':vm_info,"type":"scatter", "name":"vm1",
         "line":{"color":"rgb(123,78,3)", "width":6, "dash":"dot"},
         "marker":{"opacity":1.0,"symbol":"square", "size":12,"color":"rgb(54,144,192)",
                   "line":{"width":3, "color":"darkred"}}}

# plot the line
py.plot([line1,line2])
