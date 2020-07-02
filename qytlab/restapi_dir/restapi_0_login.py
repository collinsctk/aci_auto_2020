#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
import requests
import urllib3
import json
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from qytlab.acitoolkit_dir.conf import config_data
username = config_data.get('login')
password = config_data.get('password')

apic_host = config_data.get('ip')

my_headers = {"content-type": "application/json"}


def get_session(ip):
    client = requests.session()
    login_url = 'https://' + ip + '/api/aaaLogin.json'
    name_pwd = {'aaaUser': {'attributes': {'name': username, 'pwd': password}}}
    client.post(login_url, json=name_pwd, headers=my_headers, verify=False)
    return client


dict_data = {'totalCount': '1', 'imdata': [{'fvTenant': {'attributes': {'childAction': '', 'descr': '', 'dn': 'uni/tn-Heroes', 'extMngdBy': '', 'lcOwn': 'local', 'modTs': '2018-11-29T13:29:29.152+00:00', 'monPolDn': 'uni/tn-common/monepg-default', 'name': 'Heroes', 'nameAlias': '', 'ownerKey': '', 'ownerTag': '', 'status': '', 'uid': '15374'}}}]}


def pprint_json(json_data):
    print(json.dumps(json_data, indent=4, sort_keys=True))


if __name__ == "__main__":
    print(get_session(apic_host))
    # pprint_json(dict_data)