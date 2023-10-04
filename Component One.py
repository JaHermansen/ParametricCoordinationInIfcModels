import ifcpatch
import ifcopenshell

from datetime import datetime
from progress.bar import ChargingBar
from progress.bar import Bar
from alive_progress import alive_bar
import uuid
import time


## Initialization ##
__author__ = 'Jacob Hein Hermansen (s173794)'
__version__ = '1.2'
__email__ = 's173794@student.dtu.dk'
__status__ = 'Prototype'
__date__ = str(datetime.now())
__description__ = 'Stage 1: Extraction of Desired Entities and Merging of Projects'
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



print("Initializing...\n")
print("Welcome!\nThis script serves the function to extract specific IFC entities and secondly to merge IFC projects.\nPlease fill in the inputs to proceed.")

#Define user input
initStatement = input("\nProjects to merge?\nInput: ")

#Handle user input and potential errorsa
if initStatement.lower() not in choices:
    print("\n###### ERROR MESSAGE ######")        
    print("Please state either Yes or No")
    
    
    initStatement = input("\nInput: ") 
    
    if initStatement.lower() not in choices:
        print("Terminating")



## Initiating subevent of merging projects ##
if initStatement.lower() in Gochoices:
    print("\nProceeding to assign projects to merge...")
## User input of source file ##
    #while True:
    print("\n### IFC PROJECT MERGER ###")
    print("\nSource file:")
    sourcefile = input("Specify directory of source file\nInput: ")
    
    print("\nMerge file:")
    mergefile = input("Specify directory of merge file\nInput: ")


    ## load model1 begin ##
    start1 = time.time()
    print("Loading input files...")
    model1 = ifcopenshell.open(sourcefile)
    model2 = ifcopenshell.open(mergefile)
    timeStep1 = time.time() - start1
    print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep1)))

    ## MODEL 1 ##
    
    ## Screening of model1 ## 
    
        ## Determine building name ##

    Name1 = "Source file"
                
    print("\n### IFC ENTITY IDENTIFIER: " + Name1+" ###")
    print("Multiple entities has been detected in " + str(Name1) + ". Based on the IFC model screening at " + str(datetime.now()) + ", an entity and quantity list has been created\n")
    
    
    #Determine all entity classes in the file
    rootedEntities = model1.by_type('IfcProduct')
    elementEntities = set()
    for entity in rootedEntities:
        elementEntities.add(entity.is_a())
    
    #Display entity classes
    entityClasses = []
    for ifcClassName in elementEntities:
        entityClasses.append(ifcClassName)
    print("The file consists of " + str(len(rootedEntities)) + " objects, and " + str(len(entityClasses)) + " entity classes.")
    
    
    entityClasses.sort()
    for i in range(len(entityClasses)-1):
        print(entityClasses[i], end=", ")
    for i in range(len(entityClasses)-1,len(entityClasses)):
        print(entityClasses[i], end=".")
        
    #Define user input
    print("\n\nSpecify extraction entity\n----------\nFormat:\nSingle: e.g. .IfcWall\nMultiple: e.g. .IfcWall | .IfcFlowSegment\n----------")
    EntityInput1 = input("\nInput: ")
            

    
    
    ## Initiating read out of source file extraction ##
    print("\nInitiating extraction of " + EntityInput1 +" from " + Name1)
    
    print("\nNew source project directory:")
    Source = input("Specify directory of extraction of source project\nInput: ")
    
    start2 = time.time()
    print('Writing the model...')
    output = ifcpatch.execute({
        "input": model1,
        "recipe": "ExtractElements",
        "arguments": [EntityInput1],
    })
    ifcpatch.write(output, Source)
    
    timeStep2 = time.time() - start2
    print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep2)))
    
    
    print("Extraction of entities within " + Name1 +" complete!")
    ## MODEL 2 ##
    
    ## Screening of model2 ## 
    
        ## Determine building name ##

    Name2 = "Merge file"
    print('\n--------------------------\n')
                
    print("\n### IFC ENTITY IDENTIFIER: " + Name2+" ###")
    print("Multiple entities has been detected in " + str(Name2) + ". Based on the IFC model screening at " + str(datetime.now()) + ", an entity and quantity list has been created\n")
    
    
    #Determine all entity classes in the file
    rootedEntities = model2.by_type('IfcProduct')
    elementEntities = set()
    for entity in rootedEntities:
        elementEntities.add(entity.is_a())
    
    #Display entity classes
    entityClasses = []
    for ifcClassName in elementEntities:
        entityClasses.append(ifcClassName)
    print("The file consists of " + str(len(rootedEntities)) + " objects, and " + str(len(entityClasses)) + " entity classes.")
    
    
    entityClasses.sort()
    for i in range(len(entityClasses)-1):
        print(entityClasses[i], end=", ")
    for i in range(len(entityClasses)-1,len(entityClasses)):
        print(entityClasses[i], end=".")
        
    #Define user input
    print("\n\nSpecify extraction entity\n----------\nFormat:\nSingle: e.g. .IfcWall\nMultiple: e.g. .IfcWall | .IfcFlowSegment\n----------")
    EntityInput2 = input("\nInput: ")
    
            
    
    
    ## Initiating read out of source file extraction ##
    print("\nInitiating extraction of " + EntityInput2 +" from " + Name2)
    
    print("\nNew source project directory:")
    Merge = input("Specify directory of extraction of source project\nInput: ")
    
    start3 = time.time()
    print('Writing the model...')
    output = ifcpatch.execute({
        "input": model2,
        "recipe": "ExtractElements",
        "arguments": [EntityInput2],
    })
    ifcpatch.write(output, Merge)
    
    timeStep3 = time.time() - start3
    print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep3)))
        
        
        #break
    print("\nProceeding to merge extracted files...")
    print("\nMerged project directory:")
    mergedproject = input("Specify directory of merged project\nInput: ")
    

    sovs = Source
    Sovs = ifcopenshell.open(sovs)
    fil = Merge
    start4 = time.time()
    print("\nMerging assigned projects...")
    bar = ChargingBar('Processing', max=1)
    for i in range(1):
        output = ifcpatch.execute({
            "input": Sovs,
            "recipe": "MergeProject",
            "arguments": [fil],
        })
        ifcpatch.write(output, mergedproject)
        bar.next()
    timeStep4 = time.time() - start4
    print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep4)))
    print("Merging complete!\nLook up merged project file: " + mergedproject)





