import sys
import logging
import json

from acitoolkit_dir.acitoolkit import Tenant, Context,BridgeDomain,AppProfile, NetworkPool
from acitoolkit_dir.acitoolkit import L2Interface,Session,EPGDomain, PhysDomain, EPG, Interface


logging.basicConfig(
    level=logging.INFO, format='%(asctime)s|%(levelname)s|%(message)s')
logger = logging.getLogger("NEW_Tenant")
#logger.setlevel(Logging.INFO)


CONFFILE='conf.py'
DESCRFILE='descr.json'

def main():

    # load config
    # Configuration parameters will be in conf dictionary
    with open(CONFFILE, 'r') as r:
        conf = json.loads(r.read())

    #login to apic
    session = Session(conf['url'],conf['login'],conf['password'])
    resp=session.login()
    if not resp.ok:
        print('%% Could not login to APIC')
        return
        sys.exit(0)

	#Remove existing Tenant with the specified name if it exists
    tenant = Tenant(conf['tenant'])
    tenant.mark_as_deleted()
    resp = tenant.push_to_apic(session)
    if resp.ok:
        logger.info('Successfully Deleted existing Tenant:{}'.format(tenant.name))

    ###create physical Domain
    dom = PhysDomain(name=conf['domain'],parent=None)
    # vlanpool = NetworkPool(name=conf['pool_name'], encap_type=conf['pool_encap_type'],start_id=conf['pool_start'], end_id=conf['pool_end'],mode=conf['pool_mode'])
    # resp = session.push_to_apic(vlanpool.get_url(),vlanpool.get_json())
    # if not resp.ok:
    #     logger.error("!! Could not create VLAN pool:{}!!".format(vlanpool.name))
    #     sys.exit(0)
    #
    # dom.attach(vlanpool)
    resp = dom.push_to_apic(session) ### create domain on APIC (AEEP should be created alredy
    if resp.ok:
        logger.info("successfully created Domain:{}".format(dom.name))

    #create a tenant
    tenant = Tenant(conf['tenant'])

    #Create a VRF as unenforced
    vrf = Context(conf['vrf'], tenant)
    vrf.set_allow_all()

    #Fetch Domain
    dom = EPGDomain.get_by_name(session, conf['domain'])

    #Create an app profile
    ap = AppProfile(conf['ap'],tenant)
    resp = tenant.push_to_apic(session)
    if resp.ok:
        logger.info("successfully created Tenant: {}".format(tenant.name))
        logger.info("successfully created VRF: {}".format(vrf.name))
        logger.info("successfully created Application profile:{}".format(ap.name))

    #README: Related to question 2
    #Load all EPG descriptions
    with open(DESCRFILE, 'r') as r:
        descr = json.loads(r.read())
	
	
    #Loop MAXVLANS time to create BDS and EPGs
    #for i in range (MAXVLANS):
    MAXVLANS = 251
    for i in range (201,MAXVLANS):
    
        #Create BridgeDomain

        bdname = "{}-{}".format(conf['bd_prefix'],i)

        bd = BridgeDomain(bdname,tenant)

        bd.add_context(vrf)

        logger.info("Addes BD:{} to Tenant:{}".format(bd.name,tenant.name))
        #create EPG
        epgname = "{}-{}".format(conf['epg_prefix'],i)
        epg = EPG(epgname, ap)
        epg.descr = descr[epgname]['epg_descr']
        epg.attach(bd)
        logger.info("Attached EPG:{} to BD:{}".format(epg.name,bd.name))

        #attach the EPG to 2 interface using correct VLAN as the encap
        
        intf1 = Interface('eth','1', '103', '1' ,'33')
        intf2 = Interface('eth','1', '102', '1' ,'33')
        vlan = i
        logger.info("VLAN:{}".format(vlan))
        l2intf1 = L2Interface('l2int1', 'vlan', str(i))
        l2intf1.attach(intf1)
        epg.attach(l2intf1)

        l2intf2 = L2Interface('l2int2', 'vlan', str(i))
        l2intf2.attach(intf2)
        epg.attach(l2intf2)
        
        epg.add_infradomain(dom)
        #print sufix
    #dump the necessary configuration
    logger.info("URL:" +(tenant.get_url()))
    logger.info("JSON:" +  str(tenant.get_json()))
    resp = tenant.push_to_apic(session)
    if resp.ok:
        logger.info("Response code :{}".format(resp))
        logger.info("successully deployed configuration change")
    else:
        logger.error("Error deploying configuration changes")
        logger.error("Response is :{}".format(resp))

if __name__ == '__main__':
    main()









