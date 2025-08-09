---
categories:
    - Linux
---
# How To Use a VPN On a Linux Server

With this guide you can set up Linux to automatically connect to a VPN every time the system boots. These steps have been tested only on a Raspberry Pi (64-bit ARM).

## 1. Install OpenVPN

```bash
sudo apt install openvpn
```

## 2. Create OpenVPN configuration

```bash
sudo vim /etc/openvpn/default.conf
```

Your VPN provider should provide you with all the things you should put here.

## 3. Remove the Authentication Prompt

If your VPN provider requires authentication before connecting, it will prompt for login on every connection. We will solve that now.

Create `login.conf`

```bash
sudo touch /etc/openvpn/login.conf
```

and add your username and password in that file

```bash
<username>
<password>
```

Make sure the file is only accessible to root/OpenVPN, especially if you share this machine with other users

```bash
sudo chmod 400 /etc/openvpn/login.conf
```

Next, make OpenVPN use that file to authenticate you automatically:

```bash
sudo vim /etc/openvpn/default.conf

# Add this to your file
auth-user-pass login.conf
```

## 4. Start OpenVPN on system startup

```bash
sudo systemctl enable openvpn@default
sudo systemctl start openvpn@default
```

Now your machine should automatically start with VPN and restart it if needed.

## Bonus: Create command to check your IP

I like to double-check that I'm connected to the VPN, and for that I tend to create a small script that prints my current IP.

```bash
#!/bin/bash
curl https://ipinfo.io/ip
```
