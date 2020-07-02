#!/usr/bin/env python3
# -*- coding=utf-8 -*-
# 本脚由亁颐堂现任明教教主编写，用于乾颐盾Python课程！
# 教主QQ:605658506
# 亁颐堂官网www.qytang.com
# 教主技术进化论拓展你的技术新边疆
# https://ke.qq.com/course/271956?tuin=24199d8a

from restapi_0_login import get_session, apic_host, my_headers, pprint_json

# ---------------class names---------------
# https://learninglabs.cisco.com/modules/intermediate-aci-prog/sbx-intermediate-aci-01_aci-api/step/1
# fvTenant = Tenant [tn-]
# fvCtx = VRF (this was originally called Context) [ctx-]
# fvBD = Bridge Domain [BD-]
# fvAp = Application [ap-]
# fvAEPg = Endpoint Groups [epg-]
# fvSubnet = Subnet [subnet-[x.x.x.x/x]]
# l3extOut = Layer 3 External Out


# Search by Class
def query_tenants(ip):
    request_url = 'https://' + ip + '/api/node/class/fvTenant.json?'
    session = get_session(ip)
    result = session.get(request_url, headers=my_headers)
    # print(result.text)
    return result.json()


def tenants_show(ip):
    tenants_list = query_tenants(ip)['imdata']
    for tenant in tenants_list:
        print(tenant['fvTenant']['attributes']['name'])


# Search by Class with filter
def tenant_show(ip, tenant_name):
    request_url = 'https://' + ip + '/api/node/class/fvTenant.json?query-target-filter=and(eq(fvTenant.name,"' + tenant_name + '"))'
    session = get_session(ip)
    result = session.get(request_url, headers=my_headers)
    return result.json()


def search_by_dn(ip, dn):
    request_url = 'https://' + ip + '/api/node/mo/' + dn + '.json'
    session = get_session(ip)
    result = session.get(request_url, headers=my_headers)
    return result.json()

# --------------------------Filter------------------------
# https://learninglabs.cisco.com/modules/intermediate-aci-prog/sbx-intermediate-aci-01_aci-api/step/3
# Operator	Description
# eq	Equal to
# ne	Not equal to
# lt	Less than
# gt	Greater than
# le	Less than or equal to
# ge	Greater than or equal to
# not	Logical inverse
# and	Logical AND
# or	Logical OR
# wcard	Wildcard

# https://learninglabs.cisco.com/modules/intermediate-aci-prog/sbx-intermediate-aci-01_aci-api/step/5
# query-target={self|children|subtree}
#   - self is the MO itself
#   - children is just the MO's child objects
#   - subtree contains the MO and its child objects

# target-subtree-class=[list of 1 or more subclassess of the MO]
#   - only returns child objects of the specified classes

# rsp-subtree={no|children|full}
#   - no is the default and the response does not include any children
#   - children will return only the child objects
#   - full includes the full tree structure

# query-target-filter=filter expression (this was reviewed above)

# rsp-prop-include={all|naming-only|config-only}
#   - all returns all properties of the objects
#   - all returns all properties of the objects
#   - config-only returns only properties that are configurable


def search_by_dn_filter(ip, dn, filter):
    request_url = 'https://' + ip + '/api/node/mo/' + dn + '.json' + filter
    session = get_session(ip)
    result = session.get(request_url, headers=my_headers)
    return result.json()


def tenant_children_show(ip, tenant_name):
    request_url = 'https://' + ip + '/api/node/mo/uni/tn-' + tenant_name + '.json?query-target=children'
    print(request_url)
    session = get_session(ip)
    result = session.get(request_url, headers=my_headers)
    return result.json()


if __name__ == '__main__':
    # pprint_json(query_tenants(apic_host))
    tenants_show(apic_host)
    # pprint_json(tenant_show(apic_host, "Heroes"))
    # pprint_json(search_by_dn(apic_host, "uni/tn-Heroes/ap-Save_The_Planet/epg-app"))
    # pprint_json(search_by_dn(apic_host, "uni/tn-Heroes/ap-Save_The_Planet/epg-web"))
    # pprint_json(search_by_dn_filter(apic_host, "uni/tn-Heroes", '?query-target=children'))
    # pprint_json(tenant_children_show(apic_host, "Heroes"))

