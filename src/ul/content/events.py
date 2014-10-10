# -*- coding: utf-8 -*-

from zope.interface import implementer
from zope.component.interfaces import ObjectEvent, IObjectEvent


class IApplicationInitializedEvent(IObjectEvent):
    pass


@implementer(IApplicationInitializedEvent)
class ApplicationInitializedEvent(ObjectEvent):
    pass
