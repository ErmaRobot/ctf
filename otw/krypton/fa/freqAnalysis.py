#! /usr/bin/python

import sys

def read_grams(f):
  grams = {}
  with open(f) as fin:
    for line in fin:
      gram = line.split(' ')
      grams[gram[0]] = float(gram[1])
  return grams

class n_gram:
  def __init__(self):
    self.mono = {}
    self.di = {}
    self.tri = {}
    self.quad = {}

if len(sys.argv) != 2:
  print('freAnalysis.py [found cipher text file]')

english = n_gram()
crypt = n_gram()

english.mono = read_grams('english_monograms')
english.di = read_grams('english_digrams')
english.tri = read_grams('english_trigrams')
english.quad = read_grams('english_quadgrams')

found = ''
with open(sys.argv[1]) as cin:
  found = cin.read().lstrip().rstrip()

#init window
window = f'{found[0]}{found[1]}{found[2]}{found[3]}'
crypt.mono[found[0]] = 1
crypt.mono[found[1]] = 1
crypt.mono[found[2]] = 1
crypt.di[window[:2]] = 1
crypt.di[window[1:3]] = 1
crypt.tri[window[:3]] = 1
#loop through remaining found text
for i in range(4, len(found)):
  #quad
  if window in crypt.quad.keys():
    crypt.quad[window] += 1
  else:
    crypt.quad[window] = 1
  #tri
  if window[1:] in crypt.tri.keys():
    crypt.tri[window[1:]] += 1
  else:
    crypt.tri[window[1:]] = 1
  #di
  if window[2:] in crypt.di.keys():
    crypt.di[window[2:]] += 1
  else:
    crypt.di[window[2:]] = 1
  #mono
  if window[3] in crypt.mono.keys():
    crypt.mono[window[3]] += 1
  else:
    crypt.mono[window[3]] = 1
  #update window
  window = f'{window[1]}{window[2]}{window[3]}{found[i]}'

for m in crypt.mono.keys():
  crypt.mono[m] = (crypt.mono[m] / len(found)) * 100
for d in crypt.di.keys():
  crypt.di[d] = (crypt.di[d] / (len(found)-1)) * 100
for t in crypt.tri.keys():
  crypt.tri[t] = (crypt.tri[t] / (len(found)-2)) * 100
for q in crypt.quad.keys():
  crypt.quad[q] = (crypt.quad[q] / (len(found)-3)) * 100

#print frequency analysis of english vs found cipher text to .csv
print(f'Printing analysis to {sys.argv[1]}_analysis.csv')
csv = open(f'{sys.argv[1]}_analysis.csv', 'w')
csv.write('english monograms,,cipher monograms,,english digrams,,cipher digrams,,english trigrams,,cipher trigrams,,english quadgrams,,cipher quadgrams\n')

ekeys = {'m':[x for x in english.mono.keys()], 'd':[x for x in english.di.keys()], 't':[x for x in english.tri.keys()], 'q':[x for x in english.quad.keys()]}
ckeys = {}
ckeys['m'] = sorted(crypt.mono.keys(), key=lambda x: crypt.mono[x], reverse=True)
ckeys['d'] = sorted(crypt.di.keys(), key=lambda x: crypt.di[x], reverse=True)
ckeys['t'] = sorted(crypt.tri.keys(), key=lambda x: crypt.tri[x], reverse=True)
ckeys['q'] = sorted(crypt.quad.keys(), key=lambda x: crypt.quad[x], reverse=True)
for i in range(26):
  output = ''
  #mono - english, cipher
  output += ekeys['m'][i] + ',' + '{:.3f}'.format(english.mono[ekeys['m'][i]])
  output += ','
  output += ckeys['m'][i] + ',' + '{:.3f}'.format(crypt.mono[ckeys['m'][i]])
  output += ','
  #di - english, cipher
  output += ekeys['d'][i] + ',' + '{:.3f}'.format(english.di[ekeys['d'][i]])
  output += ','
  output += ckeys['d'][i] + ',' + '{:.3f}'.format(crypt.di[ckeys['d'][i]])
  output += ','
  #tri - english, cipher
  output += ekeys['t'][i] + ',' + '{:.3f}'.format(english.tri[ekeys['t'][i]])
  output += ','
  output += ckeys['t'][i] + ',' + '{:.3f}'.format(crypt.tri[ckeys['t'][i]])
  output += ','
  #quad - english, cipher
  output += ekeys['q'][i] + ',' + '{:.3f}'.format(english.quad[ekeys['q'][i]])
  output += ','
  output += ckeys['q'][i] + ',' + '{:.3f}'.format(crypt.quad[ckeys['q'][i]])
  output += '\n'
  csv.write(output)

csv.close()

print(''.join(ekeys['m']))
print(''.join(ckeys['m']))

