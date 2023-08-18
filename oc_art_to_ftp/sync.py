#!/usr/bin/env python3
import os
import logging
from oc_art_to_ftp.app.art_to_ftp import ArtToFTP

logging.basicConfig(level=logging.DEBUG)

logging.info('%s started' % os.path.basename(__file__))

src_repo = os.getenv('ART_SRC_REPO', 'cdt.builds')
logging.info('src_repo: [%s]' % src_repo)

a = ArtToFTP()

logging.info('Starting ArtToFTP.sync...')
a.sync(src_repo)

logging.info('%s ended.' % os.path.basename(__file__))

