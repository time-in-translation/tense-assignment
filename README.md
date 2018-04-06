# tense-assignment

This is a simple script (`process.py`) that reads in a .csv-file and assigns a tense.

## Requirements

### Python

This script runs in Python 2.7 and requires an external package to run: [Pattern](https://www.clips.uantwerpen.be/pattern). You can install this package either locally (in a [virtualenv](http://virtualenv.readthedocs.io/en/latest/)) or globally by running:

	pip install -r requirements.txt

## Running the script

Run the `process.py` script. It requires two parameters: your language of choice for tense assignment, and your input file. In the `examples/` directory you can find two example .csv-files. Run

	python process.py nl examples/nl.csv

to process the Dutch example.

