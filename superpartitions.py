###
#
#  Class pour les superpartitions
#  Version 1 (OBF, mardi 12 juillet 2016)
#
#  To do:  - Introduction crap...
#          - Test with Maple Symmetric+
#          - N=2 ??
#
# ----
#  A superpartition \La is a pair of two partitions \la, \mu, s.t.
#
#    \La = (\la ; \mu) = (\La^a ; \La^s)
#
#      \la, is a stricly decreasing partition (the part zero is allowed)
#      \mu, is weakly decreasing partition
#
#  The superparition \La has also another (useful) representation.  Let
#   \La^\star: remove semi-colon of \La and order the parts in weakly decreasing
#              order (ignore  the zero is one).
#   \La^\circlestar: add 1 to every parts of \la, remove the semi-colon and order
#                    in weakly decreasing order.
#
#   Then, equivalently \La  <->  \La^\star, \La^\circlestar
#   Inversely, \La is defined from two regular partitions \la, \mu s.t.
#
#    \la \incl \mu   and    \mu/\la is a skew diagram horizontal and vertical.
#   So that \La^\star = \la, \La^\circlestar = \mu
#
#
#  We will use the notation
#  \La = [ [\La^a],  [\La^s]]
#  when entring superpartitions into sagemath.
#
###

from sage.combinat.partition import Partition


def pparts_to_spart(la, mu):
    # Convert 2 partitions la \incl mu into a superpartition
    # (see above)
    # return false if not a valid superpatition
    '''
    Example ::  La = SPartition([[5,2,1,0],[3,3,3,3,2,1]])
    pparts_to_spart(La.star(), La.cstar()) must gives La back
    sage: pparts_to_spart([3,2,1], [2,1,1,1,1,1,1])
    '''
    if (len(la) == len(mu)) or (len(la) == len(mu)-1):
        LaA=list([])
        LaS=list([])
        for i in range(len(la)):
            if la[i] == mu[i]:
                LaS = LaS + [la[i]]
            elif la[i] == mu[i]-1:
                if (la[i] in LaA):
                    return None
                else:
                    LaA = LaA + [la[i]]
            else:
                return None
    else:
        return None
    if (len(la) == len(mu)-1):
        if mu[len(la)] == 1:
            LaA = LaA + [0]
        else:
            return None
    return SPartition([LaA,LaS])





class SPartition(object): #, Partition
    '''Class for superparitions. Merci beaucoup / Thank you.
        Superpartitions are in the form
        La = [[La^a],[La^s]] where La^a has no repeated parts and
        can have a zero part, and La^s is a regular partition with no
        zero parts
    '''
    def __init__(self, args):
        '''
        sage: Lambda = SPartition([[4,3,1,0],[2,2,2,2,1]]); Lambda
        (4,3,1,0;2,2,2,2,1)
        '''
        self.args = list(args)
        self.Asym = list(args[0])
        self.Sym = list(args[1])
#        Partition.__init__()



    def __repr__(self):
        return '('+','.join(str(x) for x in self.Asym)+';'+','.join(str(x) for x in self.Sym)+')'


    def star(self):
        '''
        Return the partition from the operation La^* for a superpartition La
        '''
        return Partition(sorted(flatten(self.args), reverse=true))


    def cstar(self):
        '''
        Return the partition from the operation La^\circlestar for a superpartition La
        '''
        L1A=[x+1 for x in self.Asym]+self.Sym
        return Partition(sorted(flatten(L1A), reverse=true))


    #Comparaison logique___
    def __eq__(self, other):
        return (self.star() == other.star()) and (self.cstar() == other.cstar())


    def __ge__(self, other):
        return ( (Partition(self.star()) >= Partition(other.star())) and
                (Partition(self.cstar()) >= Partition(other.cstar())))
    def __le__(self, other):
        return (other >= self)

    def __gt__(self, other):
        return (self >= other) and (self != other)

    #Dominates___
    def dominates(self,other):
        return (self >=other)

    def dominated_spartitions(self):
        # La >= Om  iff La^* >= Om^* and La^\cstar>=Om^\cstar
        '''
        sage: La = SPartition([[3,2],[2]])
        sage: La.dominated_spartitions()
        [(3,2;2),
        (3,0;2,2),
        (2,0;3,2),
        (3,2;1,1),
        (3,1;2,1),
        (3,0;2,1,1),
        (2,1;3,1),
        (2,0;3,1,1),
        (1,0;3,2,1),
        (3,1;1,1,1),
        (3,0;1,1,1,1),
        (1,0;3,1,1,1),
        (2,1;2,2),
        (2,0;2,2,1),
        (1,0;2,2,2),
        (2,1;2,1,1),
        (2,0;2,1,1,1),
        (1,0;2,2,1,1),
        (2,1;1,1,1,1),
        (2,0;1,1,1,1,1),
        (1,0;2,1,1,1,1),
        (1,0;1,1,1,1,1,1)]
        '''
        ldo = list([])
        lOms = (Partition(self.star())).dominated_partitions()
        lOmc = (Partition(self.cstar())).dominated_partitions()

        for i in lOms:
            for j in lOmc:
                La = pparts_to_spart(i, j)
                if  La is not None:
                    ldo = ldo + [ La ]
        return ldo

    #Transpose/conjuguate__
    def conjuguate(self):
        return pparts_to_spart((self.star()).conjugate(), (self.cstar()).conjugate())


    def sdiagram(self):
        '''
        sage: La = SPartition([[4,3,1],[2,2,2,1,1]])
        sage: La.sdiagram()
        [][][][]()
        [][][]()
        [][]
        [][]
        [][]
        []()
        []
        []
        '''
        sdia = str()
        LaAA = self.Asym
        for x in self.star():
            if x in LaAA:
                LaAA.remove(x)
                sdia = sdia + '[]'*x + '()' + '\n'
            else:
                sdia = sdia + '[]'*x + '\n'
        if LaAA == [0]:
            sdia = sdia + '()' + '\n'
        print(sdia)

#   def __iter__(self):







# to do:
#        - iteration sur les boites de La
#        - qtes combinatoires ?






















## Fin du fichier.
