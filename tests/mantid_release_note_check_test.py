import os
import unittest

from typing import List

from mantid_hooks.mantid_release_note_check import check_bullet_points


class MantidReleaseNoteCheckTest(unittest.TestCase):

    RELEASE_NOTE_PATH = "release_note.rst"

    def setUp(self) -> None:
        open(self.RELEASE_NOTE_PATH, 'a').close()

    def tearDown(self) -> None:
        os.remove(self.RELEASE_NOTE_PATH)

    def _write_release_note(self, lines: List[str]) -> None:
        with open(self.RELEASE_NOTE_PATH, 'w') as rn:
            rn.writelines(l + '\n' for l in lines)

    def _match_file_content(self, lines: List[str]):
        with open(self.RELEASE_NOTE_PATH, 'r') as rn:
            self.assertEqual([l + '\n' for l in lines], rn.readlines())

    def _run_check(self, input_lines: List[str], expected_output_lines: List[str], expoected_retv: int):
        self._write_release_note(input_lines)
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), expoected_retv)
        self._match_file_content(expected_output_lines)

    def test_good_single_release_note(self):
        lines = ["- good note"]
        self._run_check(lines, lines, 0)

    def test_bad_single_release_note_star(self):
        self._run_check(["* bad note"], ["- bad note"], 1)

    def test_bad_single_release_note_plus(self):
        self._run_check(["+ bad note"], ["- bad note"], 1)

    def test_mixed_bullet_points(self):
        lines = ["* note one",
                 "- note two",
                 "+ note three"]
        fixed_lines = ["- note one",
                       "- note two",
                       "- note three"]
        self._run_check(lines, fixed_lines, 1)

    def test_nested_bullet_lists(self):
        lines = ["- note 1",
                 "",
                 "  - note 1a",
                 "  - note 1b",
                 "",
                 "- note 2"]
        self._run_check(lines, lines, 0)

    def test_different_nested_bullet_lists(self):
        lines = ["- note 1",
                 "",
                 "  * note 1a",
                 "  * note 1b",
                 "",
                 "- note 2"]
        self._run_check(lines, lines, 0)

    def test_adding_bullet_point_to_the_first_line(self):
        self._run_check(["this is my release note"], ["- this is my release note"], 1)

    def test_adding_bullet_point_to_the_first_line_only(self):
        lines = ["this is my release note",
                 "another line",
                 "and another"]
        fixed_lines = ["- this is my release note",
                       "another line",
                       "and another"]
        self._run_check(lines, fixed_lines, 1)
