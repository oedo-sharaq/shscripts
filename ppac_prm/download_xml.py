#!/usr/bin/python
# coding: UTF-8

from urllib.request import urlopen
import re
import os
from html.parser import HTMLParser
import yaml
from yaml.loader import SafeLoader
import generate_yaml


def configure():
    script_path = os.path.dirname(os.path.realpath(__file__))
    obj = {}
    try:
        with open(script_path + '/config.yaml', 'r') as file:
            conf = yaml.load(file, Loader=SafeLoader)
            url = conf['url']
            path = conf['path']
            obj = {'url': url, 'path': path}
    except:
        print('config.yaml not found. Creating one...')
        print('Input url to the ppac xml download page (on bripscnt):')
        url = input()
        print('Input path to the xml/yaml file location:')
        path = input()
        obj = {'url': url, 'path': path}
        with open(script_path + '/config.yaml', 'w') as file:
            yaml.dump(obj, file)
    return obj


class Bripscnt01Parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.url = ""
        self.file_name = ""
        self.download_urls = []
        self.file_names = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs = dict(attrs)
            if 'href' in attrs:
                self.url = attrs['href']

    def handle_data(self, data):
        self.file_name = data

    def handle_endtag(self, tag):
        if self.url and re.match('^download', self.url):
            self.download_urls.append(self.url)
            self.file_names.append(self.file_name)
            self.url = ""
            self.file_name = ""


if __name__ == "__main__":

    conf = configure()
    url = conf['url']
    path = conf['path']
    list_page_response = urlopen(url+"xml.php")
    parser = Bripscnt01Parser()
    parser.feed(str(list_page_response.read()))
    list_page_response.close()
    download_response = urlopen(url+parser.download_urls[0])
    xml_file = open(path+parser.file_names[0], 'w')
    xml_file.write(download_response.read().decode('utf-8'))
    xml_file.close()
    download_response.close()
    os.system('rm '+path+'BigRIPSPPAC.xml')
    cmd = 'ln -s ' + path + \
        parser.file_names[0] + ' ' + path + 'BigRIPSPPAC.xml'
    os.system(cmd)

    yaml_name = generate_yaml.generate_yaml(path+parser.file_names[0])

    os.system('rm '+path+'ppac.prm.yaml')
    cmd = 'ln -s ' + yaml_name + ' ' + path + 'ppac.prm.yaml'
    os.system(cmd)
    parser.close()
