# -*- coding: utf-8 -*-

from pattern.text import PRESENT, PAST, IMPERFECTIVE
from pattern.text.es import tenses


def get_tense_es(words, pos, lemmata):
    """
    Very naive implementation of a classifier for Spanish tense
    :param words: annotated words/tokens
    :param pos: part-of-speech tags for the annotated words
    :param lemmata: lemmata for the annotated words
    :return: a (probable) tense
    """
    tense = ''

    if len(pos) == 1:
        if pos[0] in ['VEfin', 'VHfin', 'VLfin', 'VMfin', 'VSfin']:
            t = tenses(words[0])
            if t and t[0][0] == PRESENT:
                tense = u'presente'
            if t and t[0][0] == PAST:
                if t[0][4] == IMPERFECTIVE:
                    tense = u'pretérito imperfecto'
                else:
                    tense = u'pretérito indefinido'
        if pos[0] == 'VLger':
            tense = u'gerundio'
    if len(pos) == 2:
        if pos[0] == 'VHfin' and pos[1] in ['VEadj', 'VHadj', 'VLadj', 'VMadj', 'VSadj']:
            tense = u'pretérito perfecto compuesto'
        elif pos[0] == 'SE' and pos[1] == 'VLfin':
            tense = u'presente'
        elif pos[0] == 'VEfin' and pos[1] == 'VLadj':
            tense = u'gerundio'
    if len(pos) == 3:
        if pos == ['SE', 'VHfin', 'VLadj']:
            tense = u'pretérito perfecto compuesto'
        elif pos == ['VLfin', 'PREP', 'VLinf'] or pos == ['VLfin', 'CSUBI', 'VLinf']:
            tense = u'pasado reciente'

    return tense
