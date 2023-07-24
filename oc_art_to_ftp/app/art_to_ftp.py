import io
import logging
import os
import posixpath

from oc_cdtapi import NexusAPI
from ftplib import FTP, error_perm


class ArtToFTP:

    def __init__(self):
        """
        initialize class
        """
        self.supported_media = ['artifactory', 'ftp']

    def gav_copy(self, gav, target_path):
        """
        copies specified gav from artifactory to target_path on FTP
        """
        logging.debug('Reached gav_copy')
        logging.debug('gav: [%s]' % gav)
        logging.debug('target_path: [%s]' % target_path)
        
        if not posixpath.isabs(target_path):
            logging.debug('Target path is not absolute, adding leading slash')
            target_path = '/' + target_path
            logging.debug('target_path: [%s]' % target_path)
        
        logging.debug('Initializing NexusAPI')
        na = NexusAPI.NexusAPI()
        logging.debug('Checking existence of [%s]' % gav)
        
        if not na.exists(gav):
            logging.error('Source artifact was not found')
            return self._response(404, 'Source artifact not found')
        
        logging.debug('Artifact exisits, downloading')
        data = na.cat(gav, binary=True)
        datalen = len(data)
        logging.debug('Downloaded [%s] bytes' % datalen)
        logging.debug('Checking existence of [%s] on ftp' % target_path)
        size = self._size(target_path)

        # this logic is to be discussed
        if size is None:
            logging.debug('Error retrieving file size from ftp')
            # do nothing, proceed with upload
        elif size > 0:
            logging.debug('File already exists')
            if size == datalen:
                logging.debug('And is of the same size, skipping upload')
                # refuse to upload file of the same size
                return self._response(304, 'File [%s] exists and is of the same size' % target_path)
            # file sizes differ, do nothing, proceed with upload
        elif size == -1:
            # file was not found, do nothing, proceed with upload
            logging.debug('File was not found')
        # end of questionnable block

        ftp_path, ftp_file = posixpath.split(target_path)

        if not self._ftp_path_exists(ftp_path):
            logging.debug('Path [%s] does not exits on FTP server' % ftp_path)
            self._ftp_path_create(ftp_path)
        
        fd = io.BytesIO(data)
        ftp = self._ftp_connect()
        ftpcmd = 'STOR %s' % target_path
        logging.debug('Trying to store file to [%s]' % target_path)
        
        try:
            retmsg = ftp.storbinary(ftpcmd, fd)
        except:
            return self._response(500, 'Failed to execute storbinary')
        
        logging.debug('FTP server responded with [%s]' % retmsg)
        
        if retmsg.startswith('226'):
            return self._response(200, retmsg)
        else:
            logging.error('Unexpected response from FTP')
            return self._response(500, retmsg)

    def sync(self, source_repo, mask=None):
        """
        Checks source_repo is in sync with FTP, uploads what's missing
        """
        logging.debug('Reached sync')
        logging.debug('source_repo: [%s]' % source_repo)
        logging.debug('Requesting list of files')
        gavs = self.ls('artifactory', source_repo, mask)
        g = 0
        u = 0
        for gav in gavs:
            g = g + 1
            logging.debug('Processing gav N %s [%s]' % (g, gav))
            target_path = self._ftp_path_from_gav(gav)
            if target_path is None:
                logging.debug('Could not determine target_path, skipping')
                continue
            self.gav_copy(gav, target_path)
            u = u + 1
            logging.debug('Requested upload: %s (total %s)' % (u, g))

        return self._response(200, 'Sync finished, requested upload %s of %s artifacts.' % (u, g))


    def ls(self, media, location, mask=None):
        """
        Returns list of files on FTP/artifactory at specified location
        """
        logging.debug('Reached ls')
        logging.debug('media: [%s]' % media)
        logging.debug('location: [%s]' % location)
        logging.debug('mask: [%s]' % mask)
        if not self._media_is_supported(media):
            return self._unsupported()
        if media == 'artifactory':
            logging.debug('Requesting result from _ls_artifactory')
            return self._ls_artifactory(location, mask)
        elif media == 'ftp':
            logging.debug('Requesting result from _ls_ftp')
            return self._ls_ftp(location, mask)
        return self._unimplemented()

    def exists(self, media, location):
        logging.debug('Reached exists')
        logging.debug('media: [%s]' % media)
        logging.debug('locatino: [%s]' % location)
        if not self._media_is_supported(media):
            return self._unsupported()
        if media == 'ftp':
            return self._exists_ftp(location)
        elif media == 'artifactory':
            na = NexusAPI.NexusAPI()
            return na.exists(location)
        return self._unimplemented()

    def _client_code_from_gav(self, gav):
        # consider moving this to NexusAPI
        """
        retrieves client code from gav
        """
        logging.debug('Reached _client_code_from_gav')
        logging.debug('gav: [%s]' % gav)
        group = NexusAPI.parse_gav(gav)['g']
        logging.debug('group: [%s]' % group)
        code = None
        gl = group.split('.')
        l = len(gl)
        for p in range(0, l-1):
            if gl[p] == 'cards' and gl[p+1] == gl[p+1].upper():
                code = gl[p+1]
                logging.debug('Found client code [%s]' % code)
                break
        if code is None:
            logging.debug('Client code not found')
        return code

    def _ftp_connect(self):
        """
        Tries to connect to FTP server, returns ftp handle
        """
        logging.debug('Reached _ftp_connect')
        ftp_host = os.getenv('FTP_URL')
        ftp_user = os.getenv('FTP_USER')
        ftp_pass = os.getenv('FTP_PASSWORD')
        if not all([ftp_host, ftp_user, ftp_pass]):
            logging.error('FTP credentials missing')
            raise ValueError('Missing FTP credentials')
        logging.debug('Trying to connect [%s] to [%s]' % (ftp_user, ftp_host))
        try:
            ftp = FTP(ftp_host, ftp_user, ftp_pass)
        except error_perm as e:
            logging.error('Failed to connect to FTP')
            if str(e).startswith('530'):
                logging.error('Invalid ftp credentials: [%s]' % e)
                raise ValueError('Invalid FTP credentials')
            raise
        logging.debug('Successfully connected to [%s]' % ftp_host)
        return ftp

    def _ftp_dir_create(self, path):
        """
        """
        logging.debug('Reached _ftp_dir_create')
        logging.debug('path: [%s]' % path)
        ftp = self._ftp_connect()
        try:
            ftp.mkd(path)
        except error_perm as e:
            logging.error('Failed to create [%s]: [%s]' % (path, e))
            raise
        logging.debug('[%s] created successfully' % path)

    def _ftp_path_create(self, path):
        """
        """
        logging.debug('Reached _ftp_path_create')
        logging.debug('path: [%s]' % path)
        ftp = self._ftp_connect()
        path_parts = path.split(posixpath.sep)
        logging.debug('path_parts: %s' % path_parts)
        current_path = ''

        for pp in path_parts:
            current_path = current_path + pp + posixpath.sep
            logging.debug('current_path: [%s]' % current_path)
            if not self._ftp_path_exists(current_path):
                logging.debug('Creating [%s]' % current_path)
                self._ftp_dir_create(current_path)

        logging.debug('Paths created successfully')
            
    def _ftp_path_exists(self, path):
        """
        """
        logging.debug('Reached _ftp_path_exists')
        logging.debug('path: [%s]' % path)
        ftp = self._ftp_connect()
        try:
            ftp.cwd(path)
        except error_perm as e:
            if str(e).startswith('550'):
                logging.debug('Path does not exist')
                return False
            raise
        logging.debug('Path exists')
        return True

    def _ftp_path_from_gav(self, gav):
        """
        """
        logging.debug('Reached _ftp_path_from_gav')
        logging.debug('gav: [%s}' % gav)
        logging.debug('stripping gav')
        gav = gav.strip()
        client_code = self._client_code_from_gav(gav)
        filename = NexusAPI.gav_to_filename(gav)
        logging.debug('client_code: [%s]' % client_code)
        logging.debug('filename: [%s]' % filename)
        if client_code:
            path = '/%s/TO_BNK/%s' % (client_code, filename)
            logging.debug('path: [%s]' % path)
            return path
        else:
            logging.error('Failed to get client_code')
            return None

    def _ls_artifactory(self, location, mask=None):
        logging.debug('Reached _ls_artifactory')
        logging.debug('location: [%s]' % location)
        logging.debug('mask: [%s]' % mask)
        logging.debug('Initializing NexusAPI')
        na = NexusAPI.NexusAPI()
        if mask is None: mask = '.*'
        files = na.ls(mask, repo = location)
        logging.debug('na.ls returned: %s' % files)
        return files

    def _media_is_supported(self, media):
        """
        """
        logging.debug('Reached _media_is_supported')
        logging.debug('media: [%s]' % media)

        if media.lower() not in self.supported_media:
            logging.debug('Media is not supported')
            logging.debug('Currently supported are: %s' % self.supported_media)
            return False
        
        logging.debug('Media is supported')
        return True

    def _response(self, code, message):
        """
        """
        logging.debug('Reached _responsee')
        logging.debug('code: [%s]' % code)
        logging.debug('message: [%s]' % message)

        if 200 <= code <= 299:
            result = 'ok'
        else:
            result = 'error'
        
        return code, '{"result": "%s", "message": "%s"}' % (result, message)

    def _size(self, location):
        """
        try to get file size from FTP
        """
        logging.debug('Reached _size')
        ftp = self._ftp_connect()
        size = 0

        try:
            size = ftp.size(location)
        except error_perm as e:
            logging.debug('ftp returned [%s]' % e)
            if str(e).startswith('550'):
                logging.debug('Assuming file not found')
                return -1
            else:
                return None
        
        logging.debug('File found, size: [%s]' % size)
        return size

    def _unimplemented(self):
        logging.error('Support for media is not implemented')
        return None

    def _unsupported(self):
        logging.error('Media is not supported')
        return None
