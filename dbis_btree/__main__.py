from .BBaum_Creator import BTree_Creator
from .BBaum_Creator import WrongInputVariables
import sys

height = 1
maxValueInTree = 100
valuesCountInOneNode = 4
isInsertionTree = True

def checkInput():
    global height
    global maxValueInTree
    global valuesCountInOneNode
    global isInsertionTree

    if len(sys.argv) > 1:
        if (len(sys.argv) - 1) % 2 != 0:
            return 1

        flagsCount = (len(sys.argv) - 1) // 2

        if '-h' in sys.argv:
            index = sys.argv.index('-h')
            height = int(sys.argv[index + 1])
            flagsCount -= 1
        elif '--height' in sys.argv:
            index = sys.argv.index('--height')
            height = int(sys.argv[index + 1])
            flagsCount -= 1

        if '--valueRange' in sys.argv:
            index = sys.argv.index('--valueRange')
            maxValueInTree = int(sys.argv[index + 1])
            flagsCount -= 1
        elif '-v' in sys.argv:
            index = sys.argv.index('-v')
            maxValueInTree = int(sys.argv[index + 1])
            flagsCount -= 1

        if '--countValuesInOneNode' in sys.argv:
            index = sys.argv.index('--countValuesInOneNode')
            valuesCountInOneNode = int(sys.argv[index + 1])
            flagsCount -= 1
        elif '-c' in sys.argv:
            index = sys.argv.index('-c')
            valuesCountInOneNode = int(sys.argv[index + 1])
            flagsCount -= 1

        if '-t' in sys.argv:
            index = sys.argv.index('-t')
            height = bool(sys.argv[index + 1])
            flagsCount -= 1
        elif '--isInsertingTree' in sys.argv:
            index = sys.argv.index('--isInsertingTree')
            height = bool(sys.argv[index + 1])
            flagsCount -= 1

        if flagsCount != 0:
            return 1

    return 0

def main():
    # standart values
    global height
    global maxValueInTree
    global valuesCountInOneNode
    global isInsertionTree

    errorCode = checkInput()

    if errorCode != 0:
        return 1

    tree = BTree_Creator(height, maxValueInTree,
                         valuesCountInOneNode,
                         isInsertionTree)
    
    tree.myBBaum.graph.save()
    tree.myBBaum.graph.render(filename='graph', view=True, cleanup=1)

    return 0

if __name__ == "__main__":
    errorCode = main()
    if errorCode == 1:
        print("usages: python3 -m dbis-bbaum [-flag value]")
        print("flags:")
        print("--height | -h [interger >= 0]   for example:  --height 2")
        print("--valueRange | -v [interger > 0]   for example:  --valueRange 100")
        print("--countValuesInOneNode | -c [interger > 0]   for example:  --countValuesInOneNode 4")
        print("--isInsertingTree | -t [Boolean]   for example:  --isInsertingTree True")



