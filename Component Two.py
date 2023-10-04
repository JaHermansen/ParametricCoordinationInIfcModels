import ifcopenshell
import ifcopenshell.geom
import ifcopenshell.util

from datetime import datetime
from progress.bar import ChargingBar
from progress.bar import Bar
from alive_progress import alive_bar
import uuid
import xlrd
import os
import time


import pandas as pd
import os
import numpy as np


## Initialization ##
__author__ = 'Jacob Hein Hermansen (s173794)'
__version__ = '2.3'
__email__ = 's173794@student.dtu.dk'
__status__ = 'Prototype'
__date__ = str(datetime.now())
__description__ = 'Stage 2: Allocation of properties'
__course__ = 'Master Thesis'


print('# ' + '=' * 78)
print('Author: ' + __author__)
print('Version: ' + __version__)
print('Email: ' + __email__)
print('Status: ' + __status__)
print('Date: ' + __date__)
print('Description: ' + __description__)
print('Project: ' + __course__)
print('# ' + '=' * 78)

## User input of import directory ##

choices = ['yes', 'y', 'no', 'n']
Gochoices = ['yes', 'y']
Nogochoices = ['no', 'n']

## User input of file ##
print("\n### IFC ALLOCATION OF PROPERTIES ###")
sourcefile = input("Specify directory of file\nInput: ")
    


## load model begin ##
start5 = time.time()
print('Loading the model...')
bar1 = ChargingBar('Processing', max=1)
for i in range(1):
    model = ifcopenshell.open(sourcefile)
    bar1.next()

timeStep5 = time.time() - start5
print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep5)))


## Load external data set ##
print("\nExternal Datasheet:")
input_path = input("Specify directory of data sheet\nInput: ")

search_word = "Dashboard"
DashboardTemplate = pd.DataFrame(columns=['PipeID','Missing Dimension'])


if os.path.exists(input_path):
    df1 = pd.ExcelFile(input_path)
    sheetNames = df1.sheet_names
    
    
    if not search_word in sheetNames:
        df2 = pd.DataFrame(DashboardTemplate)
        with pd.ExcelWriter(input_path, engine='openpyxl', mode='a') as writer:  
            df2.to_excel(writer, sheet_name=search_word)
    
    
else:
    print("Path {} do not exists".format(input_path))
    

print("\nExternal data sheet loaded")
print("Sheets:")
print(sheetNames)

print("\nScreening...")
## Preparing for pset assignment ##
owner_history = model.by_type("IfcOwnerHistory")[0]
products = model.by_type("IfcProduct")

## Creating container stats ##
missingDataOccurence = 0
missingDataKeys = []
missingDataKeysSheets = []


## Initiating allocation of parameters ##
start3 = time.time()
procs = []
for i in products:
    if i.is_a("IfcFlowSegment"):
        procs.append(i)


for proc in procs:
    pset = ifcopenshell.util.element.get_psets(proc, psets_only=True)

    try:
        DictGEOM = pset['COWI_Measurements']
    except:
        pass
    keyGEOM = list(DictGEOM)
    try:
        PipeKey = pset['COWI_Identification']
    except:
        pass
    PipeID = list(PipeKey)


    idIndex = PipeID.index("DrwTypeMark_Type_CW")
    geomIndex = keyGEOM.index("NorminalSize")

    PipeID = PipeKey[PipeID[idIndex]]
    NormSizeValue = DictGEOM[keyGEOM[geomIndex]]

    for item in sheetNames:
        if PipeID in item:
            index = sheetNames.index(item)
            


    ## Getting pipe specific worksheet ##
    sheetid = sheetNames[index]
    DataSheet = pd.read_excel(df1, sheetNames[index])
    RorDim = DataSheet.iloc[:,0].tolist()
    
    RorDim_clean = [s.replace("ø", "") for s in RorDim]


    ## Testing for valid values ##
    try:
        indexGeoDia = RorDim_clean.index(NormSizeValue)
        
    except:
        indexGeoDia = "Missing data"
        missingDataOccurence = missingDataOccurence + 1
        missingDataKeys.append(NormSizeValue)
        missingDataKeysSheets.append(sheetid)
    

    ## Creating values for drilling diameter ##
    if indexGeoDia == "Missing data":
        DrillingDiameter = "Missing data"


    if indexGeoDia != "Missing data":
        ## Getting DrillingDimensions ##
        DataSheet = pd.read_excel(df1, sheetNames[index])
        DrillDim = DataSheet.iloc[:,1].tolist()
        #print(DrillDim)
        
            
        DrillDim_clean = [s.replace("ø", "") for s in DrillDim]

        DrillingDiameter = DrillDim_clean[indexGeoDia]
        
        
        
    property_values = [
        model.createIfcPropertySingleValue("BoreholeDiameter", "BoreholeDiameter", model.create_entity("IfcText", DrillingDiameter), None),
    ]   
    property_set = model.createIfcPropertySet(proc.GlobalId, owner_history, "BoreholeDiameter", None, property_values)
    model.createIfcRelDefinesByProperties(proc.GlobalId, owner_history, None, None, [proc], property_set)
timeStep3 = time.time() - start3
print("\nExectuion time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep3)))


recountObjects = len(procs)
RecountObjects = str(len(procs))
recountMissing = str(missingDataOccurence)
MissingDataKeys = str(list(dict.fromkeys(missingDataKeys)))
MissingDataKeysSheets = str(list(dict.fromkeys(missingDataKeysSheets)))


MissingID = missingDataKeys
MissingDims = missingDataKeysSheets
#NewDash = DashboardTemplate.append((missingDataKeysSheets,missingDataKeys))

dx = {"PipeID": missingDataKeysSheets, "Missing Dimension": missingDataKeys}
df_Dashboard_pre = pd.DataFrame(dx)
df_Dashboard = df_Dashboard_pre.drop_duplicates()
NewDash = DashboardTemplate.append(df_Dashboard)
    
with pd.ExcelWriter(input_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    NewDash.to_excel(writer, sheet_name=search_word)


## Determining export scenarios based on level of success ## 

if missingDataOccurence > 0:
    res = recountObjects - missingDataOccurence
    Res = str(res)
    print("\nThe allocation of parameters is complete! " + Res + " entities out of a total of " + RecountObjects + " were eligible to get a parameter from the workbook.")
    print("Inspect the Dashboard sheet in " + input_path + " to see distribution of missing data.")
   # print("The non-eligible entites considers the following geometric diameters: " + MissingDataKeys + ", within sheet " + MissingDataKeysSheets)
    
    while True:
        print("\nWish to see location of missing data keys?")
        #Define user input
        choice = input("Yes/No:  ")
        
        if choice.lower() in Gochoices:
            for i in range(missingDataOccurence):
                print(missingDataKeysSheets[i])
                print(missingDataKeys[i])
                
            break
        break
        
        if choice.lower() in Nogochoices:
            break
        break


if missingDataOccurence == 0:
    print("\nThe allocation of parameters is complete without occurence of missing data!")
    print("Number of allocated parameters: " + RecountObjects)



## Export scheme ##
start2 = time.time()

print("\nProceed to export objects?")
#Define user input
choice = input("Yes/No:  ")
    
if choice.lower() in Gochoices:
    # Initializing export ##
    print("\nSpecify directory of export file")
    outFile = input("Specify directory of file\nInput: ")

    print('\n\nInitializing export') 
    bar1 = ChargingBar('Exporting', max=1)
    for i in range(1):
        model.write(outFile)
        bar1.next()
        
    print('\n\nWritting complete!')




timeStep2 = time.time() - start2
print("\nExectuion time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep2)))