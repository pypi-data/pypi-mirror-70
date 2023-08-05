from tkinter import Label, LabelFrame, Frame, Spinbox, Button, END, VERTICAL, N, S, W, E, StringVar, filedialog
from multiprocessing import cpu_count
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg#,NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.axes3d import Axes3D
from re import findall, match
import numpy as np
import toolbox as toolbox
import WannierKit as wan
import fileio as io

global gui  # root gui
global latticeGui, supercellGui, latticeData # read lattice matrix
global nOrbnBondGui, nOrb, nBonds  # read number of orbitals and bonds

global OrbListBox, IDandTypeNote, PosNote, AnisotropyNote
global BondBox, IDandTypeOfBondNote, BondDetailNote

global TlistGui, MCparamGui, modelGui, modelStr, algorithmGui, algoStr, corrGui, coreGui
global resultViewerBase, resultViewer, structureFrame, structureViewer, structureAxis
global submitBtn

#gui=tk.Tk(className='mc solver v0.0.1')

###################
# latice settings #
###################

def loadLatticePannel():
    global gui, latticeGui, supercellGui
    LatticeFrame=LabelFrame(gui,text='Lattice')
    LatticeFrame.grid(row=0,column=0)

    f=Figure(figsize=(2.2,0.4))
    ax=f.add_subplot(1,1,1)
    ax.axis('off')
    ax.text(-0.15,0.4,r"$H=\sum_{mn\alpha}J_{mn}^\alpha S_m^\alpha S_n^\alpha + \sum_{m\alpha} D_m^\alpha(S_m^\alpha S_m^\alpha)$")
    Hamiltonian=FigureCanvasTkAgg(f,LatticeFrame)
    Hamiltonian.draw()
    Hamiltonian.get_tk_widget().grid(row=0,column=0,columnspan=2)

    #HamiltonianLable=Label(LatticeFrame,text=r"$H=\sum_{ij}J_{i,j}S_i\dotS_j + \sum_i D_i(S_i\dot S_i)$")
    #HamiltonianLable.grid(row=0,column=0,columnspan=2)

    a0_base=Frame(LatticeFrame)
    noteFrame0=toolbox.NoteFrm(a0_base, init_notes=['a1:','',''],init_data=[1,0,0],row=True)
    a0_base.grid(row=1,column=0)

    a1_base=Frame(LatticeFrame)
    noteFrame1=toolbox.NoteFrm(a1_base, init_notes=['a2:','',''],init_data=[0,1,0],row=True)
    a1_base.grid(row=2,column=0)

    a2_base=Frame(LatticeFrame)
    noteFrame2=toolbox.NoteFrm(a2_base, init_notes=['a3:','',''],init_data=[0,0,1],row=True)
    a2_base.grid(row=3,column=0)

    latticeGui=[noteFrame0,noteFrame1,noteFrame2]

    supercell_base=Frame(LatticeFrame)
    supercellGui=toolbox.NoteFrm(supercell_base,init_notes=['SC:','x','x'],init_data=[16,16,1],row=True,entryWidth=3)
    supercell_base.grid(row=1,column=1,sticky='SE')
    
def updateLatticeData():
    global latticeGui, latticeData
    latticeData=[]
    for reporter in latticeGui:
        latticeData.append(reporter.report())
    latticeData=np.array(latticeData)

####################
# orbital settings #
####################

def correspondToOrbList(*arg):
    global OrbListBox, IDandTypeNote, PosNote, AnisotropyNote
    data=OrbListBox.report()
    if len(data)>0:
        IDandTypeNote.entry_list[0].config(state='normal')
        IDandTypeNote.setValue([data[0],data[1],data[2]]) # id, type, spin
        IDandTypeNote.entry_list[0].config(state='disabled')
        PosNote.setValue(data[3])                         # fractional coordinates
        AnisotropyNote.setValue(data[4])
        updateStructureViewer(lightOrb=data[0])

def addOrb():
    global OrbListBox, IDandTypeNote, PosNote, AnisotropyNote
    newData=list(OrbListBox.infoData)
    idAndType=IDandTypeNote.report()
    pos=PosNote.report()
    ani=AnisotropyNote.report()
    newData.append([len(newData),int(idAndType[1]),idAndType[2],tuple(pos),tuple(ani)])
    OrbListBox.updateInfo(newData)
    updateStructureViewer()
    
