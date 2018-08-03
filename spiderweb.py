
import os
import sys
import json
import copy
import random
import shutil
import argparse
import traceback
import subprocess

import salt.cloud

TEMPFILE_LOCATION = "/tmp/spiderweb"
SALT_CLOUD_CONFIG = "/etc/salt/cloud"
INPUT_FILE_LOCATION = "srv/salt/pathspider_inputs"

# probably not used
def readout_config(path):
    config_file = open(path)
    config = json.loads(config_file.read())
    config_file.close()

    return config

class Minion():
    """
    Represents a Saltstack minion to be instantiated.
    """

    NAME_TEMPLATE = '{web}-{profile}-{index}'

    def __init__(self, name, profile, grains=None):
        """
        Create a new Minion

        :param str name: the hostname of the Minion
        :param profile: the Stalt Cloud profile for the minion
        :type profile: :py:class:Profile
        :param dict grains: grains to be added to the minion
        """

        self.name = name
        self.profile = profile
        if grains:
            self.grains = grains
        else:
            grains = {}

    def __repr__(self):
        """
        Return a string representation of the Minion

        :returns: A string representing the minion
        :rtype: str
        """

        string = "<Minion: {}>".format(self.name)
        return string

    def get_name(self):
        """
        Get the name of the minion

        :returns: The name of the minion
        :rtype: str
        """

        return self.name

    def get_profile(self):
        """
        Get the profile of the minion

        :returns: the profile of the minion
        :rtype: :py:class:Profile
        """
        return profile

    def get_config(self):
        """
        Get the minion config to be passed to Salt Cloud

        :rtype: dict
        :returns: the minion configuration
        """

        return {'grains': self.grains}

    def spawn(self, dry_run):
        """
        Spawn the minion on the cloud provider
        """

        print("Spawning minion: {}".format(self.get_name()))

        # Redirecting stdout and stderr to prevent screen pollution
        # during creation of minions
        if not os.path.exists(TEMPFILE_LOCATION):
            os.makedirs(TEMPFILE_LOCATION)
        tempfile = "{}/{}-creation.txt".format(TEMPFILE_LOCATION,
            self.get_name())
        print("Temporary redirecting stdout and stderr to {}".format(tempfile))
        real_stdout = sys.stdout
        sys.stdout = open(tempfile, 'w')
        real_stderr = sys.stderr
        sys.stderr = sys.stdout

        # For some reason you have to create a new 'client'
        # instance for every profile you want to use.
        # To be safe we just do it for every minion.
        if not dry_run:
            client = salt.cloud.CloudClient(path=SALT_CLOUD_CONFIG)
            try:
                response = client.profile(self.profile.get_name(),
                    names=[self.get_name(),], minion=self.get_config())
            except:
                traceback.print_exc()
                response = "ERROR: failed to create minion"
                subprocess.run("sendmail `cat /srv/salt/failmail_recipient.txt` < /srv/salt/failmail.txt", shell=True)
        else:
            response = "<< No response, this was a dry run >>"


        # Restrong stdout and stderr
        sys.stdout.close()
        sys.stdout = real_stdout
        sys.stderr = real_stderr
        print("Stdout and stderr are back!")

        print("CloudClient response: {}".format(response))

class Profile():
    """
    A class to represent Salt Cloud profiles
    """
    
    def __init__(self, name):
        """
        Create the profile

        :param str name: the name of the profile
        """

        self.name = name
        self.counter = 0
        self.minions = set()

    def __iter__(self):
        return self.minions.__iter__()

    def __repr__(self):
        return "<Profile: {}>".format(self.name)

    def get_name(self):
        """"
        Get the name of the profile

        :rtype: str
        :returns: the name of the profile
        """

        return self.name

    def add_minion(self, web , grains=None ,count=1):
        """
        Add a minion to the profile

        :param web: the :py:class:Web the minion belongs to
        :type web: :py:class:Web
        :param dict grains: the grains that should be added to the minion
        :param int count: the number of minions to add
        """

        for i in range(count):
            name = Minion.NAME_TEMPLATE.format(
                    web = web.get_name(),
                    profile = self.name,
                    index = self.counter)
            self.counter = self.counter + 1
            self.minions.add(Minion(name, self, grains))

    def spawn(self, dry_run):
        """
        Spawn all the minions in this profile
        """
        for minion in self.minions:
            minion.spawn(dry_run = dry_run)

