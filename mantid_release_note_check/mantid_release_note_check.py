import argparse

from pathlib import Path
from typing import Sequence


def filter_files(filenames: set[str]) -> set[str]:
    files_to_keep = set()
    for filename in filenames:
        path = Path(filename)
        if path.suffix == '.rst' and 'release' in path.parts:
            files_to_keep.add(filename)

    return filenames & files_to_keep


def check_bullet_points(filenames: set[str]) -> int:
    retv = 0

    for filename in filenames:
        with open(filename, 'r') as rn:
            lines = rn.readlines()
            for i in range(len(lines)):
                line = lines[i].lstrip()
                if len(lines[i]) - len(line) > 1 or len(line) == 0:
                    # ignore nested bullet points and blank lines
                    continue
                bullet = line[0]
                if bullet in ['*', '+']:
                    print(f"{filename} has incorrect bullet point style '{bullet}'. Please only use '-'.")
                    print(f"Fixing {filename}")
                    lines[i] = lines[i].replace(bullet, '-', 1)
                    retv = 1

        with open(filename, 'w') as rn:
            rn.writelines(lines)

    return retv


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'filenames', nargs='*',
        help='Filenames pre-commit believes are changed.',
    )
    args = parser.parse_args(argv)
    release_notes = filter_files(set(args.filenames))
    return check_bullet_points(release_notes)


if __name__ == '__main__':
    raise SystemExit(main())
