### Ubuntu local dev
```shell
  python3 -m venv .venv 
  source .venv/bin/activate
  pip install --upgrade pip poetry
```

### Change version for python (if needed)
https://www.rosehosting.com/blog/how-to-install-and-switch-python-versions-on-ubuntu-20-04/
```shell
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt update
```
```shell
  sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.13 1
  # or
  sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.13 1
  # now chose version
  sudo update-alternatives --config python
```