def deletOrb():
    global OrbListBox, IDandTypeNote, PosNote
    newData=list(OrbListBox.infoData)
    if len(newData)==0:
        return
    idAndType=IDandTypeNote.report()
    idxs=int(idAndType[0])
    newData.pop(idxs)
    OrbListBox.updateInfo(newData)
    updateStructureViewer()

def resetOrb():
    global OrbListBox, IDandTypeNote, PosNote, AnisotropyNote
    newData=list(OrbListBox.infoData)
    if len(newData)==0:
        return
    idAndType=IDandTypeNote.report()
    pos=PosNote.report()
    ani=AnisotropyNote.report()
    idxs=int(idAndType[0])
    #print(idxs)
    newData.pop(idxs)
    newData.insert(idxs,[int(idAndType[0]),int(idAndType[1]),idAndType[2],tuple(pos),tuple(ani)])
    OrbListBox.updateInfo(newData)
    updateStructureViewer()

def orbitalDataFormat(info):
    return 'ID: %d Spin: %.1f FracX: %.3f %.3f %.3f Ani: %.2f %.2f %.2f'%(info[0],info[2],info[3][0],info[3][1],info[3][2],info[4][0],info[4][1],info[4][2])

def loadOrbitals():
    global gui, OrbListBox, IDandTypeNote, PosNote, AnisotropyNote
    OrbFrame=LabelFrame(gui,text='Orbital list')
    OrbFrame.grid(row=1,column=0,columnspan=1)

    list_base=Frame(OrbFrame)
    list_base.grid(row=0,column=0,columnspan=2)
    OrbListBox=toolbox.InfoList(list_base, correspondToOrbList, orbitalDataFormat, initialInfo=[[0,0,1,(0.,0.,0.),(0.,0.,0.)]],width=45,height=5)

    addOrbFrameBase=Frame(OrbFrame)
    addOrbFrameBase.grid(row=1,column=0)

    id_base=Frame(addOrbFrameBase)
    id_base.grid(row=0,column=0)
    IDandTypeNote=toolbox.NoteFrm(id_base, init_notes=['ID:','Type:','Init spin:'],init_data=[0,0,1],row=True,entryWidth=5)
    IDandTypeNote.entry_list[0].config(state='disabled')
    pos_base=Frame(addOrbFrameBase)
    pos_base.grid(row=1,column=0,sticky='W')
    PosNote=toolbox.NoteFrm(pos_base, init_notes=['pos','',''],init_data=[0.,0.,0.],row=True,entryWidth=6)

    anis_base=Frame(addOrbFrameBase)
    anis_base.grid(row=2,column=0,sticky=(W,E))
    AnisotropyNote=toolbox.NoteFrm(anis_base, init_notes=['Ani: Dz','Dx','Dy'],init_data=[0,0,0],row=True,entryWidth=6)

    addBtn=Button(addOrbFrameBase,text='add',command=addOrb)
    addBtn.grid(row=0,column=1,rowspan=3)
    resetBtn=Button(addOrbFrameBase,text='reset',command=resetOrb)
    resetBtn.grid(row=0,column=2,rowspan=3)
    delBtn=Button(addOrbFrameBase,text='delet',command=deletOrb)
    delBtn.grid(row=0,column=3,rowspan=3)


##################
# Bonds settings #
##################

def correspondToBondList(*arg):
    global BondBox, IDandTypeOfBondNote, BondDetailNote
    data=BondBox.report()
    if len(data)>0:
        IDandTypeOfBondNote.entry_list[0].config(state='normal')
        IDandTypeOfBondNote.setValue([data[0],data[1][0],data[1][1],data[1][2]]) # id, [Jz, Jx, Jy]
        IDandTypeOfBondNote.entry_list[0].config(state='disabled')
        BondDetailNote.setValue([data[2][0],data[2][1],int(data[2][2][0]),int(data[2][2][1]),int(data[2][2][2])])        # fractional coordinates
        updateStructureViewer(lightID=data[0])

