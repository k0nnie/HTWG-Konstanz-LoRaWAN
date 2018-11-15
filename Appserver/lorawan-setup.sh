#cd /home/ubuntu/
#git clone https://github.com/k0nnie/HTWG-Konstanz-LoRaWAN.git
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
pip3 install 'ttn<3'
#cd HTWG-Konstanz-LoRaWAN/Appserver
python3 receiver.py #start the script that receives packages from TTN
#sudo dpkg-reconfigure tzdata  ######select Europe/Berlin#######
