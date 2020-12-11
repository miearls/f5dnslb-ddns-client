# F5 DNS Load Balancer Dynamic DNS Client 
Ever wanted to access your home network or someone's network but they have a dynmaic IP that changes all the time. This script is for you, it makes use of a FREE service from F5.com DNS Load Balancer. Information about the FREE tier is listed below.

This script written in Python is using the F5 DNS-LB API call to generate a new json configuration including LBRs, Virtual Servers, Endpoints, Pools and Monitors and updates the endpoint IP address based on the outbound HTTP call to a 3rd party serivce to provide the external IP address of your nextwork. This will not pull the internal IP of your device. 

Sign up for a FREE Account, no credit card required. 
https://portal.cloudservices.f5.com/register

F5 Cloud Free Tier information:
https://clouddocs.f5.com/cloud-services/latest/
A Free Tier is applied to all users but is most useful to those who wish to try the service without incurring any charges. If usage is kept below the tier thresholds, no charges will be billed. Any usage beyond the free tier is charged at the normal rates. The free tier allows for:

One free Load Balanced Record (LBR) per month.
First 3 million queries per month are free.
First 10 standard health checks are free. These may span LBRs or service instances.
https://clouddocs.f5.com/cloud-services/latest/f5-cloud-services-GSLB-Pricing.html#f5-dns-load-balancer-cloud-service-pricing

## Example
1. Clone the repo and change to the directory
1. Update the `setup_config.yaml` file to match the settings you would like to use.
   * **F5 Username**: Username created to access the F5 Cloud Services Portal.
   * **F5 Password**: Password created to access the F5 Cloud Services Portal.
   * **Service Instance Name**: subdomain delegatation
   * **lbr_name**: Load Balanced Record (LBR) Friendly Name
   * **lbr_aliases**: Load Balanced Record (LBR) host record
   * **virtual_server**: Virtual Server Friendly Name.
   * **pools**: Pool Friendly Name.
   * **monitor**: Standard Health Check of Ping
   * **check interval**: How often should the script run and check your external IP.
   * **ip query service**: Which external provider 

As you can see an example of the inital json payload (my current IP) and the updated payload (Net New IP) with the new changes.
 {'VSisp': {'address': '**122.29.27.51**', 'display_name': 'VSisp', 'monitor': 'ICMP', 'port': 80, 'virtual_server_type': 'cloud'}}, 
24 Hours later:
 {'VSisp': {'address': '**24.32.18.21**', 'display_name': 'VSisp', 'monitor': 'ICMP', 'port': 80, 'virtual_server_type': 'cloud'}}, 
