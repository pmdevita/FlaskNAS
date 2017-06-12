#### Build notes:
Bootstrap 4/SCSS
SVGs compressed with http://www.scriptcompress.com/SVG-minifier.htm


#### Setup:
Before running NAS, your system will need a few packages installed
  - samba-common (required)
  - avahi-daemon (optional)
  - netatalk (optional)

samba is required for all clients. All normal local file sharing will be done through samba.
avahi is needed to broadcast to Mac clients so it appears in Shared on Finder. (Customize icon with http://simonwheatley.co.uk/2008/04/avahi-finder-icons/)
netatalk is only needed to provide Time Machine services to Mac clients.

Most distro package maintainers do not have a modern version of Netatalk (v3 or newer). You will most likely need to
build your own binary.

samba is required to start NAS. Absence of other packages will only result in those features not being available.



#### Settings Documentation
Json file with different settings

 - rootdir: Directory where all the shares will be placed


#### Architecture Documentation:
Login:
HTTPS must be supplied by web server. Other than that, NAS uses argon2 for
password hashing and server-side sessions for best security.