from f5.bigip import ManagementRoot
from f5.utils.responses.handlers import Stats
import certifi
import urllib3
import requests
import re

##Below line with ignore certificate errors ##

from requests.packages.urllib3.exceptions import InsecureRequestWarning

##Below lines will open the text file with the node names and store the values in a list##

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
x_file = open('nodes.txt', 'r')
r=list()
s=list()
for i in x_file:
    i=i.split('\n',1)[0]
    r.append(i)
#print r
# Connect to the BigIP
mgmt = ManagementRoot("ip_address", "username", "password")


##Below lines will take the values in the list above, get corresponding Pool and member name and store them as Key value pairs in a dictionary##

dict={}
pools = mgmt.tm.ltm.pools.get_collection()
for pool in pools:
#    print pool.name
     test=list()
     s=list()
     for i in r:
         for member in pool.members_s.get_collection():
             if i not in member.name: continue
             else: 
                 if '-10.' in member.name: continue
                 else: test.append((member.name).encode("utf-8"))
                 dict[pool.name]=test         

##Below lines will print the Pool and pool member names and also, disable/enable the pool members. 'user-enabled' can be changed to 'user-disabled' if pool members needs to be disabled##

for k,v in dict.items():

   print k,v
   
   update_pool = mgmt.tm.ltm.pools.pool.load(partition='Common', name=k)
   for i in v:
       update_pool_member = update_pool.members_s.members.load(partition='Common', name=i) 
       update_pool_member.session = 'user-enabled'
#       update_pool_member.description = 'modified through f5-python-SDK'
       update_pool_member.update()
#       b=Stats(update_pool_member.stats.load())
#       print i
#       print (b.stat.status_availabilityState)
#        for i in b:
#              print i
#        print b
