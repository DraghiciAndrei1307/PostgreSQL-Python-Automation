"""
    This module contains the OsRunner class.

    The methods should return something like:

    {
        "success": True,       # boolean True/False
        "stdout": "...",       # standard output message
                                    (what the command printed)
        "stderr": "...",       # standard error message
                                    (what the command printed)
        "exit_code": 0,        # process exit code
                                    (0 means success in Linux)
        "message": "..."       # this should be a short
                                    message created by you
    }

"""

import os
import shlex
import subprocess
from pathlib import Path
import shutil


class OsRunner:

    """
    This command deals with execution of basic terminal commands.
    """

    def __init__(self):
        self.home = Path.home()

    def list_entries_in_path(self, path='.'):
        """
        This method lists all the entries in the given path.
        Omit the path, and it will list the contents of the
        current directory.
        :param path:
        :return:
        """
        if not os.path.exists(path):

            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {path} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:

            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": os.listdir(path)
            }
        except PermissionError:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Permission denied!",
                "exit_code": 2,
                "data": []
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def change_current_directory(self, path='.'):
        """
        This method changes the current working directory.
        :param path:
        :return:
        """

        if not os.path.exists(path):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {path} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:
            os.chdir(path)

            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": []
            }
        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def change_mode(self, path='.', mode='0644'):

        """
        This method changes the access rights of a specific path
        :param path:
        :param mode:
        :return:
        """

        if not os.path.exists(path):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {path} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:
            os.chmod(path, int(mode, 8))
            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": []
            }
        except PermissionError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Permission denied!",
                "exit_code": 2,
                "data": []
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def create_file(self, name='hello.txt', mode='0644', path='.'):
        """
        This method creates a text file with the given name.
        :param name:
        :param mode:
        :param path:
        :return:
        """

        # Check if the path exists
        if not os.path.exists(path):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {path} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:
            file_path = os.path.join(path, name)

            with open(file_path, 'x', encoding='utf-8'):
                pass

            # Change mode of the
            self.change_mode(file_path, mode)

            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": []
            }

        except PermissionError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Permission denied!",
                "exit_code": 2,
                "data": []
            }

        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def create_folder(self, path='.', name="hello_folder", mode='0644'):

        """
        This method creates a folder with the given name.
        :param path:
        :param name:
        :param mode:
        :return:
        """

        # Check if the path exists
        if not os.path.exists(path):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {path} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:
            folder_path = os.path.join(path, name)

            os.mkdir(folder_path)

            # Change mode of the
            self.change_mode(folder_path, mode)

            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": []
            }
        except PermissionError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Permission denied!",
                "exit_code": 2,
                "data": []
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def move(self, source=".", destination="."):
        """
        This method moves the current working directory.
        :return:
        """

        if not os.path.exists(source):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {source} does not exist!",
                "exit_code": 2,
                "data": []
            }

        if not os.path.exists(destination):
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: Path {destination} does not exist!",
                "exit_code": 2,
                "data": []
            }

        try:
            shutil.move(source, destination)
            return {
                "success": True,
                "stdout": "Success",
                "stderr": "",
                "exit_code": 0,
                "data": []
            }
        except PermissionError:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Permission denied!",
                "exit_code": 2,
                "data": []
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }

    def run_cmd(self, input_command, input_data=None, env=None):
        """
        This method runs a command and returns the output.
        :param input_command:
        :return:
        """

        command = shlex.split(input_command)

        process_env = os.environ.copy()

        if env:
            if not isinstance(env, dict):
                raise TypeError("env must be a dict")
            process_env.update(env)

        try:
            cmd = subprocess.run(
                command,
                shell=False,
                check=False,
                input=input_data,
                capture_output=True,
                text=True,
                env=process_env
            )
            return {
                "success": cmd.returncode == 0,
                "stdout": cmd.stdout,
                "stderr": cmd.stderr,
                "exit_code": cmd.returncode,
                "data": []
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Error: {e}",
                "exit_code": 2,
                "data": []
            }