def addBond():
    global BondBox, IDandTypeOfBondNote, BondDetailNote
    newData=list(BondBox.infoData)
    idAndType=IDandTypeOfBondNote.report()
    bondDetail=BondDetailNote.report()
    newData.append([len(newData),
                    [idAndType[1],idAndType[2],idAndType[3]],
                    [int(bondDetail[0]),int(bondDetail[1]),[int(bondDetail[2]),int(bondDetail[3]),int(bondDetail[4])]]])
    BondBox.updateInfo(newData)
    updateStructureViewer()
    
def deletBond():
    global BondBox, IDandTypeOfBondNote, BondDetailNote
    newData=list(BondBox.infoData)
    if len(newData)==0:
        return
    idAndType=IDandTypeOfBondNote.report()
    idxs=int(idAndType[0])
    newData.pop(idxs)
    BondBox.updateInfo(newData)
    updateStructureViewer()

def resetBond():
    global BondBox, IDandTypeOfBondNote, BondDetailNote
    newData=list(BondBox.infoData)
    if len(newData)==0:
        return
    idAndType=IDandTypeOfBondNote.report()
    bondDetail=BondDetailNote.report()
    idxs=int(idAndType[0])
    newData.pop(idxs)
    newData.insert(idxs,[len(newData),
                    [idAndType[1],idAndType[2],idAndType[3]],
                    [int(bondDetail[0]),int(bondDetail[1]),[int(bondDetail[2]),int(bondDetail[3]),int(bondDetail[4])]]])
    BondBox.updateInfo(newData)
    updateStructureViewer()

def bondDataFormat(info):
    return 'ID: %d J: %.3f source: %d target: %d overLat: %d %d %d'%(info[0],info[1][0],info[2][0],info[2][1],info[2][2][0],info[2][2][1],info[2][2][2])

def loadBonds():
    global gui, BondBox, IDandTypeOfBondNote, BondDetailNote
    BondFrame=LabelFrame(gui,text='Bond list')
    BondFrame.grid(row=2,column=0,columnspan=1)

    list_base=Frame(BondFrame)
    list_base.grid(row=0,column=0,columnspan=2)
    BondBox=toolbox.InfoList(list_base, correspondToBondList, bondDataFormat, 
                             initialInfo=[[0,[-1,-1,-1],[0,0,(1,0,0)]],[1,[-1,-1,-1],[0,0,(0,1,0)]]],
                             width=45,height=5)

    addBondFrameBase=Frame(BondFrame)
    addBondFrameBase.grid(row=1,column=0)

    id_base=Frame(addBondFrameBase)
    id_base.grid(row=0,column=0,sticky=(W,E))
    IDandTypeOfBondNote=toolbox.NoteFrm(id_base, init_notes=['ID:','Jz','Jx','Jy'],init_data=[1,-1,-1,-1],row=True,entryWidth=5)
    IDandTypeOfBondNote.entry_list[0].config(state='disabled')

    detail_base=Frame(addBondFrameBase)
    detail_base.grid(row=1,column=0,sticky=(W,E))
    BondDetailNote=toolbox.NoteFrm(detail_base, init_notes=['s','t','over lat.','',''],init_data=[0,0,1,0,0],row=True,entryWidth=3)

    unitLabel=Label(BondFrame,text='Note all energy units are in Kelvin (1meV=11.58875K)')
    unitLabel.grid(row=2,column=0,sticky=(W,E))

    addBtn=Button(addBondFrameBase,text='add',command=addBond)
    addBtn.grid(row=0,column=1,rowspan=2,sticky='E')
    resetBtn=Button(addBondFrameBase,text='reset',command=resetBond)
    resetBtn.grid(row=0,column=2,rowspan=2,sticky='E')
    delBtn=Button(addBondFrameBase,text='delet',command=deletBond)
    delBtn.grid(row=0,column=3,rowspan=2,sticky='E')

###############
# MC settings #
###############

