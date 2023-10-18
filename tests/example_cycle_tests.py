#!/usr/bin/env python3
# JUBE Benchmarking Environment
# Copyright (C) 2008-2022
# Forschungszentrum Juelich GmbH, Juelich Supercomputing Centre
# http://www.fz-juelich.de/jsc/jube
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Test the cycle example"""

from __future__ import (print_function,
                        unicode_literals,
                        division)

import unittest
import os
import shutil
import jube2.main
from examples_tests import * 

class TestCycleExample(TestExample):

    """Class for testing the cycle example"""

    def setUp(self):
        self._path = os.path.join(TestExample.EXAMPLES_PREFIX, "cycle")
        self._xml_file = os.path.join(self._path, "cycle.xml")
        self._yaml_file = os.path.join(self._path, "cycle.yaml")
        self._bench_run_path = os.path.join(self._path, "bench_run")
        self._commands = ["run -e {0}".format(file).split() \
                          for file in [self._xml_file, self._yaml_file]]
        self._wp_paths = None
        self._stdout = "0\n1\n2\n3"

    def test_example(self):
        for command in self._commands:
            #execute jube run
            jube2.main.main(command)
            self._run_path = self._get_run_path(self._bench_run_path)

            #check for done file and no error file in workpackage folder
            self._test_for_status_files_in_wp_folders()

            #check also for done file in workpackage work folder
            self._test_for_status_files_in_work_folders()

            #check stdout content in work directory
            for wp_id, wp_path in self._wp_paths.items():
                work_path = self._get_work_path(wp_path)
                stdout = self._content_of_file(self._get_stdout_file(work_path))
                self.assertEqual(stdout, self._stdout,
                                 "Error: stdout file in work for workpackage with "
                                 "id {0} has not the right content".format(wp_id))

    def tearDown(self):
        #remove bench_run folder after all tests for this example
        shutil.rmtree(self._bench_run_path)


if __name__ == "__main__":
    unittest.main()
