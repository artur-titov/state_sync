"""Provides test functionality for StateSyncModel class."""

import unittest
from app.models.state_sync_model import StateSyncModel as StateSync


class TestStateSyncModel(unittest.TestCase):
    """Provides test methods for StateSyncModel class."""

    def setUp(self):
        """Prepares for tests, creates an instance of the StateSyncModel class"""
        self.obj = StateSync()


    def test__define_update_case__with_false_true__expect_install(self):
        """Case when package not present but need to install"""
        result = self.obj._define_update_case(False, True)
        self.assertEqual(result, 'install')

    def test__define_update_case__with_true_false__expect_remove(self):
        """Case when package present and need to remove"""
        result = self.obj._define_update_case(True, False)
        self.assertEqual(result, 'remove')

    def test__define_update_case__with_true_true__expect_no_changes(self):
        """Case when package present and need to install"""
        result = self.obj._define_update_case(True, True)
        self.assertEqual(result, 'no_changes')

    def test__define_update_case__with_false_false__expect_no_changes(self):
        """Case when package not present and not need to install"""
        result = self.obj._define_update_case(False, False)
        self.assertEqual(result, 'no_changes')


    def test__check_result__positive(self):
        """Case when result is succes"""
        package = "hello-world"
        return_code = 0
        self.assertIsNone(self.obj._check_result(package, return_code))

    def test__check_result__negative(self):
        """Case when result is not succes"""
        package = "hello-world"
        return_code = 1
        with self.assertRaises(RuntimeError) as context:
            self.obj._check_result(package, return_code)
        self.assertEqual(
            str(context.exception),
            "'hello-world' installation return code 1 when try to sync stack."
        )
