from acitoolkit.acitoolkit import Session, Tenant
from acitoolkit_dir.conf import config_data


def del_tenant(tenant_name):
    session = Session(config_data.get('url'), config_data.get('login'), config_data.get('password'))
    resp = session.login()
    if not resp.ok:
        print('%% Could not login to APIC')

    tenant = Tenant(tenant_name)
    tenant.mark_as_deleted()

    resp = tenant.push_to_apic(session)
    if not resp.ok:
        print('%% Error: Could not push configuration to APIC')
        print(resp.text)


if __name__ == "__main__":
    del_tenant('test_t')