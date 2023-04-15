import io
import json
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

from purgedb.main import run_app


def _make_sample_config(filepath, content):
    with open(filepath, 'w') as config_file:
        json.dump(content, config_file)


class PurgeDBTestCases(TestCase):

    def setUp(self) -> None:
        self.content = {
            'connection': {
                'host': 'dbase_host',
                'user': 'userid',
                'password': 'password'
            },
            'databases': {
                'tb1_test': {
                    'mytable': "TIMESTAMPDIFF(day, snapshot_time, now())>1"
                },
                'tb2_test': {
                    'foo': 'foo where',
                    'bar': 'bar where'
                }
            }
        }

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_run_app_return_error_if_no_config_file(self, mock_stdout):
        expected_output = 'Error: config file is missed!\n'
        with self.assertRaises(SystemExit) as cm:
            run_app()
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(expected_output, mock_stdout.getvalue())

    def test_run_app(self):
        with TemporaryDirectory() as temp_dir:
            _make_sample_config(f'{temp_dir}/test.json', self.content)
            test_args = ['command', f'{temp_dir}/test.json']
            with mock.patch('sys.argv', test_args):
                with mock.patch('purgedb.main.connector') as mocked_db_connector:
                    a = run_app()
        calls = mocked_db_connector.connect.call_args_list
        for inx, call in enumerate(calls):
            database_name = list(self.content['databases'])[inx]
            self.assertEqual(
                mock.call(
                    host=self.content['connection']['host'],
                    user=self.content['connection']['user'],
                    password=self.content['connection']['password'],
                    database=database_name
                ),
                call
            )
            exec_calls = mocked_db_connector.connect.return_value.cursor().execute.call_args_list
            for table_name, where_clause in self.content['databases'][database_name].items():
                self.assertIn(mock.call(f'DELETE FROM {table_name} WHERE {where_clause}'), exec_calls)

        self.assertEqual(a, True)
