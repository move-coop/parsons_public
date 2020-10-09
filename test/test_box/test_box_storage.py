import logging
import os
import random
import string
import unittest
import warnings

from boxsdk.exception import BoxAPIException, BoxOAuthException

from parsons.box import Box
from parsons.etl import Table

"""Prior to running, you should ensure that the relevant environment
variables have been set, e.g. via

# Note: these are fake keys, provided as examples.
export BOX_CLIENT_ID=txqedp4rqi0cz5qckz361fziavdtdwxz
export BOX_CLIENT_SECRET=bk264KHMDLVy89TeuUpSRa4CN5o35u9h
export BOX_ACCESS_TOKEN=boK97B39m3ozIGyTcazbWRbi5F2SSZ5J
"""
TEST_CLIENT_ID = os.getenv('BOX_CLIENT_ID')
TEST_BOX_CLIENT_SECRET = os.getenv('BOX_CLIENT_SECRET')
TEST_ACCESS_TOKEN = os.getenv('BOX_ACCESS_TOKEN')


def generate_random_string(length):
    """Utility to generate random alpha string for file/folder names"""
    return ''.join(random.choice(string.ascii_letters) for i in range(length))


@unittest.skipIf(not os.getenv('LIVE_TEST'), 'Skipping because not running live test')
class TestBoxStorage(unittest.TestCase):

    def setUp(self) -> None:
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

        # Create a client that we'll use to manipulate things behind the scenes
        self.client = Box()
        # Create test folder that we'll use for all our manipulations
        self.temp_folder_name = generate_random_string(24)
        logging.info(f'Creating temp folder {self.temp_folder_name}')
        self.temp_folder_id = self.client.create_folder(self.temp_folder_name)

    def tearDown(self) -> None:
        logging.info(f'Deleting temp folder {self.temp_folder_name}')
        self.client.delete_folder(self.temp_folder_id)

    def test_list_files(self) -> None:
        # Count on environment variables being set
        box = Box()

        subfolder = box.create_folder(folder_name='subfolder',
                                      parent_folder_id=self.temp_folder_id)

        # Create a couple of files in the temp folder
        table = Table([['phone_number', 'last_name', 'first_name'],
                       ['4435705355', 'Warren', 'Elizabeth'],
                       ['5126993336', 'Obama', 'Barack']])

        box.upload_table(table, 'temp1', folder_id=subfolder)
        box.upload_table(table, 'temp2', folder_id=subfolder)
        box.create_folder(folder_name='temp_folder1', parent_folder_id=subfolder)
        box.create_folder(folder_name='temp_folder2', parent_folder_id=subfolder)

        file_list = box.list_files(folder_id=subfolder)
        self.assertEqual(['temp1', 'temp2'], file_list['name'])

        # Check that if we delete a file, it's no longer there
        for box_file in file_list:
            if box_file['name'] == 'temp1':
                box.delete_file(box_file['id'])
                break
        file_list = box.list_files(folder_id=subfolder)
        self.assertEqual(['temp2'], file_list['name'])

        folder_list = box.list_folders(folder_id=subfolder)['name']
        self.assertEqual(['temp_folder1', 'temp_folder2'], folder_list)

    def test_upload_file(self) -> None:
        # Count on environment variables being set
        box = Box()

        table = Table([['phone_number', 'last_name', 'first_name'],
                       ['4435705355', 'Warren', 'Elizabeth'],
                       ['5126993336', 'Obama', 'Barack']])
        box_file = box.upload_table(table, 'phone_numbers', folder_id=self.temp_folder_id)

        new_table = box.get_table_by_file_id(box_file.id)

        # Check that what we saved is equal to what we got back
        self.assertEqual(str(table), str(new_table))

        # Check that things also work in JSON
        box_file = box.upload_table(table, 'phone_numbers_json',
                                    folder_id=self.temp_folder_id,
                                    format='json')

        new_table = box.get_table_by_file_id(box_file.id, format='json')

        # Check that what we saved is equal to what we got back
        self.assertEqual(str(table), str(new_table))

        # Check that we throw an exception with bad formats
        with self.assertRaises(ValueError):
            box.upload_table(table, 'phone_numbers', format='illegal_format')
        with self.assertRaises(ValueError):
            box.get_table_by_file_id(box_file.id, format='illegal_format')

    def test_errors(self) -> None:

        # Count on environment variables being set
        box = Box()

        nonexistent_id = '9999999'
        table = Table([['phone_number', 'last_name', 'first_name'],
                       ['4435705355', 'Warren', 'Elizabeth'],
                       ['5126993336', 'Obama', 'Barack']])

        # Upload a bad format
        with self.assertRaises(ValueError):
            box.upload_table(table, 'temp1', format='bad_format')

        # Download a bad format
        with self.assertRaises(ValueError):
            box.get_table_by_file_id(file_id=nonexistent_id, format='bad_format')

        # Upload to non-existent folder
        with self.assertLogs(level=logging.WARNING):
            with self.assertRaises(BoxAPIException):
                box.upload_table(table, 'temp1', folder_id=nonexistent_id)

        # Download a non-existent file
        with self.assertLogs(level=logging.WARNING):
            with self.assertRaises(BoxAPIException):
                box.get_table_by_file_id(nonexistent_id, format='json')

        # Create folder in non-existent parent
        with self.assertLogs(level=logging.WARNING):
            with self.assertRaises(BoxAPIException):
                box.create_folder(folder_name='subfolder', parent_folder_id=nonexistent_id)

        # Try using bad credentials
        box = Box(access_token='5345345345')
        with self.assertLogs(level=logging.WARNING):
            with self.assertRaises(BoxOAuthException):
                box.list_files()