def loadMCSettings():
    global gui, TListGui, MCparamGui, modelGui, modelStr, algorithmGui, algoStr, corrGui, coreGui
    SettingFrame=LabelFrame(gui,text='Other settings')
    SettingFrame.grid(row=3,column=0,sticky=(W,E))

    temp_base=Frame(SettingFrame)
    temp_base.grid(row=0,column=0)
    TListGui=toolbox.NoteFrm(temp_base, init_notes=['T start:','T end','total points:'], init_data=[2.0,2.4,20],row=True,entryWidth=6)

    MCparam_base=Frame(SettingFrame)
    MCparam_base.grid(row=1,column=0,sticky='W')
    MCparamGui=toolbox.NoteFrm(MCparam_base, init_notes=['nthermal:','nsweep:','tau:'], init_data=[20000,40000,1],row=True)

    model_base=Frame(SettingFrame)
    model_base.grid(row=2,column=0,sticky='W')
    label1=Label(model_base,text='Model:')
    label1.grid(row=0,column=0)
    modelStr=StringVar()
    modelGui=Spinbox(model_base,from_=1, to=3, values=['Ising','XY','Heisenberg'],textvariable=modelStr,width=12)
    modelGui.grid(row=0,column=1)
    
    label2=Label(model_base,text='Algorithm:')
    label2.grid(row=0,column=2)
    algoStr=StringVar()
    algorithmGui=Spinbox(model_base,from_=1, to=3, values=['Wolff','Metroplis','Sweden-Wang'],textvariable=algoStr,width=12)
    algorithmGui.grid(row=0,column=3)

    corr_base=Frame(SettingFrame)
    corr_base.grid(row=3,column=0,sticky='W')
    corrGui=toolbox.NoteFrm(corr_base, init_notes=['Mesure corr. si','sj','overLat:','',''], init_data=[0,0,0,0,0],entryWidth=3,row=True)

    core_base=Frame(SettingFrame)
    core_base.grid(row=4,column=0,sticky='W')
    coreGui=toolbox.NoteFrm(core_base, init_notes=['core:'], init_data=[np.max([1,int(cpu_count()/2)])])

########################
# Structure visualizer #
########################

def loadStructureViewer():
    global gui, latticeGui, OrbListBox, BondBox, supercellGui, structureFrame, structureViewer, structureAxis
    structureFrame=LabelFrame(gui, text='Structure viewer')
    structureFrame.grid(row=0,column=1,rowspan=2)

    tb=wan.TBmodel()
    a1=latticeGui[0].report()
    a2=latticeGui[1].report()
    a3=latticeGui[2].report()
    tb.lattice=np.array([a1,a2,a3])
    tb.orbital_coor=[[np.array(ele[3]),50,'red'] for ele in OrbListBox.infoData]
    tb.norbital=len(tb.orbital_coor)
    tb.hopping=[[bond_data[2][0],bond_data[2][1],np.array(bond_data[2][2]),bond_data[1][0],'green', 2] for bond_data in BondBox.infoData]
    tb.nhoppings=len(tb.hopping)
    Lx, Ly, Lz=[4 if x>1 else 1 for x in supercellGui.report() ]
    tb.make_supercell([Lx,0,0],[0,Ly,0],[0,0,Lz])
    f, structureAxis=tb.viewStructure()
    
    x0, x1 = structureAxis.get_xlim()
    y0, y1 = structureAxis.get_ylim()
    z0, z1 = structureAxis.get_zlim()

    ox=(x0+x1)/2;oy=(y0+y1)/2;oz=(z0+z1)/2
    xlen=abs(x1-x0);ylen=abs(y1-y0);zlen=abs(z1-z0)
    lenMax_half=np.max([xlen,ylen,zlen])/2
    structureAxis.set_xlim(ox-lenMax_half,ox+lenMax_half)
    structureAxis.set_ylim(oy-lenMax_half,oy+lenMax_half)
    structureAxis.set_zlim(oz-lenMax_half,oz+lenMax_half)
    #structureAxis.view_init(elev=0,azim=0)

    structureViewer=FigureCanvasTkAgg(f,structureFrame)
    structureViewer.draw()
    structureViewer.get_tk_widget().grid(row=0,column=0)
    structureAxis.figure.canvas=structureViewer
    structureAxis.mouse_init()

