# -*- coding: utf-8 -*-

import argparse
import codecs
from collections import Counter

import numpy as np
from sklearn import tree, preprocessing
from sklearn.model_selection import cross_val_score

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
        self.unf_pos = pos
        self.unf_lemmata = lemmata

    def to_array(self):
        return np.array(self.unf_pos + self.unf_lemmata)


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
                    if r.startswith('lem'):
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

    X = np.array([a.to_array() for a in annotations])
    y = np.array([a.target for a in annotations])
    print Counter(y)

    X_labeling = dict()
    i = j = 0
    for n, column in enumerate(X.T):
        le = preprocessing.LabelEncoder()
        le.fit(column)
        X[:, n] = le.transform(column)

        for c in le.classes_:
            X_labeling[j] = str(i) + ': ' + c
            j += 1
        i += 1

    enc = preprocessing.OneHotEncoder()
    enc.fit(X)
    X_OHC = enc.transform(X)

    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(X_OHC, y)

    import graphviz
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render('test')

    print clf.score(X_OHC, y)

    print cross_val_score(clf, X_OHC, y, cv=10)

    for f in clf.tree_.feature:
        if f in X_labeling:
            print f, X_labeling[f]

    # print results

    # show_differences(annotations, results)

