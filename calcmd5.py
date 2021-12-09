"""
Calculates the MD5 hash of a given file.
"""

import hashlib
import yaml

stream = open("update.yaml", 'r')
if stream is not None:
    # file is not empty, panic if its empty!!!
    md5 = hashlib.md5()
    configs = yaml.safe_load(stream)
    stream.close()
    files = configs['files']
    for file in files:
        with open(file['path'], 'rb') as filestream:
            for chunk in iter(lambda: filestream.read(4096), b""):
                md5.update(chunk)
        file['md5'] = md5.hexdigest()
        filestream.close()
    with open("update.yaml", 'w') as stream:
        yaml.dump(configs, stream, indent=2, default_flow_style=False)

# add comments again because of the yaml.dump() call
comments = """# when adding a new file, add it to the list of files to be updated
# and leave the md5 value empty. Then execute the calcmd5.py script
# to calculate the md5 sum of all files and update them in the config
# add the like this
# files:
#   - path: ./path/to/file
#   - md5: <----Leave this empty!

# config.yaml doesn't need to go here! It has its own versioning and
# uses a special function to not lose data in case of an update

# all paths are relative to calcmd5.py !!!! it will not work it's anywhere else
# ./ means the root folder of the repo

"""
with open("update.yaml", 'r+') as stream:
    contents = stream.read()
    stream.seek(0)
    stream.write(comments)
    stream.write(contents)
    stream.close()




