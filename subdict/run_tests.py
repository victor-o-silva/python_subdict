# Run main module's doctests
import doctest
import subdict
doctest.testmod(subdict)

# Run unit tests
import unittest
import tests
unittest.main(tests)
