from restapi_0_login import get_session, apic_host, my_headers
from qytlab.acitoolkit_dir.conf import config_data


def epg_domain_association(ip, tenant_name, ap_name, epg_name, dvs_name):
    request_url = f'https://{ip}/api/node/mo/uni/tn-{tenant_name}/ap-{ap_name}/epg-{epg_name}.json'
    session = get_session(ip)
    json_data = {"fvRsDomAtt":
                     {"attributes":
                          {"resImedcy": "immediate",
                           "tDn": f"uni/vmmp-VMware/dom-{dvs_name}",
                           "status": "created"},
                      "children":
                          [{"vmmSecP": {"attributes": {"status": "created"}, "children": []}}]
                      }
                 }
    result = session.post(request_url, headers=my_headers, json=json_data)
    return result.json()


if __name__ == "__main__":
    epg_domain_association(config_data.get("ip"),
                           config_data.get("tenant"),
                           config_data.get("ap"),
                           config_data.get("epg_list")[0].get("name"),
                           config_data.get("dvs"))
