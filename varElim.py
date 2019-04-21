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

def eliminateVariable(nodes, var_elim):
    print('var to elim:', var_elim)
    for i,node in enumerate(nodes):
        if node.name == var_elim:
            if len(node.children) == 0:
                del node[i]
                return nodes
            if len(node.children) == 1:
                # probabilidade marginal do no a remover
                marg_yes = node.marginal[('yes',)]
                marg_no = node.marginal[('no',)]
                new_yes = 0
                new_no = 0
                for c in node.children:
                    ve_index = c.parents.index(node)
                    for key,val in c.dist.items():
                        if key[1][ve_index] == 'yes':
                            new_yes += val[0] * marg_yes
                        else:
                            new_no += val[1] * marg_no
                    print new_yes,new_no
                    # ja temos novos valores, falta atualizar dists, e nao seria preciso atualizar filhos? not sure
                    #remove-se o parent dos parents
                    del c.parents(ve_index)
        #remover no da lista de nos
        del nodes(i)
                    '''
                    for p in c.parents:
                        if(p.name == var_elim):
                            print('child',p.name)
                    '''
                    #if var_elim in child.parents:
                    #    print('ui')
                    #    ve_index = child.parents.index(var_elim)
                    #    print (ve_index)

def main():
    # get target from input
    target = ''
    nodes = parse('asia.bif')
    
    #bp.printNodes(nodes)
    
    eliminateVariable(nodes,'asia')

    #print(nodes[1].dist[('yes', 'no'),('yes',)])
    #print(nodes[1].dist[('yes', 'no'),('yes',)])

    #print(nodes[1].dist[('yes', 'no')])
    #print(nodes[1].dist[('yes', 'no'),('yes','yes')])

    #index_rm = selectCandidate(nodes,target)
    #print('index node to rm: ', nodes[index_rm].name)
    
main()