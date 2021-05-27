def config_render():
    import sys,yaml,json
    from jinja2 import FileSystemLoader, StrictUndefined
    from jinja2.environment import Environment
    from pathlib import Path
    env = Environment(undefined=StrictUndefined)
    env.loader = FileSystemLoader([".", './templates/', './templates/dev_spec', './templates/feat_spec'])
    
    # check subdirectory exists otherwise create it:
    Path("./config/").mkdir(exist_ok=True)
    #
    # nb wrt above: the previous options used "os.path.exists" /or "os.makedirs" are
    # susceptible to race condition. 
    # Path("./config/").mkdir(parents=True, exist_ok=True) #Parents=True only required
    # where multiple subdirectoriess need to be created.
    
    # Provide exception handling if the path to variables is incorrectly specified:
    try:
        vars = sys.argv[1]
        #dut = sys.argv[2]  #this was used to nominate the <dut>
    except IndexError:
        raise SystemExit(f"\n\tUsage: {sys.argv[0]} ./vars/<site_specific_vars_filename> <dut>\n")
    
    # import data containing platform specific yaml config parameters:
    with open(vars) as f:
        platf_spec_vars = yaml.load(f)
    print() #provides separation for the logging generated below
    
    # compile a dictionary to iterate over to produce output configs:
    #
    site_dict = {
        "p_ce": 'ce' + platf_spec_vars['p_ce_hnn'],
        "s_ce": 'ce' + platf_spec_vars['s_ce_hnn'],
        "p_dr": 'dr' + platf_spec_vars['p_dr_hnn'],
        "s_dr": 'dr' + platf_spec_vars['s_dr_hnn'],
        "p_al": 'al' + platf_spec_vars['p_al_hnn'],
        "s_al": 'al' + platf_spec_vars['s_al_hnn']
        }
    # function acronyms used in above host filenames:
    # ce = MPLS core facing customer edge where p = primary, s = sec
    # dr = distribution router (L3)
    # al = access-layer switch (L2)
    
    # import device specific mgmt-vrf config:
    with open ("./vars/mgmt_vrf_dict_dict.json") as f:
        mgmt_dict=json.load(f)

    template_vars = {
        "mgmt_dict": mgmt_dict,
    }
    template_file = "p_ar_mgmt_config.j2"
    template = env.get_template(template_file)
    output = template.render(**template_vars)
    print(output)

    for k,v in site_dict.items():
        with open("./config/{}.config".format(v), "w") as g:
            template_file = k + '_master.j2'
            t = env.get_template(template_file)
            g.write(t.render(**platf_spec_vars))
            print("\tConfiguration for {} in site {} has been written to ./config/".format(v,platf_spec_vars['snn']))
    print("\n\tCompilation of all configuration is complete.\n")

def scp_config():
    # this function used netmiko inbuilt function to change software 
    # version (which also validates md5 checksum)
    return

def verify_config_defaults():
    # this function checks whether any previous config has been rejected 
    # and/or whether config defaults have changed since ios-xe up/dowwngrade.
    return

def config_replace():
    # first backup target device existing config to flash
    # ssh_conn.send_command("copy runn flash:<unix_tick_runn_conf")
    # then execute config replace
    return

  def config_rollback():
    # first backup target device existing config to flash
    # ssh_conn.send_command("copy runn flash:<unix_tick_runn_conf")
    # then execute config replace
    return

def q_in_q_underlay():
    # L2 tunnel vlan changes required to build the required site topology
    return

def site_is_up():
    # verify rapdi-pvst, hsrp, ospf, pim and bgp adjacencies, then generate
    # STC unicast/multicast traffic and analyse Rx counters
    return

def main():
    config_render()

if __name__ == '__main__':
    main()
