# -*- coding: utf-8 -*-

# Copyright (c) 2006 - 2020 Detlev Offenbach <detlev@die-offenbachs.de>
#

"""
Module implementing some common utility functions for the subversion package.
"""


import os

import Utilities

from .Config import DefaultConfig, DefaultIgnores


def getServersPath():
    """
    Module function to get the filename of the servers file.
    
    @return filename of the servers file (string)
    """
    if Utilities.isWindowsPlatform():
        appdata = os.environ["APPDATA"]
        return os.path.join(appdata, "Subversion", "servers")
    else:
        homedir = Utilities.getHomeDir()
        return os.path.join(homedir, ".subversion", "servers")


def getConfigPath():
    """
    Module function to get the filename of the config file.
    
    @return filename of the config file (string)
    """
    if Utilities.isWindowsPlatform():
        appdata = os.environ["APPDATA"]
        return os.path.join(appdata, "Subversion", "config")
    else:
        homedir = Utilities.getHomeDir()
        return os.path.join(homedir, ".subversion", "config")


def createDefaultConfig():
    """
    Module function to create a default config file suitable for eric.
    """
    config = getConfigPath()
    try:
        os.makedirs(os.path.dirname(config))
    except OSError:
        pass
    try:
        f = open(config, "w")
        f.write(DefaultConfig)
        f.close()
    except IOError:
        pass


def amendConfig():
    """
    Module function to amend the config file.
    """
    config = getConfigPath()
    try:
        f = open(config, "r")
        configList = f.read().splitlines()
        f.close()
    except IOError:
        return
    
    newConfig = []
    ignoresFound = False
    amendList = []
    for line in configList:
        if line.find("global-ignores") in [0, 2]:
            ignoresFound = True
            if line.startswith("# "):
                line = line[2:]
            newConfig.append(line)
            for amend in DefaultIgnores:
                if amend not in line:
                    amendList.append(amend)
        elif ignoresFound:
            if line.startswith("##"):
                ignoresFound = False
                if amendList:
                    newConfig.append("  " + " ".join(amendList))
                newConfig.append(line)
                continue
            elif line.startswith("# "):
                line = line[2:]
            newConfig.append(line)
            oldAmends = amendList[:]
            amendList = []
            for amend in oldAmends:
                if amend not in line:
                    amendList.append(amend)
        else:
            newConfig.append(line)
    
    if newConfig != configList:
        try:
            f = open(config, "w")
            f.write("\n".join(newConfig))
            f.close()
        except IOError:
            pass
