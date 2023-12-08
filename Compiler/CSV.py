
#HLC instruction    |   YMC Address  |   YMC assembly |  YMC encoding | Modified registers | Modified flags
#while y > 0        | XXXX           |  cmp eax, 0    | AB CD 20 XXXX |----                | SF = , OF, ZF, CF 
#                   |                |  Jg xxx

#--------------------------
#reads File, gets line count
#--------------------------
def lineCount(fileName):
    with open(fileName, "r") as file:
        content = file.read()

    #split content by newline characters
    lines = content.split("\n")

    lineAmount = len(lines)
    return lineAmount

#--------------------------------
#'HLC instruction', 'YMC Address', 'YMC assembly', 'YMC Encoding', 'Modified Registers', 'Modified Flags'
# hlcData, assemblyData, machineData, addressArray, modReg, modFlags
def csvCreate(): #HLC, ASM, Machine
    from betaCompiler import flagArr, ASMArr, YMCArr, HLCArr, modReg, fileName2, fileName4
    from ASM import machineArr
    import csv
    
    textStop = lineCount(fileName2)    #checks how long the ASM File is

    #create/open 'output.csv' File
    with open(fileName4, 'w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter='\t')

        #write headers
        writer.writerow(['HLC instruction', '       ', 'YMC Address', '           ', 'YMC assembly', '       ', 'YMC Encoding', '       ', 'Modified Registers', '       ', 'Modified Flags'])




        #make for loop to check and alter all files to remove \n or \t
        for i in range(0, textStop, +1):
            HLCArr[i] = HLCArr[i].replace("\n", "")
            HLCArr[i] = HLCArr[i].replace("\t", "")

            ASMArr[i] = str(ASMArr[i])
            ASMArr[i] = ASMArr[i].replace("\n", "")
            ASMArr[i] = ASMArr[i].replace("\t", "")

            machineArr[i] = machineArr[i].replace("\n", "")
            machineArr[i] = machineArr[i].replace("\t", "")

            YMCArr[i] = str(YMCArr[i])  #convert to string to increase length later
            #makes it 4 long with 0000
            if (len(YMCArr[i]) == 1):
                YMCArr[i] = '000' + YMCArr[i]
                if (YMCArr[i] == '' or ' '):
                    YMCArr[i] = ' '
                
            elif (len(YMCArr[i]) == 2):
                YMCArr[i] = '00' + YMCArr[i]  
            elif (len(YMCArr[i]) == 3):
                YMCArr[i] = '0' + YMCArr[i]

            YMCArr[i] = YMCArr[i].replace("\n", "")
            YMCArr[i] = YMCArr[i].replace("\t", "")
            
            modReg[i] = modReg[i].replace("\n", "")
            modReg[i] = modReg[i].replace("\t", "")

            flagArr[i] = flagArr[i].replace("\n", "")
            flagArr[i] = flagArr[i].replace("\t", "")

            #makes them all a certain length by adding white space
            HLCArr[i] = HLCArr[i].ljust(21)
            ASMArr[i] = ASMArr[i].ljust(21)
            machineArr[i] = machineArr[i].ljust(21)
            YMCArr[i] = YMCArr[i].ljust(21)
            modReg[i] = modReg[i].ljust(21)
            flagArr[i] = flagArr[i].ljust(21)

            

        #loop to write each row
        for i in range(0, textStop, +1):
            writer.writerow([HLCArr[i], YMCArr[i], machineArr[i], ASMArr[i], modReg[i], flagArr[i]])


    print('Successfully created CSV File')
    return 0



#-------------------------
#loop to print CSV File
#-------------------------