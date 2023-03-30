import copy

from graphviz import Digraph, nohtml
from IPython.display import display
from string import printable
import warnings


class Node:
    # if root node then previousNode will be None
    def __init__(self, identifier, values, valuesCountInNode, posInParentArray=None):
        assert all(
            isinstance(item, int) for item in values
        ), "values has to be a int-list"
        self.previousNode = None
        self.positionInParent_nextNodesArray = (
            posInParentArray  # easier to get siblings
        )
        self.identifier = identifier  # unique identifier
        self.values = values  # e.g. Int-Array
        self.valuesCountInNode = valuesCountInNode
        self.nextNodes = [None] * (
            valuesCountInNode + 1
        )  # all children are firstly None


class BTree:
    def __init__(self, M):
        self.valuesCountInNode = M
        self.halffull = M // 2 + (M % 2)
        self.graph = Digraph(
            "btree",
            comment="dot",
            node_attr={
                "shape": "record",
                "height": ".05",
                "fontsize": "10",
                "style": "filled",
                "fillcolor": "#FFFFFF",
            },
            graph_attr={"splines": "line", "label": "M = " + str(M)},
        )

        # all the node that were added
        self.nodeArray = []
        # if someone insert a node with an id
        #  that was already inserted -> throw an error
        self.identifierArray = []

    # if you used myBBaum.graph.render(filename='graph.dot')
    #  graphiz will save tree in dot-file format
    @staticmethod
    def loadFromDotFile(filepath):
        graphFile = open(filepath, "r")

        # following line is to get M value
        #  graph [label="M = 4" splines=line]
        M_value = graphFile.read().split('"', 2)[1].split(" ")[-1]
        newBtree = BTree(int(M_value))

        graphFile = open(filepath, "r")
        # add nodes to newBtree
        for line in graphFile:
            # print("line:",line)
            if '[label="<' in line:
                # is a node
                # we only need to split once because line looks like:
                #   0 [label="<f1> |18|<f2> |40|<f3> |63|<f4> |85|<f5> "]
                #   ^nodeName
                nodeName = line.split(" ", 1)[0]
                # delte all invisible characters
                nodeName = "".join(c for c in nodeName if c.isprintable())
                valuesString = line.split("|")
                values = []
                for eventualVal in valuesString:
                    if eventualVal.isdigit():
                        values.append(int(eventualVal))

                newBtree.add_node(nodeName, values)

            elif ":" in line and "->" in line:
                # is an edge
                # strange code therefore look at the dotGraph source code
                #   0:f1 -> 1
                #   ^nodeName
                #   0:f1 -> 1
                # childNode ^
                #   0:f1 -> 1
                #      ^ atParentsPoint
                splitDot = line.split(":", 1)
                parentNode = splitDot[0]
                # delete all invisible characters
                parentNode = "".join(c for c in parentNode if c.isprintable())
                # print("parentNode:",parentNode)
                childNode = line.split(" ")[-1]
                # delte all invisible characters
                childNode = "".join(c for c in childNode if c.isprintable())
                # print("childNode:", childNode)
                # [1:] delte the first character which is a 'f'
                atParentsPoint = int(splitDot[1].split(" ", 1)[0][1:])

                # print("atParentsPoint:", atParentsPoint)

                newBtree.add_edge(parentNode, childNode, atParentsPoint)

        return newBtree

    # this method takes the node-datastructure form
    #  the old tree and build a new tree based on this
    #  node-datastructure
    @staticmethod
    def updateGraph(oldBtree):
        newTree = BTree(oldBtree.valuesCountInNode)
        # add nodes
        for node in oldBtree.nodeArray:
            newTree.add_node(node.identifier, node.values)
            curNode = newTree.getNode(node.identifier)
            # ugly bufix workaround
            curNode.nextNodes = [None] * len(node.nextNodes)

        # add edges
        for node in oldBtree.nodeArray:
            for i, child in enumerate(node.nextNodes):
                if child != None:
                    # print("length of node",len(node.nextNodes))
                    newTree.add_edge(node.identifier, child.identifier, i + 1)

        return newTree

    def add_node(self, name, elements):
        i = 1
        res_str = "<f" + str(i) + "> "

        for x in elements:
            if not isinstance(x, int):
                print(str(x) + " should be an integer.")

            i = i + 1
            append_str = "|" + str(x) + "|<f" + str(i) + "> "
            res_str = res_str + append_str

        self.graph.node(name, nohtml(res_str))

        if len(self.identifierArray) == 0:
            # root node
            self.nodeArray = [Node(name, elements, self.valuesCountInNode)]
            self.identifierArray.append(name)
        elif name in self.identifierArray:
            assert False, "Bitte nutze einen anderen Name für diese Node."
        else:
            self.nodeArray.append(Node(name, elements, self.valuesCountInNode))
            self.identifierArray.append(name)

    def add_edge(self, parent, child, n_child):
        self.graph.edge(parent + ":f" + str(n_child), child)

        # search both nodes and add their relations
        parentNode = self.getNode(parent)
        childNode = self.getNode(child)

        assert (
            parentNode != None and childNode != None
        ), "internal bug: could not find parent or child node in nodeArray."

        # add in previous or next node array
        childNode.previousNode = parentNode

        isNotInNextArray = (
            next(
                (
                    x
                    for x in parentNode.nextNodes
                    if x != None and childNode.identifier == x.identifier
                ),
                None,
            )
            == None
        )
        if isNotInNextArray:
            # index of the node in nextnodes determindes how the tree locks like
            # print("parent:",parent,"child:",child,"n_child:",n_child)
            if n_child - 1 >= len(parentNode.nextNodes):
                parentNode.nextNodes.insert(n_child - 1, childNode)
            else:
                parentNode.nextNodes[n_child - 1] = childNode
            childNode.positionInParent_nextNodesArray = n_child - 1

    def getNode(self, nodeID):
        return next((x for x in self.nodeArray if x.identifier == nodeID), None)

    def getRootNode(self):
        # if there are two rootNodes return None
        rootNodes = []
        for node in self.nodeArray:
            if node.previousNode == None:
                rootNodes.append(node)
        if len(rootNodes) != 1:
            return None
        return rootNodes[0]

    def delteNode(self, nodeID):
        node = next((x for x in self.nodeArray if nodeID == x.identifier), None)
        if not nodeID in self.identifierArray or node == None:
            warnings.warn("Node ID: " + nodeID + " does not exist.")
            return

        # delte from own datastructure
        self.identifierArray.remove(nodeID)
        for i, tmpNode in enumerate(self.nodeArray):
            if tmpNode.identifier == nodeID:
                self.nodeArray.pop(i)
                continue
            # delte if node was parent
            if (
                tmpNode.previousNode != None
                and tmpNode.previousNode.identifier == nodeID
            ):
                tmpNode.previousNode = None
            # delete if node is next node
            for i, child in enumerate(tmpNode.nextNodes):
                if child != None and child.identifier == nodeID:
                    tmpNode.nextNodes[i] = None

        # delete from graphviz data structure
        #  easy trick: just create the newTree we are having NOW
        #  and set it to self
        # self = BTree.updateGraph(self)
        # IMPORTANT but do it in upper function call

    def valueIsInBbaum(self, value):
        for node in self.nodeArray:
            if value in node.values:
                return True
        return False

    @staticmethod
    def isLeafNode(node):
        return node.nextNodes.count(None) == len(node.nextNodes)

    @staticmethod
    def getSibling(currentNode, bool_getLeft):
        if currentNode.previousNode == None:
            return None

        # save in variable because I chose a too long name
        indexNextNodes = currentNode.positionInParent_nextNodesArray

        if indexNextNodes == None:
            # should ... never be the case...
            warnings.warn("WARNING: positionInParent_nextNodesArray is None!")
            return None

        if bool_getLeft:
            if indexNextNodes == 0:
                return None

            return currentNode.previousNode.nextNodes[indexNextNodes - 1]
        else:
            if indexNextNodes == len(currentNode.previousNode.nextNodes) - 1:
                return None

            return currentNode.previousNode.nextNodes[indexNextNodes + 1]

    # its easier for students if they can easily copy the generate graph text
    # in order to make the exercsie
    @staticmethod
    def generateCopyText(node, text, treeName):
        if node == None:
            return ""
        tmpText = (
            treeName
            + ".add_node('"
            + str(node.identifier)
            + "', "
            + str(node.values)
            + ")\n"
        )
        for i, child in enumerate(node.nextNodes):
            if child != None:
                tmpText += BTree.generateCopyText(child, text, treeName)
                tmpText += (
                    treeName
                    + ".add_edge('"
                    + node.identifier
                    + "', '"
                    + child.identifier
                    + "', "
                    + str(i + 1)
                    + ")\n"
                )
        return text + tmpText

    def draw(self):
        display(self.graph)
