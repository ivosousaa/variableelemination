import bifParser as bp
import Node

def parse(file):
    file = open(file)
    BIF = file.readlines()
    BIF = bp.fixWhiteSpace(BIF)

    nodes = bp.parseBIF(BIF)

    return nodes

#def removeVariables():
def selectCandidate(nodes,target):
    childrenSizes = []
    parentSizes = []
    minChildren = float('inf')
    minParents = float('inf')

    for i,node in enumerate(nodes):
        if(node.name != target):
            if(len(node.children) == 0):
                return i
            
            childrenSizes.append(len(node.children))
            parentSizes.append(len(node.children))
            if(len(node.children) < minChildren):
                minChildren = len(node.children)
            if(len(node.parents) < minParents):
                minParents = len(node.parents)
        else: 
            childrenSizes.append(-1)
            parentSizes.append(-1)

    else: print('te logo')
    return -1

def main():
    # get target from input
    target = ''
    nodes = parse('asia.bif')
    index_rm = selectCandidate(nodes,target)
    print('index node to rm: ', nodes[index_rm].name)
    
main()