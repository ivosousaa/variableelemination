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

    # CHECK FACTOR SIZES

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
            # in no childre we have to just remove it and remove it from it's parents parents atrib
            if len(node.children) == 0:
                for p in node.parents:
                    p_index = nodes.index(p)
                    c_index = nodes[p_index].children.index(node)
                    del nodes[p_index].children[c_index]
                del nodes[i]
                return nodes
            
            if len(node.children) == 1:
                # probabilidade marginal do no a remover
                marg_yes = node.marginal[('yes',)]
                marg_no = node.marginal[('no',)]
                print marg_yes,marg_no
                new_yes = 0
                new_no = 0
                for c in node.children:
                    ve_index = c.parents.index(node)
                    if len(c.parents) == 1:
                        for key,val in c.dist.items():
                            if key[1][ve_index] == 'yes':
                                new_yes += val[0] * marg_yes
                                new_no += val[1] * marg_yes
                            else:
                                new_yes += val[0] * marg_no
                                new_no += val[1] * marg_no
                        print new_yes,new_no
                        for key,value in c.dist.items():
                            #print 'aa:',len(key[1])
                            if(len(key[1])):
                                print 'empty'
                            print 'k',key,'len'
                            #del key[1][0]
                            #print 'k2',key
                        print 'cdist',c.dist
                    else:
                        for key,value in c.dist.items():
                            print 'k',key
                        print 'cdist',c.dist
                                            
                    # ja temos novos valores, falta atualizar dists, e nao seria preciso atualizar filhos? not sure
                    #remove-se o parent dos parents
                    del c.parents[ve_index]
        #remover no da lista de nos
            del nodes[i]
            return nodes
        '''
        for p in c.parents:
            if(p.name == var_elim):
                print('child',p.name)
        '''
                    #if var_elim in child.parents:
                    #    print('ui')
                    #    ve_index = child.parents.index(var_elim)
                    #    print (ve_index)
#def calc
def singleVarElim(nodes, var, newFactor):
    # 2 cases, when it has parents when it doesn't, and maybe also when no children
    # let's start with the easier
    # when it has parents need to create a factor to substitute it, else just make a new table for the children, 
    # but this is allways needed
    for i,node in enumerate(nodes):
        if node.name == var:
            var_node = node
            if ( len(var_node.children) > 0 ):
                marg_probs = []
                print var_node.dist
                # here when the var doens't have marginal prob we calculate by doing the median of the 
                # values of the states for that vars parents (tablesize) 
                for i in range(0,var_node.numStates):
                    marg_probs.append(0)
                    for key,val in var_node.dist.items():
                        marg_probs[i] += val[i] 
                    for p in var_node.parents:
                        marg_probs[i] /= p.numStates     
                print var_node.name, marg_probs
                
                for c in var_node.children:
                    nodes[nodes.index(c)].dist = calcNewDist(c,var_node,marg_probs)
                    # falta apagar pai da lista de pais
                
def calcNewDist(c, p, mp):
    newDist = {}
    p_index = c.parents.index(p)
    if len(c.parents) == 1:
        new_vals = [0]*c.numStates
        for key,val in c.dist.items():
            p_state_index = p.getStates().index(key[1][p_index])
            for i in range(0,c.numStates):
                new_vals[i] += val[i] * mp[p_state_index]
        #print c.name,new_vals
        newDist[c.getStates()] = tuple(new_vals)
        print newDist
        return newDist
    else:
        new_keys = []
        total_vals = []
        for key,val in c.dist.items():
            new_vals = [0]*c.numStates
            p_state_index = p.getStates().index(key[1][p_index])
            for i in range(0,c.numStates):
                new_vals[i] += val[i] * mp[p_state_index]
                
            for i,k in enumerate(key[1]):
                #print k
                if i != p_index:
                    new_keys.append(k)
            total_vals.append(new_vals)
        #entries_size = 1
        #    print key,val,new_vals
        #print new_keys, total_vals
        
        '''valueToGroup = 0
        for i,k in enumerate(new_keys):
            if k == new_keys[0] and i != 0:
                valueToGroup = i + 1
        '''
        #print 'nks', new_keys
        #print 'nvls', total_vals
        checked_keys = []
        for i in range(0,len(new_keys)):
            if ( new_keys[i] not in checked_keys ):
                checked_keys.append(new_keys[i])
                final_sums = total_vals[i]
                for j in range(i+1,len(new_keys)):
                    if new_keys[i] == new_keys[j]:
                        final_sums[0] += total_vals[j][0]
                        final_sums[1] += total_vals[j][1]
                #print 'fs',final_sums
                newDist[c.getStates(),tuple([new_keys[i]])] = tuple(final_sums)
        print newDist
        
        '''for i in range(0,valueToGroup):
            new_sum = [total_vals[i]]    
            #new_sum.append()
            j = i + valueToGroup
            while ( j < len(new_keys) ):
                new_sum[0][0] += total_vals[j][0]     
                new_sum[0][1] += total_vals[j][1]
                j += valueToGroup'''
            #print 'nk',tuple(c.getStates()) +,tuple([new_keys[i]]))
            #print 'aiii',new_keys[i]
            
            #newDist[c.getStates(),tuple([new_keys[i]])] = tuple(new_sum[0])
            
            #print 'nova',newDist
            #newDist[] = tuple(new_sum)

        '''for p in c.parents:
            entries_size *= p.numStates
        final_vals = []*entries_size
        for i in range(0,entries_size):
            j = 0
            while(j < len(total_vals)):
                j = 999999999
            #newDist[c.getStates()] = tuple(new_vals)
        #print c.name,new_vals
        '''
        
   
def getFactorsWithVar(nodes,var):
    varsWithFactors = []
    for node in nodes:
        for c in node.children:
            if( c.name == var):
                varsWithFactors.append(node.name)
        for p in node.parents:
            if (p.name == var):
                varsWithFactors.append(node.name)
    return varsWithFactors

def main():
    # get target from input
    target = ''
    nodes = parse('cancer.bif')
    #bp.printNodes(nodes)
    # select var to elim using X algo
    
    var = 'Pollution'
    factorsToElim = getFactorsWithVar(nodes,var)
    singleVarElim(nodes, var, factorsToElim)
    
    #print factorsToElim
    #nodes = eliminateVariable(nodes,'asia')
    #bp.printNodes(nodes)
    
    
main()