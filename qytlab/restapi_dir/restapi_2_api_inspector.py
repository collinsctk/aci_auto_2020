#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a
from restapi_0_login import get_session, apic_host, my_headers


def create_tenant(ip, name):
    request_url = 'https://' + ip + '/api/node/mo/uni/tn-' + name + '.json'
    json_data = {"fvTenant":
                            {"attributes":{"dn":"uni/tn-" + name,
                                           "name":name,
                                           "rn":"tn-" + name,
                                           "status":"created"},
                             "children":[]}
                 }
    session = get_session(ip)
    result = session.post(request_url, headers=my_headers, json=json_data)

    return result.json()


def create_application_profiles(ip, tenant_name, app_profile_name):
    request_url = 'https://' + ip + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + app_profile_name + '.json'
    json_data = {"fvAp": {"attributes": {"dn": "uni/tn-" + tenant_name + "/ap-" + app_profile_name,
                                         "name": app_profile_name,
                                         "rn": "ap-" + app_profile_name,
                                         "status": "created"},
                          "children": []}
                 }
    session = get_session(ip)
    result = session.post(request_url, headers=my_headers, json=json_data)

    return result.json()


def create_epg(ip, tenant_name, app_profile_name, epg_name, bd_name):
    request_url = 'https://' + ip + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + app_profile_name + '/epg-' + epg_name + '.json'
    json_data = {"fvAEPg": {"attributes": {"dn": "uni/tn-" + tenant_name + "/ap-" + app_profile_name + "/epg-" + epg_name,
                                           "name": epg_name,
                                           "rn": "epg-" + epg_name,
                                           "status": "created"},
                            "children": [{"fvRsBd": {"attributes": {"tnFvBDName": bd_name,
                                                                    "status": "created,modified"},
                                                     "children": []}}]}}
    session = get_session(ip)
    result = session.post(request_url, headers=my_headers, json=json_data)

    return result.json()


def epg_add_contract(ip, tenant_name, app_profile_name, epg_name, contract_name, type):
    request_url = 'https://' + ip + '/api/node/mo/uni/tn-' + tenant_name + '/ap-' + app_profile_name + '/epg-' + epg_name + '.json'
    print(request_url)
    if type == 'Consumed':
        json_data = {"fvRsCons": {"attributes": {"tnVzBrCPName": contract_name,
                                                 "status": "created,modified"},
                                  "children": []}}
    elif type == 'Provided':
        json_data = {"fvRsProv": {"attributes": {"tnVzBrCPName": contract_name,
                                                 "status": "created,modified"},
                                  "children": []}}
    else:
        print("contract type error!!!")
    print(json_data)
    session = get_session(ip)
    result = session.post(request_url, headers=my_headers, json=json_data)

    return result.json()


if __name__ == '__main__':
    print(create_tenant(apic_host, 'a_qytang_final_t1'))
    print(create_application_profiles(apic_host, 'a_qytang_final_t1', 'qytang-ap'))
    print(create_epg(apic_host, 'a_qytang_final_t1', 'qytang-ap', 'web', 'default'))
    print(epg_add_contract(apic_host, 'a_qytang_final_t1', 'qytang-ap', 'web', 'sql', 'Consumed'))
