# Web Tool Manager

A simple web tool manager use discord bot to manage web tools which require NAT traversal wherever you are, especially on mobile devices.


## Installation

### Install the Python

Python version is not important for this program

but Python 3.10.6 is suggested

### Install this repository

Using git:
```cmd
git clone https://github.com/LittleOrange666/Web_Tool_Manager.git
```
Or you can download zip file from github and unzip it.

### Install Python dependencies

```cmd
pip install -r requirements.txt
```

### Install this cloudflare tunnel

You can download it from [Download Page](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

Then, rename the executable to "cloudflared.exe" and put it in this folder or somewhere in the PATH

### Create your discord bot

First, ask Google to create a discord bot

Then, copy the Token, and create a file named "token.json", and write token like this:

```json
{
    "token":"XXXXXXXXXXXXXXXXXXXXXXXXXX.XXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
```

## Add Web Tools

Create a file named "tools.json", and input tools info

Ex.
```json
{
  "gpt": {
    "cmd": "wsl -e python3 /home/orange/text-generation-webui/server.py",
    "port":7860
  }
}
```

This example displayed a basic web tool, you should use "name: {config}" to add a tool

First, config named "cmd" should be the direct command to your web tool and it should can be access in any place

In this example, I use "wsl -e" to access the web tool inside the WSL, and use "python3" to run python executable.

If your web tool will access some file with relative path, you should change dir in the beginning of the program

For Python, you can place

```python
import os
os.chdir(os.path.dirname(__file__))
```

at the beginning.

For cmd, you can use

```cmd
cd %~dp0
```

For other, you can use cmd to run it indirectly.

Second, config named "port" should be the port of your web tool, that means they will be opened in "127.0.0.1:{port}"

### Static link

This tool defaultly uses trycloudflared to do NAT traversal.

But if your have your own domains, you can use your own domain to 

First, your should have a cloudflare accound and connect your domain to it.

Second, do following action in cmd where you can access cloudflared.exe

1. authorize

```cmd
cloudflared login
```
you should visit the web page it provides to give it acccess to your domains

2. create tunnel and connect to domain 

```cmd
cloudflared tunnel create {tunnel name}

cloudflared tunnel route dns {tunnel id} {your domain name}
```

tunnel name can be anything, but you should remember it.

you will get the tunnel id after enter the first command, it will looks like "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx".

3. write config

Add two config "tunnel_name" and "static_link" in config file.

It may look like this:

```json
{
  "gpt": {
    "cmd": "wsl -e python3 /home/orange/text-generation-webui/server.py",
    "port":7860,
    "tunnel_name": "web1",
    "static_link": "http://xxx.xxx"
  }
}
```

## Tool Usage

Double click on the "run.bat" will start this program.

Following commands is in discord

+ !start {name}     --start web tool
+ !stop {name}      --stop web tool
+ !restart {name}   --restart web tool
+ !stat             --list stat of web tools
+ !temp             --get GPU temperature

info: stop+start is different than restart, restart will not restart the cloudflare tunnel.