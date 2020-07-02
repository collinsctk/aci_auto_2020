from acitoolkit.acitoolkit import Session, AppProfile, Tenant
from acitoolkit_dir.conf import config_data


def create_application_profile(tenant_name, ap_name):
    session = Session(config_data.get('url'), config_data.get('login'), config_data.get('password'))
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    tenant = Tenant(tenant_name)
    ap = AppProfile(ap_name, tenant)
    resp = tenant.push_to_apic(session)

    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)


if __name__ == "__main__":
    create_application_profile(config_data.get("tenant"), config_data.get("ap"))