# -*- coding: utf-8 -*-

import setuptools

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setuptools.setup(
    name='lool-monitor',
    version='0.3.0',
    author='Jérémie Lesage, Philippe Hemmel',
    author_email='jeremie.lesage@jeci.fr, phemmel@arawa.fr',
    description='Web-socket serveur listening for Lool Admin Worker',
    long_description=readme,
    long_description_content_type="text/markdown",
    url='https://github.com/ArawaFr/libreoffice-online-monitor',
    license=license,
    packages=setuptools.find_packages(),
    package_data={
        'loolmonitor': ['INSTALL.README', '*.bash', 'service/*', 'systemd/*', 'conf/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    install_requires=['websockets', 'requests'],
)
