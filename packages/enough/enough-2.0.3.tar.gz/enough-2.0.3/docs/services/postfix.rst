.. _postfix:

SMTP server
===========

A SMTP server is running on each host. A service running on
`some-host.example.com` can use the SMTP server as follows:

* Address: some-host.example.com
* Port: 25
* Authentication: No
* SSL/TLS: No

It is not possible (and it would not be secure) for services running
on another host (`other-host.example.com` for instance) to use this
SMTP server.
