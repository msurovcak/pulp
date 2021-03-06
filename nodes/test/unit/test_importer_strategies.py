# Copyright (c) 2013 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.


from unittest import TestCase
from mock import Mock

from pulp.plugins.model import Unit
from pulp_node.importers.strategies import ImporterStrategy
from pulp_node.importers.reports import SummaryReport, ProgressListener
from pulp_node.reports import RepositoryProgress


class TestBase(TestCase):

    def test_abstract(self):
        # Setup
        repo_id = 'foo'
        conduit = 1
        config = 2
        downloader = 3
        progress = RepositoryProgress(repo_id, ProgressListener(conduit))
        summary = SummaryReport()
        # Test
        strategy = ImporterStrategy(conduit, config, downloader, progress, summary)
        # Verify
        self.assertEqual(conduit, strategy.conduit)
        self.assertEqual(config, strategy.config)
        self.assertEqual(downloader, strategy.downloader)
        self.assertEqual(progress, strategy.progress_report)
        self.assertEqual(strategy.progress_report.listener.conduit, conduit)
        self.assertRaises(NotImplementedError, strategy._synchronize, None)


class TestConduit:

    def get_units(self):
        return [
            Unit('T', {1:1}, {2:2}, 'path_1'),
            Unit('T', {1:2}, {2:2}, 'path_2'),
            Unit('T', {1:3}, {2:2}, 'path_3'),
        ]

    add_unit = Mock()


class TestMirror(TestCase):

    def setUp(self):
        TestConduit.add_unit.reset_mock()

    def test_successful(self):
        # WORK IN PROGRESS
        pass
