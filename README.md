![UPPERSAFE](https://web.uppersafe.com/resources/images/uppersafe-color.svg)

# *UPPERSAFE Open Source Firewall*

[![Build status](https://travis-ci.org/dev2lead/uppersafe-osfw.svg?branch=master)](https://travis-ci.org/dev2lead/uppersafe-osfw) [![Python 3.4|3.5|3.6](https://img.shields.io/badge/python-3.4|3.5|3.6-yellow.svg)](https://www.python.org)

OSFW is a firewall written in Python that provides an IP / domain filtering based on a collection of threat intelligence public feeds. It relies on underlying dependencies like iptables (netfilter) and unbound.

It blocks in real time incoming and outcoming traffic considered as *malicious* (matching the filtering rules automatically set up for each threat).

It also provides a secure DNS service that blocks different kind of *malicious servers* (phishing websites, malware hosting, malvertising, C&C servers, etc).

## Summary

- [Firewall components](#firewall-components)
- [Quick start](#quick-start)
- [Configuration](#configuration)
  - [DNS service](#dns-service)
  - [Remote access](#remote-access)
  - [Launch mode](#launch-mode)
  - [Filter mode](#filter-mode)
  - [Miscellaneous](#miscellaneous)
- [Dependencies](#dependencies)
- [Support](#support)
- [License](#license)

## Firewall components

OSFW includes 3 main components:

|Name|Description|
|-|-|
|`osfw-sensor`|In charge of monitoring and logging the requests blocked by the firewall|
|`osfw-syncfw`|In charge of collecting and syncing the threat intelligence feeds|
|`osfw-webapp`|In charge of managing the web interface (work in progress)|

![Screenshot](https://i.imgur.com/ZIz7eIP.png)

## Quick start

Install the dependencies with your package manager (for example `apt` on Ubuntu or `yum` on Fedora):

    apt install python3 virtualenv iptables unbound systemd supervisor screen

Install the virtual environment:

    cd uppersafe-osfw
    virtualenv -p python3 venv
    source venv/bin/activate && pip install -r requirements.txt

Start the firewall components:

    bash run.sh

Attach a screen:

    screen -r osfw-sensor
    screen -r osfw-syncfw
    screen -r osfw-webapp

## Configuration

It is possible to customize the behaviour of the firewall by copying the default `config.default.yml` file and editing your own `config.yml` file:

    cp config.default.yml config.yml && chmod 600 config.yml

### DNS service

To enable the secure DNS service, simply create a symbolic link of the `unbound.conf` file to the Unbound configuration directory with the following command:

    ln -s "$PWD/assets/unbound.conf" /etc/unbound/unbound.conf.d/osfw.conf

### Remote access

To securely enable remote access to the web interface, you need to install a web server with reverse proxy capabilities with your package manager (for example `apt` on Ubuntu or `yum` on Fedora):

    apt install nginx ssl-cert

Then, create a symbolic link of the `nginx.conf` file to the Nginx configuration directory with the following command:

    ln -s "$PWD/assets/nginx.conf" /etc/nginx/sites-enabled/osfw.conf

If you want to use your own SSL certificates instead of those provided by the `ssl-cert` package, don't forget to update the default `nginx.conf` file.

### Launch mode

There are 3 ways to launch the firewall:

|Mode|Description|
|-|-|
|`standalone`|This is the default mode of the firewall, in this mode the firewall works on his own without interacting with a server or a client|
|`server`|In server mode the firewall dumps the threats, after processing them, to a file (by default `/tmp/threats.txt`) intended to be shared through an HTTP(S) server and fetched by the client|
|`client`|In client mode the firewall does not process the threats, so it is recommended to only fetch the file generated by the server instead of all the feeds|

### Filter mode

Filtering can be achieved through 2 different methods:

|Mode|Description|
|-|-|
|`classic`|Filtering is based on the INPUT chain and OUTPUT chain of iptables|
|`forward`|Filtering is only based on the FORWARD chain of iptables|

### Miscellaneous

It happens that some legit and top ranked websites got blocked because of different reaspns, most of the time one of the following cases:

- Their users can upload files on the main domain (file transfer providers or cloud storage providers)
- Their users can upload files or even web pages on a subdomain (hosting providers)
- Their users can perform URL redirect (link shortener websites)

To prevent these websites from being blocked, you can specify them as a list in the configuration file.

In case you want to edit the default list, you can use a magic keyword `tld` that will match any top level domain and some specific second level domain names.
For example, `domain.tld` will match all of the following cases:

- `domain.uk`
- `domain.co.uk`
- `domain.com.uk`
- `domain.net.uk`
- `domain.org.uk`
- `domain.edu.uk`
- `domain.gov.uk`
- `domain.jp`
- `domain.co.jp`
- `domain.com.jp`
- `domain.net.jp`
- `domain.org.jp`
- `domain.edu.jp`
- `domain.gov.jp`

There is a way to perform a subdomain wildcard, to do so you need to use a `*?` instead of the subdomain (for example `*?.domain.com` will match `domain.com` and `a.domain.com` but not `b.a.domain.com`).

## Dependencies

- python3 (see also `requirements.txt`)
- virtualenv
- iptables
- unbound
- systemd
- supervisor
- screen
- nginx
- ssl-cert

## Support

Nicolas THIBAUT (nicolas[@]uppersafe[.]com)

https://www.patreon.com/dev2lead/memberships

## License

This software is provided under a GNU AGPLv3 License.
