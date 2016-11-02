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

## Step 1: Setting up the box with Debian Testing

Because the SaltStack version in Debian Stable are ancient, we will set up our box on Debian Testing.

1. Create a Debian VM on DigitalOcean. I used a box with 4 GiB of RAM.
1. SSH into it `$ ssh root@256.256.256.256`
1. Update it to Debian Testing by editing `\etc\apt\sources.list`
   And replacing all distribution names by testing.
   After doing this, my file looked as follows:
   ```
   deb http://mirrors.digitalocean.com/debian testing main
   deb-src http://mirrors.digitalocean.com/debian testing main

   deb http://security.debian.org/ testing/updates main
   deb-src http://security.debian.org/ testing/updates main

   deb http://mirrors.digitalocean.com/debian testing-updates main
   deb-src http://mirrors.digitalocean.com/debian testing-updates main
   ```
1. Upgrade: `$ apt update; apt full-upgrade`
1. Go out for a walk
