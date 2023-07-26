from oc_art_to_ftp.app.art_to_ftp import ArtToFTP
from unittest.mock import patch, Mock
import os
import unittest

class TestArtToFTPExternals(unittest.TestCase):

    def test_nothing(self):
        return None

    @patch('ftplib.FTP')
    def test_ftp_connect_no_creds(self, MockFTP):
        a = ArtToFTP()
        with self.assertRaises(ValueError):
            mf = a._ftp_connect()

    @patch('ftplib.FTP.connect', autospec=True)
    def _est_ftp_connect_ok(self, MockFTP):
        os.environ['FTP_URL']='nonexistent'
        os.environ['FTP_USER']='testftp'
        os.environ['FTP_PASSWORD']='testftp'
        a = ArtToFTP()
        MockFTP.return_value = Mock()
        mf = a._ftp_connect()


class TestArtToFTPInternals(unittest.TestCase):

    def test_nothing(self):
        return None

    def test_client_code_from_gav(self):
        a = ArtToFTP()
        test_gav = 'com.example.cdt.yards.TEST_CLIENT.blah:artifact_desc:version:zip'
        test_client = a._client_code_from_gav(test_gav)
        self.assertEqual(test_client, 'TEST_CLIENT')

    def test_ftp_path_from_gav(self):
        a = ArtToFTP()
        test_gav = 'com.example.cdt.yards.TEST_CLIENT.blah:artifact_desc:version:zip'
        test_path = a._ftp_path_from_gav(test_gav)
        self.assertEqual(test_path, '/TEST_CLIENT/TO_BNK/artifact_desc-version.zip')

    def test_media_is_supported(self):
        a = ArtToFTP()
        sm = a.supported_media
        for media in sm:
            self.assertTrue(a._media_is_supported(media))
        self.assertFalse(a._media_is_supported('foobarbaz'))

    def test_response(self):
        a = ArtToFTP()
        code = 200
        message = 'success'
        self.assertEqual(a._response(code, message), (200, '{"result": "ok", "message": "success"}'))
        code = 300
        message = 'failure'
        self.assertEqual(a._response(code, message), (300, '{"result": "error", "message": "failure"}'))
