# -*- coding: utf-8 -*-

from unidecode import unidecode
from cromlech.container.components import Container as BaseContainer
from cromlech.container.contained import Contained
from cromlech.container.interfaces import IContainer, INameChooser
from uvc.content import schematic_bootstrap, schema
from uvc.content.interfaces import IContent, IDescriptiveSchema
from zope.interface import implementer
from grokcore.component import context, Adapter


@implementer(IContent)
class Content(Contained):
    """Base Content
    """
    schema(IDescriptiveSchema)
    __init__ = schematic_bootstrap


@implementer(IContent, IContainer)
class Container(BaseContainer):
    """Base Container
    """
    schema(IDescriptiveSchema)
    __init__ = schematic_bootstrap


@implementer(INameChooser)
class NormalizingNamechooser(Adapter):
    context(IContainer)

    retries = 100

    def __init__(self, context):
        self.context = context

    def checkName(self, name, object):
        return not name in self.context

    def _findUniqueName(self, name, object):
        if not name in self.context:
            return name

        idx = 1
        while idx <= self.retries:
            new_name = "%s_%d" % (name, idx)
            if not new_name in self.context:
                return new_name
            idx += 1

        raise ValueError(
            "Cannot find a unique name based on "
            "`%s` after %d attempts." % (name, self.retries))

    def chooseName(self, name, object):
        if not name:
            dc = IDescriptiveSchema(object, None)
            if dc is not None and dc.title:
                name = dc.title.strip()
                name = unidecode(name).strip().replace(' ', '_').lower()
            else:
                name = object.__class__.__name__.lower()

        return self._findUniqueName(name, object)
