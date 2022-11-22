""".. versionadded:: 0.0.1

Control the macOS Preview application using JXA-like syntax.
"""

from typing import Union, Self

import AppKit

from PyXA import XABase
from PyXA import XABaseScriptable
from ..XAProtocols import XACanOpenPath, XACanPrintPath, XAClipboardCodable, XACloseable, XAPrintable

class XAPreviewApplication(XABaseScriptable.XASBApplication, XACanOpenPath, XACanPrintPath):
    """A class for managing and interacting with Preview.app.

    .. seealso:: :class:`XAPreviewWindow`, :class:`XAPreviewDocument`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XAPreviewWindow

    @property
    def frontmost(self) -> bool:
        """Whether Preview is the active application.
        """
        return self.xa_scel.frontmost()

    @frontmost.setter
    def frontmost(self, frontmost: bool):
        self.set_property("frontmost", frontmost)

    @property
    def name(self) -> str:
        """The name of the application.
        """
        return self.xa_scel.name()

    @property
    def version(self) -> str:
        """The version of Preview.app.
        """
        return self.xa_scel.version()

    def print(self, path: Union[str, AppKit.NSURL], show_prompt: bool = True):
        """Opens the print dialog for the file at the given path, if the file can be opened in Preview.

        :param path: The path of the file to print.
        :type path: Union[str, AppKit.NSURL]
        :param show_prompt: Whether to show the print dialog or skip directly printing, defaults to True
        :type show_prompt: bool, optional

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            path = AppKit.NSURL.alloc().initFileURLWithPath_(path)
        self.xa_scel.print_printDialog_withProperties_(path, show_prompt, None)

    def documents(self, filter: dict = None) -> 'XAPreviewDocumentList':
        """Returns a list of documents matching the filter.

        :Example 1: List all documents

        >>> import PyXA
        >>> app = PyXA.Application("Preview")
        >>> print(app.documents())
        <<class 'PyXA.apps.Preview.XAPreviewDocumentList'>['Example1.pdf', 'Example2.pdf']>

        .. versionchanged:: 0.0.4

           Now returns an object of :class:`XAPreviewDocumentList` instead of a default list.

        .. versionadded:: 0.0.1
        """
        return self._new_element(self.xa_scel.documents(), XAPreviewDocumentList, filter)




class XAPreviewWindow(XABaseScriptable.XASBWindow, XABaseScriptable.XASBPrintable):
    """A class for managing and interacting with Preview windows.

    .. seealso:: :class:`XAPreviewApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the window.
        """
        return self.xa_elem.properties()

    @property
    def document(self) -> 'XAPreviewDocument':
        """The document currently displayed in the window.
        """
        return self._new_element(self.xa_elem.document(), XAPreviewDocument)

    @document.setter
    def document(self, document: 'XAPreviewDocument'):
        self.set_property("document", document.xa_elem)

    @property
    def floating(self) -> bool:
        """Whether the window floats.
        """
        return self.xa_elem.floating()

    @property
    def modal(self) -> bool:
        """Whether the window is a modal view.
        """
        return self.xa_elem.modal()

    @property
    def titled(self) -> bool:
        """Whether the window has a title bar.
        """
        return self.xa_elem.titled()




