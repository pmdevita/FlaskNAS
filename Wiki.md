#### Build notes:
Bootstrap 4/SCSS

SVGs compressed with http://www.scriptcompress.com/SVG-minifier.htm


### Setup:

##### Step 1: Packages
Before running NAS, your system will need a few packages installed
  - python3 (required)
  - samba-common (required)
  - avahi-daemon (optional)
  - netatalk (optional)

avahi-daemon provides Mac compatibility and netatalk implements Time
Machine backups.

You will also need to install virtualenv into your python3 installation
 by running

    pip3 install virtualenv

or if you have a custom python3 installation

    python3 -m pip install virtualenv

##### Step 2: Storage

You will need to decide where to locate your shares and create the
parent folder for them.

### Optional
#### Redis Sessions

By default, FlaskNAS uses filesystem-based server side sessions. However
, we can switch to Redis to gain speed and reduce filesystem clutter.

##### Step 1: Build/Install Redis

Make a temp directory to build Redis. Inside that directory, run the
following commands. The defaults utils/install_server.sh gives are fine.

    wget http://download.redis.io/redis-stable.tar.gz
    tar xvzf redis-stable.tar.gz
    cd redis-stable
    make
    sudo make install
    sudo utils/install_server.sh

##### Step 2: Install redis-py

CD to the directory FlaskNAS is located at and run

    NAS-ve/bin/pip install redis

Restart FlaskNAS or continue to the optional third step

##### (Optional) Step 3: Configure FlaskNAS

If you are not using Redis's default settings or you are running the
server on a different machine on the network, create a file named
"redis.json" with the following contents.

    {
      "host": "localhost",
      "port": 6379
    }

Change host and port to match your Redis server.

Restart FlaskNAS.

###### Sources:

https://redis.io/topics/quickstart
http://grainier.net/how-to-install-redis-in-ubuntu/

#### Architecture Documentation:
Login:
HTTPS must be supplied by web server. Other than that, NAS uses argon2 for
password hashing and server-side sessions for best security.