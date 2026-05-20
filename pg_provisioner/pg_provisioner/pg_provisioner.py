"""
 This module was created to run deploy the PostgreSQL VM.
"""

import os
from os_runner import OsRunner
import logging

class PgProvisioner:

    def __init__(self):
        self.os_runner = OsRunner()
        self.become_password = os.environ.get('BECOME_PASSWORD')
        self.vault_password = os.environ.get('VAULT_PASSWORD')

        # configure logging
        self.logging_path = os.environ.get('LOGGING_PATH')
        self.logger = logging.getLogger('pg_provisioner')
        self.logger.setLevel(logging.DEBUG)

        # clear existing handlers (avoid duplicates)
        self.logger.handlers.clear()

        # create console handler
        self.console_handler = logging.StreamHandler()

        # define and set formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s: %(name)s: %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # set formatter
        self.console_handler.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(self.console_handler)

        # configure file handler

        if self.logging_path:
            # create FileHandler
            self.file_handler = logging.FileHandler(self.logging_path)
            # set the same formatter for the FileHandler
            self.file_handler.setFormatter(formatter)
            # add the new FileHandler to the logger
            self.logger.addHandler(self.file_handler)

    def start_pg_vm_provisioning(self, name, vm_id):

        self.os_runner.change_current_directory('/home/student/PostgreSQL-Ansible-Automation/ansible/')

        result = self.os_runner.run_cmd(
            input_command=(
                "ansible-playbook "
                "-i /home/student/PostgreSQL-Ansible-Automation/ansible/inventories/ "
                "/home/student/PostgreSQL-Ansible-Automation/ansible/provision_postgresql_VM.yml "
                "--vault-password-file /home/student/.vault_pass "
                f"-e 'vm_name_user_input={name} vm_id={vm_id}'"),
            input_data=f"{self.vault_password}\n"
        )

        return result