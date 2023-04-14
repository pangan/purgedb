import io
import json
from unittest import TestCase, mock
from tempfile import TemporaryDirectory

from purgedb.main import run_app


def _make_sample_config(filepath):
    with open(filepath, 'w') as config_file:
        json.dump({}, config_file)


class PurgeDBTestCases(TestCase):

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_run_app_return_error_if_no_config_file(self, mock_stdout):
        expected_output = 'Error: config file is missed!\n'
        with self.assertRaises(SystemExit) as cm:
            run_app()
        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(expected_output, mock_stdout.getvalue())

    def test_run_app(self):
        with TemporaryDirectory() as temp_dir:
            _make_sample_config(f'{temp_dir}/test.json')
            test_args = ['command', f'{temp_dir}/test.json']
            with mock.patch('sys.argv', test_args):
                a = run_app()
        self.assertEqual(a, True)
