import sys

from tests.config import configure


def run_tests(verbose, *args):
    # must be imported after settings configuration
    try:
        from django_nose import NoseTestSuiteRunner
    except ImportError:
        raise ImportError("To fix this error, run: pip install -r requirements-test.txt")

    if not args:
        args = ['tests']
    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=verbose)
    failures = test_runner.run_tests(args)
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    configure()
    verbosity = 1
    run_tests(verbosity, *sys.argv[1:])