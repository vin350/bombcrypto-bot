from enum import Enum

import yaml


class ConfigChecker:
    @staticmethod
    def checkConfig() -> str:
        """Returns the name of the property that the user
        didn't complete correctly
        :return: the path of the property that the user didn't complete corretly,
        if the file is empty/doesn't exist, will return "EMPTY" """

        # load file
        stream = open("config.yaml","r")
        if stream is None:
            # file is empty, return "EMPTY"
            return "EMPTY"

        # the file exists, now check for the configs :)
        config = yaml.safe_load(stream)
        for essentialconfig in ConfigProperties:
            filevalue = config[essentialconfig['main']][essentialconfig['secondary']]
            # check if its an list

        stream.close()

    @staticmethod
    def isConfigComplete() -> bool:
        """Returns a boolean representing if the
        config file has been completed accordingly

        Example: true -> everything is ok
                 false -> the user didn't complete something
        """

        stream = open("config.yaml", 'r')
        if stream is not None:
            config = yaml.safe_load(stream)

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
            stream.close()
        else:
            return False
        return True

    @staticmethod
    def checkConfigVersion() -> :

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
    major:int
    minor:int
    patch:int
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

    def Parse(self, version: str):
        versions = version.split('.')
        self.major = int(versions[0])
        self.minor = int(versions[1])
        self.patch = int(versions[2])
