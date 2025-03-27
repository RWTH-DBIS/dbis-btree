import warnings

from graphviz import Digraph, nohtml
from IPython.display import display

NODE_ID_TYPE = str | int
NODE_VALUE_TYPE = list[str | int | float]


class Node:
    # if root node then previousNode will be None
    def __init__(
        self,
        identifier: NODE_ID_TYPE,
        values: NODE_VALUE_TYPE,
        valuesCountInNode: int,
        posInParentArray=None,
    ):
        assert isinstance(values, list), "values has to be a tuple"
        self.previousNode = None
        self.positionInParent_nextNodesArray = (
            posInParentArray  # easier to get siblings
        )
        self.identifier = identifier  # unique identifier
        self.values = values  # e.g. Int-Array
        self.valuesCountInNode = valuesCountInNode
        self.nextNodes: list[Node | None] = [None] * (
            valuesCountInNode + 1
        )  # all children are firstly None

    def get_dot_label(self) -> str:
        """
        Returns a dot representation of the node
        definition of the node and its relations to its childs
        """
        i = 1
        res_str = "<f" + str(i) + "> "

        for x in self.values:
            i = i + 1
            append_str = "|" + str(x) + "|<f" + str(i) + "> "
            res_str = res_str + append_str
        return res_str


class BTree:
    def __init__(self, M: int):
        if M % 2 != 0:
            raise ValueError("M must be an even value")
        self.valuesCountInNode = M
        self.halffull = M // 2 + (M % 2)

        # all the node that were added
        self.nodeArray: list[Node] = []
        # if someone insert a node with an id
        #  that was already inserted -> throw an error
        self.identifierArray = []

    @property
    def graph(self) -> Digraph:
        """
        Generate the Btree graph
        """
        graph = Digraph(
            "btree",
            comment="dot",
            node_attr={
                "shape": "record",
                "height": ".05",
                "fontsize": "10",
                "style": "filled",
                "fillcolor": "#FFFFFF",
            },
            graph_attr={
                "splines": "line",
                "label": "M = " + str(self.valuesCountInNode),
            },
        )
        for node in self.nodeArray:
            graph.node(node.identifier, nohtml(node.get_dot_label()))
            for n_child, child in enumerate(node.nextNodes, 1):
                if child is not None:
                    graph.edge(node.identifier + ":f" + str(n_child), child.identifier)
        return graph

    def add_node(self, name: NODE_ID_TYPE, elements: NODE_VALUE_TYPE):
        if len(self.identifierArray) == 0:
            # root node
            self.nodeArray = [Node(name, elements, self.valuesCountInNode)]
            self.identifierArray.append(name)
        elif name in self.identifierArray:
            raise AssertionError("Bitte nutze einen anderen Namen für diese Node.")
        else:
            self.nodeArray.append(Node(name, elements, self.valuesCountInNode))
            self.identifierArray.append(name)

    def add_edge(self, parent: NODE_ID_TYPE, child: NODE_ID_TYPE, n_child: int) -> None:
        # search both nodes and add their relations
        parentNode = self.getNode(parent)
        childNode = self.getNode(child)

        assert (
            parentNode is not None and childNode is not None
        ), "internal bug: could not find parent or child node in nodeArray."

        # add in previous or next node array
        childNode.previousNode = parentNode

        isNotInNextArray = (
            next(
                (
                    x
                    for x in parentNode.nextNodes
                    if x is not None and childNode.identifier == x.identifier
                ),
                None,
            )
            is None
        )
        if isNotInNextArray:
            # index of the node in nextnodes determindes how the tree locks like
            # print("parent:",parent,"child:",child,"n_child:",n_child)
            if n_child - 1 >= len(parentNode.nextNodes):
                parentNode.nextNodes.insert(n_child - 1, childNode)
            else:
                parentNode.nextNodes[n_child - 1] = childNode
            childNode.positionInParent_nextNodesArray = n_child - 1

    def getNode(self, nodeID: NODE_ID_TYPE) -> Node | None:
        return next((x for x in self.nodeArray if x.identifier == nodeID), None)

    def getRootNode(self):
        # if there are two rootNodes return None
        rootNodes = []
        for node in self.nodeArray:
            if node.previousNode is None:
                rootNodes.append(node)
        if len(rootNodes) != 1:
            return None
        return rootNodes[0]

    def deleteNode(self, nodeID: NODE_ID_TYPE):
        node = next((x for x in self.nodeArray if nodeID == x.identifier), None)
        if nodeID not in self.identifierArray or node is None:
            warnings.warn("Node ID: " + nodeID + " does not exist.", stacklevel=2)
            return

        # delete from own datastructure
        self.identifierArray.remove(nodeID)
        for i, tmpNode in enumerate(self.nodeArray):
            if tmpNode.identifier == nodeID:
                self.nodeArray.pop(i)
                continue
            # delete if node was parent
            if (
                tmpNode.previousNode is not None
                and tmpNode.previousNode.identifier == nodeID
            ):
                if node.previousNode is not None:
                    tmpNode.previousNode = node.previousNode
                else:
                    tmpNode.previousNode = None
            # delete if node is next node
            for j, child in enumerate(tmpNode.nextNodes):
                if child is not None and child.identifier == nodeID:
                    tmpNode.nextNodes[j] = None

    def valueIsInBbaum(self, value):
        return any(value in node.values for node in self.nodeArray)

    @staticmethod
    def isLeafNode(node: Node) -> bool:
        return node.nextNodes.count(None) == len(node.nextNodes)

    @staticmethod
    def getSibling(currentNode: Node, bool_getLeft: bool) -> Node | None:
        if currentNode.previousNode is None:
            return None

        # save in variable because I chose a too long name
        indexNextNodes = currentNode.positionInParent_nextNodesArray

        if indexNextNodes is None:
            # should ... never be the case...
            warnings.warn(
                "WARNING: positionInParent_nextNodesArray is None!", stacklevel=2
            )
            return None

        if bool_getLeft:
            if indexNextNodes == 0:
                return None

            return currentNode.previousNode.nextNodes[indexNextNodes - 1]
        else:
            if indexNextNodes == len(currentNode.previousNode.nextNodes) - 1:
                return None

            return currentNode.previousNode.nextNodes[indexNextNodes + 1]

    @staticmethod
    def generateCopyText(node: Node, text: str, treeName: str):
        """
        its easier for students if they can easily copy the generate graph text in order to make the exercise
        :param node:
        :param text:
        :param treeName:
        :return:
        """
        if node is None:
            return ""
        tmpText = f"{treeName}.add_node('{node.identifier}', {node.values})\n"
        for i, child in enumerate(node.nextNodes):
            if child is not None:
                tmpText += BTree.generateCopyText(child, text, treeName)
                tmpText += f"{treeName}.add_edge('{node.identifier}', '{child.identifier}', {i + 1})\n"

        return text + tmpText

    def draw(self):
        display(self.graph)
