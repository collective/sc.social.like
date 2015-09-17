# -*- coding:utf-8 -*-

from setuptools import find_packages
from setuptools import setup

version = '2.4'
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
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
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
          'plone.app.controlpanel',
          'plone.app.layout',
          'plone.app.upgrade',
          'plone.memoize',
          'Products.Archetypes',
          'Products.CMFCore',
          'Products.CMFDefault',
          'Products.CMFPlone >=4.1',
          'Products.CMFQuickInstallerTool',
          'Products.GenericSetup',
          'plone.api',
          'setuptools',
          'zope.component',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.browserlayer',
              'plone.app.robotframework',
              'plone.app.testing [robot] >=4.2.2',
              'robotsuite',
              'unittest2',
          ],
          'develop': ['docutils'],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
