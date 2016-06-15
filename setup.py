# Copyright 2016 Canonical Ltd.  This software is licensed under the
# GNU Affero General Public License version 3 (see the file LICENSE).

"""Distutils installer for txsse."""

from setuptools import (
    find_packages,
    setup,
)


setup(
    name="txSSE",
    version="0.1.0",
    packages=find_packages(),

    install_requires=[
        "Twisted",
    ],
    extras_require=dict(
        test=[
            "testtools",
            "daemonfixture",
            "selenium",
        ],
    ),

    author="Free Ekanayaka",
    author_email="<free.ekanayaka@canonical.com>",
    description="Server-Sent Events implementation for Twisted",
    license="AGPL",
    keywords="twisted sse",
    url="http://launchpad.net/txsse",
)
