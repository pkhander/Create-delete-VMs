def print_values_ip(ip_list):
    for ip in ip_list:
        print("-"*35)
        print("fixed_ip : %s" % ip.fixed_ip)
        print("id : %s" % ip.id)
        print("instance_id : %s" % ip.instance_id)
        print("ip : %s" % ip.ip)
        print("pool : %s" % ip.pool)
