pitch-data-reader
=================

A reader for BATS Multicast PITCH protocol, written in Python.
Given some PITCH data the program returns a table of the top ten symbols by executed volume.
PITCH documentation can be found at http://www.batstrading.com/resources/membership/BATS_PITCH_Specification.pdf

The executed volume is the amount of shares executed by each symbol.

The reader can only parse a subset of the PITCH messages:
Add order
Execute order

Quickstart

```python main.py test_data```

Usage
-----

* ```python main.py --help```
* ```python main.py <path_to_pitch_data_file>```


Tests
-----

```python tests.py```


TODO
----

* Validation on messages
* Implement Cancel order
* Implement Trade message
* Refactor pitch_parser
