import numpy as np
from matplotlib.figure import Figure

class Orbital:
    '''
    represent the orbital, it is linked to many other orbitals
    '''
    def __init__(self,id,spin=1.,D=[],x=0.,y=0.,z=0.):
        self.id=id
        self.linkedOrb=[]
        self.linkStrength=[]
        self.spin=spin
        self.D=D
        self.inBlock=False

        #use to plot on screen
        self.x=x
        self.y=y
        self.z=z

        # mark for renormalization
        self.chosen=False
        self.orb_cluster=[]
        self.linkedOrb_rnorm=[]
        self.linkStrength_rnorm=[]
    
    def addLinking(self,targetOrb,strength):
        # check redundancy
        for orb in self.linkedOrb:
            if targetOrb.id==orb.id:
                print('Warning: redundant bonding between orb: %d and %d'%(self.id, orb.id))
                return
        self.linkedOrb.append(targetOrb)
        self.linkStrength.append(strength)
        #print(strength)
    
    def addLinking_rnorm(self,targetOrb,strength):
        for orb in self.linkedOrb_rnorm:
            if targetOrb.id==orb.id:
                print('Warning: redundant renormalizing bonding between orb: %d and %d'%(self.id, orb.id))
                return
        self.linkedOrb_rnorm.append(targetOrb)
        self.linkStrength_rnorm.append(strength)

    def classifyTheLinking(self,On=False):
        initialType=-1
        self.classStrength=[]
        self.linkedOrbType=[]
        for linkStrength in self.linkStrength:
            #print(linkStrength)
            findType=False
            for itype, StrengthType in enumerate(self.classStrength):
                condition=sum(abs(linkStrength-StrengthType)) if On else abs(linkStrength-StrengthType)
                if condition<0.0001:#abs(linkStrength-StrengthType).all()<0.0001:
                    self.linkedOrbType.append(itype)
                    findType=True
                    break
            if not findType:
                initialType+=1
                self.linkedOrbType.append(initialType)
                self.classStrength.append(linkStrength)
        self.totLinkingTypes=initialType+1

    def getCorrEnergy(self,corrList=[]):
        corr=0.
        for targetOrb, bondStrengh in zip(self.linkedOrb,self.linkStrength):
            excluded=True
            for corrOrb in corrList:
                if targetOrb.id==corrOrb.id:
                    excluded=False
                    break
            if excluded:
                continue
            corr+=self.spin*targetOrb.spin*bondStrengh
        return corr

    def getCorrEnergyDirect(self):
        corr=0.
        for targetOrb, bondStrengh in zip(self.linkedOrb,self.linkStrength):
            corr+=self.spin*targetOrb.spin*bondStrengh
        return corr
    
    def getCorrEnergyWithBlock(self):
        corr=0.
        for targetOrb, bondStrengh in zip(self.linkedOrb,self.linkStrength):
            if targetOrb.inBlock:
                corr+=self.spin*targetOrb.spin*bondStrengh
        return corr

    def addOrbIntoCluster(self,orb_trial):
        newOrb=True
        for orb in self.orb_cluster:
            if orb.id==orb_trial.id:
                newOrb=False
                break
        if newOrb:
            self.orb_cluster.append(orb_trial)
        return
    
class Bond:
    '''
    represent the bond
    '''
    def __init__(self,source,target,overLat,strength,strength1=0.,strength2=0.,On=False):
        self.source=source
        self.target=target
        self.overLat=overLat
        self.strength=strength

        self.On=On
        if On:
            self.strength=np.array([strength,strength1,strength2])
        #print('bond',strength,strength1,strength2,On,self.strength)
    
    def copy(self):
        bond=Bond(self.source,self.target,self.overLat,0,0,0,self.On)
        bond.strength=np.array(list(self.strength)) if self.On else self.strength
        return bond

