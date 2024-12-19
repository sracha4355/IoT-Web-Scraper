#metrics.py
import numpy as np

def get_vocab(token_list):
    vocab = []
    for token in token_list:
        if token not in vocab:
            vocab.append(token)

    return vocab

def to_unigram(token_list, vocab):
    counts = {}
    total = len(token_list)
    v = len(vocab)
    for token in vocab:
        counts[token] = 1
    for token in token_list:
        counts[token] += 1
    probs = {}
    for i in range(v):
        probs[list(counts.keys())[i]] = ( list(counts.values())[i])/ ( total + v )
    return probs

def kl_divergence(p, q):
    p_arr = np.array(list(p.values()))
    q_arr = np.array(list(q.values()))
    d_kl = np.sum(p_arr * np.log(p_arr / q_arr))
    return d_kl

def span_distinctiveness(span_tokens, all_tokens):
    vocab = get_vocab(all_tokens)
    p = to_unigram(all_tokens, vocab)
    p_span = to_unigram(span_tokens, vocab)
    return float(kl_divergence(p_span, p))

def boundary_distinctiveness(bound_tokens, all_tokens):
    vocab = get_vocab(all_tokens)
    p = to_unigram(all_tokens, vocab)
    p_bound = to_unigram(bound_tokens, vocab)
    return float(kl_divergence(p_bound, p))