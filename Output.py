"""
Collection of functions that convert a given data container to an text based output format
"""

from xml.dom.minidom import getDOMImplementation
import random  # Used only for testing func, remove in final
import types   # Used only in assertions

def toXML(tag_list, filename):
    """
    toXML(): Creates an XML-style document from the tags and their values
    :param tag_list: A dictionary of lists of values
    :param filename: Name of file to write to, no extension
    :return: None
    """

    assert len(filename) > 0, \
        "Filename cannot be empty."
    assert isinstance(tag_list, types.DictionaryType), \
        "Dictionary of lists required."

    # Setup DOM Object and list
    impl = getDOMImplementation()
    doc = impl.createDocument(None, "ABIF", None)
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
        # Add the new element and its children to the tree
        top_element.appendChild(new_elem)

    # Output contents to file
    filename += ".xml"
    file_writer = open(filename, 'wb')
    doc.writexml(file_writer, indent='\t\n', addindent='\t', encoding='utf-8')
    file_writer.close()


def testXML():
    tag_list = {"Tag1" : 0, "Tag2" : 0, "Tag3" : 0, "Tag4" : 0, "Tag5" : 0, "Tag6" : 0}
    for tag in tag_list:
        values = []
        for val in range(10):  # Add 10 values to the tag's list of values
            values.append(str(random.randrange(1, 100, 15)))  # Append random values
        tag_list[tag] = values

    toXML(tag_list, "test")