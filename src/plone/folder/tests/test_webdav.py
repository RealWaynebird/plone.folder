# -*- coding: utf-8 -*-
from Acquisition import Explicit
from plone.folder.ordered import CMFOrderedBTreeFolderBase
from plone.folder.tests.layer import PloneFolderLayer
from plone.folder.tests.utils import DummyObject
from unittest import defaultTestLoader
from unittest import TestCase
from webdav.NullResource import NullResource
from zope.publisher.browser import TestRequest


class TestRequestContainer(Explicit):

    REQUEST = TestRequest()


class WebDAVTests(TestCase):
    """ tests regarding support for WebDAV NullResources """

    layer = PloneFolderLayer

    def test_getitem_not_dav_request(self):
        root = TestRequestContainer()
        folder = CMFOrderedBTreeFolderBase("f1").__of__(root)

        root.REQUEST.maybe_webdav_client = False
        root.REQUEST._environ['REQUEST_METHOD'] = 'GET'

        foo = DummyObject('foo')
        folder['foo'] = foo

        self.assertEquals(folder['foo'], foo)
        try:
            folder['bar']
            self.fail()
        except KeyError:
            pass

    def test_getitem_dav_request(self):
        root = TestRequestContainer()
        folder = CMFOrderedBTreeFolderBase("f1").__of__(root)

        root.REQUEST.maybe_webdav_client = True
        root.REQUEST._environ['REQUEST_METHOD'] = 'PUT'

        foo = DummyObject('foo')
        folder['foo'] = foo

        self.assertEquals(folder['foo'], foo)
        self.failUnless(isinstance(folder['bar'], NullResource))
