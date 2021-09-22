import re
import sys
from pathlib import Path
from typing import List

# GitPython
import git


def main():
    root = get_repo_root()
    pytest_files = grep_pytest_files(root)
    cmake_files = grep_cmake_files(root)
    has_missing = compare_file_paths(cmake_files=cmake_files, pytest_files=pytest_files)
    if has_missing:
        sys.exit(1)  # Exit with non-zero for CI


def get_repo_root():
    return git.Repo("", search_parent_directories=True)


def grep_pytest_files(repo: git.Repo) -> List[str]:
    # CMake enforces all pytest files use unittest.main(), so let's use this as our marker
    pytest_file_marker = "unittest.main()"
    git_command = ["git", "grep", "--files-with-matches", pytest_file_marker]
    pytest_file_names: str = repo.git.execute(git_command)
    full_filename_paths = pytest_file_names.split("\n")
    return _get_file_name(full_filename_paths)


def _get_file_name(file_paths: List[str]):
    full_file_paths = [i for i in file_paths if ".py".casefold() in i.casefold()]
    full_file_paths = [i.strip() for i in full_file_paths]
    # Replace any rogue ( or ) chars
    full_file_paths = [i.replace(')', '').replace('(', '') for i in full_file_paths]
    return [Path(file).name for file in full_file_paths]


def _parse_py_filenames_from_cmake(repo_root: Path, file_path: str):
    if "mantidqt" in file_path:
        foo = 2

    cmake_file = repo_root / file_path
    with open(cmake_file.resolve(strict=True), 'r') as handle:
        raw_file_text: str = handle.read()
    # Use *.py as the file indicator - where \S+ is 1-n non whitespace chars
    file_lines = re.findall(r"\S+\.py", raw_file_text, flags=re.IGNORECASE)
    return _get_file_name(file_lines)


def grep_cmake_files(repo: git.Repo) -> List[str]:
    cmake_file_marker = "pyunittest_add_test"
    git_command = ["git", "grep", "--files-with-matches", cmake_file_marker]
    cmake_file_names: str = repo.git.execute(git_command)

    file_names = []
    git_dir = Path(repo.working_tree_dir)
    for cmake_file in cmake_file_names.split("\n"):
        file_names.extend(_parse_py_filenames_from_cmake(git_dir, cmake_file))
    return file_names


def compare_file_paths(cmake_files: List[str], pytest_files: List[str]) -> bool:
    todo_remove = sorted(cmake_files, key=str.casefold)

    cmake_set = set(cmake_files)
    pytest_set = set(pytest_files)
    difference = pytest_set - cmake_set
    if len(difference) > 0:
        warning_str = "The following Pytest files are missing from CMakeLists, and will not be run:\n"
        sorted_list = sorted(list(difference), key=str.casefold)
        for missing_name in sorted_list:
            warning_str += missing_name + '\n'
        print(warning_str, file=sys.stderr)
    return len(difference) > 0


if __name__ == '__main__':
    main()
