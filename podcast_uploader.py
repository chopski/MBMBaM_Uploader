#!/usr/bin/python3
import dropbox
from dbaccess import token
import os
from requests import get
import urllib.request
from bs4 import BeautifulSoup
import sys
from pushbullet import Pushbullet
from pbkey import *

# mbmbam address
mbmbam_url = "http://www.maximumfun.org/shows/my-brother-my-brother-and-me"
# access to dropbox
dbx = dropbox.Dropbox(token)
# pushbullet access
pb = Pushbullet(api_key)

# was going to need to do this more than once so made it a function
def create_soup(address):
    mbmbam = urllib.request.urlopen(address)
    mbmbam_source = mbmbam.read()
    soup = BeautifulSoup(mbmbam_source,"html5lib")
    return soup

# open mbmbam link, create soup object of source, find link of latest show
def get_latest_ep_url():
    soup = create_soup(mbmbam_url)
    latest_ep_a = soup.find("a",string="Show notes")
    latest_ep_href = latest_ep_a['href']
    latest_ep_url = "http://www.maximumfun.org" + latest_ep_href
    return latest_ep_url

# open link of latest show, create soup object of source, find link to download
def get_dl_url():
    latest_ep_url = get_latest_ep_url()
    soup = create_soup(latest_ep_url)
    dl_a = soup.find("a",string="Download This Show")
    dl_url = dl_a['href']
    return dl_url

# need to do this in order to remove '/' from the date
def converter(dte):
    date_lst = list(dte)
    for i in date_lst:
        if i == "/":
            date_lst.remove(i)
    converted_date = ''.join(date_lst)
    return converted_date

# this is a bit more intuitive than using datetime. Gets actual date
# that the podcast was submitted
def get_posted_date():
    url = get_latest_ep_url()
    soup = create_soup(url)
    posted_tag = soup.find("span",class_="submitted")
    posted = posted_tag.text
    posted_lst = posted.split()
    for i in posted_lst:
        if "/" in i:
            date = i
        else:
            continue
    return date

# open latest episode, create soup object of source, find ep title and
# concatenate the date plus file format
def create_file_name():
    date = get_posted_date()
    converted_date = converter(date)
    latest_ep_url = get_latest_ep_url()
    soup = create_soup(latest_ep_url)
    show_title_tag = soup.find("h2",class_=" ")
    show_title = show_title_tag.text
    file_name = show_title + " " + converted_date + ".mp3"
    return file_name

# download function gets url then writes the content to file_name
def download(addr,fname):
    with open(fname,"wb") as file:
        response = get(addr)
        file.write(response.content)
        file.close()

# upload to dropbox
def upload(fobject,fpath):
    dbx.files_upload(fobject,fpath)

def main():
    print('Executing script...')
    file_name = create_file_name()
    if file_name in open("episode_cache.txt","r").readline():
        sys.exit()
    else:
        with open("episode_cache.txt","w") as file:
            file.write(file_name + "\n")
            file.close()
        dl_url = get_dl_url()
        download(dl_url,file_name)
        podcast = open(file_name,"rb")
        upload(podcast,"/MBMBaM/" + file_name)
        podcast.close()
        os.remove(file_name)
        push = pb.push_note("New MBMBaM","The new MBMBaM has been uploaded to your Dropbox. Kiss your dad square on the lips.")

if __name__ == "__main__":
    main()
