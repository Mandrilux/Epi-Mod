#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import requests
import json

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


def getFree(autologin, url):
    try:
        response = requests.get(url)
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        module = response.json()
        return (len(module))

def getSpace(autologin, data, free):
    for module in data['module']:
        print(module)
    #for module in modules:
        base = autologin + "/module/2019/" +  module['codebase']
        urlfree = base + "/registered/?format=json"
        url = base + "/?format=json"
        try:
            response = requests.get(url)
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            modulejson = response.json()
            module["student"] = getFree(autologin, urlfree)
            maxValue = modulejson["max_ins"]
            if maxValue is None:
                maxValue = 0
            else :
                maxValue = int(maxValue)
            module["max_student"] = maxValue
            #module.append(maxValue)
            print(module)
            if free:
                if module["student"] <  module["max_student"]:
                    print(module)
            else:
                print(module)

def getModule(autologin):
    #moduleslist = []
    data = {}
    data['module'] = []
    try:
        # If the response was successful, no Exception will be raised
        response = requests.get(autologin + "/course/filter?format=json&preload=1&location%5B%5D=FR&location%5B%5D=FR%2FPAR&course%5B%5D=master%2Fclassic&scolaryear%5B%5D=2019")
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        modules = response.json()
        nbmobule = modules["items"]
        print ("load %d modules" %len(modules["items"]))

        for module in modules["items"]:

            data['module'].append({
                'code':  module["codeinstance"],
                'codeinstance': module["codeinstance"],
                'codebase' : module["code"] + "/" + module["codeinstance"],
                'credit' : module["credits"],
                'begin' : module["begin"],
                'end' : module["end"],
                'open' : module["open"],
                'student' : 0,
                'max_student' : 0
                })


            #codeinstance = module["code"] + "/" + module["codeinstance"]
            #moduleslist.append([codeinstance, module["title"] , module["credits"]])
            #print (module["code"] + "/" + module["codeinstance"])
        return data


def WritejsonModule(modules):
    print ("Dump modules to json")
    with open('modules.json', 'w+') as outfile:
        json.dump(modules, outfile)

def loadModule():
    with open('modules.json') as json_file:
        data = json.load(json_file)
    return data


def main():
    freeModule = 0
    reloadM = 0

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", action="store_true", default=False)
    parser.add_argument("-f", "--free", action="store_true", default=False)
    parser.add_argument("-r", "--reload", action="store_true", default=False)
    try:
        args = parser.parse_args()
    except:
        sys.exit(0)
    if args.free:
        freeModule = 1
    if args.reload:
        reloadM = 1
    if args.config:
        autologin = createConfig()
    else:
        autologin = checkConfig()

    if reloadM:
        modules = getModule(autologin)
        WritejsonModule(modules)
    else:
        modules = loadModule()
    getSpace(autologin, modules, freeModule)

if __name__ == "__main__":
    main()
