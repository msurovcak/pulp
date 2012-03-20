#!/usr/bin/python
#
# Copyright (c) 2012 Red Hat, Inc.
#
#
# This software is licensed to you under the GNU General Public
# License as published by the Free Software Foundation; either version
# 2 of the License (GPLv2) or (at your option) any later version.
# There is NO WARRANTY for this software, express or implied,
# including the implied warranties of MERCHANTABILITY,
# NON-INFRINGEMENT, or FITNESS FOR A PARTICULAR PURPOSE. You should
# have received a copy of GPLv2 along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.

import glob
import mock
import os
import shutil
import sys
import tempfile
import time
import unittest

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../../src/")
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../../../plugins/importers/yum_importer/")
import importer_mocks
from importer import YumImporter
from importer import YUM_IMPORTER_TYPE_ID
from importer_rpm import RPM_TYPE_ID, RPM_UNIT_KEY
import importer_rpm

from pulp.server.content.plugins.model import Repository, Unit

class TestRPMs(unittest.TestCase):

    def setUp(self):
        super(TestRPMs, self).setUp()
        self.init()

    def tearDown(self):
        super(TestRPMs, self).tearDown()
        self.clean()

    def init(self):
        self.temp_dir = tempfile.mkdtemp()
        self.working_dir = os.path.join(self.temp_dir, "working")
        self.pkg_dir = os.path.join(self.temp_dir, "packages")
        self.data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data")

    def clean(self):
        shutil.rmtree(self.temp_dir)

    def get_files_in_dir(self, pattern, path):
        files = []
        for d,_,_ in os.walk(path):
            files.extend(glob.glob(os.path.join(d,pattern))) 
        return files

    def get_expected_rpms_from_pulp_unittest(self, repo_label, pkg_dir=None, repo_working_dir=None):
        """
        @param repo_label label of repo, typically repo.id
        @type repo_label str

        @param pkg_dir: path of where packages are stored
        @type pkg_dir: str

        @param repo_working_dir: path of where symlinks to RPMs are stored
        @type repo_working_dir: str
        """
        if not pkg_dir:
            pkg_dir = self.pkg_dir
        if not repo_working_dir:
            repo_working_dir = self.working_dir
        rpms = {
                ('pulp-test-package', '0', '0.2.1', 'x86_64', 'pulp-test-package-0.2.1-1.fc11.x86_64.rpm', 'sha256', '4dbde07b4a8eab57e42ed0c9203083f1d61e0b13935d1a569193ed8efc9ecfd7'):{
                    'size': 2216, 
                    'vendor': '', 
                    'checksumtype': 'sha256', 
                    'license': 'MIT', 
                    'checksum': '4dbde07b4a8eab57e42ed0c9203083f1d61e0b13935d1a569193ed8efc9ecfd7', 
                    'description': 'Test package.  Nothing to see here.', 
                    'pkgpath': '%s/.//pulp-test-package/0.2.1/1.fc11/x86_64/4dbde07b4a8eab57e42ed0c9203083f1d61e0b13935d1a569193ed8efc9ecfd7' % (pkg_dir), 
                    'savepath': '%s/%s/' % (repo_working_dir, repo_label), 
                    'filename': 'pulp-test-package-0.2.1-1.fc11.x86_64.rpm', 
                    'downloadurl': 'http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/pulp-test-package-0.2.1-1.fc11.x86_64.rpm', 
                    'item_type': 'rpm', 
                    'epoch': '0', 
                    'version': '0.2.1', 
                    'arch': 'x86_64', 
                    'provides': [
                            ('pulp-test-package(x86-64)', 'EQ', ('0', '0.2.1', '1.fc11')), 
                            ('pulp-test-package', 'EQ', ('0', '0.2.1', '1.fc11')), 
                            ('config(pulp-test-package)', 'EQ', ('0', '0.2.1', '1.fc11'))
                            ], 
                    'relativepath': 'pulp-test-package-0.2.1-1.fc11.x86_64.rpm', 
                    'release': '1.fc11', 
                    'buildhost': 'gibson', 
                    'requires': [], 
                    'name': 'pulp-test-package'
                }, 
                ('pulp-dot-2.0-test', '0', '0.1.2', 'x86_64', 'pulp-dot-2.0-test-0.1.2-1.fc11.x86_64.rpm', 'sha256', '435d92e6c09248b501b8d2ae786f92ccfad69fab8b1bc774e2b66ff6c0d83979'):{
                    'size': 2359, 
                    'vendor': '', 
                    'checksumtype': 'sha256', 
                    'license': 'MIT', 
                    'checksum': '435d92e6c09248b501b8d2ae786f92ccfad69fab8b1bc774e2b66ff6c0d83979', 
                    'description': 'Test package to see how we deal with packages with dots in the name', 
                    'pkgpath': '%s/.//pulp-dot-2.0-test/0.1.2/1.fc11/x86_64/435d92e6c09248b501b8d2ae786f92ccfad69fab8b1bc774e2b66ff6c0d83979' % (pkg_dir), 
                    'savepath': '%s/%s/' % (repo_working_dir, repo_label), 
                    'filename': 'pulp-dot-2.0-test-0.1.2-1.fc11.x86_64.rpm', 
                    'downloadurl': 'http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/pulp-dot-2.0-test-0.1.2-1.fc11.x86_64.rpm', 
                    'item_type': 'rpm', 
                    'epoch': '0', 
                    'version': '0.1.2', 
                    'arch': 'x86_64', 
                    'provides': [
                        ('pulp-dot-2.0-test(x86-64)', 'EQ', ('0', '0.1.2', '1.fc11')), 
                        ('pulp-dot-2.0-test', 'EQ', ('0', '0.1.2', '1.fc11')), 
                        ('config(pulp-dot-2.0-test)', 'EQ', ('0', '0.1.2', '1.fc11'))
                        ], 
                    'relativepath': 'pulp-dot-2.0-test-0.1.2-1.fc11.x86_64.rpm', 
                    'release': '1.fc11', 
                    'buildhost': 'gibson', 
                    'requires': [], 
                    'name': 'pulp-dot-2.0-test'
                }, 
                ('pulp-test-package', '0', '0.3.1', 'x86_64', 'pulp-test-package-0.3.1-1.fc11.x86_64.rpm', 'sha256', '6bce3f26e1fc0fc52ac996f39c0d0e14fc26fb8077081d5b4dbfb6431b08aa9f'): {
                    'size': 2216, 
                    'vendor': '', 
                    'checksumtype': 'sha256', 
                    'license': 'MIT', 
                    'checksum': '6bce3f26e1fc0fc52ac996f39c0d0e14fc26fb8077081d5b4dbfb6431b08aa9f', 
                    'description': 'Test package.  Nothing to see here.', 
                    'pkgpath': '%s/.//pulp-test-package/0.3.1/1.fc11/x86_64/6bce3f26e1fc0fc52ac996f39c0d0e14fc26fb8077081d5b4dbfb6431b08aa9f' % (pkg_dir), 
                    'savepath': '%s/%s/' % (repo_working_dir, repo_label), 
                    'filename': 'pulp-test-package-0.3.1-1.fc11.x86_64.rpm', 
                    'downloadurl': 'http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/pulp-test-package-0.3.1-1.fc11.x86_64.rpm', 
                    'item_type': 'rpm', 
                    'epoch': '0', 
                    'version': '0.3.1', 
                    'arch': 'x86_64', 
                    'provides': [
                        ('pulp-test-package(x86-64)', 'EQ', ('0', '0.3.1', '1.fc11')), 
                        ('pulp-test-package', 'EQ', ('0', '0.3.1', '1.fc11')), 
                        ('config(pulp-test-package)', 'EQ', ('0', '0.3.1', '1.fc11'))
                    ], 
                    'relativepath': 'pulp-test-package-0.3.1-1.fc11.x86_64.rpm', 
                    'release': '1.fc11', 
                    'buildhost': 'gibson', 
                    'requires': [], 
                    'name': 'pulp-test-package'
                    }
                }
        return rpms


    def get_simple_rpm(self, value=None):
        if not value:
            value = "test_value"
        rpm = {}
        for k in RPM_UNIT_KEY:
            rpm[k] = value
        for k in ("vendor", "description", "buildhost", "license", 
                "vendor", "requires", "provides", "pkgpath"):
            rpm[k] = value
        return rpm
    
    def test_metadata(self):
        metadata = YumImporter.metadata()
        self.assertEquals(metadata["id"], YUM_IMPORTER_TYPE_ID)
        self.assertTrue(RPM_TYPE_ID in metadata["types"])

    def test_basic_sync(self):
        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_basic_sync"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(summary is not None)
        self.assertTrue(details is not None)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 3)
        self.assertEquals(summary["num_resynced_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        self.assertEquals(summary["num_orphaned_rpms"], 0)
        self.assertEquals(details["size_total"], 6791)
        # Confirm regular RPM files exist under self.pkg_dir
        pkgs = self.get_files_in_dir("*.rpm", self.pkg_dir)
        self.assertEquals(len(pkgs), 3)
        for p in pkgs:
            self.assertTrue(os.path.isfile(p))
        # Confirm symlinks to RPMs exist under repo.working_dir
        sym_links = self.get_files_in_dir("*.rpm", repo.working_dir)
        self.assertEquals(len(pkgs), 3)
        for link in sym_links:
            self.assertTrue(os.path.islink(link))
    
    def test_basic_local_sync(self):
        feed_url = "file://%s/pulp_unittest/" % (self.data_dir)
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_basic_local_sync"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(summary is not None)
        self.assertTrue(details is not None)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 3)
        self.assertEquals(summary["num_resynced_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        self.assertEquals(summary["num_orphaned_rpms"], 0)
        self.assertEquals(details["size_total"], 6791)
        # Confirm regular RPM files exist under self.pkg_dir
        pkgs = self.get_files_in_dir("*.rpm", self.pkg_dir)
        self.assertEquals(len(pkgs), 3)
        for p in pkgs:
            self.assertTrue(os.path.isfile(p))
        # Confirm symlinks to RPMs exist under repo.working_dir
        sym_links = self.get_files_in_dir("*.rpm", repo.working_dir)
        self.assertEquals(len(pkgs), 3)
        for link in sym_links:
            self.assertTrue(os.path.islink(link))

    def test_validate_config(self):
        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        importer = YumImporter()
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        repo = mock.Mock(spec=Repository)
        state, msg = importer.validate_config(repo, config)
        self.assertTrue(state)

        # Ensure if we are missing a required argument validate fails and the missing 
        # config parameter is mentioned in the message
        config = importer_mocks.get_basic_config()
        state, msg = importer.validate_config(repo, config)
        self.assertFalse(state)
        self.assertTrue("feed_url" in msg)

        # Test that an unknown argument in the config throws an error 
        # and the unknown arg is identified in the message
        config = importer_mocks.get_basic_config(feed_url=feed_url, bad_unknown_arg="blah")
        state, msg = importer.validate_config(repo, config)
        self.assertFalse(state)
        self.assertTrue("bad_unknown_arg" in msg)

    def test_basic_orphaned_sync(self):
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_basic_sync"
        unit_key = {}
        for k in RPM_UNIT_KEY:
            unit_key[k] = "test_value"
        existing_units = [Unit(RPM_TYPE_ID, unit_key, "test_metadata", os.path.join(self.pkg_dir, "test_rel_path"))]
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=existing_units, pkg_dir=self.pkg_dir)
        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(summary is not None)
        self.assertTrue(details is not None)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 3)
        self.assertEquals(summary["num_resynced_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        self.assertEquals(summary["num_orphaned_rpms"], 1)
        # Add a verification that sync_conduit.remove_unit was called for our orphaned unit
        # Test package removed from packages dir
        # Test package removed from working repo dir

    def test_basic_missing_file_sync(self):
        # Sync an existing repo
        # Remove rpm from packages dir
        # Verify a re-sync brings package back to packages dir
        pass


    def test_skip_packages(self):
        # Set skip packages
        # Verify no rpms are downloaded
        pass
    
    def test_progress_sync(self):
        global updated_progress
        updated_progress = None

        def set_progress(progress):
            global updated_progress
            updated_progress = progress
            if "Errata" not in progress["step"]:
                # We want to skip checking the fields for Errata steps
                for key in importer_rpm.PROGRESS_REPORT_FIELDS:
                    self.assertTrue(key in updated_progress)

        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        importer = YumImporter()
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_progress_sync"
        sync_conduit = importer_mocks.get_sync_conduit(pkg_dir=self.pkg_dir)
        sync_conduit.set_progress = mock.Mock()
        sync_conduit.set_progress.side_effect = set_progress
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer._sync_repo(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 3)
        self.assertTrue(updated_progress is not None)
        self.assertTrue(updated_progress.has_key("step"))
        self.assertTrue(updated_progress["step"])

    def test_get_existing_units(self):
        unit_key = {}
        for k in RPM_UNIT_KEY:
            unit_key[k] = "test_value"
        existing_units = [Unit(RPM_TYPE_ID, unit_key, "test_metadata", os.path.join(self.pkg_dir, "test_rel_path"))]
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=existing_units, pkg_dir=self.pkg_dir)
        actual_existing_units = importer_rpm.get_existing_units(sync_conduit)
        self.assertEquals(len(actual_existing_units), 1)
        self.assertEquals(len(existing_units), len(actual_existing_units))
        lookup_key = importer_rpm.form_lookup_key(unit_key)
        self.assertEqual(existing_units[0], actual_existing_units[lookup_key])

    def test_get_available_rpms(self):
        rpm = {}
        for k in RPM_UNIT_KEY:
            rpm[k] = "test_value"
        available_rpms = importer_rpm.get_available_rpms([rpm])
        lookup_key = importer_rpm.form_lookup_key(rpm)
        self.assertEqual(available_rpms[lookup_key], rpm)

    def test_get_orphaned_units(self):
        # Create A & B, Orphan B
        unit_key_a = {}
        for k in RPM_UNIT_KEY:
            unit_key_a[k] = "test_value"
        unit_key_b = {}
        for k in RPM_UNIT_KEY:
            unit_key_b[k] = "test_value_b"
        unit_a = Unit(RPM_TYPE_ID, unit_key_a, "test_metadata", "test_rel_path")
        unit_b = Unit(RPM_TYPE_ID, unit_key_b, "test_metadata", "test_rel_path")
        existing_units = {
                importer_rpm.form_lookup_key(unit_key_a):unit_a, 
                importer_rpm.form_lookup_key(unit_key_b):unit_b
                }
        available_rpms = {}
        available_rpms[importer_rpm.form_lookup_key(unit_key_a)] = unit_key_a
        orphaned_units = importer_rpm.get_orphaned_units(available_rpms, existing_units)
        expected_orphan_key = importer_rpm.form_lookup_key(unit_key_b)
        self.assertEquals(len(orphaned_units), 1)
        self.assertTrue(expected_orphan_key in orphaned_units)

    def test_get_new_rpms_and_units(self):
        # 1 Existing RPM
        # 2 RPMs in available
        # Expected 1 New RPM
        rpm_a = self.get_simple_rpm("test_value_a")
        rpm_b = self.get_simple_rpm("test_value_b")
        rpm_lookup_key_a = importer_rpm.form_lookup_key(rpm_a)
        rpm_lookup_key_b = importer_rpm.form_lookup_key(rpm_b)
        available_rpms = {}
        available_rpms[rpm_lookup_key_a] = rpm_a
        available_rpms[rpm_lookup_key_b] = rpm_b

        unit_a = Unit(RPM_TYPE_ID, importer_rpm.form_rpm_unit_key(rpm_a), "test_metadata", "rel_path")
        existing_units = {}
        existing_units[rpm_lookup_key_a] = unit_a
        sync_conduit = importer_mocks.get_sync_conduit(pkg_dir=self.pkg_dir)
        new_rpms, new_units = importer_rpm.get_new_rpms_and_units(available_rpms, 
                existing_units, sync_conduit)
        self.assertEquals(len(new_rpms), 1)
        self.assertEquals(len(new_units), 1)
        self.assertTrue(rpm_lookup_key_b in new_rpms)
        self.assertTrue(rpm_lookup_key_b in new_units)
        self.assertEquals(new_rpms[rpm_lookup_key_b], rpm_b)
        #
        # Repeat test but now nothing is new
        #
        unit_b = Unit(RPM_TYPE_ID, importer_rpm.form_rpm_unit_key(rpm_b), "test_metadata", "rel_path_b")
        existing_units = {}
        existing_units[rpm_lookup_key_a] = unit_a
        existing_units[rpm_lookup_key_b] = unit_b
        new_rpms, new_units = importer_rpm.get_new_rpms_and_units(available_rpms, 
                existing_units, sync_conduit)
        self.assertEquals(len(new_rpms), 0)
        self.assertEquals(len(new_units), 0)
        #
        # Repeat test but now both rpms in available are new
        #
        existing_units = {}
        new_rpms, new_units = importer_rpm.get_new_rpms_and_units(available_rpms, 
                existing_units, sync_conduit)
        self.assertEquals(len(new_rpms), 2)
        self.assertEquals(len(new_units), 2)
        self.assertTrue(rpm_lookup_key_a in new_rpms)
        self.assertTrue(rpm_lookup_key_b in new_rpms)

    def test_get_missing_rpms_and_units(self):
        # 2 Existing RPMs, one is missing
        # Expecting return of the one missing rpm
        # Fake out the verify_exists
        def side_effect(arg):
            if arg == "rel_path_b":
                return False
            return True
        importer_rpm.verify_exists = mock.Mock()
        importer_rpm.verify_exists.side_effect = side_effect

        rpm_a = self.get_simple_rpm("test_value_a")
        rpm_b = self.get_simple_rpm("test_value_b")
        rpm_lookup_key_a = importer_rpm.form_lookup_key(rpm_a)
        rpm_lookup_key_b = importer_rpm.form_lookup_key(rpm_b)
        available_rpms = {}
        available_rpms[rpm_lookup_key_a] = rpm_a
        available_rpms[rpm_lookup_key_b] = rpm_b

        unit_a = Unit(RPM_TYPE_ID, importer_rpm.form_rpm_unit_key(rpm_a), "test_metadata", "rel_path_a")
        unit_b = Unit(RPM_TYPE_ID, importer_rpm.form_rpm_unit_key(rpm_b), "test_metadata", "rel_path_b")
        existing_units = {}
        existing_units[rpm_lookup_key_a] = unit_a
        existing_units[rpm_lookup_key_b] = unit_b

        missing_rpms, missing_units = importer_rpm.get_missing_rpms_and_units(available_rpms, 
                existing_units)
        self.assertEquals(len(missing_rpms), 1)
        self.assertEquals(len(missing_units), 1)
        self.assertTrue(rpm_lookup_key_b in missing_rpms)
        self.assertTrue(rpm_lookup_key_b in missing_units)
        self.assertEquals(missing_rpms[rpm_lookup_key_b], rpm_b)

    def test_remove_packages(self):
        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_remove_packages"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 3)
        self.assertEquals(len(self.get_files_in_dir("*.rpm", self.pkg_dir)), 3)
        self.assertEquals(len(self.get_files_in_dir("*.rpm", repo.working_dir)), 3)
        expected_rpms = self.get_expected_rpms_from_pulp_unittest(repo.id)
        # Confirm that both the RPM and the Symlink for each expected rpm does exist
        #  Then run remove_unit
        # Confirm that both the RPM and the Symlink have been deleted from the file system
        for rpm in expected_rpms.values():
            rpm_save_path = os.path.join(rpm["pkgpath"], rpm["filename"])
            self.assertTrue(os.path.exists(rpm_save_path))

            symlink_save_path = os.path.join(rpm["savepath"], rpm["filename"])
            self.assertTrue(os.path.lexists(symlink_save_path))

            unit = Unit(RPM_TYPE_ID, 
                    importer_rpm.form_rpm_unit_key(rpm), 
                    importer_rpm.form_rpm_metadata(rpm),
                    rpm_save_path)
            importer_rpm.remove_unit(sync_conduit, repo, unit)
            self.assertFalse(os.path.exists(rpm_save_path))
            self.assertFalse(os.path.exists(symlink_save_path))
        self.assertEquals(len(self.get_files_in_dir("*.rpm", self.pkg_dir)), 0)
        self.assertEquals(len(self.get_files_in_dir("*.rpm", repo.working_dir)), 0)

    def test_remove_old_packages(self):
        feed_url = "http://jmatthews.fedorapeople.org/repo_multiple_versions/"
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_remove_old_packages"
        sync_conduit = importer_mocks.get_sync_conduit(pkg_dir=self.pkg_dir)
        ###
        # Test that old packages are not in rpmList and are never intended to be downloaded
        # Additionallity verify that already existing packages which are NOT orphaned are also
        # removed with remove_old functionality
        ###
        config = importer_mocks.get_basic_config(feed_url=feed_url, remove_old=False, num_old_packages=0)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], 12)
        pkgs = self.get_files_in_dir("*.rpm", self.pkg_dir)
        self.assertEquals(len(pkgs), 12)

        yumRepoGrinder = importer_rpm.get_yumRepoGrinder(repo.id, repo.working_dir, config)
        yumRepoGrinder.setup(basepath=repo.working_dir)
        rpm_items = yumRepoGrinder.getRPMItems()
        yumRepoGrinder.stop()
        del yumRepoGrinder
        self.assertEquals(len(rpm_items), 12)

        existing_units = []
        for rpm in rpm_items:
            u = Unit(RPM_TYPE_ID, 
                    importer_rpm.form_rpm_unit_key(rpm), 
                    importer_rpm.form_rpm_metadata(rpm),
                    os.path.join(self.pkg_dir, rpm["pkgpath"], rpm["filename"]))
            existing_units.append(u)
        config = importer_mocks.get_basic_config(feed_url=feed_url, remove_old=True, num_old_packages=6)
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=existing_units, pkg_dir=self.pkg_dir)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertEquals(summary["num_rpms"], 7)
        self.assertEquals(summary["num_orphaned_rpms"], 5)
        self.assertEquals(summary["num_synced_new_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        pkgs = self.get_files_in_dir("*.rpm", self.pkg_dir)
        self.assertEquals(len(pkgs), 7)

        config = importer_mocks.get_basic_config(feed_url=feed_url, remove_old=True, num_old_packages=0)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertEquals(summary["num_rpms"], 1)
        self.assertEquals(summary["num_orphaned_rpms"], 11)
        self.assertEquals(summary["num_synced_new_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        pkgs = self.get_files_in_dir("*.rpm", self.pkg_dir)
        self.assertEquals(len(pkgs), 1)

    def test_srpm_sync(self):
        feed_url = "http://pkilambi.fedorapeople.org/test_srpm_repo/"
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_srpm_sync"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url)
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        self.assertTrue(status)
        self.assertTrue(summary is not None)
        self.assertTrue(details is not None)
        self.assertEquals(summary["num_rpms"], 3)
        self.assertEquals(summary["num_synced_new_srpms"], 3)
        self.assertEquals(summary["num_synced_new_rpms"], 0)


    def test_grinder_config(self):
        repo_label = "test_grinder_config"
        feed_url = "http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/pulp_unittest/"
        num_threads = 25
        max_speed = 1
        proxy_url = "http://example.com"
        proxy_port = "3128"
        proxy_user = "username"
        proxy_pass = "password"
        ssl_verify = True
        ssl_ca_cert = "path_ca_cert"
        ssl_client_cert = "path_client_cert"
        ssl_client_key = "path_client_key"
        newest = True
        remove_old = True
        num_old_packages = 99
        tmp_path = "/tmp"

        config = importer_mocks.get_basic_config(feed_url=feed_url, num_threads=num_threads, max_speed=max_speed,
                proxy_url=proxy_url, proxy_port=proxy_port, proxy_user=proxy_user, proxy_pass=proxy_pass,
                ssl_verify=ssl_verify, 
                ssl_ca_cert=ssl_ca_cert, ssl_client_cert=ssl_client_cert, ssl_client_key=ssl_client_key,
                newest=newest, remove_old=remove_old, num_old_packages=num_old_packages)

        yumRepoGrinder = importer_rpm.get_yumRepoGrinder(repo_label, tmp_path, config)
        self.assertEquals(yumRepoGrinder.repo_label, repo_label)
        self.assertEquals(yumRepoGrinder.repo_url, feed_url)
        self.assertEquals(yumRepoGrinder.numThreads, num_threads)
        self.assertEquals(yumRepoGrinder.max_speed, max_speed)
        self.assertEquals(yumRepoGrinder.proxy_url, proxy_url)
        self.assertEquals(yumRepoGrinder.proxy_port, proxy_port)
        self.assertEquals(yumRepoGrinder.proxy_user, proxy_user)
        self.assertEquals(yumRepoGrinder.proxy_pass, proxy_pass)
        self.assertEquals(yumRepoGrinder.sslverify, ssl_verify)
        self.assertEquals(yumRepoGrinder.sslcacert, ssl_ca_cert)
        self.assertEquals(yumRepoGrinder.sslclientcert, ssl_client_cert)
        self.assertEquals(yumRepoGrinder.sslclientkey, ssl_client_key)
        self.assertEquals(yumRepoGrinder.newest, newest)
        self.assertEquals(yumRepoGrinder.remove_old, remove_old)
        self.assertEquals(yumRepoGrinder.numOldPackages, num_old_packages)
        self.assertEquals(yumRepoGrinder.tmp_path, tmp_path)
        # Verify that the pkgpath is set to "./", hardcoded in importer_rpm to 
        # force the package dir to be a relative path with the checksum components in the path
        self.assertEquals(yumRepoGrinder.pkgpath, "./")

    def test_bandwidth_limit(self):
        # This test assumes an available bandwidth of more than 100KB for 2 threads
        feed_url = 'http://repos.fedorapeople.org/repos/pulp/pulp/demo_repos/test_bandwidth_repo_smaller/'
        expected_size_bytes = 209888 # 5 1MB RPMs are in this repo
        expected_num_packages = 2
        num_threads = 2
        max_speed = 100 # KB/sec

        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_bandwidth_limit"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url, num_threads=num_threads, max_speed=max_speed)

        start = time.time()
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        end = time.time()
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], expected_num_packages)
        self.assertEquals(summary["num_resynced_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        self.assertEquals(summary["num_orphaned_rpms"], 0)
        self.assertEquals(details["size_total"], expected_size_bytes)

        expected = (float(expected_size_bytes)/(num_threads*max_speed*1000))
        actual_A = end - start
        self.assertTrue(actual_A > expected)
        #
        # Clean up and resync with no bandwidth limit
        # Ensure result is quicker than above
        #
        max_speed = 0
        self.clean()
        self.init()
        repo = mock.Mock(spec=Repository)
        repo.working_dir = self.working_dir
        repo.id = "test_bandwidth_limit"
        sync_conduit = importer_mocks.get_sync_conduit(existing_units=[], pkg_dir=self.pkg_dir)
        config = importer_mocks.get_basic_config(feed_url=feed_url, num_threads=num_threads, max_speed=max_speed)
        start = time.time()
        status, summary, details = importer_rpm._sync(repo, sync_conduit, config)
        end = time.time()
        self.assertTrue(status)
        self.assertEquals(summary["num_synced_new_rpms"], expected_num_packages)
        self.assertEquals(summary["num_resynced_rpms"], 0)
        self.assertEquals(summary["num_not_synced_rpms"], 0)
        self.assertEquals(summary["num_orphaned_rpms"], 0)
        self.assertEquals(details["size_total"], expected_size_bytes)
        self.assertTrue(end-start < actual_A)