class Web():
    """
    A class to represent a web of minions

    A web is used to indicate a group of minions spawned together.
    Typically all minions in a web belong to the same campaign.
    """

    WEB_NAME_CHARS = \
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    WEB_NAME_LENGTH = 10

    def __init__(self, config_file):
        """
        Create the web

        :param str config_file: the path of the config file for the web
        """

        self.profiles = set()
        self.generate_name()
        self.readout_config(config_file)

    def __iter__(self):
        return self.profiles.__iter__()

    def __repr__(self):
        return "<Web: {}>".format(self.name)

    def generate_name(self):
        """
        Generate a random name for the web

        :rtype: str
        :return: a random name for the web
        """

        name = ''
        for i in range(self.WEB_NAME_LENGTH):
            name += random.choice(self.WEB_NAME_CHARS)
        self.name = name

        return name

    def get_name(self):
        """
        Get the name of the web

        :rtype: str
        :returns: the name of the web
        """

        return self.name

    def readout_config(self, path):
        """
        Read out a web config file

        :param str path: the path of the JSON formated file to read
        :rtype: dict
        :returns: a dict containing the content of the config file
        """

        config_file = open(path)
        self.config = json.loads(config_file.read())
        config_file.close()

        self.read_grains_from_config()
        self.add_minions_from_config()

        return self.config

    def read_grains_from_config(self):
        """
        Read the grains that are present in the config
        Add additional grains
        """

        grains = copy.deepcopy(self.config)
        grains['web'] = self.get_name()
        grains['task'] = 'pathspider'
        self.grains = grains

    def add_minions_from_config(self):
        """
        Add the minions that are defined in the spiderweb config to the web
        """

        for profile in self.config['minions']:
            new_profile = Profile(profile)
            new_profile.add_minion(web = self,
                count = self.config['minions'][profile],
                grains = self.grains)
            self.profiles.add(new_profile)

    def spawn(self, dry_run):
        """
        Spawn all profiles (and thus minion) in the web.
        """

        print("Starting to spawn web: {}".format(self.get_name()))

        self.copy_input()

        for profile in self.profiles:
            profile.spawn(dry_run = dry_run)

    def copy_input(self):
        """
        Copy the input file of the web to the Salt fileserver root,
        and name it to the web.
        """

        destination = "{}/{}.ndjson".format(INPUT_FILE_LOCATION, self.get_name())
        print("Destination: " + destination)
        print("Input file: " + self.config['input_file'])
        shutil.copy(self.config['input_file'], destination)
        

    def pretty_grains(self):
        """
        Generator that prints pretty strings for all grains in the web

        :rtype: str
        :yields: pretty strings for all the grains in the web
        """

        for grain in self.grains:
            result = "<Grain: '{}'='{}'>".format(grain, self.grains[grain])
            yield result

    def pretty_string(self):
        """
        Create a pretty string representing the web

        :rtype: str
        :returns: a multiline string describing the web
        """

        info_string = str(self) + '\n'
        for profile in self:
            info_string = info_string + ' '*4 + str(profile) + '\n'
            for minion in profile:
                info_string = info_string + ' '*8 + str(minion) + '\n'
        
        for grain in self.pretty_grains():
            info_string = info_string + ' '*4 + grain + '\n'

        return info_string

def run(args):
    # creates the web and minions
    w = Web(args.config_file)
    print("You are about to spawn the following web:")
    print(w.pretty_string())
    if(args.ask_confirmation):
        user = input("Continue? [Y/n] ")
        if user in ('y', 'Y', ''):
            pass
        else:
            return
    # spawn the web
    w.spawn(dry_run = args.dry_run)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Spawn a web of spiders')

    parser.add_argument('config_file', type=str,
            help='Path to an JSON formated spiderweb config file')
    
    parser.add_argument('-y, --yes', dest='ask_confirmation',
            action='store_const', const=False, default=True,
            help='Assume yes for all questions')

    parser.add_argument('--dry-run', dest='dry_run',
            action='store_const', const=True, default=False,
            help='Do everything except for spawning the minions')

    args = parser.parse_args()

    run(args)
    print('Goodnight')
