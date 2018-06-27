# *UPPERSAFE Open Source Firewall*

OSFW is a firewall, fully written in Python 3, that provides an IP / domain filtering based on a collection of public threat intelligence feeds.

It blocks in real time incoming and outcoming traffic considered as *malicious* (matching the filtering rules automatically set up for each threat).

It also provides a secure DNS service that blocks different kind of *malicious servers* (phishing websites, malware hosting, malvertising, C&C servers, etc).

## Components

OSFW includes 3 main components:

|Name|Description|
|-|-|
|`osfw-sensor`|In charge of monitoring and logging the requests blocked by the firewall|
|`osfw-syncfw`|In charge of collecting and syncing the threat intelligence feeds|
|`osfw-webapp`|In charge of managing the web interface|

## Quick start

Setup the virtual environment:

`python3 -m venv venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

Start the firewall components:

`bash run.sh`

Attach a screen:

`screen -r osfw-sensor`
`screen -r osfw-syncfw`
`screen -r osfw-webapp`

## Configuration

To enable the secure DNS service, simply create a symbolic link of the `unbound.conf` file to the unbound configuration directory with the following command:

`ln -s "$PWD/assets/unbound.conf" /etc/unbound/unbound.conf.d/firewall.conf`

It is possible to customize the behaviour of the firewall by editing the default `config.yaml` file.

One of the reasons you would want to edit this file is to unblock specific websites.
It happens that some legit and top ranked websites got blocked because of different purposes, most of the time one of the following:

- Their users can upload files on the main domain (file transfer providers or cloud storage providers)
- Their users can upload files or even web pages on a subdomain (hosting providers)
- Their users can perform URL redirect (link shortener websites)

To prevent these websites from being blocked, you can specify them as a list in the configuration file.
In case you want to edit the default list, you can use a magic keyword `.tld` that will match any top level domain and the following second level domain names:

- .co.tld
- .com.tld
- .net.tld
- .org.tld
- .edu.tld
- .gov.tld

There is also a way to make a rule act as a subdomain wildcard, to do so you need to start the rule with a `.` such as the ones already in the configuration file.

## Dependencies

- python3
- iptables
- unbound
- screen

## Python requirements

- pyyaml
- colorlog
- requests
- flask
- sqlalchemy
- pebble

## Support

Nicolas THIBAUT (nicolas[@]uppersafe[.]com)

https://www.patreon.com/dev2lead/memberships
