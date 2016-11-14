from pyconcepticon.util import data_path
from pyconcepticon.api import Concepticon
from lingpy import *
from collections import defaultdict

con = Concepticon()
comb = csv2list('combined.tsv', strip_lines=False)

languages = ['es', 'fr', 'de', 'pt', 'ru', 'zh']
D = defaultdict(lambda : defaultdict(list))
for lang in languages:
    lst = csv2list(data_path('..', 'pyconcepticon', 'data', 'map-{0}.tsv'.format(lang)))
    for line in lst[1:]:
        gloss = line[1].split('///')[1]
        cid = line[0]
        D[cid][lang] += [gloss]
clists = ['Swadesh-1952-200', 'Swadesh-1955-100', 'Tadmor-2009-100',
        'Blust-2008-210', 'Matisoff-1978-200', 'Mann-2004-500']
for c in con.conceptsets.values():
    D[c.id]['definition'] += [c.definition]
for lst in clists:
    cls = con.conceptlists[lst]
    for c in cls.concepts.values():
        D[c.concepticon_id][lst] += [c.english]

combo = [['NUMBER', 'GLOSS', 'CONCEPTICON_ID', 'SEE_ALSO', 'DEFINITION'] + \
        [x.upper() for x in languages] + [x.replace('-', '_') for x in clists]]
for line in comb:
    no = line[0]
    cid = line[2]
    tmp = [no, line[1], line[2], line[3].replace('None', 'STDB')]
    tmp += [''.join(D[cid]['definition'])]
    for lst in languages + clists:
        if D[cid][lst]:
            tmp += [' // '.join(D[cid][lst])]
        else:
            tmp += ['']
    combo += [tmp]
with open('combined-list.tsv', 'w') as f:
    for line in combo:
        f.write('\t'.join(line)+'\n')
    

