# -*- coding: utf-8 -*-

import argparse
import csv
from collections import Counter

import numpy as np
from sklearn import tree, preprocessing
from sklearn.metrics import confusion_matrix, f1_score
from sklearn.model_selection import cross_val_score
from pattern.text.es import tenses as tenses_es
from pattern.text.nl import tenses as tenses_nl

from languages.es import get_tense_es
from languages.nl import get_tense_nl


class Annotation(object):
    def __init__(self, language, identifier, target, words, pos, lemmata):
        self.identifier = identifier
        self.target = target
        self.words = list(filter(None, words))
        self.pos = list(filter(None, pos))
        self.lemmata = list(filter(None, lemmata))
        self.unf_words = words
        self.unf_pos = pos
        self.unf_lemmata = lemmata
        tense_func = tenses_es if language == 'es' else tenses_nl
        tenses = [tense_func(w) if w else '' for w in words]
        # For all features below, we take the first given tense classification by Pattern
        self.tense = [xstr(t[0][0]) if t else '' for t in tenses]
        self.person = [xstr(t[0][1]) if t else '' for t in tenses]
        self.number = [xstr(t[0][2]) if t else '' for t in tenses]
        self.mood = [xstr(t[0][3]) if t else '' for t in tenses]
        self.aspect = [xstr(t[0][4]) if t else '' for t in tenses]

    def to_array(self):
        return np.array(self.unf_words + self.unf_pos + self.unf_lemmata +
                        self.tense + self.person + self.number + self.mood + self.aspect)


def xstr(s):
    return '' if s is None else str(s)


def import_csv(language, filename):
    result = []

    with open(filename, 'r') as handler:
        word_columns = []
        pos_columns = []
        lemmata_columns = []

        reader = csv.reader(handler, delimiter=';')
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
                identifier = int(row[0])
                target = row[1]
                words = [row[c] for c in word_columns]
                pos = [row[c] for c in pos_columns]
                lemmata = [row[c] for c in lemmata_columns]
                result.append(Annotation(language, identifier, target, words, pos, lemmata))

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
            print('target:', annotation.target, annotation.pos, annotation.lemmata, ', but found:', results[n])
        else:
            correct += 1

    print(correct, total, correct/total)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Assign tenses')
    parser.add_argument('language', type=str)
    parser.add_argument('filename', type=str)
    args = parser.parse_args()

    annotations = import_csv(args.language, args.filename)

    X = np.array([a.to_array() for a in annotations])
    y = np.array([a.target for a in annotations])

    counter = Counter(y)
    print(counter)

    # Naive classifier
    results = assign_tenses(annotations, language=args.language)
    y_prediction = np.array(results)
    sorted_keys = [t for t, _ in counter.most_common()]
    print(sorted_keys)
    print(confusion_matrix(y, y_prediction, labels=sorted_keys))
    print(f1_score(y, y_prediction, labels=sorted_keys, average='micro'))
    # show_differences(annotations, results)

    # DecisionTreeClassifier
    X_labeling = dict()
    i = j = 0
    for n, column in enumerate(X.T):
        le = preprocessing.LabelEncoder()
        X[:, n] = le.fit_transform(column)

        for c in le.classes_:
            X_labeling[j] = str(i) + ': ' + c
            j += 1
        i += 1

    ohc = preprocessing.OneHotEncoder()
    X_OHC = ohc.fit_transform(X)

    clf = tree.DecisionTreeClassifier(max_depth=3)
    clf = clf.fit(X_OHC, y)

    import graphviz
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render('test')

    print(clf.score(X_OHC, y))
    print(cross_val_score(clf, X_OHC, y, cv=5))

    for f in clf.tree_.feature:
        if f in X_labeling:
            print(f, X_labeling[f])
