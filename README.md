## Artifactory to FTP
Service that loads an artifact from artifactory and uploads it to FTP
The following environment variables are required:

**MVN_URL** — Artifactory/Maven URL
**MVN_USER** — Repository username
**MVN_PASSWORD** — Repository password
**FTP_URL** — FTP URL
**FTP_USER** — FTP username
**FTP_PASSWORD** — FTP password

Application listens on specified (default 5700) port for a POST http request with the following payload:

    {
      "gav": "group-artifact-value for artifact in repository",
      "target_path": "full path at FTP server where artifact should be uploaded"
    }

checks existence of artifact and if found downloads it from repository and uploads to FTP.
