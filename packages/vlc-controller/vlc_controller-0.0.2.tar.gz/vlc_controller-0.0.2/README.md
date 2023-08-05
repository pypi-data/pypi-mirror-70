# Python VLC Controller via Telnet

## Based on https://github.com/DerMitch/py-vlcclient

## https://wiki.videolan.org/Documentation:Streaming_HowTo/VLM

```
python3 -m pip install vlc-controller
```

### Need to Create a Systemd Service to Keep VLC Running in Background

```
sudo nano /etc/systemd/system/vlc-daemon.service
```

```
sudo systemctl daemon-reload
```

```
sudo systemctl start vlc-daemon.service
```

```
sudo systemctl enable vlc-daemon.service
```

```
sudo systemctl status vlc-daemon.service
```