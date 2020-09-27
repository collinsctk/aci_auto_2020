from qytlab.acitoolkit_dir.conf import config_data
from qytlab.acitoolkit_dir.create_application_profile import create_application_profile
from qytlab.acitoolkit_dir.del_application_profile import del_application_profile
from qytlab.acitoolkit_dir.del_tenant import del_tenant
from qytlab.acitoolkit_dir.create_epg import create_epg
from qytlab.acitoolkit_dir.attach_epg_contract import attach_epg_contract
from qytlab.restapi_dir.restapi_3_vm_domain_association import epg_domain_association
import time

ip = config_data.get('ip')
tenant = config_data.get('tenant')
ap = config_data.get("ap")
epg_list = config_data.get("epg_list")
bd = config_data.get("bd")
dvs = config_data.get("dvs")


def main():
    time.sleep(1)
    create_application_profile(tenant, ap)
    print('created new ap')
    time.sleep(1)
    for e in epg_list:
        create_epg(tenant, ap, e.get("name"), bd)
        print(f'created epg {e.get("name")}')
        time.sleep(1)
        if e.get("provided"):
            attach_epg_contract(tenant, ap, e.get("name"), provided_contract=e.get("provided"))
        time.sleep(1)
        if e.get("consumed"):
            attach_epg_contract(tenant, ap, e.get("name"), consumed_contract=e.get("consumed"))
        time.sleep(1)
        epg_domain_association(ip, tenant, ap, e.get("name"), dvs)
        print(f'association epg {e.get("name")} to dvs')
        time.sleep(1)


if __name__ == "__main__":
    # del_application_profile(tenant, ap)
    # print('deleted old ap')
    main()