def establishLattice(Lx=1,Ly=1,Lz=1,norb=1,Lmatrix=np.array([[1,0,0],[0,1,0],[0,0,1]]),bmatrix=[np.array([0.,0.,0.])],SpinList=[1],DList=[0.,0.,0.]):
    '''
    create a Lx X Ly X Lz lattice, and create norb orbitals
    for each cell
    '''
    # pre-checking if bmatrix is not consistent with norb
    if len(bmatrix)<norb:
        print('Error: when establish lattice list, we find there is no enough bshift for each orbital')
        exit()

    # now let us begin
    lattice_flatten=[]
    lattice=[]
    id=0
    for x in range(Lx):
        lattice_x=[]
        for y in range(Ly):
            lattice_y=[]
            for z in range(Lz):
                lattice_z=[]
                for o in range(norb):
                    pos=np.dot(np.array([x,y,z])+bmatrix[o],Lmatrix)
                    orbital=Orbital(id,spin=SpinList[o],D=DList[o],
                                    x=pos[0],y=pos[1],z=pos[2])
                    lattice_z.append(orbital)
                    lattice_flatten.append(orbital)
                    id+=1
                    if x%2+y%2+z%2==0: # mark 1/8 or 1/4 or half orb. for renormalization
                        orbital.chosen=True
                lattice_y.append(lattice_z)
            lattice_x.append(lattice_y)
        lattice.append(lattice_x)
    
    # construct orb cluster for renormalizations
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                for o in range(norb):
                    orbital=lattice[x][y][z][o]
                    if orbital.chosen: # 8 possible orbs to add, totally
                        orbital.addOrbIntoCluster(lattice[x][y][z][o])
                        orbital.addOrbIntoCluster(lattice[x][y][(z+1)%Lz][o])
                        orbital.addOrbIntoCluster(lattice[x][(y+1)%Ly][z][o])
                        orbital.addOrbIntoCluster(lattice[(x+1)%Lx][y][z][o])
                        orbital.addOrbIntoCluster(lattice[x][(y+1)%Ly][(z+1)%Lz][o])
                        orbital.addOrbIntoCluster(lattice[(x+1)%Lx][y][(z+1)%Lz][o])
                        orbital.addOrbIntoCluster(lattice[(x+1)%Lx][(y+1)%Ly][z][o])
                        orbital.addOrbIntoCluster(lattice[(x+1)%Lx][(y+1)%Ly][(z+1)%Lz][o])

    # check cluster
    '''print("checking orb cluster after building >>>>>>")
    for orb in lattice_flatten:
        if orb.chosen:
            print("orb%d is chosen, involving:"%orb.id)
            for sub_orb in orb.orb_cluster:
                print("    orb%d"%sub_orb.id)        
    print("<<<<<<")'''       
    return lattice, lattice_flatten

def establishLinking(lattice,bondList,ki_s=0,ki_t=0,ki_overLat=[0,0,0]):
    Lx=len(lattice)
    Ly=len(lattice[0])
    Lz=len(lattice[0][0])
    Lo=len(lattice[0][0][0])

    correlatedOrbitalPair=[]
    # uncode every orbitals
    On=False
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                for o in range(Lo):
                    # start linking type1: normal bond
                    sourceOrb=lattice[x][y][z][o]
                    for bond in bondList:
                        if o==bond.source:
                            targetOrb=lattice[(x+bond.overLat[0])%Lx][(y+bond.overLat[1])%Ly][(z+bond.overLat[2])%Lz][bond.target]
                            sourceOrb.addLinking(targetOrb,bond.strength)
                            if sourceOrb.id!=targetOrb.id:
                                targetOrb.addLinking(sourceOrb,bond.strength)
                    # type2: bond in renormalized system
                    
                    if sourceOrb.chosen:
                        for bond in bondList:
                            if o==bond.source:
                                targetOrb=lattice[(x+bond.overLat[0]*2)%Lx][(y+bond.overLat[1]*2)%Ly][(z+bond.overLat[2]*2)%Lz][bond.target]
                                sourceOrb.addLinking_rnorm(targetOrb,bond.strength)
                                if sourceOrb.id!=targetOrb.id:
                                    targetOrb.addLinking_rnorm(sourceOrb,bond.strength)
                # save the correlated orbital pairs
                correlatedOrbitalPair.append([lattice[x][y][z][ki_s].id, lattice[(x+ki_overLat[0])%Lx][(y+ki_overLat[1])%Ly][(z+ki_overLat[2])%Lz][ki_t].id])
    # after process
    '''
    On=bondList[0].On
    for x in range(Lx):
        for y in range(Ly):
            for z in range(Lz):
                for o in range(Lo):
                    lattice[x][y][z][o].classifyTheLinking(On=On)
    '''
    return correlatedOrbitalPair

def plotLattice(lattice):
    '''
    uncode the lattice pack and print each orbital on screen
    '''
    f=Figure()
    ax=f.add_subplot(111)
    for x in lattice:
        for y in x:
            for z in y:
                for o in z:
                    ax.scatter(o.x,o.y,color='blue')
                    ax.annotate(o.id,(o.x,o.y),size=10.5)
                    for target in o.linkedSite:
                        ax.plot([o.x,target.x],[o.y,target.y],color='red')
    f.show()

