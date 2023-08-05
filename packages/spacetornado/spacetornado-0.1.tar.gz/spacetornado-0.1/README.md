# SpaceTornado

A tiny [Tornado](https://www.tornadoweb.org/en/stable/) API for [Spacy](https://spacy.io/) text analytics.

## Requirements

The following are required to run `spacetornado` in a Unix environment:

- Python 3
- Pip 3

## Installation

`pip install spacetornado`

## Usage

First download a Spacy language model.

```bash
python -m spacy download en_core_web_sm
```

Modify `spacetornado/server.py` to configure the server:

```python
# Production-ready configuration solution :)
host = "localhost"
port = "8888"
```

Start it with `spacetornado`, then take it for a spin!

```bash
> $ curl -X POST --data "text=Who said there were no tornados in space?" http://localhost:8888/tokens
> [
    {
        "text": "Who",
        "lemma": "who",
        "pos": "PRON",
        "tag": "WP",
        "prettytag": "wh-pronoun, personal",
        "dep": "nsubj",
        "shape": "Xxx",
        "alpha": "True",
        "stop": "True"
    },
    {
        "text": "said",
        "lemma": "say",
        "pos": "VERB",
        "tag": "VBD",
        "prettytag": "verb, past tense",
        "dep": "ROOT",
        "shape": "xxxx",
        "alpha": "True",
        "stop": "False"
    },
    {
        "text": "there",
        "lemma": "there",
        "pos": "PRON",
        "tag": "EX",
        "prettytag": "existential there",
        "dep": "expl",
        "shape": "xxxx",
        "alpha": "True",
        "stop": "True"
    },
    {
        "text": "were",
        "lemma": "be",
        "pos": "AUX",
        "tag": "VBD",
        "prettytag": "verb, past tense",
        "dep": "ccomp",
        "shape": "xxxx",
        "alpha": "True",
        "stop": "True"
    },
    {
        "text": "no",
        "lemma": "no",
        "pos": "DET",
        "tag": "DT",
        "prettytag": "determiner",
        "dep": "det",
        "shape": "xx",
        "alpha": "True",
        "stop": "True"
    },
    {
        "text": "tornados",
        "lemma": "tornado",
        "pos": "NOUN",
        "tag": "NNS",
        "prettytag": "noun, plural",
        "dep": "attr",
        "shape": "xxxx",
        "alpha": "True",
        "stop": "False"
    },
    {
        "text": "in",
        "lemma": "in",
        "pos": "ADP",
        "tag": "IN",
        "prettytag": "conjunction, subordinating or preposition",
        "dep": "prep",
        "shape": "xx",
        "alpha": "True",
        "stop": "True"
    },
    {
        "text": "space",
        "lemma": "space",
        "pos": "NOUN",
        "tag": "NN",
        "prettytag": "noun, singular or mass",
        "dep": "pobj",
        "shape": "xxxx",
        "alpha": "True",
        "stop": "False"
    },
    {
        "text": "?",
        "lemma": "?",
        "pos": "PUNCT",
        "tag": ".",
        "prettytag": "punctuation mark, sentence closer",
        "dep": "punct",
        "shape": "?",
        "alpha": "False",
        "stop": "False"
    }
]
```
