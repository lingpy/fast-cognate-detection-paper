from bipskip.bipskip import fcdet, fast_ccm, make_skips
from sys import argv
from glob import glob
from itertools import product
from lingpy import *
from lingpy.evaluate.acd import *
import tqdm
from tabulate import tabulate
from lingpy.convert.strings import write_nexus

if 'ccm' in argv:
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test/*.tsv'))):
        wl = Wordlist(f)
        fast_ccm(wl, ref='autocog')
        p, r, fs = bcubes(wl, 'cogid', 'autocog', pprint=False)
        table += [[f[7:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 6, 4),
        round(sum([line[2] for line in table]) / 6, 4),
        round(sum([line[3] for line in table]) / 6, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))

if 'lexstat' in argv:
    if 'infomap' in argv:
        method='infomap'
        threshold=0.55
    else:
        method='upgma'
        threshold=0.6
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test/*.tsv'))):
        lex = LexStat(f)
        lex.get_scorer(runs=10000) 
        lex.cluster(method='lexstat', threshold=threshold, cluster_method=method, ref='autocog')
        p, r, fs = bcubes(lex, 'cogid', 'autocog', pprint=False)
        table += [[f[7:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 6, 4),
        round(sum([line[2] for line in table]) / 6, 4),
        round(sum([line[3] for line in table]) / 6, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))



if 'sca' in argv:
    if 'infomap' in argv:
        method='infomap'
    else:
        method='upgma'
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test/*.tsv'))):
        lex = LexStat(f)
        lex.cluster(method='sca', threshold=0.45, cluster_method=method, ref='autocog')
        p, r, fs = bcubes(lex, 'cogid', 'autocog', pprint=False)
        table += [[f[7:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 6, 4),
        round(sum([line[2] for line in table]) / 6, 4),
        round(sum([line[3] for line in table]) / 6, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))


if 'test' in argv:
    if 'infomap' in argv:
        method='infomap'
    else:
        method='cc'
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test/*.tsv'))):
        wl = Wordlist(f)
        fcdet(
                wl,
                exclude='V_+T',
                ngrams=4,
                ngram_gaps=True,
                cut=0.2,
                model=['sca'],
                gaps=True,
                all_ngrams=True,
                ref='autocog',
                method=method
                )
        p, r, fs = bcubes(wl, 'cogid', 'autocog', pprint=False)
        table += [[f[7:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 6, 4),
        round(sum([line[2] for line in table]) / 6, 4),
        round(sum([line[3] for line in table]) / 6, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))

if 'lexstat2' in argv:
    if 'infomap' in argv:
        method='infomap'
        threshold=0.55
    else:
        method='upgma'
        threshold=0.6
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test2/*.csv'))):
        lex = LexStat(f)
        lex.get_scorer(runs=10000)
        lex.cluster(method='lexstat', cluster_method=method, ref='autocog',
                threshold=threshold)
        lex.add_entries('cogidn', 'cogid,concept', lambda x, y:
                str(x[y[0]])+'-'+x[y[1]])
        lex.renumber('cogidn')
        if 'nex' in argv:
            write_nexus(lex, ref='autocog',
                    filename='nexus/'+method+f.split('/')[-1][4:-4]+'.nex')

        p, r, fs = bcubes(lex, 'cogidnid', 'autocog', pprint=False)
        table += [[f[16:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 5, 4),
        round(sum([line[2] for line in table]) / 5, 4),
        round(sum([line[3] for line in table]) / 5, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))



if 'sca2' in argv:
    if 'infomap' in argv:
        method='infomap'
    else:
        method='upgma'
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test2/*.csv'))):
        lex = LexStat(f)
        lex.cluster(method='sca', cluster_method=method, ref='autocog',
                threshold=0.45)
        lex.add_entries('cogidn', 'cogid,concept', lambda x, y:
                str(x[y[0]])+'-'+x[y[1]])
        lex.renumber('cogidn')
        if 'nex' in argv:
            write_nexus(lex, ref='autocog',
                    filename='nexus/'+method+f.split('/')[-1][4:-4]+'.nex')

        p, r, fs = bcubes(lex, 'cogidnid', 'autocog', pprint=False)
        table += [[f[16:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 5, 4),
        round(sum([line[2] for line in table]) / 5, 4),
        round(sum([line[3] for line in table]) / 5, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))

if 'ccm2' in argv:
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test2/*.csv'))):
        wl = Wordlist(f)
        fast_ccm(wl, ref='autocog')
        wl.add_entries('cogidn', 'cogid,concept', lambda x, y:
                str(x[y[0]])+'-'+x[y[1]])
        wl.renumber('cogidn')
        if 'nex' in argv:
            write_nexus(wl, ref='autocog',
                    filename='nexus/'+method+f.split('/')[-1][4:-4]+'.nex')

        p, r, fs = bcubes(wl, 'cogidnid', 'autocog', pprint=False)
        table += [[f[15:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 5, 4),
        round(sum([line[2] for line in table]) / 5, 4),
        round(sum([line[3] for line in table]) / 5, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))



if 'test2' in argv:
    if 'infomap' in argv:
        method='infomap'
    else:
        method='cc'
    table = []
    for f in tqdm.tqdm(sorted(glob('data/test2/*.csv'))):
        wl = Wordlist(f)
        fcdet(
                wl,
                exclude='V_+T',
                ngrams=4,
                ngram_gaps=True,
                cut=0.2,
                model=['sca'],
                gaps=True,
                all_ngrams=True,
                ref='autocog',
                method=method
                )
        wl.add_entries('cogidn', 'cogid,concept', lambda x, y:
                str(x[y[0]])+'-'+x[y[1]])
        wl.renumber('cogidn')
        if 'nex' in argv:
            write_nexus(wl, ref='autocog',
                    filename='nexus/'+method+f.split('/')[-1][4:-4]+'.nex')

        p, r, fs = bcubes(wl, 'cogidnid', 'autocog', pprint=False)
        table += [[f[15:-4], round(p, 2), round(r, 2), round(fs, 4)]]
    table += [['total', 
        round(sum([line[1] for line in table]) / 5, 4),
        round(sum([line[2] for line in table]) / 5, 4),
        round(sum([line[3] for line in table]) / 5, 4)]]

    print(tabulate(table, tablefmt='latex', headers=['data', 'p', 'r', 'fs']))

if 'training' in argv:
    ngrams = [4, 5, 3, 2, 6]
    excludes = [
            'V_+T',
            'V_+',
            '_+T',
            '_+',
            ][::-1]
    ngram_gaps = [True, False]
    allngrams = [True, False]
    cuts = [0.2, 0.4][::-1]
    models = [['sca'], ['asjp'], ['sca', 'asjp'], ['sca', 'dolgo'], ['asjp',
        'dolgo'], ['asjp', 'dolgo', 'sca'] ][::-1]
    gaps = [True, False]
    best = 0.0
    methods = [
            'infomap', #'multilevel', 
            'cc']
    for ngram, exclude, ngram_gap, cut, model, gap, allngram, method in product(
            ngrams, excludes, ngram_gaps, cuts, models, gaps, allngrams,
            methods):
        table = []
        if 'sea' in argv:
            files = [f for f in glob('data/training/*.csv') if 'BAI' in f or 'SIN' in f]
            print(len(files))
        else:
            files = [f for f in glob('data/training/*.csv') if not 'BAI' in f
                    and not 'SIN' in f]
        for f in files:# glob('data/training/*.csv'):
            wl = Wordlist(f)
            if not 'tokens' in wl.header:
                wl.add_entries('tokens', 'ipa', ipa2tokens)

            fcdet(
                    wl, 
                    exclude=exclude,
                    ngrams=ngram,
                    ngram_gaps=ngram_gap,
                    cut=cut,
                    model=model,
                    gaps=gap,
                    all_ngrams=allngram,
                    ref='autocog',
                    method=method
                    )
            p, r, fs = bcubes(wl, 'cogid', 'autocog', pprint=False)
            print(f, p, r)

            table += [[f[:-4], round(p, 2), round(r, 2), round(fs, 4)]]
        
        fs =  round(sum([line[3] for line in table]) / len(table), 4)
        if fs > best:
            best = fs
            star = '*'
        else:
            star = ' '

        print('{0:5} | {1} | {2:6} | {3:6} | {4:6} | {5:6} | {6:6} | {7:.2f} | {8:.2f} | {9:.4f} | {10:10} {11}'.format(
            exclude,
            ngram,
            str(ngram_gap),
            cut,
            '/'.join(model),
            str(gap),
            str(allngram),
            round(sum([line[1] for line in table]) / len(table), 2),
            round(sum([line[2] for line in table]) / len(table), 2),
            round(sum([line[3] for line in table]) / len(table), 4),
            method,
            star,
            ))

if 'bipskip' in argv:
    
    all_forms = defaultdict(list)
    segs = []
    for i, word in enumerate(argv[2:]):
        segments = ipa2tokens(word)
        segs += [''.join(tokens2class(segments, 'sca'))]
        skips = make_skips(segments, ngrams=5, gaps=True, ngram_gaps=False,
                all_ngrams=True)
        for skip in skips:
            all_forms[skip] += [i]

    table = [['Skip-Gr.']+segs]
    for skip, refs in sorted(all_forms.items(), key=lambda x: x[0]):
        if len(refs) > 1:
            line = [skip]
            for i in range(len(argv[2:])):
                if i in refs:
                    line += ['+']
                else:
                    line += ['-']
            table += [line]
    print(tabulate(table, headers=argv[2:], #str(i+1) for i in range(len(argv[2:]))], 
        tablefmt='latex'))
        
