# -*- coding: utf-8 -*-

def get_tense_nl(words, pos, lemmata):
    """
    Very naive implementation of a classifier for Dutch tense
    :param words: annotated words/tokens
    :param pos: part-of-speech tags for the annotated words
    :param lemmata: lemmata for the annotated words
    :return: a (probable) tense
    """
    tense = ''

    if len(pos) == 1:
        if pos[0] in ['verbpressg', 'verbprespl']:
            tense = 'ott'
        elif pos[0] in ['verbpastsg', 'verbpastpl']:
            tense = 'ovt'
    if len(pos) == 2:
        if set(pos) == {'verbpressg', 'verbpapa'} or set(pos) == {'verbprespl', 'verbpapa'}:
            tense = 'vtt'
        if set(pos) == {'verbpastsg', 'verbpapa'} or set(pos) == {'verbpastpl', 'verbpapa'}:
            tense = 'vvt'
    if len(pos) == 3:
        if set(pos) == {'pronrefl', 'verbpressg', 'verbpapa'} or set(pos) == {'pronrefl', 'verbprespl', 'verbpapa'}:
            tense = 'vtt'
        if set(pos) == {'pronrefl', 'verbpastsg', 'verbpapa'} or set(pos) == {'pronrefl', 'verbpastpl', 'verbpapa'}:
            tense = 'vvt'

    return tense
