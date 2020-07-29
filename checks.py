#!/usr/bin/env python

""" Script to check VM creation on openstack """

import sys
import time
import paramiko
from novaclient import client
from keystoneauth1 import session
from keystoneauth1 import loading
from connection import auth
from utlis import print_values_ip

s = session.Session(auth)
nova_client = client.Client(2, session=s)


def crete_vm():
    global instance
    global group

    image = nova_client.images.find(name="centos7-1907")
    flavor = nova_client.flavors.find(name="m1.tiny")

    nova_client.security_groups.create(name="ssh", description="ssh rule")

    # group = nova_client.security_groups.find(name="ssh")
    # nova_client.security_group_rules.create(group.id, ip_protocol="tcp",
    #                                         from_port=22, to_port=22)

    group = nova_client.security_groups.find(name="ssh")
    security = nova_client.security_groups.get(group)

    instance = nova_client.servers.create(
        name="Test_VM", image=image, flavor=flavor, key_name="pk", security_group=security)

    status = instance.status
    while status == 'BUILD':
        time.sleep(5)
        instance = nova_client.servers.get(instance.id)
        status = instance.status

    if status == "ACTIVE":
        return True
    return False


def assing_ip():
    """ Assigns floating IPs"""
    floating_ip = ""
    list_of_ips = nova_client.floating_ips.list()

    # print(list_of_ips)

    for ip in list_of_ips:
        if ip.fixed_ip is None:
            floating_ip = ip.ip
            break

    if not floating_ip:
        floating_ip = nova_client.floating_ips.create("external")
        floating_ip = floating_ip.ip

    instance.add_floating_ip(floating_ip)

    return True


def terminate():
    """Deletes the VM and security group"""
    # servers_list = nova_client.servers.list()
    # print(servers_list)

    nova_client.servers.delete(instance)

    # nova_client.security_groups.delete(group)

    return True


if __name__ == "__main__":

    is_created = crete_vm()
    if is_created:
        print("created:1\n")

        if assing_ip():
            print("IP assigned:1\n")

        else:
            print("IP assigned:0\n")

    else:
        print("created:0\n")\

    # time.sleep(60)
    # is_connected = check_ssh()
    # if is_created:
    #     print("ssh is working")

    is_terminted = terminate()

    if is_terminted:
        print("terminate:1\n")

    else:
        print("terminate:0\n")
