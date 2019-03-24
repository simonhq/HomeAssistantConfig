# KEVO Locks Configuration

Software: AppDaemon Python Script
Version: 0.1
Dependencies: 
* pykevoplus.py
* beautifulSoup4 (bs4)

This was the adapted from work of others in the HA Community, especially Bahnburner. 

I have added the random checking time (4-9 minutes) to aim to have different locks hitting the KEVO server at different times, as I was experiencing a lot of 500 errors.

## Usage

Create an input_boolean for each lock you want to control. Setup the scripts below and then check the appdaemon logs to see if the locks are updating and the time between checks.

You should then just be able to change the input_boolean from 'on' to 'off' and vis-versa and the lock should then be triggered.

## Installation

### Dependencies

Using [SSH](https://github.com/hassio-addons/addon-ssh), connect to your HassIO instance,

```
    $ cd /usr/bin
    $ wget -O pykevoplus_v2.0.tar.gz https://github.com/Bahnburner/pykevoplus/archive/v2.0.tar.gz
    $ sudo pip3 install pykevoplus_v2.0.tar.gz
```

This will install the dependencies, then find them using
```
    $ find / -name pykevoplus
```

Then use the appropriate from directory (found above), copy to appdaemon directory
```
    $ cp -R /usr/lib/python3.6/site-packages/pykevoplus /config/appdaemon/apps
    $ cp -R /usr/lib/python3.6/site-packages/bs4 /config/appdaemon/apps
```

### Appdaemon Setup
This is an appdaemon python script, download it into a directory called appdaemon/apps/kevo

In the appdaemon/apps/ directory, in the apps.yaml file, add (one block for each lock) 

  ```yaml
  front-lock:
    module: locks
    class: DoorLock
    select_name: "fdoor" #you need to setup an input_boolean.fdoor
    lock_id: "XXXXX" # the id from your lock (can be found in the KEVO app on your phone)
    k_user: "XXXXX" # the username for the KEVO application
    k_pass: "XXXXX" # the password for the KEVO application
  ```



