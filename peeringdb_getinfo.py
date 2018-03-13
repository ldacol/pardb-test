#! /usr/bin/env python
# Module: 		peeringdb_getinfo.py
# Usage:		python peeringdb_getinfo.py <asn>
# Author:		ldacol
# Release Verson: 	1.0
# Release Date: 	03.11.2018

from urllib.request import urlopen, HTTPError
from json import loads
import sys
import MySQLdb
import json

def peeringdb_getinfo(pdp_type, pdp_asn, pdp_id):
    pdb_url = 'https://peeringdb.com/api/%s?%s=%s'% (pdp_type,pdp_asn, pdp_id)

    try :
        result_json = urlopen(pdb_url).read().decode('utf8')
        result_dict = json.loads(result_json)
    except HTTPError as err:
        if err.code == 404:
            return None
    return result_dict

if __name__ == '__main__' :
    as_num = sys.argv[1]

    # connect to the database
    db = MySQLdb.connect(host="localhost",  user="ubuntu", passwd="1111", db="peeringdb")

    # create a cursor for the database
    cur = db.cursor()


    # get company and AS information
    as_info_dict = peeringdb_getinfo('net', 'asn', as_num)
    # print as_info_dict
    company_name = as_info_dict["data"][0]["name"]
    company_website = as_info_dict["data"][0]["website"]

    print (as_num)
    print (company_name)
    print (company_website)

    print ('-'*20)

    as_netixlan_dict = peeringdb_getinfo('netixlan', 'asn', as_num)
    ix_name_list = []
    ix_name_list_sorted = []
    ix_speed = []
    ix_speed_tot = 0

    for netixlan_set in as_netixlan_dict["data"]:
        ixlan_id = netixlan_set["ixlan_id"]
        ipaddr4 = netixlan_set["ipaddr4"]
        ipaddr6 = netixlan_set["ipaddr6"]
        ix_name = netixlan_set["name"]
        ix_speed.append (netixlan_set["speed"])
        ix_name_list.append(ix_name)
        ix_speed_tot = ix_speed_tot + netixlan_set["speed"]

        try:
            cur.execute("""INSERT INTO peeringdbweb_peeringdbnodes (companyname,asn,peeringnode,ipv4addr,ipv6addr) VALUES (%s,%s,%s,%s,%s)""",(company_name,as_num,ix_name,ipaddr4,ipaddr6))
            db.commit()
        except MySQLdb.Error as error:
            print(error)
            db.rollback()              #rollback transaction here

        print (ix_name)
        print (ipaddr4)
        print (ipaddr6)
        print ('-'*20)
    ix_name_list_sorted = sorted (set (ix_name_list))
    print ('Total peerings:',len(ix_name_list))
    print ('Total unique organization peerings:', len (ix_name_list_sorted))
    print ('Total Aggregate speed:',sum (ix_speed))
    print ('Total Aggregate speed:',ix_speed_tot)

    cur.close()
    db.close()
