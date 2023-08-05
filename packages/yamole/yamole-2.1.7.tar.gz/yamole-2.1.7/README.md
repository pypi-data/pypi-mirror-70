# yamole

[![Build Status](https://travis-ci.org/YagoGG/yamole.svg?branch=master)](https://travis-ci.org/YagoGG/yamole)
[![PyPI package](https://img.shields.io/pypi/v/yamole.svg)](https://pypi.org/project/yamole)

Dig through the JSON references inside a YAML file, the kind of situation
you may run into when parsing [OpenAPI](https://www.openapis.org/) files.

The result is a single, big YAML file with all the references resolved (i.e.
with their contents replaced in the corresponding places).

yamole also includes small features that help you parse OpenAPI files, like
combining all the elements in an
[`allOf`](https://swagger.io/docs/specification/data-models/oneof-anyof-allof-not/#allof)
key into a single object.

## Installation

yamole is available as a PyPI module, so you can install it using `pip`:

    $ pip install yamole

## Usage

Using yamole is pretty straightforward. The parser is available through the
`YamoleParser` class:

```python
with open('input_file.yaml') as file:
    parser = YamoleParser(file,
        merge_allof=False,  # Combine allOfs into single dicts and disable
                            # inheritance for "example" keys (def: True)
        max_depth=314)  # Allow a maximum of 314 nesting levels (def: 1000)

output_str = parser.dumps()

parser.data['some-key']  # The dict with the parsed file's structure
```

## Testing

To test that yamole works properly, you can run:

    $ pip install -r requirements.txt
    $ python tests/test.py

This will run the parser against a specific test case that makes use of all of
yamole's features, and will compare the result with a fixture
(`tests/expected.yaml`).

---

(c) 2018 Yago González. All rights reserved
