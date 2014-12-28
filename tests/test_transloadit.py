import unittest
import responses
import StringIO
import pytest

from transloadit.TransloaditClient import TransloaditClient


class UploadTest(unittest.TestCase):

    def setUp(self):
        self.file = StringIO.StringIO()
        self.steps = {
            "resize_to_250": {
                "robot": "/image/resize",
                "width": 250,
                "height": 250
            },
        }
        self.client = TransloaditClient('test', 'test')

    @responses.activate
    def test_upload_file_success(self):
        responses.add(
            responses.POST, 'https://api2.transloadit.com/assemblies',
            body='{"ok": "ASSEMBLY_COMPLETED"}',
            status=200,
            content_type='application/json',
        )
        self.assertTrue(self.client.upload(self.file, self.steps))

    @responses.activate
    def test_upload_file_failure(self):
        responses.add(
            responses.POST, 'https://api2.transloadit.com/assemblies',
            body='{"error": "WORKER_JOB_ERROR"}',
            status=200,
            content_type='application/json',
        )
        with pytest.raises(ValueError):
            self.client.upload(self.file, self.steps)

    @responses.activate
    def test_upload_api_error(self):
        responses.add(
            responses.POST, 'https://api2.transloadit.com/assemblies',
            body='',
            status=404,
            content_type='application/json',
        )
        with pytest.raises(ValueError):
            self.client.upload(self.file, self.steps)
