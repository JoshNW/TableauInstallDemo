sudo yum --disablerepo=google-cloud-sdk,google-compute-engine update -y
sudo yum --disablerepo=google-cloud-sdk,google-compute-engine install wget -y
wget https://downloads.tableau.com/tssoftware/tableau-server-2021-1-0.x86_64.rpm
sudo yum --disablerepo=google-cloud-sdk,google-compute-engine install tableau-server-2021-1-0.x86_64.rpm -y
sudo /opt/tableau/tableau_server/packages/scripts.20211.21.0320.1853/initialize-tsm --accepteula -f
echo -e "demopassword\ndemopassword" | sudo passwd joshandersontampa
