from setuptools import setup

__version = "0.0.1"

setup(name="oc-art-to-ftp",
        version=__version,
        description="Artifactory to FTP",
        long_description="Copies artifact from artifactory to FTP",
        long_description_content_type="text/plain",
        license="Apache2.0",
        install_requires=[
            "oc-cdtapi",
            "flask",
            "gunicorn",
        ],
      packages={"oc_art_to_ftp"},
      python_requires=">=3.6")
