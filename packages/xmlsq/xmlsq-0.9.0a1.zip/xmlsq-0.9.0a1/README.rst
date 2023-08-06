README: A Python interface to xmlsq
===================================

The utility **xmlsq** performs simple and full XPath 1.0 queries on an XML document.

>>> import xmlsq
>>> xml = r"<a><b foo='baz'>hello</b><b>world</b><e /></a>"
>>> xmlsq.get_text(xml, "//b")
'hello'
>>> xmlsq.get_text(xml, "//b[2]")
'world'
>>> xmlsq.full_query(xml, "//b")
'<b foo="baz">hello</b>\n<b>world</b>\n'
>>> xmlsq.get_text(xml, "//b/@foo")
'baz'
>>> xmlsq.full_query(xml, "//b/@foo")
'foo="baz"\n'
>>> xmlsq.full_query(xml, "/a", xmlsq.Opts.RAW)
'<a><b foo="baz">hello</b><b>world</b><e/></a>'
>>> xmlsq.count(xml, "//b")
2
>>> xmlsq.count(xml, "//notthere")
0
>>> xmlsq.count(xml, "//e")
1
>>> xmlsq.full_query(xml, "2+3.5")
'5.500000'

``xmlsq.get_text()`` extracts the text value of the *first* node found selected by the query.

``xmlsq.full_query()`` outputs the result of the full XPath 1.0 query as a string.

``xmlsq.count()`` computes the integer value of ``count(query)``.

For ``xmlsq.get_text()`` and ``xmlsq.count()`` the query *must* evaluate to a node.
``xmlsq.full_query()`` accepts any valid XPath 1.0 expression and returns the result as a string.

For full details of all available methods and options, please see the `documentation <https://www.cryptosys.net/xmlsq/pydocxmlsq/index.html>`_.
	

System requirements
-------------------

Windows platform with Python 3.
Requires the Windows native library **diXmlsq.dll** to be installed on your system, available from
https://www.cryptosys.net/xmlsq/.

Acknowledgment
--------------

This software is based on the pugixml library (https://pugixml.org). Pugixml is Copyright (C) 2006-2019 Arseny Kapoulkine.

Contact
-------

For more information or to make suggestions, please contact us at
https://cryptosys.net/contact/

| David Ireland
| DI Management Services Pty Ltd
| Australia
| 5 June 2020
