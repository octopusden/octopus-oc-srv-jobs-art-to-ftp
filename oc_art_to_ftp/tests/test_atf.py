from oc_art_to_ftp.app.art_to_ftp import ArtToFTP
from unittest.mock import patch, Mock
import os
import unittest
from oc_art_to_ftp.tests.mock import MockConnections, MockNexusAPI

class MockArtToFTP(ArtToFTP):

    def _init_svn(self):
        mc = MockConnections()
        svn_client_fs = mc.get_svn_fs_client()
        return svn_client_fs

class TestArtifactoryToFTP(unittest.TestCase):

    def setUp(self):
        os.environ['MVN_URL'] = 'dummy'
        os.environ['MVN_USER'] = 'dummy'
        os.environ['MVN_PASSWORD'] = 'dummy'

    def test_nothing(self):
        return None

    def test_client_code_from_gav(self):
        a = MockArtToFTP()
        test_gav = 'com.example.cdt.yards.TEST_CLIENT.blah:artifact_desc:version:zip'
        test_client = a._client_code_from_gav(test_gav)
        self.assertEqual(test_client, 'TEST_CLIENT')

    def test_ftp_path_from_gav(self):
        a = MockArtToFTP()
        test_gav = 'com.example.cdt.yards.TEST_CLIENT.blah:artifact_desc:version:zip'
        test_path = a._ftp_path_from_gav(test_gav)
        self.assertEqual(test_path, '/TEST_CLIENT/TO_BNK/artifact_desc-version.zip')

    def test_media_is_supported(self):
        a = MockArtToFTP()
        sm = a.supported_media
        for media in sm:
            self.assertTrue(a._media_is_supported(media))
        self.assertFalse(a._media_is_supported('foobarbaz'))

    def test_response(self):
        a = MockArtToFTP()
        code = 200
        message = 'success'
        self.assertEqual(a._response(code, message), (200, '{"result": "ok", "message": "success"}'))
        code = 300
        message = 'failure'
        self.assertEqual(a._response(code, message), (300, '{"result": "error", "message": "failure"}'))

    def test_ls(self):
        a = MockArtToFTP()
        a.nexus_api = MockNexusAPI()
        filelist = a.ls('artifactory','/')
        self.assertEqual(filelist, ['com.example.group:TEST_CLIENT.artifact:version:zip'])

    @patch('oc_art_to_ftp.app.art_to_ftp.FTP', autospec=True)
    def test_ftp_connect(self, mfc):
        os.environ['FTP_URL'] = 'url'
        os.environ['FTP_USER'] = 'dummy'
        os.environ['FTP_PASSWORD'] = 'dummy'
        a = MockArtToFTP()
        ftp = a._ftp_connect()
        mfc.assert_called_with('url', 'dummy', 'dummy')
 
    def test_ftp_conn_no_creds(self):
        a = MockArtToFTP()
        with self.assertRaises(ValueError):
            ftp = a._ftp_connect()

    @patch('oc_art_to_ftp.app.art_to_ftp.FTP', autospec=True)
    def test_ftp_dir_create(self, mfc):
        mf = mfc.return_value
        os.environ['FTP_URL'] = 'url'
        os.environ['FTP_USER'] = 'dummy'
        os.environ['FTP_PASSWORD'] = 'dummy'
        a = MockArtToFTP()
        a._ftp_dir_create('/somedir')
        mf.mkd.assert_called_with('/somedir')

    @patch('oc_art_to_ftp.app.art_to_ftp.FTP', autospec=True)
    def test_ftp_path_exists(self, mfc):
        mf = mfc.return_value
        os.environ['FTP_URL'] = 'url'
        os.environ['FTP_USER'] = 'dummy'
        os.environ['FTP_PASSWORD'] = 'dummy'
        a = MockArtToFTP()
        r = a._ftp_path_exists('/somedir')
        mf.cwd.assert_called_with('/somedir')
        self.assertTrue(r)

    def test_gav_to_upload(self):
        a = MockArtToFTP()
        self.assertFalse(a._gav_to_upload('something'))
        self.assertTrue(a._gav_to_upload('some:customization-23:zip'))

    @patch('oc_art_to_ftp.app.art_to_ftp.FTP', autospec=True)
    def test_size(self, mfc):
        mf = mfc.return_value
        mf.size.return_value = 65535
        os.environ['FTP_URL'] = 'url'
        os.environ['FTP_USER'] = 'dummy'
        os.environ['FTP_PASSWORD'] = 'dummy'
        a = MockArtToFTP()
        size = a._size('/somedir/somefile')
        mf.size.assert_called_with('/somedir/somefile')
        self.assertEqual(size, 65535)

    def test_unimplemented(self):
        a = MockArtToFTP()
        self.assertIsNone(a._unimplemented())

    def test_unsupported(self):
        a = MockArtToFTP()
        self.assertIsNone(a._unsupported())