class XAPreviewDocumentList(XABase.XAList, XAClipboardCodable):
    """A wrapper around lists of documents that employs fast enumeration techniques.

    All properties of documents can be called as methods on the wrapped list, returning a list containing each documents's value for the property.

    .. versionadded:: 0.0.4
    """
    def __init__(self, properties: dict, filter: Union[dict, None] = None):
        super().__init__(properties, XAPreviewDocument, filter)

    def properties(self) -> list[dict]:
        """Gets the properties dictionary of each document in the list.

        :return: A list of document properties dictionaries
        :rtype: list[dict]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("properties"))

    def name(self) -> list[str]:
        """Gets the name of each document in the list.

        :return: A list of document names
        :rtype: list[str]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("name"))

    def path(self) -> list[XABase.XAPath]:
        """Gets the path of each document in the list.

        :return: A list of document paths
        :rtype: list[XABase.XAPath]
        
        .. versionadded:: 0.0.4
        """
        ls = self.xa_elem.arrayByApplyingSelector_("path")
        return [XABase.XAPath(x) for x in ls]

    def modified(self) -> list[str]:
        """Gets the modified status of each document in the list.

        :return: A list of document modified status booleans
        :rtype: list[bool]
        
        .. versionadded:: 0.0.4
        """
        return list(self.xa_elem.arrayByApplyingSelector_("modified"))

    def by_properties(self, properties: dict) -> Union['XAPreviewDocument', None]:
        """Retrieves the document whose properties dictionary matches the given properties, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPreviewDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("properties", properties)

    def by_name(self, name: str) -> Union['XAPreviewDocument', None]:
        """Retrieves the document whose name matches the given name, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPreviewDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("name", name)

    def by_path(self, path: Union[str, XABase.XAPath]) -> Union['XAPreviewDocument', None]:
        """Retrieves the document whose path status matches the given path, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPreviewDocument, None]
        
        .. versionadded:: 0.0.4
        """
        if isinstance(path, str):
            path = XABase.XAPath(str)
        return self.by_property("path", str(path.xa_elem))

    def by_modified(self, modified: bool) -> Union['XAPreviewDocument', None]:
        """Retrieves the document whose modified status matches the given boolean value, if one exists.

        :return: The desired document, if it is found
        :rtype: Union[XAPreviewDocument, None]
        
        .. versionadded:: 0.0.4
        """
        return self.by_property("modified", modified)

    def get_clipboard_representation(self) -> list[AppKit.NSURL]:
        """Gets a clipboard-codable representation of each document in the list.

        When the clipboard content is set to a document, each documents's file URL is added to the clipboard.

        :return: The document's file URL
        :rtype: list[AppKit.NSURL]

        .. versionadded:: 0.0.8
        """
        paths = self.path()
        return [x.xa_elem for x in paths]

    def __repr__(self):
        return "<" + str(type(self)) + str(self.name()) + ">"
    
class XAPreviewDocument(XABase.XATextDocument, XAPrintable, XACloseable, XAClipboardCodable):
    """A class for managing and interacting with documents in Preview.

    .. seealso:: :class:`XAPreviewApplication`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

    @property
    def properties(self) -> dict:
        """All properties of the document.
        """
        return self.xa_elem.properties()

    @property
    def name(self) -> str:
        """The name of the document.
        """
        return self.xa_elem.name()

    @name.setter
    def name(self, name: str):
        self.set_property("name", name)

    @property
    def path(self) -> XABase.XAPath:
        """The document's file path.
        """
        return XABase.XAPath(self.xa_elem.path())

    @path.setter
    def path(self, path: XABase.XAPath):
        self.set_property("path", path.xa_elem)

    @property
    def modified(self) -> bool:
        """Whether the document has been modified since the last save.
        """
        return self.xa_elem.modified()

    def print(self, print_properties: Union[dict, None] = None, show_dialog: bool = True) -> Self:
        """Prints the document.

        :param print_properties: Properties to set for printing, defaults to None
        :type print_properties: Union[dict, None], optional
        :param show_dialog: Whether to show the print dialog, defaults to True
        :type show_dialog: bool, optional
        :return: The document object
        :rtype: Self

        .. versionadded:: 0.0.4
        """
        if print_properties is None:
            print_properties = {}
        self.xa_elem.print_printDialog_withProperties_(self.xa_elem, show_dialog, print_properties)
        return self

    def save(self, file_path: str = None):
        """Saves the document.
        
        If a file path is provided, Preview will attempt to save the file with the specified file extension at that path. If automatic conversion fails, the document will be saved in its original file format. If no path is provided, the document is saved at the current path for the document.

        :Example 1: Save a PDF (or any compatible document) as a PNG

        >>> import PyXA
        >>> app = PyXA.Application("Preview")
        >>> doc = app.documents()[0] # A PDF
        >>> # Save to Downloads to avoid permission errors
        >>> doc.save("/Users/steven/Downloads/Example.png")
        
        .. versionadded:: 0.0.4
        """
        self.xa_elem.saveAs_in_(None, file_path)

    def get_clipboard_representation(self) -> AppKit.NSURL:
        """Gets a clipboard-codable representation of the document.

        When the clipboard content is set to a document, the documents's file URL is added to the clipboard.

        :return: The document's file URL
        :rtype: AppKit.NSURL

        .. versionadded:: 0.0.8
        """
        return self.path.xa_elem

    def __repr__(self):
        return self.name