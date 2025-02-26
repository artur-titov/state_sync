"""Provides test functionality for StateSyncModel class.

Generated by AI (Claude 3.7 Sonnet).
Edited by human.
"""

import unittest
from unittest.mock import patch, MagicMock
from services import CommandRunner as Runner


class TestCommandRunner(unittest.TestCase):

    def setUp(self):
        self.command_runner = Runner()
        self.mock_process = MagicMock()


    @patch('subprocess.run')
    def test__execute__one_command__success(self, mock_run):
        self.mock_process.returncode = 0
        mock_run.return_value = self.mock_process

        # Test with a single command
        result = self.command_runner._execute(
            item="Test",
            commands=["test_command"]
        )

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            args="test_command",
            shell=True,
            check=False
        )

        # Verify the method returns True on successful execution
        self.assertTrue(result)

    @patch('subprocess.run')
    def test__execute__multiple_commands__success(self, mock_run):
        self.mock_process.returncode = 0
        mock_run.return_value = self.mock_process

        # Test with multiple commands
        commands_list = [
            "test",
            "command"
        ]

        result = self.command_runner._execute(
            item="Test",
            commands=commands_list
        )

        # Verify subprocess.run was called correct number of times with right arguments
        self.assertEqual(mock_run.call_count, second=2)
        mock_run.assert_any_call(args="test", shell=True, check=False)
        mock_run.assert_any_call(args="command", shell=True, check=False)

        # Verify the method returns True on successful execution
        self.assertTrue(result)

    @patch('subprocess.run')
    def test__execute__one_command__failure(self, mock_run):
        self.mock_process.returncode = 1
        self.mock_process.stderr = "execution error"
        mock_run.return_value = self.mock_process

        # Test with a failing command
        with self.assertRaises(RuntimeError) as context_manager:
            self.command_runner._execute(
                item="Test",
                commands=["invalid command"]
            )

        # Verify subprocess.run was called with correct arguments
        mock_run.assert_called_once_with(
            args="invalid command",
            shell=True,
            check=False
        )

        # Verify the error message contains the item name and error details
        expected_error = "Test --> Error code: '1' (execution error)"
        self.assertEqual(str(context_manager.exception), expected_error)

    @patch('subprocess.run')
    def test__execute__partial_execution__failure(self, mock_run):
        success_process = MagicMock()
        success_process.returncode = 0

        failure_process = MagicMock()
        failure_process.returncode = 1
        failure_process.stderr = "Test command failed"

        # Make mock_run return different values on consecutive calls
        mock_run.side_effect = [success_process, failure_process]

        # Test with multiple commands where the second one fails
        commands = ["normal command", "invalid command"]

        with self.assertRaises(RuntimeError) as context:
            self.command_runner._execute(
                item="Test",
                commands=commands
            )

        # Verify mock_run was called twice with the correct arguments
        self.assertEqual(mock_run.call_count, second=2)
        mock_run.assert_any_call(args="normal command", shell=True, check=False)
        mock_run.assert_any_call(args="invalid command", shell=True, check=False)

        # Verify the error message
        expected_error = "Test --> Error code: '1' (Test command failed)"
        self.assertEqual(str(context.exception), expected_error)


    @patch('subprocess.run')
    def test__app_item_installation_check__apt__installed(self, mock_run):
        self.mock_process.returncode = 0
        mock_run.return_value = self.mock_process

        context = {
            "distributor": "apt",
            "package": "test_package"
        }

        result = self.command_runner.app_item_installation_check(context)

        # Verify 'subprocess.run' was called with correct arguments.
        mock_run.assert_called_with(
            args=[f"dpkg -l | grep {context.get("package")} > /dev/null 2>&1"],
            shell=True,
            check=False
        )

        # Verify the method returns True when package is installed
        self.assertTrue(result)

    @patch('subprocess.run')
    def test__app_item_installation_check__snap__installed(self, mock_run):
        self.mock_process.returncode = 0
        mock_run.return_value = self.mock_process

        context = {
            "distributor": "snap",
            "package": "test_package"
        }

        result = self.command_runner.app_item_installation_check(context)

        # Verify 'subprocess.run' was called with correct arguments.
        mock_run.assert_called_with(
            args=[f"snap list {context.get("package")} > /dev/null 2>&1"],
            shell=True,
            check=False
        )

        # Verify the method returns True when package is installed
        self.assertTrue(result)

    @patch('subprocess.run')
    def test__app_item_installation_check__flatpak__installed(self, mock_run):
        self.mock_process.returncode = 0
        mock_run.return_value = self.mock_process

        context = {
            "distributor": "flatpak",
            "package": "org.test.package"
        }

        result = self.command_runner.app_item_installation_check(context)

        # Verify 'subprocess.run' was called with correct arguments.
        mock_run.assert_called_with(
            args=[f"flatpak list | grep {context.get("package")} > /dev/null 2>&1"],
            shell=True,
            check=False
        )

        # Verify the method returns True when package is installed
        self.assertTrue(result)

    @patch('subprocess.run')
    def test__app_item_installation_check__apt__not_installed(self, mock_run):
        self.mock_process.returncode = 1
        mock_run.return_value = self.mock_process

        context = {
            "distributor": "apt",
            "package": "test_package"
        }

        result = self.command_runner.app_item_installation_check(context)

        # Verify 'subprocess.run' was called with correct arguments.
        mock_run.assert_called_with(
            args=[f"dpkg -l | grep {context.get("package")} > /dev/null 2>&1"],
            shell=True,
            check=False
        )

        # Verify the method returns True when package is installed
        self.assertFalse(result)

    def test__app_item_installation_check__unknown_distributor(self):
        # Test with unknown distributor
        context = {
            "distributor": "unknown",  # An unsupported distributor
            "package": "test_package"
        }

        # Verify RuntimeError is raised with the correct error message
        with self.assertRaises(RuntimeError) as context_manager:
            self.command_runner.app_item_install(context)

        # Verify the error message contains the expected text
        expected_error = f"{context.get("package")} --> Distributor '{context.get("distributor")}' not supported yet."
        self.assertIn(expected_error, str(context_manager.exception))


    @patch.object(Runner, attribute='_execute')
    def test__app_item_install__apt__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        # Test apt package installation
        context = {
            "distributor": "apt",
            "package": "test_package"
        }

        self.command_runner.app_item_install(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo apt install {context.get("package")} -y"
            ]
        )

    @patch.object(Runner, attribute='_execute')
    def test__app_item_install__flatpak__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        # Test flatpak package installation
        context = {
            "distributor": "flatpak",
            "package": "org.test.package"
        }

        self.command_runner.app_item_install(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo flatpak install flathub {context.get("package")} -y"
            ]
        )

    @patch.object(Runner, attribute='_execute')
    def test__app_item_install__snap_regular__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        # Test snap package installation (regular)
        context = {
            "distributor": "snap",
            "package": "test_package"
        }

        self.command_runner.app_item_install(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo snap install {context.get("package")}"
            ]
        )

    @patch.object(Runner, attribute='_execute')
    def test__app_item_install__snap_classic__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        # Test snap package installation with classic flag
        context = {
            "distributor": "snap",
            "package": "test_package",
            "classic": True
        }

        self.command_runner.app_item_install(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo snap install {context.get("package")} --classic"
            ]
        )

    def test__app_item_install__unknown_distributor__failure(self):
        # Test with unknown distributor
        context = {
            "distributor": "unknown",  # An unsupported distributor
            "package": "test_package"
        }

        # Verify RuntimeError is raised with the correct error message
        with self.assertRaises(RuntimeError) as context_manager:
            self.command_runner.app_item_install(context)

        # Verify the error message contains the expected text
        expected_error = "test_package --> Distributor 'unknown' not supported yet."
        self.assertIn(expected_error, str(context_manager.exception))


    @patch.object(Runner, attribute='_execute')
    def test__app_item_remove__apt__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        context = {
            "distributor": "apt",
            "package": "test-package"
        }

        self.command_runner.app_item_remove(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo apt purge {context.get("package")} -y",
                "sudo apt autoremove -y"
            ]
        )

    @patch.object(Runner, attribute='_execute')
    def test__app_item_remove__flatpak__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        context = {
            "distributor": "flatpak",
            "package": "org.test.package"
        }

        self.command_runner.app_item_remove(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo flatpak kill {context.get("package")}",
                f"sudo flatpak uninstall -v -y --force-remove --delete-data flathub {context.get("package")}",
                "sudo flatpak uninstall -y --unused"
            ]
        )

    @patch.object(Runner, attribute='_execute')
    def test__app_item_remove__snap__success(self, mock_execute):
        # Set up mock to return True
        mock_execute.return_value = True

        context = {
            "distributor": "snap",
            "package": "test_package"
        }

        self.command_runner.app_item_remove(context)

        # Verify _execute was called with correct arguments
        mock_execute.assert_called_once_with(
            item=context.get("package"),
            commands=[
                f"sudo snap remove --purge {context.get("package")}"
            ]
        )

    def test__app_item_remove__unknown_distributor__failure(self):
        # Test with unknown distributor
        context = {
            "distributor": "unknown",  # An unsupported distributor
            "package": "test_package"
        }

        # Verify RuntimeError is raised with the correct error message
        with self.assertRaises(RuntimeError) as context_manager:
            self.command_runner.app_item_install(context)

        # Verify the error message contains the expected text
        expected_error = "test_package --> Distributor 'unknown' not supported yet."
        self.assertIn(expected_error, str(context_manager.exception))
