"""
    This module was created to run simple
    PostgreSQL management procedures.
"""

import os
import logging

from os_runner import OsRunner


class PgRunner:
    """
        This class is used for running the
        PostgreSQL management procedures.
    """
    def __init__(self):
        self.os_runner = OsRunner()
        self.become_password = os.environ.get('BECOME_PASSWORD')

        # configure logging
        self.logging_path = os.environ.get('LOGGING_PATH')
        self.logger = logging.getLogger('pg_runner')
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

    def check_postgresql_status(self, version):
        """
        This method checks if the cluster is running or not.
        """

        result = self.os_runner.run_cmd(
            input_command=(
                'sudo -S systemctl status '
                f'postgresql-{version}'
            ),
            input_data=f"{self.become_password}\n"
        )

        if 'Active: active (running)' in result['stdout']:
            self.logger.info("PostgreSQL 14 database server is ACTIVE.")
        else:
            self.logger.info("PostgreSQL 14 database server is INACTIVE.")

    def start_pg(self, version):
        """
        This method starts the cluster.
        """

        result = self.os_runner.run_cmd(
            input_command=f'sudo -S systemctl start postgresql-{version}',
            input_data=f"{self.become_password}\n"
        )

        if result['success']:
            self.logger.info(
                "PostgreSQL 14 database server is UP and RUNNING."
            )
        else:
            self.logger.error(
                "PostgreSQL 14 database encountered "
                "an error: %s",
                {result['stderr']}
            )

    def stop_pg(self, version):
        """
        This method stops the cluster.
        """

        result = self.os_runner.run_cmd(
            input_command=f'sudo -S systemctl stop postgresql-{version}',
            input_data=f"{self.become_password}\n"
        )

        if result['success']:
            self.logger.info(
                "PostgreSQL 14 database server is STOPPED."
            )
        else:
            self.logger.error(
                "PostgreSQL 14 database encountered "
                "an error: %s",
                result['stderr']
            )

    def backup_pg(self):
        """
        This method performs database backup.
        """

        result = self.os_runner.run_cmd(
            input_command=(
                'sudo -S -u postgres pgbackrest '
                '--stanza=demo '
                '--type=full '
                '--log-level-console=info backup'
            ),
            input_data=f"{self.become_password}\n"
        )

        if result['success']:
            self.logger.info("Full backup successful.")
        else:
            self.logger.error(
                "PostgreSQL backup_pg: %s",
                result['stderr']
            )

    def restore_pg(self, version=14, path='/var/lib/pgsql'):
        """
            This method performs database 'default' restore.
        """

        pg_data_path = path + version + '/data'

        # remove everything from pg_data_path

        remove_pg_data_contents_result = self.os_runner.run_cmd(
            input_command=f'sudo -S -u postgres rm -rf {pg_data_path}/*',
        )

        if remove_pg_data_contents_result['success']:

            self.os_runner.run_cmd(
                input_command=(
                    'sudo -S -u postgres pgbackrest '
                    '--stanza=demo restore'
                )
            )

    def backup_info(self):
        """
            This method checks the backup history.
        """

        result = self.os_runner.run_cmd(
            input_command='sudo -S -u postgres pgbackrest info',
            input_data=f"{self.become_password}\n"
        )

        if result['success']:

            raw_list = result['stdout'].splitlines()

            list_to_format = raw_list[7:]

            output = ''

            for _ in list_to_format:
                output += _ + '\n'

            self.logger.info(
                "\nPostgreSQL 14 database BACKUPS:\n"
                "%s",
                output
            )
        else:
            self.logger.error(
                "The backup info cannot be loaded due to: %s",
                result['stderr']
            )

    def check_stanza(self):
        """
            This method checks the pgbackrest stanza.
        """
        result = self.os_runner.run_cmd(
            input_command=(
                'sudo -S -u postgres pgbackrest '
                '--stanza=demo '
                '--log-level-console=info '
                'check'
            ),
            input_data=f"{self.become_password}\n"
        )

        if result['success']:
            self.logger.info(
                "\nPostgreSQL 14 database "
                "STANZA: %s\n",
                result['stdout']
            )
        else:
            self.logger.error(
                "PostgreSQL stanza info cannot "
                "be checked due to: %s",
                result['stderr']
            )
