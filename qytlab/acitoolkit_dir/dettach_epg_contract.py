from acitoolkit.acitoolkit import Session, AppProfile, Tenant, EPG, Contract
from acitoolkit_dir.conf import config_data


def dettach_epg_provide_contract(tenant_name, ap_name, epg_name, provided_contract="", consumed_contract=""):
    session = Session(config_data.get('url'), config_data.get('login'), config_data.get('password'))
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    tenant = Tenant(tenant_name)
    ap = AppProfile(ap_name, tenant)
    epg = EPG(epg_name, ap)
    if provided_contract:
        provided_contract = Contract(provided_contract, tenant)
        epg.dont_provide(provided_contract)
    if consumed_contract:
        consumed_contract = Contract(consumed_contract, tenant)
        epg.dont_consume(consumed_contract)
    resp = tenant.push_to_apic(session)

    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)


if __name__ == "__main__":
    dettach_epg_provide_contract(config_data.get("tenant"),
                                 config_data.get("ap"),
                                 config_data.get("epg_list")[0].get("name"),
                                 config_data.get("epg_list")[0].get("provided"),
                                 config_data.get("epg_list")[0].get("consumed"),
                                )
