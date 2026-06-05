
"""
    This module contains the TestOsRunner class
"""

import os

from os_runner.os_runner import OsRunner


class TestOsRunner:

    """
    This class contains tests that check the
    functionality of the OsRunner class
    """

    runner: OsRunner = None

    def setup_method(self):
        """
        Setup method to run before each test
        :return:
        """

        self.runner = OsRunner()

    def test_path_not_exist(self, path="fake_path"):
        """
        Test path not exist
        :return:
        """

        result = self.runner.list_entries_in_path(path)
        assert not result["success"]

    def test_path_exist(self, path="."):
        """
        Test path exist
        :return:
        """
        result = self.runner.run_cmd(["ls", "-la", path])

        assert result["exit_code"] == 0

    def test_list_entry_current_dir(self, entry="setup.py"):
        """
        Test list entries current directory
        :return:
        """

        result = self.runner.list_entries_in_path()

        assert result["success"]

        data = result["data"]

        # check to see if the result is a list
        assert isinstance(data, list)

        # check if the list is no empty
        assert len(data) > 0

        # check for a specific element
        assert entry in data

    # def test_create_file(self, name="hello_world.txt"):
    #     """
    #         Test creating a file.
    #     """
    #     result = self.runner.create_text_file(name=name)
    #
    #     assert result["success"]
    #     assert result["exit_code"] == 0

    # def test_create_file_rights_missing(
    #         self,
    #         name="hello_world.txt",
    #         path="/"
    # ):
    #     result = self.runner.create_text_file(name=name, path=path)
    #
    #     assert result["exit_code"] == 2
    #     # we should not do this
    #     self.test_path_not_exist(path=os.path.join(path, name))

    def test_create_folder(self, path=".", name="hello_world"):
        """
            Test create folder.
        """

        result = self.runner.create_folder(path=path, name=name)

        assert result["success"]
        # we should not do this
        self.test_path_exist(path=os.path.join(path, name))

    def test_create_folder_rights_missing(self, name="hello_world", path="/"):
        """
            Test for creating a folder with missing rights.
        """

        result = self.runner.create_folder(name=name, path=path)

        assert result["exit_code"] == 2
        self.test_path_not_exist(path=os.path.join(path, name))

    # def test_change_mode(self, path=".", mode="0641", name="andrei.txt"):
    #
    #     self.runner.create_text_file(
    #         name=name,
    #         mode=mode,
    #         path=path
    #     )
    #
    #     new_path = os.path.join(path, name)
    #     # we should not do this
    #     self.test_path_exist(path=new_path)
    #
    #     result = self.runner.change_mode(
    #         path=new_path,
    #         mode="0644"
    #     )
    #
    #     assert result["success"]
    #     assert result["exit_code"] == 0
