# consulted code from Stack Overflow https://stackoverflow.com/questions/51328609/python-dictionary-comprehension-filtering
def dict_filter(func, dct):
    return ({item:dct[item] for (item, dct[item]) in dct.items() if func(item, dct[item])})

class KVTree:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
    
    def __str__(self):
        print('(%s, %s)' % (self.key, self.value))

def treemap(func, tree):
    tree.key, tree.value = func(tree.key, tree.value)
    for child in tree.children:
        treemap(func, child)
        
func = lambda x, y: (x.upper(), y * 1000000)
        
class DTree():
    def __init__(self, variable, threshold, lessequal, greater, outcome):
        s1 = [variable == None, threshold == None, lessequal == None, greater == None]
        if not ((True not in s1) ^ (outcome is not None)):
            raise ValueError('Inputs are not valid.')
        
        self.variable = variable
        self.threshold = threshold
        self.lessequal = lessequal
        self.greater = greater
        self.outcome = outcome
        
        # helpful for later
        self.options = list(set(self.helper_tuple([])))
        
    def helper_tuple(self, decision_options):
        if isinstance(self.variable, int):
            decision_options.append(self.variable)
        if isinstance(self.lessequal, DTree):
            self.lessequal.helper_tuple(decision_options)
        if isinstance(self.greater, DTree):
            self.greater.helper_tuple(decision_options)
        return decision_options
    
    def tuple_atleast(self):
        if self.options != []:
            return max(self.options) + 1
        return 0

    def find_outcome(self, tup, counter = 0):
        if self.outcome is not None:
            return self.outcome
        counter += 1
        if counter - 1 in self.options:
            if tup[0] <= self.threshold:
                return self.lessequal.find_outcome(tup[1:], counter)
            return self.greater.find_outcome(tup[1:], counter)
        return self.find_outcome(tup[1:], counter)

    def paths(self, v, parents = []):
        if self.variable is not None:
            parents.append(self.variable)
        if (isinstance(self.lessequal, DTree) and self.lessequal.variable in parents) or (isinstance(self.greater, DTree) and self.greater.variable in parents):
            v.append('F')
        if isinstance(self.lessequal, DTree):
            self.lessequal.paths(v)
        if isinstance(self.greater, DTree):
            self.greater.paths(v)
        parents.clear()
        return not 'F' in v

    def no_repeats(self):
        return self.paths([])
