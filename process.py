# -*- coding: utf-8 -*-

import argparse
import codecs

from sklearn import tree

from languages.es import get_tense_es
from languages.nl import get_tense_nl
from utils import unicode_csv_reader


class Annotation(object):
    def __init__(self, id, target, words, pos, lemmata):
        self.id = id
        self.target = target
        self.words = filter(None, words)
        self.pos = filter(None, pos)
        self.lemmata = filter(None, lemmata)


def import_csv(filename):
    result = []

    with codecs.open(filename, 'rb', 'utf-8') as f:
        word_columns = []
        pos_columns = []
        lemmata_columns = []

        reader = unicode_csv_reader(f, delimiter=';')
        for i, row in enumerate(reader):
            if i == 0:  # header row
                for j, r in enumerate(row):
                    if r.startswith('w'):
                        word_columns.append(j)
                    if r.startswith('pos'):
                        pos_columns.append(j)
                    if r.startswith('lemmata'):
                        lemmata_columns.append(j)
            else:  # other rows
                id = int(row[0])
                target = row[1]
                words = [row[c] for c in word_columns]
                pos = [row[c] for c in pos_columns]
                lemmata = [row[c] for c in lemmata_columns]
                result.append(Annotation(id, target, words, pos, lemmata))

    return result


def assign_tenses(annotations, language):
    result = []

    for annotation in annotations:
        if language == 'es':
            result.append(get_tense_es(annotation.words, annotation.pos, annotation.lemmata))
        if language == 'nl':
            result.append(get_tense_nl(annotation.words, annotation.pos, annotation.lemmata))

    return result


def show_differences(annotations, results):
    total = 0
    correct = 0

    for n, annotation in enumerate(annotations):
        total += 1
        if annotation.target != results[n]:
            print 'target:', annotation.target, annotation.pos, ', but found:', results[n]
        else:
            correct += 1

    print correct, total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assign tenses')
    parser.add_argument('language', type=str)
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    annotations = import_csv(args.filename)
    results = assign_tenses(annotations, language=args.language)

    from sklearn.datasets import load_iris
    iris = load_iris()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(iris.data, iris.target)
    print annotations
    print iris.data

    # show_differences(annotations, results)

