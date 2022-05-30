from .BBaum_Creator import BTree_Creator
from .BBaum_Creator import TreeTypes
from .BBaum import BTree
import numpy as np
import random
import warnings

class BTree_Ex_Generator:

    pathToValues = "values.txt"
    pathToGraph = "graph.dot"

    def __init__(self, operationCount, treeType, bbaum=None,
                        values=None, # <- this values do not have a correction checkt!
                        M=4,height=1,numbersUntil=100):

        self.treeType = treeType
        # create insert tree
        if bbaum == None:
            self.bbaum = \
                BTree_Creator(height, numbersUntil, M, treeType).myBBaum
        else:
            self.bbaum = bbaum

        self.operationsAndSol = [] #array of the class BTree_OneOp
        self.howManyOperations = self.checkOperationCount(operationCount,treeType==TreeTypes.INSERT)
        #init both arrays: deleteOperationsAndSol and insertOperationsAndSol

        self.generateOperationValues(values)

        self.copyPastTextForTree = BTree.generateCopyText(
                                    self.bbaum.getRootNode(),"","b")


    def saveArrayToDisk(self,array,toPath):
        out = ""
        for i,elm in enumerate(array):
            out += str(elm)
            if i < len(array) - 1:
                out += " "

        f = open(toPath, "w")
        f.write(out)
        f.close()

    def readArrayFromDisk(self,fromPath):
        f = open(fromPath, "r")
        strArray = f.read().split(" ")
        return [int(x) for x in strArray]



    def generateOperationValues(self, values):

        if self.howManyOperations > 0:

            if values != None:
                #insertValues = self.readArrayFromDisk(pathtoValues)
                self.operationsAndSol = values
            else:

                leafNodes = [node for node in self.bbaum.nodeArray if
                             node.nextNodes.count(None) == len(node.nextNodes)]
                self.operationsAndSol = self.createOperationValues(leafNodes)
                #self.saveArrayToDisk( [x.operation for x in self.insertOperationsAndSol], self.pathToValues)

    def createOperationValues(self,leafNodes):
        tmpOperationValues = []

        allValuesOfTheTree = []
        for node in leafNodes:
            for value in node.values:
                allValuesOfTheTree.append(value)
        allValuesOfTheTree.sort()
        #print("type",str(self.treeType)==str(TreeTypes.INSERT_TRIVIAL))
        if str(self.treeType) == str(TreeTypes.INSERT) \
            or str(self.treeType) == str(TreeTypes.INSERT_TRIVIAL):
            if str(self.treeType) == str(TreeTypes.INSERT):
                    # first insertion is in a full leaf
                    fullLeaf = next((x for x in leafNodes if len(x.values) == self.bbaum.valuesCountInNode), None)
                    if fullLeaf != None:
                        value = int(np.random
                                    .random_integers(low=fullLeaf.values[0],
                                                     high=fullLeaf.values[-1]))
                        tmpOperationValues.append(value)
                        self.howManyOperations -= 1
                    else:
                        # no full leafNode in Tree
                        warnings.warn("Was not able to ask for insertion in full leaf.")
            else:
                #is trivial
                notFullLeaf = next((x for x in leafNodes if len(x.values) < self.bbaum.valuesCountInNode), None)
                if notFullLeaf != None:
                    value = int(np.random
                                .random_integers(low=notFullLeaf.values[0],
                                                 high=notFullLeaf.values[-1]))
                    tmpOperationValues.append(value)
                    self.howManyOperations -= 1
                else:
                    # no full leafNode in Tree
                    warnings.warn("Was not able to ask for insertion in a not full leaf.")
            # other can be random
            minVal = allValuesOfTheTree[0]
            maxVal = allValuesOfTheTree[-1]
            while self.howManyOperations > 0:
                value = int(np.random
                            .random_integers(low=minVal,
                                             high=maxVal))
                tmpOperationValues.append(value)
                self.howManyOperations -= 1

        elif str(self.treeType) == str(TreeTypes.DELETE_VERSCHMELZ)\
            or str(self.treeType) == str(TreeTypes.DELETE_AUSGLEICH)\
            or str(self.treeType) == str(TreeTypes.DELETE_TRIVIAL):
            print("delete")
            # ---------------  ensure augleich and verschmelzung  ---------------
            # tree is an deletion Tree
            #  search for ausgleich situation:
            #      none halffull halffull+1  or  halffull halffull halffull+1
            if not str(self.treeType) == str(TreeTypes.DELETE_TRIVIAL):
                (ausgleichLeaf,
                 verschmelzLeaf) = self.findAusgleichVerschmelzLeaf(leafNodes)

                for i, node in enumerate([ausgleichLeaf, verschmelzLeaf]):
                    if node == None:
                        if i == 0:
                            if str(self.treeType) == TreeTypes.DELETE_AUSGLEICH:
                                warnings.warn("Was not able to ensure ausgleich operation")
                                break
                        else:
                            if str(self.treeType) == TreeTypes.DELETE_VERSCHMELZ:
                                warnings.warn("Was not able to ensure verschmelz operation")
                                break
                        continue

                    if i >= len(node.values):
                        # the tree has just 1 value per node
                        warnings.warn("The tree has too less values in one node.")
                        break

                    if node != None and self.howManyOperations > 0:
                        index = int(np.random
                                    .random_integers(low=0,
                                                     high=len(node.values) - 1))
                        # this loop is important
                        stopInfinityLoop = 10
                        while not node.values[index] in allValuesOfTheTree \
                                and stopInfinityLoop > 0:
                            index = int(np.random
                                        .random_integers(low=0,
                                                         high=len(node.values) - 1))
                            stopInfinityLoop -= 1
                        if stopInfinityLoop == 0:
                            break

                        tmpOperationValues.append(node.values[index])

                        # delete from allValuesOfTheTree array
                        allValuesOfTheTree.remove(node.values[index])
                        self.howManyOperations -= 1
            else:
                #is trivial
                notHalfFullLeaf = next((x for x in leafNodes if len(x.values) > self.bbaum.halffull), None)
                if notHalfFullLeaf != None:
                    value = random.choice(notHalfFullLeaf.values)
                    tmpOperationValues.append(value)

                    # delete from allValuesOfTheTree array
                    allValuesOfTheTree.remove(value)
                    self.howManyOperations -= 1
                else:
                    # no full leafNode in Tree
                    warnings.warn("Was not able to ask for trivial deltion.")
            # ------------------------------------------------------------

            # other can be random
            while len(allValuesOfTheTree) > 0 and self.howManyOperations > 0:
                index = 0
                if len(allValuesOfTheTree) > 1:
                    index = int(np.random
                                .random_integers(low=0,
                                                 high=len(allValuesOfTheTree) - 1))
                tmpOperationValues.append(allValuesOfTheTree[index])
                # delete from allValuesOfTheTree array
                allValuesOfTheTree.pop(index)
                self.howManyOperations -= 1

        return tmpOperationValues


    #helper function for finding delting leaf
    def findAusgleichVerschmelzLeaf(self, leafNodes):
        ausgleichLeaf = None
        verschmelzLeaf = None
        for i, node in enumerate(leafNodes):
            leftSibling = BTree.getSibling(node, True)
            leftHalffull = True
            leftMoreThanHalffull = False
            if leftSibling != None:
                leftHalffull = len(leftSibling.values) == self.bbaum.halffull
                leftMoreThanHalffull = len(leftSibling.values) > self.bbaum.halffull

            rightSibling = BTree.getSibling(node, False)
            rightHalffull = True
            rightMoreThanHalffull = False
            if rightSibling != None:
                rightHalffull = len(rightSibling.values) == self.bbaum.halffull
                rightMoreThanHalffull = len(rightSibling.values) > self.bbaum.halffull

            if len(node.values) == self.bbaum.halffull:
                # first search for ausgleich
                if ausgleichLeaf == None and (leftMoreThanHalffull or rightMoreThanHalffull):
                    ausgleichLeaf = node
                if verschmelzLeaf == None and (leftHalffull and rightHalffull):
                    verschmelzLeaf = node
        return (ausgleichLeaf, verschmelzLeaf)




    #if there are less nodes than you want to delete than in the tree
    #  -> try to avoid that situation
    def checkOperationCount(self, operCount, isInsertingTree):
        if operCount <= 0:
            return 0
        if not isInsertingTree:
            leafNodes = [node for node in self.bbaum.nodeArray if node.nextNodes.count(None) == len(node.nextNodes)]
            countLeafNodeValues = 0
            for node in leafNodes:
                countLeafNodeValues += sum(x is not None for x in node.values)

            if operCount > countLeafNodeValues:
                return countLeafNodeValues
        return operCount


    def generateText(self):
        operations = [x for x in self.operationsAndSol]

        return str(self.treeType)+": "+str(operations)



