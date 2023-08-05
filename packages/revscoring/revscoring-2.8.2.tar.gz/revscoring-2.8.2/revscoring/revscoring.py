"""
Provides access to a set of utilities for working with revision scorer models.

Utilities:

* score             Scores a set of revisions using a trained model
* extract           Extracts a cache of dependencies for a set of observations
* fetch_text        Fetches text for a set of observations
* test_model        Tests an MLScorerModel with extracted features
* cv_train          Cross-validates, and then trains a Model with extracted features
* model_info        Reads a model-file and reports metadata and testing
                    statistics
* tune              Tunes a set of models against a training set to identify
                    the best model/configuration
* dump_cache        Reads a cache file and dumps out a set of features, target
                    label, and (optionally) score documents in a TSV file.

Usage:
    revscoring (-h | --help)
    revscoring <utility> [-h|--help]
"""  # noqa

import sys
import traceback
from importlib import import_module


USAGE = """Usage:
    revscoring (-h | --help)
    revscoring <utility> [-h|--help]\n"""


def main():
    if len(sys.argv) < 2:
        sys.stderr.write(USAGE)
        sys.exit(1)
    elif sys.argv[1] in ("-h", "--help"):
        sys.stderr.write(__doc__ + "\n")
        sys.exit(1)
    elif sys.argv[1][:1] == "-":
        sys.stderr.write(USAGE)
        sys.exit(1)

    module_name = sys.argv[1]
    try:
        module = import_module(".utilities." + module_name,
                               package="revscoring")
    except ImportError:
        sys.stderr.write(traceback.format_exc())
        sys.stderr.write("Could not find utility {0}.\n".format(module_name))
        sys.exit(1)

    module.main(sys.argv[2:])


if __name__ == "__main__":
    main()
