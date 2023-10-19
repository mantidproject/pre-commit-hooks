import os
import unittest

from typing import List

from mantid_release_note_check.mantid_release_note_check import check_bullet_points


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

    def test_good_single_release_note(self):
        lines = ["- good note"]
        self._write_release_note(lines)
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 0)
        self._match_file_content(lines)

    def test_bad_single_release_note_star(self):
        self._write_release_note(["* bad note"])
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 1)
        self._match_file_content(["- bad note"])

    def test_bad_single_release_note_plus(self):
        self._write_release_note(["+ bad note"])
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 1)
        self._match_file_content(["- bad note"])

    def test_mixed_bullet_points(self):
        lines = ["* note one",
                 "- note two",
                 "+ note three"]
        self._write_release_note(lines)
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 1)
        fixed_lines = ["- note one",
                       "- note two",
                       "- note three"]
        self._match_file_content(fixed_lines)

    def test_nested_bullet_lists(self):
        lines = ["- note 1",
                 "",
                 "  - note 1a",
                 "  - note 1b",
                 "",
                 "- note 2"]
        self._write_release_note(lines)
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 0)
        self._match_file_content(lines)

    def test_different_nested_bullet_lists(self):
        lines = ["- note 1",
                 "",
                 "  * note 1a",
                 "  * note 1b",
                 "",
                 "- note 2"]
        self._write_release_note(lines)
        self.assertEqual(check_bullet_points({self.RELEASE_NOTE_PATH}), 0)
        self._match_file_content(lines)
