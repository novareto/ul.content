# -*- coding: utf-8 -*-

from cromlech.container.components import Container as BaseContainer
from cromlech.container.contained import Contained
from cromlech.container.interfaces import INameChooser
from uvc.content import schematic_bootstrap, schema
from zope.interface import implementer
from .interfaces import Icontent, IContainer, IDescriptiveSchema


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
