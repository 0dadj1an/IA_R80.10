#!/bin/python

'''
This code is for Check Point R80.10 IA API testing
@author: ivohrbacek@gmail.com / ivo.hrbacek@ixperta.com
'''


import pprint
import json
import requests
import urllib3
import socket




class Connector():
    
    def __init__(self, url, command, payload):
        
         self.url = url
         self.command = command
         self.payload = payload  

         self.headers = {
             'content-type': "application/json",
              'Accept': "*/*",
              }
        
    def call_api(self):
        urllib3.disable_warnings()
        try:

            responce = requests.post(self.url+self.command, json=self.payload, headers=self.headers, verify=False)
            a = responce.json()
            print (a)
        except json.decoder.JSONDecodeError:
            print("some parameters are wrong")     



def get_ipv4_from_machine():
        try:
            from netifaces import interfaces, ifaddresses, AF_INET # important for get_ipv4_from_machine()
            addresses = []
            for interface in interfaces():
                config = ifaddresses(interface)
                # AF_INET is not always present
                if AF_INET in config.keys():
                    for link in config[AF_INET]:
                        # loopback holds a 'peer' instead of a 'broadcast' address
                        if 'addr' in link.keys() and 'peer' not in link.keys():
                            addresses.append(link['addr']) 
            return addresses
        except ImportError:
            print ("issue with getting IP addresses")



def main():

    url= 'https://10.10.0.5/_IA_API/'
    payload_list_common= {
                    "shared-secret":"m9C3Hkp1W5",
                    "user":"ivos",
                    "machine":"ivoslaptop",
                    "fetch-user-groups":0,
                    "fetch-machine-groups":0,
                    "machine-os":"Windows 7 ",
                    "domain":"test.com",
                    "user-groups": ["MyUserGroup"],
                    "roles":[""],
                    "calculate-roles":1,
                    "identity-source":"Python API Client"
                    }  

    a=get_ipv4_from_machine()

    for item in a:
        if item != '127.0.0.1':
            payload_list_common['ip-address'] = item
            connect = Connector(url, 'add-identity', payload_list_common)
            connect.call_api()
            payload_list_common['ip-address'] = ""
    
    #print (locals())
            
        
    
if __name__ == "__main__":
    main()

        
        
