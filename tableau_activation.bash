tsm licenses activate -t
wget https://raw.githubusercontent.com/JoshNW/TableauInstallDemo/main/reg.json
tsm register --file reg.json
wget https://raw.githubusercontent.com/JoshNW/TableauInstallDemo/main/ident.json
tsm settings import -f ident.json
tsm configuration set -k install.component.samples -v false
tsm pending-changes apply
tsm initialize --start-server --request-timeout 1800
echo -e "demopassword\ndemopassword" | sudo passwd joshandersontampa
echo -e "demopassword\ndemopassword" | tabcmd initialuser --username 'admin' --password 'password' --server http://localhost
sudo mkdir -p /opt/tableau/tableau_driver/jdbc
sudo wget https://downloads.tableau.com/drivers/linux/postgresql/postgresql-42.2.14.jar -P /opt/tableau/tableau_driver/jdbc
