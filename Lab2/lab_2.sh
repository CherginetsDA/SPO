path=$(pwd)
git clone https://github.com/cjdelisle/cjdns.git
cd cjdns/
apt-get install nodejs git build-essential python2.7
./do
./cjdroute 
LANG=C cat /dev/net/tun 
./cjdroute --genconf >> cjdroute.conf
cd $path
sudo mv ./cjdns /opt
cd /opt/cjdns
./cjdroute < cjdroute.conf 
cd $path
