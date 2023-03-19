import pytest
from dbis_btree.BBaum import BTree
from dbis_btree.BBaum_Creator import BTree_Creator

def test_get_node_name():
    assert BTree_Creator.getNodeName(2) == "C"
    assert BTree_Creator.getNodeName(3) == "D"
    assert BTree_Creator.getNodeName(27) == "BB"


def test_convert_node_name_in_number():
    assert BTree_Creator.convertNodeNameInNumber("C") == 2
    assert BTree_Creator.convertNodeNameInNumber("D") == 3
    assert BTree_Creator.convertNodeNameInNumber("BB") == 27
