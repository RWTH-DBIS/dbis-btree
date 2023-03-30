import pytest
from dbis_btree.BBaum import BTree


def test_add_node():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    assert len(tree.nodeArray) == 2
    assert tree.nodeArray[0].identifier == "A"
    assert tree.nodeArray[0].values == [10, 20]
    assert tree.nodeArray[1].identifier == "B"
    assert tree.nodeArray[1].values == [1, 2]


def test_add_duplicate_node():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    with pytest.raises(
        AssertionError, match="Bitte nutze einen anderen Name für diese Node."
    ):
        tree.add_node("A", [15, 25])


def test_add_edge():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    tree.add_edge("A", "B", 1)
    assert tree.nodeArray[0].nextNodes[0] == tree.nodeArray[1]


def test_add_invalid_edge():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    with pytest.raises(
        AssertionError,
        match="internal bug: could not find parent or child node in nodeArray.",
    ):
        tree.add_edge("A", "C", 1)


def test_getNode():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    node = tree.getNode("A")
    assert node.identifier == "A"
    assert node.values == [10, 20]
    assert tree.getNode("C") == None


def test_isLeafNode():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    tree.add_edge("A", "B", 1)
    assert BTree.isLeafNode(tree.nodeArray[0]) == False
    assert BTree.isLeafNode(tree.nodeArray[1]) == True


def test_getSibling():
    tree = BTree(3)
    tree.add_node("A", [10, 20])
    tree.add_node("B", [1, 2])
    tree.add_node("C", [30, 40])
    tree.add_edge("A", "B", 1)
    tree.add_edge("A", "C", 2)
    assert BTree.getSibling(tree.nodeArray[1], True) == None
    assert BTree.getSibling(tree.nodeArray[1], False) == tree.nodeArray[2]
    assert BTree.getSibling(tree.nodeArray[2], True) == tree.nodeArray[1]
    assert BTree.getSibling(tree.nodeArray[2], False) == None


def test_deleteNode():
    btree = BTree(3)
    btree.add_node("A", [10, 20])
    btree.add_node("B", [5, 6])
    btree.add_node("C", [15, 16])
    btree.add_node("D", [25, 26])
    btree.add_edge("A", "B", 1)
    btree.add_edge("A", "C", 2)
    btree.add_edge("A", "D", 3)

    assert btree.getNode("B") is not None
    btree.delteNode("B")
    # Update the graph after deleting the node
    btree = BTree.updateGraph(btree)
    assert btree.getNode("B") is None

    # Test deleting non-existent node
    with pytest.warns(UserWarning, match="Node ID: E does not exist."):
        btree.delteNode("E")


def test_valueIsInBbaum():
    btree = BTree(3)
    btree.add_node("A", [10, 20])
    btree.add_node("B", [5, 6])
    assert btree.valueIsInBbaum(10) is True
    assert btree.valueIsInBbaum(5) is True
    assert btree.valueIsInBbaum(30) is False


def test_isLeafNode():
    btree = BTree(3)
    btree.add_node("A", [10, 20])
    btree.add_node("B", [5, 6])
    btree.add_edge("A", "B", 1)

    assert BTree.isLeafNode(btree.getNode("A")) is False
    assert BTree.isLeafNode(btree.getNode("B")) is True


def test_getSibling():
    btree = BTree(3)
    btree.add_node("A", [10, 20])
    btree.add_node("B", [5, 6])
    btree.add_node("C", [15, 16])
    btree.add_node("D", [25, 26])
    btree.add_edge("A", "B", 1)
    btree.add_edge("A", "C", 2)
    btree.add_edge("A", "D", 3)

    assert BTree.getSibling(btree.getNode("B"), False) == btree.getNode("C")
    assert BTree.getSibling(btree.getNode("C"), True) == btree.getNode("B")
    assert BTree.getSibling(btree.getNode("D"), True) == btree.getNode("C")
    assert BTree.getSibling(btree.getNode("B"), True) is None
    assert BTree.getSibling(btree.getNode("D"), False) is None
    assert BTree.getSibling(btree.getNode("A"), True) is None
    assert BTree.getSibling(btree.getNode("A"), False) is None


def test_generateCopyText():
    btree = BTree(3)
    btree.add_node("A", [10, 20])
    btree.add_node("B", [5, 6])
    btree.add_edge("A", "B", 1)

    copy_text = BTree.generateCopyText(btree.getRootNode(), "", "btree")
    expected_text = (
        "btree.add_node('A', [10, 20])\n"
        "btree.add_node('B', [5, 6])\n"
        "btree.add_edge('A', 'B', 1)\n"
    )
    assert copy_text == expected_text
