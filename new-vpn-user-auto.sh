#!/bin/bash

PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin
OPENVPN_KEY=/etc/openvpn/keys

if [ -z "$1" ] ; then
        echo -n "Enter new VPN user name: "
        read -e VPN_USERNAME
else
        VPN_USERNAME=$1
fi

if [ -z "$2" ] ; then
        echo -n "Enter Outgoing IP: "
        read -e OUT_I
else
        OUT_IP=$2
fi

EMAIL="administrator@abr-region.ru"
VPN_ZIP=/usr/ovpn-zip
OPENVPN_KEYS=/etc/openvpn/keys

cd /usr/easyrsa3/
source vars
export KEY_EXPIRE=3650
./easyrsa --batch --req-cn=$VPN_USERNAME gen-req $VPN_USERNAME nopass
./easyrsa --batch sign-req client $VPN_USERNAME nopass
#$(/usr/easyrsa3/keypass.sh $VPN_USERNAME)
cp /usr/easyrsa3/pki/issued/$VPN_USERNAME.crt /etc/openvpn/keys/
cp /usr/easyrsa3/pki/private/$VPN_USERNAME.key /etc/openvpn/keys/

cd $OPENVPN_KEYS

echo client >> $VPN_USERNAME.ovpn
echo dev tun1 >> $VPN_USERNAME.ovpn
echo proto udp >> $VPN_USERNAME.ovpn
echo remote vpn.abr-region.ru 21194 >> $VPN_USERNAME.ovpn
echo "" >> $VPN_USERNAME.ovpn
echo persist-key >> $VPN_USERNAME.ovpn
echo persist-tun >> $VPN_USERNAME.ovpn
echo  >> $VPN_USERNAME.ovpn
echo key-direction 1 >> $VPN_USERNAME.ovpn
echo '<ca>' >> $VPN_USERNAME.ovpn
awk 'FNR==1{print ""}1' $OPENVPN_KEYS/ca.crt  >> $VPN_USERNAME.ovpn
echo '</ca>' >> $VPN_USERNAME.ovpn
echo '<cert>' >> $VPN_USERNAME.ovpn
grep -A1000 "BEGIN"  $OPENVPN_KEY/$VPN_USERNAME.crt  >> $VPN_USERNAME.ovpn
echo '</cert>' >> $VPN_USERNAME.ovpn
echo '<key>' >> $VPN_USERNAME.ovpn
awk 'FNR==1{print ""}1' $OPENVPN_KEY/$VPN_USERNAME.key  >> $VPN_USERNAME.ovpn
echo '</key>' >> $VPN_USERNAME.ovpn
echo '<tls-auth>' >> $VPN_USERNAME.ovpn
awk 'FNR==1{print ""}1' $OPENVPN_KEYS/ta.key  >> $VPN_USERNAME.ovpn
echo '</tls-auth>' >> $VPN_USERNAME.ovpn
echo "" >> $VPN_USERNAME.ovpn
echo cipher AES-256-GCM >> $VPN_USERNAME.ovpn
echo auth SHA512 >> $VPN_USERNAME.ovpn
echo "" >> $VPN_USERNAME.ovpn
echo verb 3 >> $VPN_USERNAME.ovpn
echo mute 20 >> $VPN_USERNAME.ovpn
echo explicit-exit-notify 1 >> $VPN_USERNAME
echo auth-user-pass >> $VPN_USERNAME.ovpn
echo auth-nocache >> $VPN_USERNAME.ovpn
echo "" >> $VPN_USERNAME.ovpn

if [[ -d $VPN_ZIP ]] ; then
        :
else
        mkdir -p $VPN_ZIP
fi

zip -r -9 $VPN_ZIP/$VPN_USERNAME.zip $VPN_USERNAME.ovpn

echo "Сертификаты для OpenVPN - $HOSTNAME - $VPN_USERNAME" | mutt -a $VPN_ZIP/$VPN_USERNAME.zip -s "Сертификаты для OpenVPN - $HOSTNAME - $VPN_USERNAME" -- $EMAIL

$(/usr/scripts/ccdip.sh $VPN_USERNAME)

VPN_USER_IP=$(cat /etc/openvpn/ccd/$VPN_USERNAME | awk '{print $2}')

#	 echo "Input Outgoing IP:"
#         read -e  OUT_IP
#         while [ -n "$OUT_IP"   ];
#         do
#             #echo $VPN_USER_IP
firewall-cmd --permanent --direct --add-rule ipv4 filter FORWARD 0 -i tun1 -s $VPN_USER_IP/32 -o ens192 -d $OUT_IP -j ACCEPT
#             echo "Input Another Outgoing IP:"
#             read -e  OUT_IP

#         done

firewall-cmd --reload
