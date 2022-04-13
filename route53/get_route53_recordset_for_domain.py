#
#   Author : Yogesh Agrawal
#
#   License Agrement : Apache License
#
#   Disclaimer : Script is used for demostration purpose. Review before deploying in production
#
#   Access need : DNS hostzone list and DNS recordset list permission is needed


import boto3
import pandas as pd 

## Add actual domain name
zone_domain = "cloudtechsavvy.com"





def get_record_details(response):
    """
    This will parse all all records. 
    Only Alias, A record, CNAME, and TXT record is added with this  
    """
    #print(response)
    domain_name = ""
    for i in response:
        if i["Type"] == "NS":
            domain_name = i["Name"]
            domain_name = "." + domain_name
            break

    skiped_record = []
    for i in response:
        if i["Type"] == "A":
            if 'AliasTarget' in i.keys():
                print(f"{i['Name'].replace(domain_name,'')} 86400 IN CNAME {i['AliasTarget']['DNSName']}")
            else:
                print(f"{i['Name'].replace(domain_name,'')} 86400 IN A {i['ResourceRecords'][0]['Value']}")
        elif i["Type"] == "CNAME":
            print(f"{i['Name'].replace(domain_name,'')} 86400 IN {i['Type']} {i['ResourceRecords'][0]['Value']}")
        elif i["Type"] == "TXT":
            print(f"{i['Name'].replace(domain_name,'')} 86400 IN {i['Type']} {i['ResourceRecords'][0]['Value']}")
        else:
            skiped_record.append(i)

    print(f"\n\nSkipped Recordds: \n {skiped_record}")

dns = boto3.client('route53')

response = dns.list_hosted_zones()
zone_id = None
if zone_domain[-1] != ".":
    zone_domain += "."
for hosted_zones in response['HostedZones']:
    #print(hosted_zones)
    if hosted_zones['Name'] == zone_domain:
        zone_id = hosted_zones['Id']

if zone_id is None:
    print("Zone not found")
    exit()


paginator = dns.get_paginator('list_resource_record_sets')

page_iterator = paginator.paginate(HostedZoneId=zone_id,
    PaginationConfig={
        'MaxItems': 123,
        'PageSize': 123
    })
for page in page_iterator:
    get_record_details(page["ResourceRecordSets"])
