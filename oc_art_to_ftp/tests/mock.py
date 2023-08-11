from fs.memoryfs import MemoryFS

class MockConnections(object):

    def get_svn_fs_client(self):
        svn_fs = MemoryFS()
        data = '{ "TestCountry": ["TEST_CLIENT"] }'
        svn_fs.writetext('clients.json', data)
        return svn_fs

class MockNexusAPI(object):

    def exists(self, gav):
        return True

    def cat(self, gav):
        return 'this is a file'

    def ls(self, mask=None, repo=None):
        return ['com.example.group:TEST_CLIENT.artifact:version:zip']
