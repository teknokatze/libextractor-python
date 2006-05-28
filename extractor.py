# -*- coding: utf-8 -*-
## Python bindings for GNU libextractor
## 
## Copyright (C) 2006 Bader Ladjemi <bader@tele2.fr>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139,
## USA.
##
"""
Python bindings for GNU libextractor

libextractor is a simple library for keyword extraction.  libextractor
does not support all formats but supports a simple plugging mechanism
such that you can quickly add extractors for additional formats, even
without recompiling libextractor. libextractor typically ships with a
dozen helper-libraries that can be used to obtain keywords from common
file-types.  

libextractor is a part of the GNU project (http://www.gnu.org/).     
"""
from ctypes import *
#fake cdll import
libextractor = cdll.extractor

__all__ = ['Extractor', 'isBinaryType']
__version__ = "0.5"
__licence__ = "GNU GPL"

EXTRACTOR_ENCODING = "utf-8"

KeywordType = c_int
Keywords_p = POINTER('Keywords')
class Keywords(Structure):
    """
    EXTRACTOR_Keywords struct
    """
    _fields_ = [('keyword', c_char_p),
		('keywordType', KeywordType),
		('next', Keywords_p)]	
SetPointerType(Keywords_p, Keywords)

KEYWORDS = POINTER(Keywords)

libextractor.EXTRACTOR_getKeywords.restype = KEYWORDS
libextractor.EXTRACTOR_getKeywords2.restype = KEYWORDS
libextractor.EXTRACTOR_removeDuplicateKeywords.restype = KEYWORDS
libextractor.EXTRACTOR_getKeywordTypeAsString.restype = c_char_p

## Extractors_p = POINTER('Extractors')
## ExtractMethod = CFUNCTYPE(Keywords, c_char_p, c_int, Keywords, c_char_p)
## class Extractors(Structure):
##     """
##     EXTRACTOR_Extractor struct
##     """
##     _field_ = [('libraryHandle', c_void_p),
## 	       ('libname', c_char_p),
## 	       ('extractMethod', ExtractMethod),
## 	       ('next', Extractors_p),
## 	       ('options', c_char_p)]
## SetPointerType(Extractors_p, Extractors)

## EXTRACTORS = POINTER(Extractors)

## libextractor.EXTRACTOR_loadDefaultLibraries.restype = EXTRACTORS
## libextractor.EXTRACTOR_loadConfigLibraries.restype = EXTRACTORS
## libextractor.EXTRACTOR_addLibrary.restype = EXTRACTORS
## libextractor.EXTRACTOR_addLibraryLast.restype = EXTRACTORS

libextractor.EXTRACTOR_getDefaultLibraries.restype = c_char_p

