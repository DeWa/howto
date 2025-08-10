---
categories:
    - Linux
---
# UFW Cheatsheet

## Basic Commands

### Status and Information

```bash
# Check UFW status
sudo ufw status

# Check UFW status with numbered rules (useful when deleting rules)
sudo ufw status numbered

# Check UFW status verbose
sudo ufw status verbose

# Show UFW rules
sudo ufw show added
```

### Enable/Disable

```bash
# Enable UFW
sudo ufw enable

# Disable UFW
sudo ufw disable

# Reset UFW to default settings
sudo ufw reset
```

## Rule Management

### Adding Rules

```bash
# Allow incoming connection on port 22 (SSH)
sudo ufw allow 22

# Allow incoming connection on port 80 (HTTP)
sudo ufw allow 80

# Allow incoming connection on port 443 (HTTPS)
sudo ufw allow 443

# Allow specific IP address
sudo ufw allow from 192.168.1.100

# Allow specific IP to specific port
sudo ufw allow from 192.168.1.100 to any port 22

# Allow specific subnet
sudo ufw allow from 192.168.1.0/24

# Allow specific protocol
sudo ufw allow 53/udp  # DNS
sudo ufw allow 67/udp  # DHCP
```

### Denying Rules

```bash
# Deny incoming connection on port 23 (Telnet)
sudo ufw deny 23

# Deny specific IP address
sudo ufw deny from 192.168.1.200

# Deny specific IP to specific port
sudo ufw deny from 192.168.1.200 to any port 80
```

### Deleting Rules

```bash
# Delete rule by number (use 'ufw status numbered' to see numbers)
sudo ufw delete 1

# Delete rule by specification
sudo ufw delete allow 22
sudo ufw delete deny from 192.168.1.200
```

## Application Profiles

### Managing Application Profiles

```bash
# List available application profiles
sudo ufw app list

# Get info about specific application
sudo ufw app info 'Apache'

# Allow application profile
sudo ufw allow 'Apache'

# Allow application profile with specific profile
sudo ufw allow 'Apache Full'

# Deny application profile
sudo ufw deny 'Apache'
```

## Advanced Rules

### Port Ranges

```bash
# Allow port range
sudo ufw allow 8000:9000/tcp

# Allow multiple ports
sudo ufw allow 80,443/tcp
```

### Specific Interfaces

```bash
# Allow on specific interface
sudo ufw allow in on eth0 to any port 22

# Allow outbound on specific interface
sudo ufw allow out on eth0
```

### Logging

```bash
# Enable logging
sudo ufw logging on

# Set logging level
sudo ufw logging low
sudo ufw logging medium
sudo ufw logging high

# Disable logging
sudo ufw logging off
```

## Default Policies

### Setting Default Policies

```bash
# Set default incoming policy to deny
sudo ufw default deny incoming

# Set default outgoing policy to allow
sudo ufw default allow outgoing

# Set both defaults
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

## Common Use Cases

### Web Server Setup

```bash
# Enable UFW
sudo ufw enable

# Allow SSH (important to do this first!)
sudo ufw allow ssh
sudo ufw allow 22

# Allow HTTP and HTTPS
sudo ufw allow 'Apache'
sudo ufw allow 80
sudo ufw allow 443

# Check status
sudo ufw status
```

### Database Server Setup

```bash
# Allow SSH
sudo ufw allow ssh

# Allow PostgreSQL
sudo ufw allow 5432

# Allow Redis
sudo ufw allow 6379
```

### Development Environment

```bash
# Allow SSH
sudo ufw allow ssh

# Allow web server port
sudo ufw allow 3000  # Node.js for example
```

## Monitoring and Troubleshooting

### View Logs

```bash
# View UFW logs
sudo tail -f /var/log/ufw.log

# View all firewall logs
sudo journalctl -u ufw

# View recent UFW activity
sudo ufw status verbose
```

### Testing Connections

```bash
# Test if port is open locally
netstat -tuln | grep :80

# Test if port is reachable from outside
telnet your-server-ip 80

# Test with nmap
nmap -p 80,443 your-server-ip
```

## Configuration Files

### Main Configuration

```bash
# Edit UFW configuration
sudo vim /etc/ufw/ufw.conf

# Edit user rules
sudo vim /etc/ufw/user.rules

# Edit before rules
sudo vim /etc/ufw/before.rules

# Edit after rules
sudo vim /etc/ufw/after.rules
```

## Examples

### Basic Server Setup

```bash
# 1. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. Allow SSH
sudo ufw allow ssh

# 3. Allow web traffic
sudo ufw allow 80
sudo ufw allow 443

# 4. Check status
sudo ufw status verbose

# 5. Enable UFW
sudo ufw enable
```

### Allow Samba + SSH from local network but allow outside traffic only through VPN

```bash
# Deny all incoming and outgoing traffic by default
sudo ufw default deny outgoing
sudo ufw default deny incoming

# Allow traffic from VPN network interface
# This assumes you have already installed OpenVPN and it has
# added tun0 network interface
sudo ufw allow in on tun0 from any to any
sudo ufw allow out on tun0 from any to any

# Allow SSH from local network
sudo ufw allow from 192.168.0.0/16 to any port 22

# Allow Samba from local network
sudo ufw allow from 192.168.0.0/16 to any app Samba

# Allow other traffic through local network if needed
sudo ufw allow from 192.168.0.0/16 proto tcp to any port 8080

# Allow OpenVPN to connect your VPN provider
sudo ufw allow out to <VPN_SERVER_IP> port 443 proto tcp

# Enable UFW
sudo ufw enable

# You can now test the connection by disabling OpenVPN and e.g.
# pinging google.com. It should not go through
ping google.com
```

You may have to point Linux DNS to your VPS provider DNS to make it work (and make it more secure as well). This was the case in my setup.

```bash
sudo vim /etc/resolv.conf
```

Replace everything with:

```bash
nameserver <VPS DNS server IP>
nameserver <VPS secondary DNS server IP>
```

Some VPN providers still don't support IPv6 so you may have to disable IPv6 support
in Linux and UFW.

```bash
sudo vim /etc/sysctl.conf
```

Add these at the bottom of the file

```bash
net.ipv6.conf.all.disable_ipv6=1
net.ipv6.conf.default.disable_ipv6=1
net.ipv6.conf.lo.disable_ipv6=1
```

Save and make the system reload sysctl.conf

```bash
sudo sysctl -p
```

Check that IPv6 has been disabled by running

```bash
cat /proc/sys/net/ipv6/conf/all/disable_ipv6
```

and see if it prints 1.

Next, make UFW stop automatically creating IPv6 rules

```bash
sudo nano /etc/default/ufw
```

and change IPV6

```bash
IPV6=no
```

