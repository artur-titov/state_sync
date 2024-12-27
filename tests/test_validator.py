"""Provides test functionality for Validator class."""

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.helpers.validator import Validator as Validate


class TestValidator(unittest.TestCase):
    """Provides test methods for Validator class."""

    def setUp(self):
        """Prepares for tests, creates an instance of the Validator class"""
        self.validate = Validate()


    def test__is_file_supported__with_yml_extension__positive(self):
        """Case when the path points to a file with yml extensions"""
        path = "/example/directory/config.yml"
        self.assertTrue(self.validate.is_file_supported(path))

    def test__is_file_supported__with_yaml_extension__positive(self):
        """Case when the path points to a file with yaml extension"""
        path = "/example/directory/config.yaml"
        self.assertTrue(self.validate.is_file_supported(path))

    def test__is_file_supported__with_yaml_uppercase_extension__positive(self):
        """Case when the path points to a file with uppercase extensions"""
        path = "/example/directory/config.YAML"
        self.assertTrue(self.validate.is_file_supported(path))

    def test__is_file_supported__with_invalid_extension__negative(self):
        """Case when the path points to a file with invalid extension"""
        path = "/example/directory/config.txt"
        self.assertFalse(self.validate.is_file_supported(path))

    def test__is_file_supported__without_extension__negative(self):
        """Case when the path points to a file without extension"""
        path = "/example/directory/config"
        self.assertFalse(self.validate.is_file_supported(path))


    @patch("pathlib.Path.is_file", return_value=True)
    def test__is_file_exists__positive(self, mock_is_file):
        """Case when the file exists"""
        path = Path()
        self.assertTrue(self.validate.is_file_exists(path))

    @patch("pathlib.Path.is_file", return_value=False)
    def test__is_file_exists__negative(self, mock_is_file):
        """Case when the file not exists"""
        path = Path()
        self.assertFalse(self.validate.is_file_exists(path))


    @patch('subprocess.run')
    def test__is_package_present__positive(self, mock_run):
        """Case when package is present in OS"""
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_run.return_value = mock_process
        self.assertTrue(self.validate.is_package_present('test-package', 'apt'))

    @patch('subprocess.run')
    def test__is_package_present__negative(self, mock_run):
        """Case when package is not present in OS"""
        mock_process = MagicMock()
        mock_process.returncode = 1
        mock_run.return_value = mock_process
        self.assertFalse(self.validate.is_package_present('test-package', 'apt'))
