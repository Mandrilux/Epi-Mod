#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
def createConfig():
    try:
        f = open(".config_mod", "w+")
    except IOError:
        print("Erreur")
        return False
    autologin = input("Enter your autologin : \nExample : https://intra.epitech.eu/auth-dcb39b4bd4b964526379fefa59fcd03403ae3\n")
    f.write(autologin)
    f.close()
    return (autologin)

def checkConfig():
    try:
        f = open(".config_mod", "r")
        autologin = f.read().replace('\n', '')
        f.close()
    except IOError:
        print("l'autologin is not configured")
        print("Please restart with parametre --config")
        sys.exit(-1)
    return autologin

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true", default=False)
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)
    if args.config:
        autologin = createConfig()
    else:
        autologin = checkConfig()
    print ("Recuperation des modules depuis l'intra")
    print("Your auto login is %s" % autologin)

if __name__ == "__main__":
    main()