def updateStructureViewer(lightID=-1,lightOrb=-1):
    global gui, latticeGui, OrbListBox, BondBox, supercellGui, structureFrame, structureViewer, structureAxis
    elev, azim = structureAxis.elev, structureAxis.azim
    x0, x1 = structureAxis.get_xlim()
    y0, y1 = structureAxis.get_ylim()
    z0, z1 = structureAxis.get_zlim()

    tb=wan.TBmodel()
    a1=latticeGui[0].report()
    a2=latticeGui[1].report()
    a3=latticeGui[2].report()
    tb.lattice=np.array([a1,a2,a3])
    tb.orbital_coor=[[np.array(ele[3]),100 if ele[0]==lightOrb else 50,'yellow' if ele[0]==lightOrb else 'red' ] for ele in OrbListBox.infoData]
    tb.norbital=len(tb.orbital_coor)
    tb.hopping=[[bond_data[2][0],bond_data[2][1],np.array(bond_data[2][2]),bond_data[1][0],'yellow' if bond_data[0]==lightID else 'green', 6 if bond_data[0]==lightID else 2] for bond_data in BondBox.infoData]
    tb.nhoppings=len(tb.hopping)
    Lx, Ly, Lz=[4 if x>1 else 1 for x in supercellGui.report() ]
    tb.make_supercell([Lx,0,0],[0,Ly,0],[0,0,Lz])
    f, structureAxis=tb.viewStructure()
    structureAxis.view_init(elev=elev,azim=azim)
    structureAxis.set_xlim(x0,x1)
    structureAxis.set_ylim(y0,y1)
    structureAxis.set_zlim(z0,z1)
    
    structureViewer.get_tk_widget().destroy()
    structureViewer=FigureCanvasTkAgg(f,structureFrame)
    structureViewer.draw()
    structureViewer.get_tk_widget().pack()
    structureAxis.figure.canvas=structureViewer
    structureAxis.mouse_init()

#####################
# Resutl visualizer #
#####################

def loadResultViewer():
    global gui, resultViewerBase, resultViewer
    resultViewerBase=LabelFrame(gui, text='Result viewer')
    resultViewerBase.grid(row=2,column=1,rowspan=2)

    f=Figure(figsize=(4,3))
    f.add_subplot(111).plot([0,2],[0,0],color='black')
    resultViewer=FigureCanvasTkAgg(f,resultViewerBase)
    resultViewer.draw()
    resultViewer.get_tk_widget().pack()

def updateResultViewer(TList=[],magList=[], susList=[]):
    global gui, resultViewerBase, resultViewer
    #print('updating:',TList,magList)
    f=Figure(figsize=(4,3))
    ax=f.add_subplot(111,label=0)
    ax.scatter(TList,magList,color='red',label='<spin>')

    ax2=ax.twinx()
    ax2.scatter(TList,susList,color='blue',label=r'Capa')
    ax2.set_ylim(min(susList),max(susList))

    f.legend()

    resultViewer.get_tk_widget().destroy()
    resultViewer=FigureCanvasTkAgg(f,resultViewerBase)
    resultViewer.draw()
    resultViewer.get_tk_widget().pack()

#############
# Func btn #
#############

def loadStartBtn(submitFunc):
    global gui, saveBtn, loadBtn, submitBtn
    submit_base=Frame(gui)
    submit_base.grid(row=4,column=0,columnspan=2)

    saveBtn=Button(submit_base,text='Save',command=io.saveParam)
    saveBtn.grid(row=0,column=0,rowspan=3)

    loadBtn=Button(submit_base,text='Load',command=io.loadParam)
    loadBtn.grid(row=0,column=1,rowspan=3)

    submitBtn=Button(submit_base,text='StartMC',command=submitFunc)
    submitBtn.grid(row=0,column=2,rowspan=3)

    note1=Label(submit_base, text='Thanks for your attention and I wish you would find sth. helpful.', width=80)
    note1.grid(row=0,column=3)
                        
    note2=Label(submit_base, text='Please cite: Magnetic switches via electric field in BN nanoribbons. Appl. Surf. Sci. 480(2019)', width=80)
    note2.grid(row=1,column=3)

    note3=Label(submit_base, text='Thank you very much!', width=80)
    note3.grid(row=2,column=3)

def loadEverything(root,submitFunc):
    global gui
    gui=root
    loadLatticePannel()
    updateLatticeData()

    loadOrbitals()
    loadBonds()
    loadMCSettings()
    loadStructureViewer()
    loadResultViewer()
    loadStartBtn(submitFunc)
