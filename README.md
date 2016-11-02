This repo contains all the configuration files and custom modules used to automate pathspider measurements
with SaltStack.

# Step-by-step guide

This guide provides a step by step guide to setting up automated PATHspider measurements using SaltStack.

For this guide, we will set everything up on a DigitalOcean server. But any Debian(-based) box should be similar.

## Step 0: Learn about SaltStack

You will probably want to learn a bit about SaltStack first.
The following URLs will be helpfull:

1. https://docs.saltstack.com/en/getstarted/
1. https://docs.saltstack.com/en/latest/topics/cloud/
1. https://docs.saltstack.com/en/latest/contents.html

## Step 1: Setting up the box with Debian Stable and install SaltStack

Because the SaltStack version in Debian Stable is ancient,
we will add a repo hosted by SaltStack

1. Create a Debian VM on DigitalOcean. I used a box with 4 GiB of RAM.
1. SSH into it: `$ ssh root@256.256.256.256`
1. Import the SaltStack repository key:
    `$ wget -O - https://repo.saltstack.com/apt/debian/8/amd64/latest/SALTSTACK-GPG-KEY.pub | sudo apt-key add -`
1. Add the SaltStack repo to `/etc/apt/sources.list`:
   `$ echo "deb http://repo.saltstack.com/apt/debian/8/amd64/latest jessie main" >> /etc/apt/sources.list`
1. Update apt cache: `$ apt update`
1. Install the required SaltStack packages:
    `$ apt install salt-master salt-cloud salt-api`

## Step 2: Configure Salt Cloud

1. Add the following lines to `/etc/salt/cloud`
    ```
    minion:
      master: << hostname or IP of the box you are setting this up on >>
    ```
    This will tell the workers (Salt Minions) what command server (Salt Master)
    they should connect to.

1. Make the directory `/etc/salt/keys`
1. using `ssh-keygen` generate an unencrypted keypair, and store it in `/etc/salt/keys`
1. Add the newly generated public key to your Digital Oceans account
1. While you are on the Digital Oceans site, create yourself a `personal access token`
1. in `/etc/salt/cloud.providers.d/do.conf` add a configuration for Digital Ocean.
   Mine looks like this:
   ```
   do-mami:
     driver: digital_ocean
     personal_access_token: <<Your personal access token >>
     ssh_key_file: /etc/salt/keys/<< your-key >>
     ssh_key_names: <<name you chose on Digital Ocean>>
   ```
1. in `/etc/salt/cloud.profiles.d/do.conf` add a profile.
   My file looks like this: 
   ```
   do-ams3-512:
     provider: do-mami
     image: debian-8-x64
     size: 512mb
     location: ams3
     private_networking: False
     backups_enabled: False
     ipv6: True
     create_dns_record: False
   
   do-ams3-2048:
     provider: do-mami
     image: debian-8-x64
     size: 2gb
     location: ams3
     private_networking: False
     backups_enabled: False
     ipv6: True
     create_dns_record: False
	```
1. You should now be able to create a Salt minion named by running
   `$ salt-cloud -p do-ams3-512 test1`
	This can take a few minutes to run.

1. You can delete it again by running
	`$ salt-cloud -d test1

## Copying the files
1. Copy the directories in the `srv` directory of this repository to `/srv/`
1. Copy the files in the `etc/salt/master.d/` to `/etc/salt/master.d/`
1. Copy `spiderweb` to `/opt/spiderweb`
1. Since we did not configure, comment out the slack related sections in 
   `/srv/salt/spider_completed_state.sls`, `/srv/salt/spider_started_state.sls`
   and `/srv/salt/spider_failed_state.sls`.
   (Things will still work if you don't do this, but you might see some error
    messages)
1. restart salt-master `$ service salt-master restart`

## Create a config file and running spiderweb
1. In `/etc/spiderweb/` create the file `config.json`.
   You can find find more information about the format in the readme file of the
   spiderweb directory. My file looks like this:
   ```json 
   {
     "pathspider_args": "-i eth0 -w50 --pto-campaign {campaign} --pto-url https://your.pto.example.com/hdfs --pto-api-key <<you api key>> --pto-filename {id} ecn",
     "input_file": "/opt/spiderweb/demo.csv",
     "minions":
       {"do-ams3-512": 1,
        "do-ams3-2048": 1
        },
     "when_done": "destroy",
     "campaign": "testing"
   }
	```
1. You can now run run spiderweg as `$ ./spiderweb.py config.json$
1. The created Minions should self destruct as soon as they are done measuring and uploading.
1. Enjoy! 
