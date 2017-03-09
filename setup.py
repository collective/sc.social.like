# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '2.9'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='sc.social.like',
      version=version,
      description="""Social Like is a Plone package providing simple Google+,
                     Twitter and Facebook integration for Plone
                     Content Types""",
      long_description=long_description,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
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
          'Acquisition',
          'plone.api',
          'plone.app.layout',
          'plone.app.registry',
          'plone.app.upgrade',
          'plone.memoize',
          'plone.registry',
          'plone.supermodel',
          'Products.Archetypes',
          'Products.CMFCore',
          'Products.CMFPlone >=4.2',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'setuptools',
          'zope.annotation',
          'zope.component',
          'zope.globalrequest',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'AccessControl',
              'lxml',
              'mock',
              'plone.app.robotframework',
              'plone.app.testing [robot] >=4.2.2',
              'plone.browserlayer',
              'plone.namedfile [blobs]',
              'plone.testing',
              'Products.PrintingMailHost',
              'robotsuite',
          ],
          'develop': ['docutils'],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
