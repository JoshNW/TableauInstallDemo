sudo yum --disablerepo=google-cloud-sdk,google-compute-engine install python3 -y
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install tableauhyperapi
sudo python3 -m pip install pandas
sudo python3 -m pip install tableauserverclient
wget https://raw.githubusercontent.com/JoshNW/TableauInstallDemo/main/publish_data.py
