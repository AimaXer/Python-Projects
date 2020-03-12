import requests
import json
import xmltodict
import collections

key_value_list = []

def check_if_key_exists(key, dict):
    if str(key) in dict:
        return True
    else:
        return False

with open('dsa_vars.xml', 'r') as f:
    xml_content = f.read()

json_content = xmltodict.parse(xml_content, encoding="UTF-8")
# print(str(json.dumps(json_content, indent=4, sort_keys=False)))

for obj in json.loads(json.dumps(json_content, indent=4, sort_keys=False))['arrayList']['Semaphore']:
    if check_if_key_exists('@id', obj):
        if check_if_key_exists('@value', obj):
            key_value_list.append([obj['@id'], obj['@value'], obj['@semaphoreType'], obj['@semaphoreVariableType'], obj['@tags'], obj['@dateFormat'], obj['@timeZone'], obj['@totalPermits'], obj['@domain']])
        else:
            key_value_list.append([obj['@id'], '', obj['@semaphoreType'], obj['@semaphoreVariableType'], obj['@tags'], obj['@dateFormat'], obj['@timeZone'], obj['@totalPermits'], obj['@domain']])

for i, key_value_pair in enumerate(key_value_list):
    found = False
    if '[DD]' not in key_value_pair[0]:
        if '[D]' not in key_value_pair[0]:
            tmp = key_value_pair[1].replace(':', '.')
            x = [a for a in tmp.split('.') if a]
            tmp = '.'.join(x[1:]).replace(']', '')
            for key_value_pair_2 in key_value_list:
                if str(key_value_pair[0] + '.') in key_value_pair_2[0]:
                    key_value_pair_2[0] = key_value_pair_2[0].replace(str('.' + '.'.join([a for a in key_value_pair[0].split('.') if a][-1:]) + '.'), str('.[' + tmp + '].'))
                    found = True
            
            if found:
                del key_value_list[i]

session = requests.Session()
domain = 'TEST_DOMAIN'
hdrs_get = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'User-Agent': 'Mozilla/5.0'}
url = 'http://10.0.0.22:8080/scheduleIn'

session.post(url + "/j_spring_security_check", data={'j_username': 'Administrator', 'j_password': 'i2010#'}, verify=False, headers=hdrs_get)
session.post(url + "/domain/setCurrentDomain", data={"id": domain}, verify=False, headers=hdrs_get)

for obj in key_value_list:
    payload = {
        'semaphoreType' : str(obj[2]),
        'semaphoreVariableType' : str(obj[3]),
        'tags': str(obj[4]),
        'value' : str(obj[1]),
        'dateFormat': str(obj[5]),
        'timeZone': str(obj[6]),
        'totalPermits': str(obj[7]),
        'id': str(obj[0]).replace('[' + str(obj[8]) + ']', ''),
        'description': ''
    }
    session.post(url + '/semaphore/create', data=payload, verify=False, headers=hdrs_get)

# for pair in key_value_list:
    # print(str(pair[0] + ' --- ' + pair[1] + '\n'))