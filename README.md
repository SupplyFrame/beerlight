# Beer Light!

This is a simple Python app to serve a web page that toggles the beer light at the SupplyFrame HQ.

## Installation

If you are running on OS X first check to ensure the commandline xcode tools are installed, you'll need to run this with a GUI (at a machine or remote desktop):

```bash
xcode-select --install
```

First install ouimeaux from our modified fork:

```bash
git clone https://github.com/SupplyFrame/ouimeaux.git
cd ouimeaux
sudo python setup.py install --force
cd ..
```

Now clone this repo and run the app!:

```bash
git clone https://github.com/SupplyFrame/beerlight.git
cd beerlight
sudo ./server.py
```

In order to keep this alive after you log out you might want to run this in a screen:

```bash
screen -q
sudo ./server.py
```

Now detach from the screen with `CTRL-r CTRL-d`, you can later re-attach with `screen -r`
