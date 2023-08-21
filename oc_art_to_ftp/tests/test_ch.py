from oc_art_to_ftp.app.CryptHelper import CryptHelper
from unittest.mock import patch, Mock
import json
import os
import unittest
import posixpath
from oc_art_to_ftp.tests.mock import MockConnections, MockNexusAPI

class TestCryptHelper(unittest.TestCase):

    def test_nothing(self):
        return None

    def test_client_exists(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        self.assertTrue(ch.client_exists('TEST_CLIENT'))
        return None

    def test_get_client_country(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        self.assertEqual(ch.get_client_country('TEST_CLIENT'), 'TestCountry')
        self.assertIsNone(ch.get_client_country('NONEXISTENT'))
        return None

    def test_get_client_keys(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        keys = ch.get_client_keys('TEST_CLIENT')
        self.assertEqual(keys[0], mc.key_data())
        return None

    def test_encrypt(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        ch.import_client_keys('TEST_CLIENT')
        self.assertEqual(ch.enc_keys_list[0], '91C4B2B6471CB760C4324E16FA24A17E645EEF79')
        handle = mock_svn_fs_client.openbin('TestCountry/TEST_CLIENT/sample.txt')
        encrypted_fn = ch.encrypt(handle)
        f = open(encrypted_fn)
        encrypted_data = f.read()
        f.close()
        decrypted_data = str(ch.gpg.decrypt(encrypted_data, passphrase='test'))
        self.assertEqual(decrypted_data, 'This is a test sample')
        return None
        
    def test_import_client_keys(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        ch.import_client_keys('TEST_CLIENT')
        self.assertEqual(ch.enc_keys_list[0], '91C4B2B6471CB760C4324E16FA24A17E645EEF79')
        return None

    def test_import_key(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        ch.import_key(mc.key_data())
        self.assertEqual(ch.enc_keys_list[0], '91C4B2B6471CB760C4324E16FA24A17E645EEF79')
        return None

    def test_sign(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        ch.import_client_keys('TEST_CLIENT')
        ch.passphrase = 'test'
        temp_dir = ch.tfs.getsyspath(posixpath.sep)
        filename = posixpath.join(temp_dir, 'sample.txt')
        f = open(filename, 'w')
        f.write('This is a test sample')
        f.close()
        signed_filename = ch.sign(filename)
        data = ch._read_file(signed_filename)
        self.assertIn('-----BEGIN PGP SIGNED MESSAGE-----', data)
        return None

    def test_read_file(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        temp_dir = ch.tfs.getsyspath(posixpath.sep)
        filename = posixpath.join(temp_dir, 'sample.txt')
        f = open(filename, 'w')
        f.write('This is a test sample')
        f.close()
        data = ch._read_file(filename)
        self.assertEqual('This is a test sample', data)
        return None

    def test_read_clients_list(self):
        mc = MockConnections()
        mock_svn_fs_client = mc.get_svn_fs_client()
        ch = CryptHelper(mock_svn_fs_client)
        clients = ch._read_clients_list()
        self.assertIn('TestCountry', clients)
        return None
