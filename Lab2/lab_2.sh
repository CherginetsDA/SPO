git clone https://github.com/cjdelisle/cjdns.git
cd cjdns/
sudo apt-get install nodejs git build-essential python2.7
./do
./cjdroute 
LANG=C cat /dev/net/tun 
./cjdroute --genconf >> cjdroute.conf
sudo ./cjdroute < cjdroute.conf 