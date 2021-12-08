from enum import Enum

import requests
import yaml


class ConfigProperties(Enum):
    """An enumeration of all the config properties that must be filled correctly by the user"""

    telegram_id = {
        'isArray': True,
        'main': "telegram",
        'secondary': 'telegram_chat_id',
        'keyword': ['<CHAT ID TELEGRAM 1>', '<CHAT ID TELEGRAM 2>'],
        'propertyName': 'Telegram Chat ID'
    }
    telegram_key = {
        'isArray': False,
        'main': "telegram",
        'secondary': 'telegram_bot_key',
        'keyword': '<TELEGRAM BOT TOKEN>',
        'propertyName': 'Telegram Key/Token'
    }
    metamask_pwd = {
        'isArray': False,
        'main': "metamask",
        'secondary': 'password',
        'keyword': '<METAMASK PASSWORD>',
        'propertyName': 'Metamask Password'
    }


class Version:
    """A class that represents the version of the software"""

    major: int
    minor: int
    patch: int

    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __init__(self, version: str):
        self.Parse(version)

    def Parse(self, version: str):
        versions = version.split('.')
        self.major = int(versions[0])
        self.minor = int(versions[1])
        self.patch = int(versions[2])

    @staticmethod
    def isLower(version1: str, version2: str)->bool:
        """Checks if the first version is lower than the second

        Args:
            version1 (str): The first version to check
            version2 (str): The second version to check

        Returns:
            bool: True if the first version is lower than the second, False otherwise
        """
        v1 = Version(version1)
        v2 = Version(version2)
        if v1.major < v2.major:
            return True
        elif v1.major == v2.major and v1.minor < v2.minor:
            return True
        elif v1.major == v2.major and v1.minor == v2.minor and v1.patch < v2.patch:
            return True
        else:
            return False


def checkConfig() -> str:
    """Returns the name of the property that the user
    didn't complete correctly
    :return: the path of the property that the user didn't complete corretly,
    if the file is empty/doesn't exist, will return "EMPTY" """

    # load file
    config = getConfig()

    # file is empty, return "EMPTY"
    if config == {}:
        return "EMPTY"

    # the file exists, now check for the configs :)
    for essentialconfig in ConfigProperties:
        filevalue = config[essentialconfig['main']][essentialconfig['secondary']]
        # check if it's a list


def isConfigComplete() -> bool:
    """Returns a boolean representing if the
    config file has been completed accordingly

    Example: true -> everything is ok
             false -> the user didn't complete something
    """

    config = getConfig()
    if config == {}:
        # the file is not empty
        # check the essential parameters
        for essentialconfig in ConfigProperties:
            # iterate in all must have configs
            filevalue = config[essentialconfig['main']][essentialconfig['secondary']]
            if isinstance(essentialconfig['keyword'], list) or isinstance(filevalue, list):
                for val in filevalue:
                    for key in essentialconfig['keyword']:
                        if key == val:
                            return False
            else:
                if filevalue == essentialconfig['keyword']:
                    return False
    else:
        return False
    return True


def getConfig() -> dict:
    """Returns the config file as a dictionary"""

    stream = open("config.yaml", 'r')
    if stream is not None:
        config = yaml.safe_load(stream)
        stream.close()
        return config
    else:
        return {}


def getConfigVersion() -> Version:
    """Returns the version of the config file
    :return: the version of the config file
    """
    config = getConfig()
    strversion = config['configversion']
    version = Version(strversion)
    return version


def getAppVersion() -> Version:
    """Returns the version of the app
    :return: the version of the app
    """
    config = getConfig()
    strversion = config['version']
    version = Version(strversion)
    return version


def getLastAppVersion() -> Version:
    """Returns the last version of the app
    :return: the last version of the app
    """
    config = getConfig()
    url = config['lastversionurl']
    r = requests.get(url)
    if r.status_code == 200:
        strversion = r.text
        lastversion = yaml.safe_load(strversion)
        lastappversion = Version(lastversion['version'])
        return lastappversion
    else:
        return None


def getLastConfigVersion() -> Version:
    """Returns the last version of the config file
    :return: the last version of the config file
    """
    url = getConfig()['lastversionurl']
    r = requests.get(url)
    if r.status_code == 200:
        strversion = r.text
        lastversion = yaml.safe_load(strversion)
        lastconfigversion = Version(lastversion['configversion'])
        return lastconfigversion
    else:
        return None


def checkForUpdates() -> bool:
    """Check if there is an update available
    :return: True if there is an update available, False otherwise
    """
    currentversion = getAppVersion()
    lastversion = getLastAppVersion()
    if lastversion is not None:
        if Version.isLower(currentversion, lastversion):
            return True
        else:
            return False
    else:
        return False


def updateApp() -> bool:
    """Updates the app
    :return: True if the app was updated, False otherwise
    """
    return False