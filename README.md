# FlaskNAS Manager (.3 alpha)
Web-based interface for accessing and managing network shares.

Frustrated with other NAS software's high spec requirements and the need
to install their own distribution of Linux, I decided to take a crack at
it myself. FlaskNAS manages Samba (and Netatalk/Avahi if installed) to
provide services as configured through the web. FlaskNAS also provides
access to files through the web.


##### Requirements:
- Linux (Debian-based currently, more support later)
- Python 3.5+
- Samba
- Netatalk 3+/Avahi (optional, needed for Mac support)
- WSGI solution (uWSGI + NGINX, Gunicorn, etc.) (not setup to handle yet)

##### Restrictions:
- Currently, FlaskNAS requires complete control of Samba and
    Netatalk. This will change later.

##### Roadmap:
- ~~User login~~
- ~~Basic file interface functionality~~
- Backend controls for Samba
- Frontend controls for Samba
- Backend user management
- Frontend user management
###### Future:
- Quota support
- Plugin support

##### Other stuff:
- FlaskNAS is built with Flask, Bootstrap, JQuery, argon2, virtualenv,
and PonyORM.

##### Lowest recommended specs (specs subject to change during development)
 - 256MB of RAM
 - 1 core 600MHZ

 Based on testing with my Raspberry Pi Gen 1, with handles everything
 fine. More resources (assigned with WSGI solution) will allow more
 users to be handled at a time and speed things up.


#### Installation:

Will change in future updates

 1. Download and unpackage to writable directory
 2. Run start.py as root to turn on debug server

#### Changelog:
v.3
 - Users now in a database, Samba config ORM added, setup page created, groundwork for next update

v.1
 - Basic file browsing and login capabilities

