#! /usr/bin/python

import sys

if len(sys.argv) != 3:
  print('keyGuess <key length> <found cipher text file>')
  exit()

found = ''
with open(sys.argv[2], 'r') as f:
  found = f.read().lstrip().rstrip()

N = len(found)
keylength = int(sys.argv[1])
alphabet = [chr(x) for x in range(65, 91)]

expected = {}
with open('english_monograms', 'r') as f:
  for line in f.read().lstrip().rstrip().split('\n'):
    data = line.split(' ')
    expected[data[0]] = int(float(data[1]) * (N / keylength))

def chisquare(test_dist, ex_dist):
  sigma = 0.0
  for c in alphabet:
    sigma += ((test_dist[c] - ex_dist[c]) * (test_dist[c] - ex_dist[c])) / ex_dist[c]

  return sigma 

def test_cycle(spot):
  chis = {}
  for c in alphabet:
    count = {}
    for i in range(spot, len(found), keylength):
      dec = chr((ord(found[i]) + ord(c) - 130) % 26 + 65)
      if dec in count.keys():
        count[dec] += 1
      else:
        count[dec] = 1

      for x in [x for x in alphabet if x not in count.keys()]:
        count[x] = 0

    chis[c] = chisquare(count, expected)

  return chis

guess = []
for i in range(keylength):
  test = test_cycle(i)
  guess.append(sorted(test.keys(), key=lambda x: test[x], reverse=True))

for i in range(len(alphabet)):
  for j in range(keylength):
    print(' {} '.format(guess[j][i]), end='')
  print()

