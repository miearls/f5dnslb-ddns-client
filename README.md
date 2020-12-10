# F5 DNS Load Balancer Dynamic DNS Client 
Ever wanted to access your home network or someone's network but they have a dynmaic ip that changes all the time. This script is for you, it makes use of a FREE service from F5.com (http://portal.cloudservices.f5.com) DNS Load Balancer. Using the FREE tier 1 LBR, load balanced record, and up to 3M DNS queries per month. 

This script written in Python is using the F5 DNS-LB API call to generate a new json configuration including LBRs, Virtual Servers, Endpoints, Pools and Monitors and updates the endpoint IP address based on the outbound HTTP call to a 3rd party serivce to provide the external IP address. 

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
