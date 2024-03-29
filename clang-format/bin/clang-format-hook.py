"""
pre-commit clang-format hook
============================

Runs clang-format on the given file and exits with a non-zero code if any changes were made.
"""
# std imports
import argparse
import os
import subprocess
import sys

USAGE = 'clang-format-hook <file> [<file> ...]'

DESCRIPTION = '''
Runs clang-format on the given file and exits with a non-zero code if any changes were made.
'''

if sys.platform.startswith('win32'):
    CLANG_FORMAT_EXE =  os.path.join(os.path.dirname(__file__), 'clang-format.exe')
elif sys.platform.startswith('linux'):
    CLANG_FORMAT_EXE =  os.path.join(os.path.dirname(__file__), 'clang-format-linux64')
elif sys.platform.startswith('darwin'):
    CLANG_FORMAT_EXE =  os.path.join(os.path.dirname(__file__), 'clang-format-darwin')
else:
    raise RuntimeError('Unknown platform "{}"'.format(sys.platform))


def main():
    parser = argparse.ArgumentParser(usage=USAGE, description=DESCRIPTION)
    parser.add_argument('files', nargs='+',
                        help='File to run clang-format on.')
    args = parser.parse_args()

    # return non-zero exit code of there were changes
    return 1 if clang_format_all(args.files) else 0

def clang_format_all(filepaths):
    """
    Clang format the given files and return True if contents in any were changed
    :param filepaths: A list of strings giving paths to file to be formatted
    :return: True if file contents were in changed in any file, False otherwise
    """
    changed = map(clang_format, filepaths)
    return any(changed)


def clang_format(filepath):
    """
    Clang format the given file and return True if contents were changed
    :param filepath: Path to a file to format
    :return: True if file contents were changed, False otherwise
    """
    # read current contents of file and compare with formatted content

    with open(filepath, 'rb') as f:
        contents_orig = f.read()

    contents_formatted = run_clang_format_exe(filepath)
    changed = (contents_formatted != contents_orig)
    if changed:
        print("Fixing {}".format(filepath))
        with open(filepath, 'wb') as fixed_file:
            fixed_file.write(contents_formatted)

    return changed


def run_clang_format_exe(filepath):
    """
    Runs the clang-format executable on the given filepath
    :param filepath:
    """
    p = subprocess.Popen([CLANG_FORMAT_EXE, '-fallback-style=None', filepath],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(stderr)

    return stdout


if __name__ == '__main__':
    sys.exit(main())
