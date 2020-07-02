from acitoolkit.acitoolkit import Session, AppProfile, Tenant, EPG, BridgeDomain
from acitoolkit_dir.conf import config_data


def del_epg(tenant_name, ap_name, epg_name, bd_name):
    session = Session(config_data.get('url'), config_data.get('login'), config_data.get('password'))
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    tenant = Tenant(tenant_name)
    ap = AppProfile(ap_name, tenant)
    bd = BridgeDomain(bd_name, tenant)
    epg = EPG(epg_name, ap)
    epg.mark_as_deleted()
    resp = tenant.push_to_apic(session)

    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)


if __name__ == "__main__":
    del_epg(config_data.get("tenant"),
            config_data.get("ap"),
            config_data.get("epg_list")[0].get("name"),
            config_data.get("bd"))