class Extractor(object):
    """
    Main class for extracting meta-data with GNU libextractor.

    You may create multiple instances of Extractor to use
    different sets of library.  Initially each Extractor
    will start with the default set of libraries.

    Use the extract method to obtain keywords from a file.

    Use the add and remove libraries methods to change the list of
    libraries that should be used.
    """
    
    def __init__(self, defaults=True, libraries=None, lang=None, languages=None, hash=None, use_filename=False, duplicates=True, split_keywords=False):
	"""
	Initialize Extractor's instance
	@param extractors list of strings that contains extractor's name (supported types)
	@param defaults load default plugins
	@param lang use the generic plaintext extractor for the language with the 2-letter language code LANG
	@param languages list of lang
	@param hash compute hash using the given algorithm (currently 'sha1' or 'md5')
	@param use_filename use the filename as a keyword (add filename-extractor library)
	@param duplicates remove duplicates only if types match
	@param split_keywords use keyword splitting (add split-extractor library)
	"""
	self._libraries = {}

	if defaults:
	    self.extractors = libextractor.EXTRACTOR_loadDefaultLibraries()
	    self._libraries = dict([(library, None) for library in libextractor.EXTRACTOR_getDefaultLibraries().split(':')])
	if use_filename:
	    self.addLibrary("libextractor_filename")
	if libraries:
	    self.extractors = libextractor.EXTRACTOR_loadConfigLibraries(self.extractors, libraries)
	    self._libraries.update(dict([(library, None) for library in libraries.split(':')]))
	if isinstance(lang, str):
	    self.addLibraryLast("libextractor_printable_" % lang)
	if isinstance(hash, str):
	    self.addLibraryLast("libextractor_hash_" % hash)
	if languages:
	    [self.addLibraryLast("libextractor_printable_" % language) for language in languages]
	if split_keywords:
	    self.addLibraryLast("libextractor_split")

	self.duplicates = duplicates
    
    def extract(self, filename=None, data=None, size=None):
	"""Pass a filename, or data and size, to extract keywords.

	@param filename filename string
	@param data data contents
	@param size data size
	
        This function returns a dictionary. Its keys are keywords types
	and its values are keywords values. If the file cannot be opened
	or cannot be found, the dictionary will be empty.  The list can
	also be empty if no dictionary was found for the file.

        """
	if not filename and not (data and size):
	    return None
	elif filename:
	    return self.extractFile(filename)
	else:
	    return self.extractData(data, size)
	
    def extractFile(self, filename):
	"""Pass a filename to extract keywords.

	@param filename filename string
	
        This function returns a dictionary. Its keys are keywords types
	and its values are keywords values. If the file cannot be opened
	or cannot be found, the dictionary will be empty.  The list can
	also be empty if no dictionary was found for the file.

        """
	self.keywords_p = libextractor.EXTRACTOR_getKeywords(self.extractors, filename)
	return self._extract()

    def extractData(self, data, size):
	"""Pass data to extract keywords.

	@param data data contents
	@param size data size
	
        This function returns a dictionary. Its keys are keywords types
	and its values are keywords values. If the file cannot be opened
	or cannot be found, the dictionary will be empty.  The list can
	also be empty if no dictionary was found for the file.

        """
	self.keywords_p = libextractor.EXTRACTOR_getKeywords2(self.extractors, data, size)
	return self._extract()
    
    def _extract(self):
	if not self.keywords_p:
	    return None
	
	if self.duplicates:
	    self.keywords_p = libextractor.EXTRACTOR_removeDuplicateKeywords(self.keywords_p, 1)
	    
	self.extracted = {}
	try:
	    self.keywords = self.keywords_p.contents
	except ValueError:
	    return self.extracted

	while True:
	    keyword_type = libextractor.EXTRACTOR_getKeywordTypeAsString(self.keywords.keywordType).decode(EXTRACTOR_ENCODING)
	    keyword = self.keywords.keyword
	    
	    if not isBinaryType(self.keywords.keywordType):
		keyword = keyword.decode(EXTRACTOR_ENCODING)
		
	    self.extracted[keyword_type] = keyword
	    try:
		self.keywords = self.keywords.next.contents
	    except ValueError:
		libextractor.EXTRACTOR_freeKeywords(self.keywords_p)
		return self.extracted
	    
    def addLibrary(self, library):
	"""
        Add given library to the extractor. Invoke with a string with the name
        of the library that should be added.  For example,
        
        'libextractor_filename'

        will prepend the extractor that just adds the filename as a
        keyword.

        No errors are reported if the library is not
        found.

	@param library library's name
        """	
	self._libraries[library] = None

	self.extractors = libextractor.EXTRACTOR_addLibrary(self.extractors, library)

    def addLibraryLast(self, library):
	"""
	Same as addLibrary but the library is added at the last.

	@param library library's name
	"""
	self._libraries[library] = None
	
	self.extractors = libextractor.EXTRACTOR_addLibraryLast(self.extractors, library)

    def removeLibrary(self, library):
	"""      
        Remove a library.  Pass the name of the library that is to
        be removed.  Only one library can be removed at a time.
        For example,

        'libextractor_pdf'

        removes the PDF extractor (if added).
	ValueError will be thrown if no library match.

	@param library's name
	"""
	try:
	    del self._libraries[library]
	except KeyError:
	    raise ValueError, "No such loaded library"
	
	self.extractors = libextractor.EXTRACTOR_removeLibrary(self.extractors, library)

    def addLibraries(self, libraries):
	"""
	Add given libraries. 
	Same as addLibary but libraries is a list of library's names.

	@param libraries list of libraries names
	"""
	for library in libraries:
	    if isinstance(library, str):
		self.addLibrary(library)

    def removeAllLibraries(self):
	"""
	Remove all libraries.
	"""
	self._libaries = {}
	libextractor.EXTRACTOR_removeAll(self.extractors)
	
    def keywordTypes(self):
	"""
	Returns the list of all keywords types.
	@return list of all keywords types
	"""
	i = 0
	keyword_types = []
	
	while True:
	    keyword_type = libextractor.EXTRACTOR_getKeywordTypeAsString(i)
	    if not keyword_type:
		break
	    keyword_types.append(keyword_type)
	    i += 1
	    
	return keyword_types
    
    def _get_libraries(self):
	return self._libraries.keys()

    def _set_libraries(self, libraries):
	self.addLibraries(libraries)
	
    libraries = property(fget=_get_libraries, fset=_set_libraries, fdel=removeAllLibraries, doc='list of loaded libraries (read only)')

    
    def __delete__(self):
	self.removeAllLibraries()

EXTRACTOR_THUMBNAIL_DATA = 70
def isBinaryType(keyword_type):
    return keyword_type == EXTRACTOR_THUMBNAIL_DATA
