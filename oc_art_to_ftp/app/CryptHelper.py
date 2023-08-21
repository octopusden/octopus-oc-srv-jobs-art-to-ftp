import gnupg
import json
import logging
import os
import posixpath
import random
import string
from fs.tempfs import TempFS

class CryptHelper(object):

    def __init__(self, svn_client_fs):
        """
        Initialization, requires oc_pyfs.SvnFS as an argument
        """
        logging.debug('Initializing CryptHelper')
        logging.debug('Checking if already initialized')
        if hasattr(self, 'clients'):
            logging.debug('self.clients exists, skipping initialization')
            return None
        tfs = TempFS()
        gpg = gnupg.GPG(gnupghome=tfs.getsyspath(posixpath.sep))
        self.gpg = gpg
        self.tfs = tfs
        self.enc_keys_list = []
        self.svn_client_fs = svn_client_fs
        self.clients = self._read_clients_list()
        self.passphrase = os.getenv('PGP_PASSWORD')
        self.pki_path = os.getenv('PKI_PATH')
        self.import_keys(self.pki_path)
        self.own_keys_list = self.enc_keys_list.copy()

    def client_exists(self, client_code):
        """
        """
        logging.debug('Reached client_exists')
        logging.debug('client_code: [%s]' % client_code)
        for k in self.clients.keys():
            if client_code.upper() in self.clients[k]:
                logging.debug('Client exists')
                return True
        logging.debug('Client does not exist')
        return False

    def get_client_country(self, client_code):
        """
        Returns client country
        """
        logging.debug('Reached get_client_country')
        logging.debug('client_code: [%s]' % client_code)
        for country in self.clients.keys():
            if client_code in self.clients[country]:
                logging.debug('Client found in [%s]' % country)
                return country
        logging.warn('No country found for client [%s]' % client_code)
        return None

    def get_client_keys(self, client_code):
        """
        Reads client keys from svn into list
        """
        logging.debug('Reached get_client_keys')
        logging.debug('client_code: [%s]' % client_code)
        client_country = self.get_client_country(client_code)
        logging.debug('client_country: [%s]' % client_country)
        client_keys = []
        if not client_country:
            logging.error('No country for client [%s]' % client_code)
            return None
        client_home = posixpath.join(client_country, client_code, 'data')
        files = self.svn_client_fs.opendir(client_home).listdir('/')
        logging.debug('[%s] contains following files: [%s]' % (client_home, files))
        for filename in files:
            if filename.endswith('.asc'):
                logging.debug('[%s] appears to be a key file, trying to append' % filename)
                client_keys.append(self._read_svn_file(posixpath.join(client_home, filename)))
        logging.debug('client_keys array is of [%s] elements' % len(client_keys))
        return client_keys
        
    def get_method(self, gav):
        """
        """
        logging.debug('Reached get_method')
        logging.debug('gav: [%s]' % gav)
        return 'encrypt'

    def encrypt(self, handle):
        """
        Encrypts specified handle, returns path to encrypted content
        """
        logging.debug('Reached encrypt_handle')
        if not self.enc_keys_list:
            logging.warn('Currently no keys in encryption keys list, nothing to do')
            return None
        temp_dir = self.tfs.getsyspath(posixpath.sep)
        file_exists = True
        while file_exists:
            output_filename = self._gen_filename()
            output_path = posixpath.join(temp_dir, output_filename)
            logging.debug('output_path: [%s]' % output_path)
            logging.debug('checking if output_path exists')
            file_exists = posixpath.exists(output_path)
            logging.debug('..is [%s]' % file_exists)
        logging.debug('Trying to encrypt with [%s] keys' % len(self.enc_keys_list))
        result = self.gpg.encrypt_file(handle, self.enc_keys_list, always_trust=True, output=output_path)
        if result.ok:
            logging.debug('Successfully encrypted')
            return output_path
        else:
            logging.error('Failed to encrypt:')
            logging.error(result.stderr)

    def import_client_keys(self, client_code):
        """
        Imports client keys from svn
        """
        logging.debug('Reached import_client_keys')
        logging.debug('client_code: [%s]' % client_code)
        logging.debug('Resetting enc_keys_list')
        self.enc_keys_list = self.own_keys_list.copy()
        logging.debug('Requesting client keys...')
        keys = self.get_client_keys(client_code)
        for key in keys:
            logging.debug('Calling import_key...')
            self.import_key(key)
        logging.debug('enc_key_list length is [%s]' % len(self.enc_keys_list))

    def import_key(self, key_data):
        """
        Loads specified key into gpg key storage
        """
        logging.debug('Reached import_key')
        result = self.gpg.import_keys(key_data)
        logging.debug('result: [%s]' % result)
        imported = result.results
        count = len(imported)
        logging.debug('%s keys imported' % count)
        if count == 0:
            logging.warn('No keys imported')
            return
        for key in imported:
            self._add_ek(key)

    def import_keys(self, pki_path):
        """
        Imports all keys present in pki_path
        """
        logging.debug('Reached import_keys')
        logging.debug('pki_path: [%s]' % pki_path)
        if not pki_path:
            logging.warn('PKI_PATH is not set, private keys will not be loaded, signing is not possible')
            return
        files = [f for f in os.listdir(pki_path) if os.path.isfile(f)]
        for f in files:
            if f.endswith('.asc'):
                logging.debug('Importing [%s]' % f)
                data = self._read_file(f)
                self.import_key(data)

    def sign(self, filename):
        """
        Signs specified filenane
        """
        logging.debug('Reached sign')
        if not self._check_pk():
            logging.error('No private keys for signature')
            return None
        logging.debug('filename: [%s]' % filename)
        output = filename + '.asc'
        logging.debug('output: [%s]' % output)
        s = self.gpg.sign_file(filename, passphrase=self.passphrase, output=output)
        return output

    def _add_ek(self, key):
        """
        Adds key to encryption keys list
        """
        logging.debug('Reached _add_ek')
        logging.debug('key: [%s]' % key)
        fingerprint = key.get('fingerprint')
        logging.debug('fingerprint: [%s]' % fingerprint)
        if fingerprint in self.enc_keys_list:
            logging.debug('They key is already in encryption keys list')
            return
        logging.debug('Adding key to encryption keys list')
        self.enc_keys_list.append(fingerprint)

    def _check_pk(self):
        """
        Checks if any secret keys are loaded
        """
        logging.debug('Reached _check_pk')
        keys = self.gpg.list_keys(True)
        if len(keys) == 0:
            logging.error('No private keys loaded')
            return False
        return True

    def _gen_filename(self):
        """
        Generates random string
        """
        return ''.join(random.choice(string.ascii_letters) for i in range(20))

    def _read_clients_list(self):
        """
        Reads clients.json from svn
        """
        logging.debug('Reached _read_clients_list')
        data = self._read_svn_file('clients.json')
        return json.loads(data)

    def _read_file(self, filename):
        """
        Reads arbitary file
        """
        logging.debug('Reached _read_file')
        logging.debug('filename: [%s]' % filename)
        with open(filename) as f:
            data = f.read()
        logging.debug('Read [%s] from [%s]' % (len(data), filename))
        return data

    def _read_svn_file(self, filename):
        """
        Reads file from svn
        """
        logging.debug('Reached _read_svn_file')
        logging.debug('filename: [%s]' % filename)
        with self.svn_client_fs.open(filename) as f:
            data = f.read()
        logging.debug('Read [%s] from [%s]' % (len(data), filename))
        return data
