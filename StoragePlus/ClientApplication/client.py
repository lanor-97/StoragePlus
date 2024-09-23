#!/bin/python3

import requests
from os import environ
import shutil

import warnings
warnings.filterwarnings("ignore")

SERVER_URL = 'https://storageplus:3333'


def login():
    username = input('username: ')
    password = input('password: ')

    r = requests.post(SERVER_URL + "/app-login", verify=False,
                      data={'username': username, 'password': password})
    if r.status_code == 200 and r.text == "Y":
        print("Login successful")
        return True
    elif r.status_code == 200 and r.text == 'N':
        print("Wrong credentials")
    return False


def register():
    username = input('username: ')
    password = input('password: ')

    r = requests.post(SERVER_URL + "/app-register", verify=False,
                      data={'username': username, 'password': password})
    if r.status_code == 200 and r.text == "Y":
        print("Login successful")
        return True
    elif r.text == 'N':
        print("Registration not possible")
    return False


def list_files_action():
    r = requests.get(SERVER_URL + "/list-files", verify=False)

    if r.status_code == 200:
        if r.text == "N":
            print('No files at the moment')
        else:
            for file_ in r.text.split(','):
                print(file_)


def download_action():
    filename = input('Filename: ')
    r = requests.get(SERVER_URL + "/userfiles/" + filename,
                     stream=True, verify=False)

    if(r.status_code == 200):
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Download successful')
    elif r.status_code == 404:
        print('No file found with this name')


def upload_action():
    filename = input('Filename: ')
    files = {'file': open(filename, 'rb')}
    r = requests.post(SERVER_URL + "/upload/" + filename, files=files, verify=False)

    if r.status_code == 200 and r.text == 'Y':
        print('Upload successful')
    else:
        print('Something went wrong')


def delete_action():
    filename = input('Filename: ')
    r = requests.post(SERVER_URL + "/delete", verify=False,
                      data={'filename': filename})

    if r.status_code == 200 and r.text == "Y":
        print("File deleted")
    elif r.text == "N":
        print("File not found")


if __name__ == '__main__':
    # app
    logged_in = False
    while (not logged_in):
      print('Welcome to StoragePlus, please select\n(1) login\n(2) register\n(3) quit')
      action = input()

      if action == '1':
        logged_in = True if login() else False
      elif action == '2':
        logged_in = True if register() else False
      elif action == '3':
        exit()
      else:
        print('Invalid input')

    quit = False
    while (not quit):
        print('What you want to do?\n(1) list files\n(2) download\n(3) upload\n(4) delete\n(5) quit')
        action = input()

        if action == '1':
            list_files_action()

        elif action == '2':
            download_action()

        elif action == '3':
            upload_action()

        elif action == '4':
            delete_action()
        elif action == '5':
            requests.get(SERVER_URL + "/logout", verify=False)
            quit = True
            print('Quitting . . . ')
        else:
            print('Invalid input')
