# Author : Tabrace
# Usage : python3 <filename>
# This script is used for taking open port for 22,-1,1-65535 from the security groups in the AWS accounts. And gives output in csv format.
# In order to run in all accounts,accounts name should be given in the file 'profiles'
#IPv4 & IPv6 and Security_groupid attached are cover in this script.

import boto3
import csv

profiles = open('profiles', 'r')
readprofile = profiles.readlines()
final_result=[]

regions = ['us-east-1']

total_acc = len(readprofile)
count = 0

for profile in readprofile:
    profile=profile.strip()
    count = (count + 1)
    for region in regions:
        print(f'{count}/{total_acc} [*] Running security groups check for account: {profile} and region: {region}')
        #print(f"Running security groups check for acc: {profile}, and region is: {region} {total_acc}/{count}")
        try: 
            sg_session = boto3.Session(profile_name=profile)
            sg_client= sg_session.client("ec2",region_name=region)
            response = sg_client.describe_security_groups()
            for res in response.get('SecurityGroups'):
                x = res
                for sg in x.get('IpPermissions'):
                    try:
                        if sg['FromPort'] == 22 or sg['FromPort'] == -1 or (sg['FromPort'] == 1 and sg['ToPort'] == 65535):
                            if sg['FromPort'] == sg['ToPort']:
                                port = sg['FromPort']
                            elif sg['FromPort'] != sg['ToPort']:
                                port = str(sg['FromPort']) + " - "+ str(sg['ToPort'])
                            group_name = x['GroupName']
                            description = x['Description']
                            sg_id = x['GroupId']
                            group_id = [g_pair['GroupId'] for g_pair in sg['UserIdGroupPairs']]
                            ip_range = sg['IpRanges']
                            ip_v6_range = sg['Ipv6Ranges']
                            cidrs = [ip['CidrIp'] for ip in ip_range]
                            cidripv6 = [ip['CidrIpv6'] for ip in ip_v6_range]
                            report = (profile,region,group_name,sg_id,port,cidrs,cidripv6,group_id,description)
                            print(report)
                            final_result.append(report)
                    except Exception as e:
                        pass        
        except Exception as e:
             print(e)


