channnel=rpi-config
message='hostname:'$(cat /etc/hostname)',ip:'$(ip addr|egrep -o 'inet\ 192\.168\.0\.[0-9]{1,3}' |sed s/inet\ //g )',ssid:'$(iwconfig wlan0 |grep -o ESSID:\"[^\"]*\")
function send(){
	curl -s -XPOST "https://slack.com/api/chat.postMessage?token=$SLACK_TOKEN&channel=$channnel&username=raspi&text="+"$@" >>/dev/null
}
send $message
