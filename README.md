# LoolMonitor

Web-socket serveur listening for Lool Admin Worker.

Works with Alfresco ( [libreoffice-online-repo](https://github.com/ArawaFr/libreoffice-online-repo) & [libreoffice-online-share](https://github.com/ArawaFr/libreoffice-online-share) )

## Requirements

* Need python>3.6

## Install

```bash

apt install git python3-pip
pip3 install git+https://github.com/ArawaFr/libreoffice-online-monitor.git@clean-project
python3 -m loolmonitor
```

## Run

```bash
python main.py
```


# Configuration

You can configure the monitor by placing any supported command line option to a configuration file. The system wide configuration file is located at `/etc/lool/monitor.conf` and the user wide configuration file at `~/.config/lool/monitor.conf`
