from fs.memoryfs import MemoryFS
import base64, pkg_resources, posixpath

class MockConnections(object):

    def get_svn_fs_client(self):
        svn_fs = MemoryFS()
        data = '{ "TestCountry": ["TEST_CLIENT"] }'
        svn_fs.writetext('clients.json', data)
        svn_fs.makedir('TestCountry')
        svn_fs.makedir('TestCountry/TEST_CLIENT')
        svn_fs.makedir('TestCountry/TEST_CLIENT/data')
        svn_fs.writetext('TestCountry/TEST_CLIENT/data/testkey.asc', self.key_data())
        svn_fs.writetext('TestCountry/TEST_CLIENT/sample.txt', 'This is a test sample')
        return svn_fs

    def key_data(self):
        filename = pkg_resources.resource_filename('oc_art_to_ftp.tests', posixpath.join('resources', 'gpg_keys', 'keydata.b64'))
        with open(filename, 'rb') as f:
            data = f.read()
        return base64.b64decode(data).decode('utf-8')


class MockNexusAPI(object):

    def exists(self, gav):
        return True

    def cat(self, gav):
        return 'This is a test sample'

    def ls(self, mask=None, repo=None):
        return ['com.example.group:TEST_CLIENT.artifact:version:zip']
