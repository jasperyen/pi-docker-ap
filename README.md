# pi-docker-ap
 
 python 腳本會在開機時自動執行, 並藉由 docker 啟動 wifi 分享
 
```
interface: wlan1
ssid: pi-ap_<MAC末四碼>
password: raspberry
```

## Reference

Install docker: https://phoenixnap.com/kb/docker-on-raspberry-pi

Docker hostap server: https://github.com/sdelrio/rpi-hostap

Run a Script as a Service: https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f


## Requirement

```

# install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# download script
git clone https://github.com/jasperyen/pi-docker-ap.git ~/.startap

# install requirement for root
cd ~/.startap
sudo python3 -m pip install -r requirement.txt

# Run a Script as a Service
sudo nano /lib/systemd/system/startap.service

--------------------------------------------------------

[Unit]
Description=Start AP
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/pi/.startap/startap.py
Restart=no

[Install]
WantedBy=multi-user.target

--------------------------------------------------------

sudo chmod 644 /lib/systemd/system/startap.service
chmod +x /home/pi/.startap/startap.py
sudo systemctl daemon-reload
sudo systemctl enable startap.service
sudo systemctl start startap.service

sudo reboot

```

## 常見問題
1. 執行 get-docker.sh 可能需要跳板, 安裝過程有可能會失敗, 可以試著重啟解決

2. 建議設定 /etc/wpa_supplicant/wpa_supplicant-wlan0.conf 讓 wlan0 自動連上wifi<br>
如果設定 /etc/wpa_supplicant/wpa_supplicant.conf 會讓所有的無線網卡自動連上 wifi, 這樣的話 docker 啟動就會失敗, 因為沒辦法同時連接 wifi 又開熱點
