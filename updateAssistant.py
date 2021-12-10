import codecs
import os.path
import subprocess
import sys

import requests
import yaml
import hashlib


def treatPath(path: str) -> str:
    """Treats a path to be used in a URL, start with a ./
    :return: the URL ready path"""

    path = path.replace('.', getRawGithubUrl(), 1)
    # replace double slash just in case something slips through
    return path.replace("\\", "/")


def getRawGithubUrl() -> str:
    """Returns the raw GitHub URL, without the last /"""
    url: str = getConfig()['lastversionurl']
    url = url.replace('/update.yaml', '')
    return url


def getConfig() -> dict:
    """Returns the config file as a dictionary"""

    stream = open("config.yaml", 'r')
    if stream is not None:
        config = yaml.safe_load(stream)
        stream.close()
        return config
    else:
        return {}


# hashes a file using md5
def hashFile(filepath: str) -> str:
    """Returns the md5 hash of a file
    :param filepath: the path to the file
    :return: the md5 sum of the file"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as fileStream:
        for chunk in iter(lambda: fileStream.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def downloadFile(url: str, filepath: str):
    """Downloads the text from the URL and saves it to the filepath
    :param url: the URL to download from
    :param filepath: the path to save the file to"""
    request = requests.get(url)
    filename = os.path.splitext(filepath)[0]
    if request.status_code == 200:
        with codecs.open(filepath, 'r+', 'utf-8') as fileStream:
            fileStream.seek(0)
            fileStream.truncate(0)
            fileStream.seek(0)
            fileStream.write(request.text)
        print("Updated file: " + filename)
    else:
        print("Error downloading file " + filename)


# SCRIPT TO UPDATE THE CONFIG FILE HERE #
config = getConfig()
r = requests.get(config['lastversionurl'])
if r.status_code == 200:
    rawtxt = r.text
    yamltext = yaml.safe_load(rawtxt)
    files = yamltext['files']
    for file in files:
        remotemd5 = file['md5']

        # check if file exists
        if not os.path.exists(file['path']):
            # download new file
            downloadFile(treatPath(file['path']), file['path'])

        localmd5 = hashFile(file['path'])
        if remotemd5 != localmd5:
            # need to download the file
            downloadFile(treatPath(file['path']), file['path'])
        else:
            print("File " + file['path'] + " is up to date")

    lastversion: str = yamltext['LastAppVersion']

    # find line that contains appversion
    # opening the file in read mode
    file = open("config.yaml", "r")
    replacement = ""
    # using the for loop
    for line in file:
        changes = ''
        if "appversion" in line:
            changes = f"appversion: {lastversion}\n"
            replacement += changes
        else:
            replacement += line

    file.close()
    # opening the file in write mode
    fout = open("config.yaml", "w")
    fout.write(replacement)
    fout.close()

# already updated files, try to open index.py
subprocess.Popen(['python', 'index.py'])
# close the assistant
sys.exit(0)

# END OF SCRIPT TO UPDATE THE CONFIG FILE HERE #
