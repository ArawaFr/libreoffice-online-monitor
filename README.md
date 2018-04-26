# LoolMonitor

Web-socket serveur lesting to Lool Admin Worker.

Need python>3.6

## Install

```bash
pip install --no-cache-dir -r requirements.txt
```

## Run

```bash
python main.py
```

## With docker

### Build

```bash
docker build -t jeci/ws-ping .
```

### Run

```bash
docker run --rm --net host -it --cap-add NET_BIND_SERVICE jeci/ws-ping
```
