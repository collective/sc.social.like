# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0.2.dev0'
long_description = (open("README.rst").read() + "\n" +
                    open(os.path.join("docs", "INSTALL.rst")).read() + "\n" +
                    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" +
                    open(os.path.join("docs", "HISTORY.rst")).read())

setup(name='sc.social.like',
      version=version,
      description="""Social Like is a Plone package providing simple Google+,
                     Twitter and Facebook integration for Plone
                     Content Types""",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.0",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Office/Business :: News/Diary",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='python plone zope webdev social googleplus facebook twitter',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='https://github.com/collective/sc.social.like',
      license='GPLv2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sc', 'sc.social'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Pillow',
          'Plone'
      ],
      extras_require={
          'test': ['plone.app.testing']
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
