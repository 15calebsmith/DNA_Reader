"""
Collection of functions that convert a given data container to an text based output format
"""

import random
import types
from xml.dom.minidom import getDOMImplementation


def toXML(tag_list):
    assert isinstance(tag_list, types.DictionaryType), \
        "Dictionary of lists required."
    assert isinstance(tag_list[0], types.ListType), \
        "The dictionary must contain lists."

    # Setup DOM Object and list
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "ABIF File", None)
    top_element = doc.documentElement

    # For each tag in the dict
    for tag_name in tag_list:
        new_elem = doc.createElement(str(tag_name))  # Create a new element for the tag
        # For each item in the list
        for item in tag_list[tag_name]:
            value_node = doc.createElement("value")
            text_item = doc.createTextNode(str(item))
            value_node.appendChild(text_item)
            new_elem.appendChild(value_node)

        top_element.appendChild(new_elem)

    file = open('test.xml', 'wb')
    doc.writexml(file, indent='\t\n', addindent='\t', encoding='utf-8')


def testXML():
    tag_list = {}
    for i in range(10):
        tag = []
        for j in range(10):
            tag.append(str(random.randrange(1, 100, 15)))
        tag_list[i] = tag

    toXML(tag_list)
