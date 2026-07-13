"""
 This module was created to run deploy the PostgreSQL VM.
"""

import os
import logging
from os_runner import OsRunner


class PgProvisioner:

    """
        This class contains the logic that triggers
        the provisioning procedure of the PostgreSQL VM.
    """

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

    def start_pg_vm_provisioning(self, name='test', base='bronze', vm_id='1'):
        """
            This method is used to trigger the
            provisioning procedure.
        """

        self.os_runner.change_current_directory(
            '/home/student/PostgreSQL-Ansible-Automation/ansible/'
        )

        base_path = "/home/student/PostgreSQL-Ansible-Automation/ansible"
        inv_path = f"{base_path}/inventories/"
        playbook_path = f"{base_path}/provision_postgresql_VM.yml"
        pass_file = "/home/student/.vault_pass"

        command = (
            f'ANSIBLE_LOG_PATH={base_path}/provisioning_logs/provisioning-{name}.log '
            f'ansible-playbook -i {inv_path} {playbook_path} '
            f'--vault-password-file {pass_file} '
            f'-e vm_name_user_input="{name}" '
            f'-e base_vm_name_user_input="{base}" '
            f'-e vm_id="{vm_id}"'
        )

        print(command)

        result = self.os_runner.run_cmd(
            input_command=command,
            input_data=f"{self.vault_password}\n"
        )

        print(result)

        return result

    def perform_full_backup(self, instance_name='test'):

        base_path = "/home/student/PostgreSQL-Ansible-Automation/ansible"
        inv_path = f"{base_path}/inventories/"
        playbook_path = f"{base_path}/perform_full_backup_individual_target.yml"
        pass_file = "/home/student/.vault_pass"

        return self.os_runner.run_cmd(
            input_command=(
                f'ansible-playbook -i {inv_path} {playbook_path} '
                f'--vault-password-file {pass_file} '
                f'-e db_instance={instance_name} '
            )
        )
