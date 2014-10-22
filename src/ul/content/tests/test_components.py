# -*- coding: utf-8 -*-

import pytest
from ul.content import Content, Container
from zope.location.interfaces import IContained
from uvc.content import schema
from zope.interface import Interface
from zope.schema import TextLine, Text, Int
from zope.schema.interfaces import WrongType
from uvc.content.interfaces import IContent, IDescriptiveSchema
from cromlech.container.interfaces import IContainer


class IArtPiece(Interface):
    """A work of art
    """
    artist = TextLine(
        title=u"Name of the artist",
        required=True)

    title = TextLine(
        title=u"Name of the art work",
        required=True)
    
    year = Int(
        title=u"Year the art work was done",
        required=True)
    
    theme = Text(
        title=u"About the art work",
        required=False)


class IArtStorage(Interface):
    """A place where art works are stored
    """
    title = TextLine(
        title=u"Name of the storage",
        required=True)
    
    location = TextLine(
        title=u"Place and location of the storage",
        required=True)


class Painting(Content):
    schema(IArtPiece)


class Museum(Container):
    schema(IArtStorage)


def test_interfaces():
    painting = Painting()

    # Content objects provide, by default, IContent and IDescriptiveSchema
    assert IContent.providedBy(painting)
    assert IDescriptiveSchema.providedBy(painting)

    # IDescriptiveSchema provides base fields
    assert 'description' not in IArtPiece
    assert 'description' in IDescriptiveSchema
    assert painting.description == u''

    # Container objects provide, by default, IContent and IDescriptiveSchema
    # It also provides IContainer from cromlech.container
    museum = Museum()
    assert IContent.providedBy(museum)
    assert IDescriptiveSchema.providedBy(museum)
    assert IContainer.providedBy(museum)

    # Both Content and Container are IContained (zope.location)
    assert IContained.providedBy(painting)
    assert IContained.providedBy(museum)

    
def test_schema():
    painting = Painting()

    # the schema created the fields
    assert painting.artist == None
    assert painting.title == None
    assert painting.year == None
    assert painting.theme == None

    # They are strongly typed
    # This is a minimal test : everything is tested in uvc.content
    with pytest.raises(WrongType):
        painting.artist = 1

    # The Content class allows us to bootstrap the fields' values
    lady = Painting(title=u"The Lady of Shalott")
    assert lady.title == u"The Lady of Shalott"

    # Obviously, this bootstrap errors if values are wrongly typed
    with pytest.raises(WrongType):
        lady = Painting(title=1888)

    # Unknown fields are ignored.
    dummy = Painting(beer=u"Delirium Tremens")
    with pytest.raises(AttributeError):
        getattr(dummy, 'beer')


def test_containment():
    london_museum = Museum(title=u"Tate Britain", location=u"London (UK)")
    lady = Painting(title=u"The Lady of Shalott", year=1888,
                    artist=u"John William Waterhouse",
                    theme=u"""The work is a representation of a scene from Alfred, Lord Tennyson's 1832 poem of the same name, in which the poet describes the plight of a young woman, loosely based on the figure of Elaine of Astolat from medieval Arthurian legend, who yearned with an unrequited love for the knight Sir Lancelot, isolated under an undisclosed curse in a tower near King Arthur's Camelot.""")

    # We can now persist objects in our container
    london_museum['lady'] = lady

    # Retrieving them is straightforward and defines the lineage
    # The rest of the tests are in uvc.content and cromlech.container
    # See these packages for more information and code insights.
    painting = london_museum['lady']
    assert painting.__name__ == 'lady'
    assert painting.__parent__ is london_museum

