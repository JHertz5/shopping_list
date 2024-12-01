#!/usr/bin/env python

import os
import subprocess

# This dict is the definition of the version number.
version_dict = {
    'major': 3,
    'minor': 5,
    'patch': 5
}
version_string = '.'.join(str(c) for c in version_dict.values())


def string_version_info():

    sVersion, sShaNum = get_version_info()
    return_string = 'shopping_list version: ' + str(sVersion) + ', Git commit SHA: ' + str(sShaNum)
    return return_string


def get_version_info():

    if reporting_from_zip_file():
        return version_string + '+zip.file', 'Unknown.  Installed via zip file.'

    if reporting_from_git_repo():
        return_path = os.getcwd()
        repo_path = os.path.dirname(__file__)
        os.chdir(repo_path)
        version_list = "0"  # version if no tags (shallow checkout)
        try:
            git_tag_version = subprocess.check_output(['git', 'describe', '--tags'])
            git_tag_version = str(git_tag_version.decode('utf-8')).split('\n')
            version_list = git_tag_version[0].split('-')
            version_string = str(version_list[0]) + '.dev' + str(version_list[1])
            sha_num = str(version_list[-1][1:])
        except (IndexError, subprocess.CalledProcessError):
            version_string = str(version_list[0])
            git_tag_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
            git_tag_version = str(git_tag_version.decode('utf-8')).split('\n')
            sha_num = str(git_tag_version[0])
        os.chdir(return_path)
        return version_string, sha_num


def reporting_from_git_repo():
    sPath = os.path.dirname(__file__)
    if os.path.isdir(os.path.join(sPath, '..', '.git')):
        return True
    return False


def reporting_from_zip_file():
    return not reporting_from_git_repo()

if __name__ == '__main__':
    # Print simple version number when called directly.
    print(version_string)
