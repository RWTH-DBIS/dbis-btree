from .BBaum import BTree
import numpy as np
from enum import Enum

class TreeTypes(Enum):
    INSERT = "INSERT"
    INSERT_TRIVIAL = "INSERT_TRIVIAL"
    DELETE_VERSCHMELZ = "DELETE_VERSCHMELZ"
    DELETE_AUSGLEICH = "DELETE_AUSGLEICH"
    DELETE_TRIVIAL = "DELETE_TRIVIAL"

class BTree_Creator:
    def __init__(self, height, maxValueInTree,
                 valuesCountInOneNode, treeType):
        self.height = height
        # values from 0 to maxValueInTree
        self.maxValueInTree = maxValueInTree
        # maxValuesInOneNode is the M value from the lecture
        self.valuesCountInOneNode = valuesCountInOneNode
        # because we dont want to build trivial trees
        # we disguingish between imserting and deleting trees
        self.treeType = treeType
        self.isInsertingTree = treeType == TreeTypes.INSERT
        # while correction we dont want an endless loop
        self.maxInterationsCorrection = 12
        # to ensure that not only NOT trival inserting or deleting exist
        #  counts how many leaf nodes will be skiped


        # just for safetiness check if tree is 100% correct
        treeIncorrect = True
        while self.maxInterationsCorrection > 0 and treeIncorrect:
            # HERE is btree instance
            self.delayForInsertDeleteLeaf = self.determineLeafForOperations()
            self.myBBaum = BTree(valuesCountInOneNode)
            print("creating tree...")
            self.buildTree([(0, None, 0, maxValueInTree, 0)])
            print("done.")
            print("checking if tree is correct...")
            rootNode = next((x for x in self.myBBaum.nodeArray
                             if x.previousNode == None), None)
            treeIncorrect = BTree_Creator\
                            .treeIncorrect(self.myBBaum, rootNode,self.valuesCountInOneNode)
            if not treeIncorrect:
                print("done.")
            else:
                print("not correct.")
            self.maxInterationsCorrection -= 1
        assert self.maxInterationsCorrection > 0, "Please restart program."


    # which note should be the note for non-trivial deleting and inserting
    def determineLeafForOperations(self):
        randomIndex = 0
        if self.valuesCountInOneNode > 1:
            randomIndex = int(np.random
                          .random_integers(low=0,
                                           high=self.valuesCountInOneNode-1))
        return randomIndex



    # ---------------- check if tree is correct ----------------
    @staticmethod
    def treeIncorrect(bbaum,parentNode,valuesCountInOneNode):
        if parentNode.nextNodes == [None] * (valuesCountInOneNode + 1):
            return False
        elif parentNode.nextNodes.count(None) != 0:
            #"Tree has to be full! every inner node has to have a child"
            return True
        # one of the children is not None
        isIncorrect = False
        for i, child in enumerate(parentNode.nextNodes):
            if i < len(parentNode.values):
                # because last one has to be compered differently
                if child != None:
                    # all values has to be smaller
                    if child.values[-1] >= parentNode.values[i]:
                        # last is bigger -> btree property hurted
                        print("Tree is incorrect.")
                        print("at nodeNumber:", i, "parentValues:",
                              parentNode.values, "childValues:",
                              child.values)
                        return True
                    else:
                        return isIncorrect or BTree_Creator.treeIncorrect(bbaum,child,valuesCountInOneNode)
            else:
                # now check if its bigger...
                if child != None:
                    if child.values[0] < parentNode.values[i - 1]:
                        # last is smaller -> btree property hurted
                        print("Tree is incorrect.")
                        print("at nodeNumber:", i, "parentValues:",
                              parentNode.values, "childValues:",
                              child.values)
                        return True
                    else:
                        return isIncorrect or BTree_Creator.treeIncorrect(bbaum,child)

        return isIncorrect

    # build recusivly use level order because of naming the nodes
    # min and max value determine how which values will be coveres and this
    # node and its decand
    # nodename is a number
    # parentNode for connecting
    def buildTree(self, stackForRecursion):

        # here is somehow a bug maybe not everything get loaded
        # if stack is NOT empty
        if len(stackForRecursion) == 0:
            return

        (nodeName, parentNode, minValue, maxValue,
         currentHeight) = stackForRecursion.pop(0)

        if currentHeight > self.height:
            return

        isLeftChild = True

        if parentNode != None:
            isLeftChild = maxValue <= parentNode

        values = self.createValueArray(minValue, maxValue,
                                       isLeftChild, currentHeight)

        if values == None:
            return

        # print("Nodename:",nodeName, self.getNodeName(nodeName))
        self.myBBaum.add_node(BTree_Creator.getNodeName(nodeName), values)

        if parentNode != None:
            thisNodeIsChildNumber = (nodeName % (self.valuesCountInOneNode + 1))
            if thisNodeIsChildNumber == 0:
                thisNodeIsChildNumber = self.valuesCountInOneNode + 1
            # print("add edge from:",parentNode, "to", nodeName,
            #       "N:",thisNodeIsChildNumber)

            self.myBBaum.add_edge(BTree_Creator.getNodeName(parentNode),
                                  BTree_Creator.getNodeName(nodeName),
                                  thisNodeIsChildNumber)

        # :) calculate the nodeposition in btree
        nextNodeName = nodeName * (self.valuesCountInOneNode + 1)

        borders = values.copy()
        borders.append(maxValue)
        borders.insert(0, minValue)

        for i in range(1, len(borders)):
            previousIntervallBorder = borders[i - 1]
            nextIntervallBorder = borders[i]
            nextNodeName += 1
            # print("added next node:",nextNodeName, self.getNodeName(nextNodeName))
            nodeTupel = (nextNodeName, nodeName,
                         previousIntervallBorder,
                         nextIntervallBorder, currentHeight + 1)

            stackForRecursion.append(nodeTupel)

        # rekursiv call
        for _ in range(0, self.valuesCountInOneNode + 1):
            self.buildTree(stackForRecursion)

    # ---------------- create values in one node ----------------
    def createValueArray(self, minVal, maxVal, isLeftChild,
                         currentHeight):

        distance = maxVal - minVal

        if distance == 1:
            if isLeftChild:
                return [minVal] * self.valuesCountInOneNode
            else:
                return [maxVal] * self.valuesCountInOneNode
        if distance <= 0:
            return None

        stepSize = distance // (self.valuesCountInOneNode)

        values = []
        curMin = minVal + 1
        curMax = curMin - 1 + stepSize

        fillSizeOfNodes = self.determineFillSize(currentHeight)

        for i in range(0, fillSizeOfNodes):
            low = curMin + (stepSize // 6)
            high = curMax - (stepSize // 6)
            if low >= high:
                low = curMin
                high = curMax
                if low >= high:
                    return None
                    #raise WrongInputVariables(
                        #"Die range für diesen Unterknoten besteht nur aus einer Zahl. Wir möchten diese Bäume vermeiden.\n 1. run script again\n 2. Bitte starte Script erneut mit anderen Height- und/oder maxValue-Werten.")

            newValue = int(np.random
                           .random_integers(low=low,
                                            high=high))
            if i > 0 and newValue < values[i - 1]:
                # now every value is sorted!
                newValue = values[i - 1]

            values.append(newValue)

            curMin = curMax
            curMax = curMin + stepSize

        return values

    def determineFillSize(self,currentHeight):
        fillSizeOfNodes = int(np.random
                              .random_integers(low=self.myBBaum.halffull,
                                               high=self.valuesCountInOneNode))
        if currentHeight == self.height:
            # we want neither one leaf full nor one leaf half full
            if self.isInsertingTree:
                if self.delayForInsertDeleteLeaf == 0:
                    if str(self.treeType) == str(TreeTypes.INSERT):
                        fillSizeOfNodes = self.valuesCountInOneNode
                    elif str(self.treeType) == str(TreeTypes.INSERT_TRIVIAL):
                        fillSizeOfNodes = self.valuesCountInOneNode - 1

            else:
                if self.treeType == TreeTypes.DELETE_TRIVIAL:
                    if self.delayForInsertDeleteLeaf == 0:
                        self.fillSizeOfNodes = self.valuesCountInOneNode
                else:
                    if self.delayForInsertDeleteLeaf == 1:
                        fillSizeOfNodes = self.myBBaum.halffull
                    elif self.delayForInsertDeleteLeaf == 0:
                        fillSizeOfNodes = self.myBBaum.halffull
                    elif self.delayForInsertDeleteLeaf == -1:
                        # second leaf half many +1 nodes -> ensures Ausgleich
                        # second leaf half many nodes -> ensures Verschmelzen
                        puls = 1
                        if str(self.treeType) == str(TreeTypes.DELETE_VERSCHMELZ):
                            plus = 0
                        fillSizeOfNodes = self.myBBaum.halffull + puls

            self.delayForInsertDeleteLeaf -= 1
        return fillSizeOfNodes

    # insert a number and it return the letter combination
    # for ex: 2=B,3=C,27=AA
    @staticmethod
    def getNodeName(num):
        numOfA_s = num // 26
        nodeName = ''
        for _ in range(0, numOfA_s):
            nodeName += 'A'

        return nodeName + str(chr((num % 26) + ord('A')))

    # insert a number and it return the letter combination
    # for ex: B=2,C=3,AA=27
    @staticmethod
    def convertNodeNameInNumber(name):
        number = -ord('A')
        for char in name:
            number += ord(char)

        return number