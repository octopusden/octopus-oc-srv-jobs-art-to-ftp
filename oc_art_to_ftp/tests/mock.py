from fs.memoryfs import MemoryFS

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
        return """
-----BEGIN PGP PRIVATE KEY BLOCK-----                                                                                                                        
Version: GnuPG v2.0.22 (GNU/Linux)

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
XevOiNuxH5/BpfbD
=sTaY
-----END PGP PRIVATE KEY BLOCK-----
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v2.0.22 (GNU/Linux)

mQENBGTHpYoBCADbTR9r5kuAC5vGIbIkvVB9lzJVNrDqhWe60ZChfcXYSmYsh3rD
CaiBi/JJhjXC90O6i1FlzcB3GSJYJXXzxr3H21K3uH4xrty8GLiCka7cXSehBVbv
gh1whIT9VqUwnPFEN84QDlrJuXcn+fjyuKrzgwzxJ0HwlzgCD8oJnwEbSYZ0GA9m
T1xcFrj4Hcez70019uto+OV30oC6adJAh5Pul+5WPU5T1RIcT/QRCt21PnF1F7NV
SGXZZozb1m674rD8eZFi+ptviC/YyanUJVxK4wGwP9gqg5eB569il4T0kiIPzAND
+U+ep10GqEiNkOVx5OehdE2BXQsdz+8QKzIHABEBAAG0G1Rlc3RUZXN0IDx0ZXN0
QGV4YW1wbGUuY29tPokBOQQTAQIAIwUCZMeligIbAwcLCQgHAwIBBhUIAgkKCwQW
AgMBAh4BAheAAAoJEPokoX5kXu95/qIH/2ysPvPq+oCgbZIrVv8xtgZ7Nuhm/JHX
r1Eyow20dJF4mIO8wN3zM+x62Zeu2wYNOrHAKxiUQ5sQ2qzaBHRRmaNmJf2f2qNi
fUlS22CCzOI5JS5OSfZ+BJ9/QQXMDN0hRebpfGLgslel+08RrmR7TepQmLsQu/br
ovUyZg8Ck+IeiY2ORyhtoolTSDZjF+VxnRJ2MjfIUVMLn9XazK7nece+C3QuQ46j
VmRXxKvLtrwTZnFV7eJvIMalOpDBgbISaplbuKDo7bs+xR181TiHBw+BtzEA5EJB
8znJoGA6jo6faiLnTXStWLiW32qK+lRp9lHhDfLK016yzr3UHxL6bcu5AQ0EZMel
igEIAMDYD6pzFrvpq3sqaaennA8ZlYuDUj0xL/hS8XN88TRX3pCWACYMMODm6GFG
ZpVKhBbnquzo19xvv8PzkKrIa1f50G1tcX7nqbnb9jHcSFvA4IuXQXkbi/K7wnPZ
rflwWsfb0xMBVn1gTXTghqY09YJyXtw+Vmj1vWmiEKO+xHL9z/HVo8yWIOB9IgLG
xq82uSLDh/Wz1Io3gElFXNNFaYIJ+9QVI6eJFsVQp6X37V6zMZUvfpEAawEuOgP5
mi7TkNTUSydMFcw0Ab0dOaEJ8CKBo+1cU9ZPz27GqLUFR5j1y4X8lfM6678WCFQm
JcMd9y8NYKUAqkLk0Vbl4cWlyvkAEQEAAYkBHwQYAQIACQUCZMeligIbDAAKCRD6
JKF+ZF7vedf8B/4pnbLd4eAZSJ2zQxJwfnZIH9LxLeJZ2Zcx2fYFJt86ZtHlg3Ss
bh7f/ZCOQyL9bEhSqIYeoDvRPkvnOkxa6jMWA4xOcNxkfsBJ2NJhYwenaS2preu+
Px4P/omSaCn/NM0eguF/Fg/myr4lEYnAQfZyzH8rQzUVzNVa14kb/vKyJJq3aUR5
mG1UDeZZtOGKpk5/kp1pl2ctskK1SBa+dTT86+2OLsCdPAoUerhLqpbIU6rQrNPF
pDQDcrcnrMfP15vDddbep1j2Go/BA8hU8Bjm3SwOpuQOJ39zkI+3FFeuLxHn2L5W
rfHqIn8MTq7Ffnb5hh9nXevOiNuxH5/BpfbD
=Pa34
-----END PGP PUBLIC KEY BLOCK-----
      """


class MockNexusAPI(object):

    def exists(self, gav):
        return True

    def cat(self, gav):
        return 'This is a test sample'

    def ls(self, mask=None, repo=None):
        return ['com.example.group:TEST_CLIENT.artifact:version:zip']