print("\nWish to extract entity from single file?")


#Define user input
carryon = input("Input: ")


#Handle user input and potential errorsa
if carryon.lower() not in choices:
    print("\n###### ERROR MESSAGE ######")        
    print("Please state either Yes or No")
    
    
    initStatement = input("\nInput: ") 
    
if carryon.lower() in Nogochoices:
    print("Terminating...")



## Initiating subevent of merging projects ##
if carryon.lower() in Gochoices:
## User input of file ##
    print("\n### IFC ENTITY EXTRACTOR ###")
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
    

    ## Determine building name ##
    Name = model.by_type('IfcProject')[0].LongName
    if Name == None:
        Name = "Input file"
    print('\n' + str(Name) + ' is succesfully loaded!')

    ## User input of desired objects to extract ##
    #Define display message
    print("\n### IFC ENTITY IDENTIFIER ###")
    print("Multiple entities has been detected in " + str(Name) + ". Based on the IFC model screening at " + str(datetime.now()) + ", an entity and quantity list has been created\n")
    
    
    #Determine all entity classes in the file
    rootedEntities = model.by_type('IfcProduct')
    elementEntities = set()
    for entity in rootedEntities:
        elementEntities.add(entity.is_a())
    
    #Display entity classes
    entityClasses = []
    for ifcClassName in elementEntities:
        entityClasses.append(ifcClassName)
    print("The file consists of " + str(len(rootedEntities)) + " objects, and " + str(len(entityClasses)) + " entity classes.")
       
    entityClasses.sort()
    for i in range(len(entityClasses)-1):
        print(entityClasses[i], end=", ")
    for i in range(len(entityClasses)-1,len(entityClasses)):
        print(entityClasses[i], end=".")
        
    #Define user input
    EntityInput = input("\n\nPlease enter an entity class, e.g. IfcBuilding, to screen its quantity within the file\nInput: ")
    
    #Handle user input and potential errors
    entityClasses.append('All entities')
    if EntityInput not in entityClasses:
        print("\n###### ERROR MESSAGE ######")        
        print("This entity is not contained in the file. Please input one of the following entities: ")
        
        for i in range(len(entityClasses)-1):
            print(entityClasses[i], end=", ")
        for i in range(len(entityClasses)-1,len(entityClasses)):
            print(entityClasses[i], end=".") 
        
        EntityInput = input("\nInput: ") 
        
        if EntityInput not in entityClasses:
            print("Invalid input")
            
    




    ## Determine number of entities in the buildings ##
    if EntityInput != 'All entities':
        EntityCount = 0
    
        for Entity in model.by_type(EntityInput):
            EntityCount += 1
        print("The chosen entity class considers " + str(EntityCount) + " objects in the loaded file.\n")
     
        
        
    
        
    ## If user input is a ifc entity name ##
    if EntityInput != 'All entities':
    
        print("Initiates extraction from file...")
        
        ## User input of export directory ##

        print("Specify the desired directory to export the " + str(EntityInput) + "'s.\n")
            #Define user input
        ExportDirectory = input("Please enter the desired directory of export:\nInput: ")
           
    
    ## Initializing export ##
    print("\n\nSpecify extraction entity\n----------\nFormat:\nSingle: e.g. .IfcWall\nMultiple: e.g. .IfcWall | .IfcFlowSegment\n----------")
    #Define user input
    exportOption = input("\nExport option:\nInput: ")
    
    start6 = time.time()
    print('\n\nInitializing export') 
    bar2 = ChargingBar('Exporting', max=1)
    for i in range(1):
        output = ifcpatch.execute({
            "input": model,
            "recipe": "ExtractElements",
            "arguments": [exportOption],
        })
        bar2.next()
    ifcpatch.write(output, ExportDirectory)
    
    print('\n\nWritting complete!')
    
    
    timeStep6 = time.time() - start6
    print("\nExecution time: ", time.strftime("%H:%M:%S", time.gmtime(timeStep6)))
    

