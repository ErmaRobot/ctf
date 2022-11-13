#! /usr/bin/python

import sys
import signal

if len(sys.argv) != 2 and len(sys.argv) != 3:
  print('keyLength.py <cipher file> [<max key length>]')
  exit()

found = ''
with open(sys.argv[1], 'r') as f:
  found = f.read().lstrip().rstrip()

N = len(found)

MAX = N - 1
if len(sys.argv) == 3:
  MAX = int(sys.argv[2])

targetIC = 0.06
avgic = {}
lengths = []

def print_line(key_len, ic, delta):
  print('{}  {}  {}'.format(f'{key_len}'.rjust(2).ljust(6), f'{ic}'[:10].ljust(10), f'{delta}'[:10]))

def report():
  print('-'*32)
  print('The first {}'.format(int(MAX*0.1)))
  print('{}{}{}'.format('len(k)'.ljust(8), 'avg(IC)'.ljust(12), 'delta(0.06)'))
  plengths = sorted(lengths[:int(MAX * 0.10)], key=lambda x: int(x))
  for i in range(int(MAX * 0.10)):
    if i < len(plengths):
      print_line(plengths[i], avgic[plengths[i]], avgic[plengths[i]] - targetIC)

def interrupt_handler(signum, frame):
  if signum == signal.SIGINT:
    report()
    exit(0)

def calc_ic(m_gram, N):
  freqSigma = 0.0
  for c in m_gram.keys():
    freqSigma += m_gram[c] * (m_gram[c] - 1)

  return freqSigma / (N * (N - 1))

def count_gram(cipher, inc):
  m_gram = {}
  for i in range(0, len(cipher), inc):
    if cipher[i] in m_gram.keys():
      m_gram[cipher[i]] += 1
    else:
      m_gram[cipher[i]] = 1

  return m_gram

signal.signal(signal.SIGINT, interrupt_handler)

print(f'Calculating Mean I.C. for the first {MAX} key lengths')
print('{}{}{}'.format('len(k)'.ljust(8), 'avg(IC)'.ljust(12), 'delta(0.06)'))
for i in range(MAX):
  keylength = i + 1
  aic = 0.0
  for j in range(keylength):
    aic += calc_ic(count_gram(found[j:], keylength), N/keylength) 
  aic = aic / keylength
  avgic[f'{keylength}'] = aic
  print_line(keylength, aic, aic - targetIC)

lengths = sorted(avgic.keys(), key=lambda x: (avgic[x] - targetIC) * (avgic[x] - targetIC))
report()

