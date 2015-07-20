# Run main module's doctests
import doctest
import extract_subdict
doctest.testmod(extract_subdict)

# Run unit tests
import unittest
import tests
unittest.main(tests)
