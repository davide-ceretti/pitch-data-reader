pitch-data-reader
=================

A reader for BATS Multicast PITCH protocol, written in Python.
Given some PITCH data the program returns a table of the top ten symbols by executed volume.

The reader can only parse a subset of the PITCH messages:
Add order
Cancel order
Execute order
Trade message

Usage
-----

python main.py < test_data


Tests
-----

python tests.py
