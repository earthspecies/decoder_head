# AUTOGENERATED! DO NOT EDIT! File to edit: 00_data.ipynb (unless otherwise specified).

__all__ = ['get_en_es_dict', 'top_n_translation_acc', 'embs_to_txt', 'txt_to_embs']

# Comes from 03_translate_en_to_es.ipynb, cell

from collections import defaultdict

def get_en_es_dict(vocab_en, vocab_es):
    with open('data/en-es.txt') as f:
        en_es = f.readlines()
    en_es = [l.strip() for l in en_es]

    en_es_dict = defaultdict(list)
    for l in en_es:
        source, target = l.split()
        en_es_dict[source].append(target)

    # check that we have the source word in the model trained on English
    vocab_en_set = set(vocab_en)
    en_es_dict = {k: v for k, v in en_es_dict.items() if k in vocab_en_set}

    # make sure we have the target word in Spanish
    vocab_es_set = set(vocab_es)
    en_es_dict = {k: vocab_es_set.intersection(set(v)) for k, v in en_es_dict.items() if vocab_es_set.intersection(set(v))}

    return en_es_dict

# Comes from 03_translate_en_to_es.ipynb, cell
def top_n_translation_acc(top_n=1):
    p = learn.model[0].encoder.p
    hits = 0
    for k, v in en_es_dict.items():
        idx_en = vocab_en.index(k)
        print(k, [vocab_es[i] for i in p[idx_en].argsort(descending=True)[:5]])
        for vv in v:
            idx_es = vocab_es.index(vv)
            if idx_es in p[idx_en].argsort(descending=True)[:top_n]:
                hits += 1
                break
    return hits/len(en_es_dict)

# Comes from 05_aligning_the_embeddings_using_vecmap.ipynb, cell
import numpy as np

# Comes from 05_aligning_the_embeddings_using_vecmap.ipynb, cell
def embs_to_txt(vocab, embeddings, fname):
    '''writes embeddings to txt file in word2vec format'''
    lines = []
    lines.append(f'{len(vocab)} {embeddings.shape[1]}\n')
    for word, t in zip(vocab, embeddings):
        word = re.subn('\n', '', word)[0]
        lines.append(f"{word} {' '.join([str(datum.item()) for datum in t])}\n")
    with open(fname, 'w') as f:
        f.writelines(lines)

# Comes from 05_aligning_the_embeddings_using_vecmap.ipynb, cell

def txt_to_embs(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()
    vocab = []
    embs = []
    for line in lines[1:]:
        l = line.split()
        vocab.append(l[0])
        embs.append(np.array([float(s) for s in l[1:]]))
    return vocab, np.stack(embs)