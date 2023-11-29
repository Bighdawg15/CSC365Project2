#-----------------------------------------------------------------------------------------------------
#NOTES:
#-----------------------------------------------------------------------------------------------------
#If a varible was signed or unsigned. Would i need to have a manual check for if its outside of that number range so that it gives an error message?



#-----------------------------------------------------------------------------------------------------
#variables/imports
#-----------------------------------------------------------------------------------------------------
import re
import ASM
import CSV


#dummy variable
lineCounterASM = '' #their are 389 uses of this function, that I'll clean up later


#variables
i = 0
lineCounterASMR = 0 #for the ASM
whileCheck = 'false'
ifCheck = 'false'
elseCheck = 'false'
indentCheck = 'false'
fileName = 'test.txt'   #might need to just have the name depend on the funciton imports like : compiler(fileName)

#arrays
addressArray = []   #keeps track of address's
modReg = []         #register updates
modFlags = []       #flag updates


#only positive                  Range: 0 to 255  (unsigned)
a = 0
b = 0
c = 0

#both positive and negative     Range: -128 to 127  (Signed)
x = 0
y = 0
z = 0

#registers
eax = 0
ebx = 0
ecx = 0
edx = 0

#placeHolder registers (to check for changes)
eax2 = 0
ebx2 = 0
ecx2 = 0
edx2 = 0

#-----------------------------------------------------
#writeASM fucntion (for HLC to ASM)
#-----------------------------------------------------
def writeASM (new_line):    #doeslinCounterASM need to be imported?
    global lineCounterASMR      #to many statements already include the other import
    lineCounterASMR = lineCounterASMR + 1  # increments the line for each time its added to for ASM
    #new_line = 'This is the new text for line 3\n'

    # Read all lines
    with open('assembler.txt', 'r') as f:
        lines = f.readlines()

    # Modify the specific line
    if lineCounterASMR - 1 < len(lines): 
        lines[lineCounterASMR - 1] = new_line   
    else:
        lines.append(new_line)  # Append the new line if the file has fewer lines

    # Write all lines back to the file
    with open('assembler.txt', 'w') as f:
        f.writelines(lines)

    return 0

#-----------------------------------------------------------------------------------------------------
#register updates
#-----------------------------------------------------------------------------------------------------
#stores its own backup registers after each line and compares. if something was changed, it will show on the csv file

def regCheck ():
    regChanges = None   #reset before check
    global eax2, ebx2, ecx2, edx2, eax, ebx, ecx, edx   #gets from global, all changes made will stay

    if (eax != eax2):
       regChanges = regChanges + ', eax'
       eax2 = eax
    if (ebx != ebx2):
       regChanges = regChanges + ', ebx'
       ebx2 = ebx
    if (ecx != ecx2):
       regChanges = regChanges + ', ecx'
       ecx2 = ecx
    if (edx != edx2):
       regChanges = regChanges + ', edx'
       edx2 = edx
    
    return regChanges

#-----------------------------------------------------------------------------------------------------
#indent printer (prints, to different text file the conversion, but doesn't acutally process them)
#-----------------------------------------------------------------------------------------------------
def justPrint(placeHolder):
    global elseCheck
    temp = len(placeHolder)
    #might need to split placeholder in here?

    if (temp == 3): #b = 3 : 0 1 2
        var4 = 'mov ' + placeHolder[0] + ', ' + placeHolder[2]
        writeASM(var4)

    elif (temp == 5): #y = a + b : 0 1 2 3 4 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(var4)

        if (placeHolder[3] == '+'):
            var4 = 'add eax eax ebx'
        elif (placeHolder[3] == '-'):
            var4 = 'sub eax eax ebx'
        elif (placeHolder[3] == '*'):
            var4 = 'mult eax eax ebx'
        elif (placeHolder[3] == '/'):
            var4 = 'div eax eax ebx'
        else:
            print('NoPrint: Error Temp5')

        writeASM(var4)
        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(var4)

    elif (temp == 7): #y = a + b - c : 0 1 2 3 4 5 6 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(var4)
        var4 = 'mov ebc, ' + placeHolder[6]
        writeASM(var4)
        
        if (placeHolder[3] == '+'):
            p1 = 'add'
        elif (placeHolder[3] == '-'):
            p1 = 'sub'
        elif (placeHolder[3] == '*'):
            p1 = 'mult'
        elif (placeHolder[3] == '/'):
            p1 = 'div'
        else:
            print('NoPrint: Error Temp7: 3')

        if (placeHolder[5] == '+'):
            p2 = 'add'
        elif (placeHolder[5] == '-'):
            p2 = 'sub'
        elif (placeHolder[5] == '*'):
            p2 = 'mult'
        elif (placeHolder[5] == '/'):
            p2 = 'div'
        else:
            print('NoPrint: Error Temp7: 5')
        
        temp2 = p1 + p2

        var4 = temp2 + ' eax eax ebx ecx'
        writeASM(var4)

        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(var4)

    else:
        print('justPrint: Temp Error')

    return 0

#-----------------------------------------------------------------------------------------------------
#flags
#-----------------------------------------------------------------------------------------------------
#make a function to be ran after each step for the flags to be updated
#reset at beginning of function, output to csv file
#maybe make seperate file
overflowF = 0
zeroF = 0
carryF = 0 #only true, when a signed/unsigned is borrowed (goes out of range, but is in differnt range): like 1011 is 8 4 2 1 : for signed its -8 4 2 1
signF = 0

def flagCarrier():
    


    return 0

#-----------------------------------------------------------------------------------------------------
#math function (This sucked)
#-----------------------------------------------------------------------------------------------------
#Do not make me move all those lines over by a indent space
def mathStuff(placeHolder): #do I need to import the variables and registers
    global a, b, c, x, y, z, eax, ebx, ecx, edx   #gets from global, all changes made will stay
    temp = len(placeHolder)

    if (temp == 3): # b = 3 or b = a : 0 1 2
        #this is where the zero flag will go
        if (placeHolder[0] == 'a'):
            if (placeHolder[2] == 'a'):
                eax = a
                a = eax
                writeASM('mov eax, a')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                a = eax
                writeASM('mov eax, b')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                a = eax
                writeASM('mov eax, c')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                a = eax
                writeASM('mov eax, x')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                a = eax
                writeASM('mov eax, y')
                writeASM('mov a, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                a = eax
                writeASM('mov eax, z')
                writeASM('mov a, eax')

            else:
                eax = placeHolder[2]
                a = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov a, eax')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[2] == 'a'):
                eax = a
                b = eax
                writeASM('mov eax, a')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                b = eax
                writeASM('mov eax, b')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                b = eax
                writeASM('mov eax, c')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                b = eax
                writeASM('mov eax, x')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                b = eax
                writeASM('mov eax, y')
                writeASM('mov b, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                b = eax
                writeASM('mov eax, z')
                writeASM('mov b, eax')

            else:
                eax = placeHolder[2]
                b = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov b, eax')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[2] == 'a'):
                eax = a
                c = eax
                writeASM('mov eax, a')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                c = eax
                writeASM('mov eax, b')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                c = eax
                writeASM('mov eax, c')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                c = eax
                writeASM('mov eax, x')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                c = eax
                writeASM('mov eax, y')
                writeASM('mov c, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                c = eax
                writeASM('mov eax, z')
                writeASM('mov c, eax')

            else:
                eax = placeHolder[2]
                c = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov c, eax')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[2] == 'a'):
                eax = a
                x = eax
                writeASM('mov eax, a')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                x = eax
                writeASM('mov eax, b')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                x = eax
                writeASM('mov eax, c')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                x = eax
                writeASM('mov eax, x')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                x = eax
                writeASM('mov eax, y')
                writeASM('mov x, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                x = eax
                writeASM('mov eax, z')
                writeASM('mov x, eax')

            else:
                eax = placeHolder[2]
                x = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov x, eax')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[2] == 'a'):
                eax = a
                y = eax
                writeASM('mov eax, a')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                y = eax
                writeASM('mov eax, b')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                y = eax
                writeASM('mov eax, c')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                y = eax
                writeASM('mov eax, x')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                y = eax
                writeASM('mov eax, y')
                writeASM('mov y, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                y = eax
                writeASM('mov eax, z')
                writeASM('mov y, eax')

            else:
                eax = placeHolder[2]
                y = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov y, eax')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[2] == 'a'):
                eax = a
                z = eax
                writeASM('mov eax, a')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                z = eax
                writeASM('mov eax, b')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                z = eax
                writeASM('mov eax, c')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                z = eax
                writeASM('mov eax, x')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                z = eax
                writeASM('mov eax, y')
                writeASM('mov z, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                z = eax
                writeASM('mov eax, z')
                writeASM('mov z, eax')

            else:
                eax = placeHolder[2]
                z = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(var4)
                writeASM('mov z, eax')

        else:
            print('Compiler: Error for temp3 in abc')

    elif (temp == 5): #basic math : 0 1 2 3 4 : y = a + b
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM('mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM('mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM('mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM('mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM('mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM('mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM('mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM('mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM('mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM('mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM('mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM('mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(var4)

        #does arithmetic and writes to txt assembly conversion

        if (placeHolder[0] == 'a'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                a = eax
                writeASM('add eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                a = eax
                writeASM('sub eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                a = eax
                writeASM('mult eax eax ebx')
                writeASM('mov a, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                a = eax
                writeASM('div eax eax ebx')
                writeASM('mov a, eax')

            else:
                print('Compiler: Error for Operator type in abc')
                
        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                b = eax
                writeASM('add eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                b = eax
                writeASM('sub eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                b = eax
                writeASM('mult eax eax ebx')
                writeASM('mov b, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                b = eax
                writeASM('div eax eax ebx')
                writeASM('mov b, eax')

            else:
                print('Compiler: Error for Operator type in abc')                

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                c = eax
                writeASM('add eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                c = eax
                writeASM('sub eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                c = eax
                writeASM('mult eax eax ebx')
                writeASM('mov c, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                c = eax
                writeASM('div eax eax ebx')
                writeASM('mov c, eax')

            else:
                print('Compiler: Error for Operator type in abc')   

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                x = eax
                writeASM('add eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                x = eax
                writeASM('sub eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                x = eax
                writeASM('mult eax eax ebx')
                writeASM('mov x, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                x = eax
                writeASM('div eax eax ebx')
                writeASM('mov x, eax')

            else:
                print('Compiler: Error for Operator type in abc')            

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                y = eax
                writeASM('add eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                y = eax
                writeASM('sub eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                y = eax
                writeASM('mult eax eax ebx')
                writeASM('mov y, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                y = eax
                writeASM('div eax eax ebx')
                writeASM('mov y, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                z = eax
                writeASM('add eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                z = eax
                writeASM('sub eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                z = eax
                writeASM('mult eax eax ebx')
                writeASM('mov z, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                z = eax
                writeASM('div eax eax ebx')
                writeASM('mov z, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        else:
            print ('Compiler: Error at temp5 abc')

    elif (temp == 7): #2 types for the math : Y = X + Z + 3 : 0 1 2 3 4 5 6
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM('mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM('mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM('mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM('mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM('mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM('mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM('mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM('mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM('mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM('mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM('mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM('mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(var4)
    
        #move varible to register ecx
        if (placeHolder[6] == 'a'):
            ecx = a
            writeASM('mov ecx, a')
        elif (placeHolder[6] == 'b'):
            ecx = b
            writeASM('mov ecx, b')
        elif (placeHolder[6] == 'c'):
            ecx = c
            writeASM('mov ecx, c')
        elif (placeHolder[6] == 'x'):
            ecx = x
            writeASM('mov ecx, x')
        elif (placeHolder[6] == 'y'):
            ecx = y
            writeASM('mov ecx, y')
        elif (placeHolder[6] == 'z'):
            ecx = c
            writeASM('mov ecx, z')
        else:
            ecx = placeHolder[6]
            var4 = 'mov ecx, ' + placeHolder[6]
            writeASM(var4)       
    
        #does double arithmetic and converts to assembly
        if (placeHolder[0] == 'a'): # Y = X + Z + 3 : 0 1 2 3 4 5 6
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    a = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    a = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    a = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    a = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    a = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    a = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    a = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    a = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    a = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    a = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    a = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    a = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    a = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    a = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    a = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    a = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic parta')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    b = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    b = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    b = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    b = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    b = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    b = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    b = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    b = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    b = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    b = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    b = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    b = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    b = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    b = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    b = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    b = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partb')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    c = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    c = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    c = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    c = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    c = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    c = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    c = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    c = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    c = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    c = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    c = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    c = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    c = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    c = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    c = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    c = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partc')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    x = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    x = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    x = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    x = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    x = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    x = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    x = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    x = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    x = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    x = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    x = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    x = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    x = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    x = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    x = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    x = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partx')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    y = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    y = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    y = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    y = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    y = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    y = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    y = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    y = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    y = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    y = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    y = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    y = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    y = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    y = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    y = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    y = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic party')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    z = eax
                    writeASM('addadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    z = eax
                    writeASM('addsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    z = eax
                    writeASM('addmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    z = eax
                    writeASM('adddiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    z = eax
                    writeASM('subadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    z = eax
                    writeASM('subsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    z = eax
                    writeASM('submult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    z = eax
                    writeASM('subdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    z = eax
                    writeASM('multadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    z = eax
                    writeASM('multsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    z = eax
                    writeASM('multmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    z = eax
                    writeASM('multdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    z = eax
                    writeASM('divadd eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    z = eax
                    writeASM('divsub eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    z = eax
                    writeASM('divmult eax eax ebx ecx')
                    writeASM('mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    z = eax
                    writeASM('divdiv eax eax ebx ecx')
                    writeASM('mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partz')

        else:
            print('Compiler: Error in temp7')

    else:
        print("MathStuff: Temp Length is not right")

    #flags will be thrown here
    #checks variables after math, then converts them to whats it'd actually read
    if (placeHolder[0] == 'a'): #unsigned range: 0 to 255
        if (a < 0):
            a = a-2**8  #signed = unsigned-2**8
        elif (a > 255):
            print('MathStuff: A is too big')
    elif (placeHolder[0] == 'b'): #unsigned range: 0 to 255
        if (b < 0):
            b = b-2**8  #signed = unsigned-2**8
        elif (b > 255):
            print('MathStuff: B is too big')
    elif (placeHolder[0] == 'c'): #unsigned range: 0 to 255
        if (c < 0):
            c = c-2**8  #signed = unsigned-2**8
        elif (c > 255):
            print('MathStuff: C is too big')
    elif (placeHolder[0] == 'x'): #signed range: -128 to 127
        if (x > 127):
            x = x+2**8 #unsigned = signed+2**8
        elif (x < -128):
            print('MathStuff: X is too small')
    elif (placeHolder[0] == 'y'): #signed range: -128 to 127
        if (y > 127):
            y = y+2**8 #unsigned = signed+2**8
        elif (y < -128):
            print('MathStuff: Y is too small')
    elif (placeHolder[0] == 'z'): #signed range: -128 to 127
        if (z > 127):
            z = z+2**8 #unsigned = signed+2**8
        elif (z < -128):
            print('MathStuff: Z is too small')
    else:
        print('MathStuff: unsigned/signed part check')

    return 0

#-----------------------------------------------------------------------------------------------------
#indent checker 
#-----------------------------------------------------------------------------------------------------
def checkIndent(filename, line_number):
    global indentCheck
    with open(filename, 'r') as file:
        for current_line_number, line in enumerate(file, start=1):
            if current_line_number == line_number and line.startswith('\t'):
                indentCheck = '\t'
                
            else:
                indentCheck = 'false'
    return 0

#-----------------------------------------------------------------------------------------------------
#parser
#-----------------------------------------------------------------------------------------------------
#as labels are being made, take note of the lineCounterASMR and save it to an array (Have a global varible that you add 1 to everytime you access it)
#more for the assembler

def betaParser (i):
    global a, b, c, x, y, z, whileCheck, ifCheck, whileCounter, eax, ebx, ecx, edx

    with open(fileName, 'r') as file:
        content = file.readlines()#reads all lines
        line2 = content[i] #gets line
        placeHolder = re.split('[ ]', line2)  #splits line into words : just a space, this is meant more for more than one split type though

    #statement to check if statment and else statments
    if (ifCheck == 'else' and elseCheck == 'false'):    #for if if statment was not good
        justPrint()
        return 0
    
    else:
        print('Compiler: Error for if/elseCheck')


    if (placeHolder[0] == "unsigned"):  #the varibles are consisnt with naming right?
        var4 = placeHolder[1] + ' dd $'
        writeASM(var4)       #FINISH Unsigned
        var4 = placeHolder[2] + ' dd $'
        writeASM(var4)
        var4 = placeHolder[3] + ' dd $'
        writeASM(var4)

    elif (placeHolder[0] == "signed"):
        var4 = placeHolder[1] + ' dd $'
        writeASM(var4)       #FINISH Signed
        var4 = placeHolder[2] + ' dd $'
        writeASM(var4)
        var4 = placeHolder[3] + ' dd $'
        writeASM(var4)

    elif (placeHolder[0] == "a" or "b" or "c" or "x" or "y" or "z"): #only positive range: 0 to 255
        #check lenght to figure out whats happening
        #3 = declaration, 5 = regular arithmetic, 7 = double arithmetic


        #do I have something check varibles for range, then output an error and convert them to how itd read in that situation?
        #like -12 reads as so and so for signed so it converts to binary -> 1's compliment -> converts to python to be stored


        #do if statements to check how many signed and unsigned varibales
        #actually, maybe put the changing of varibale at the end of the loop as a function
        mathStuff(placeHolder)    

    elif (placeHolder[0] == "if"): #Ex. y = 12 or y <= 3 : 1 2 3
        #check for type: <, >, <=, >=, =, !=

        #prints statement to assembly.txt
        var4 = 'cmp ' + placeHolder[1] + ', ' + placeHolder[3]
        writeASM(var4)

        if (placeHolder[2] == '<'):
            var4 = 'jl if'      #maybe have it re write this later

        elif (placeHolder[2] == '>'):
            var4 = 'jg if'      #maybe have it re write this later

        elif (placeHolder[2] == '<='):
            var4 = 'jle if'      #maybe have it re write this later

        elif (placeHolder[2] == '>='):
            var4 = 'jge if'      #maybe have it re write this later
            
        elif (placeHolder[2] == '!='):
            var4 = 'jne if'      #maybe have it re write this later

        elif (placeHolder[2] == '='):
            var4 = 'je if' 

        else:
            var4 = 'jmp else'

        #run outside of if to save space
        writeASM(var4)  #can put at end of if statement to make shorter
        writeASM('if:')

        #ifCheck will go to 'true' or 'else' depends on statement
        if (placeHolder[1] == 'a'): #if y > 0 : 0 1 2 3
            if (placeHolder[2] == '>'):
                if (a > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (a < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (a >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (a <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (a == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (a == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'b'):
            if (placeHolder[2] == '>'):
                if (b > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (b < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (b >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (b <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (b == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (b == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'c'):
            if (placeHolder[2] == '>'):
                if (c > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (c < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (c >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (c <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (c == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (c == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')      
            
        elif(placeHolder[1] == 'x'):
            if (placeHolder[2] == '>'):
                if (x > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (x < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (x >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (x <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (x == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (x == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'y'):
            if (placeHolder[2] == '>'):
                if (y > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (y < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (y >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (y <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (y == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (y == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'z'):
            if (placeHolder[2] == '>'):
                if (z > placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<'):
                if (z < placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '>='):
                if (z >= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '<='):
                if (z <= placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '='):
                if (z == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            elif (placeHolder[2] == '!='):
                if (z == placeHolder[3]):
                    ifCheck = 'true' 
                else:
                    ifCheck = 'else'

            else:
                print('Error in If statements')

        else:
            print('Compiler: Error for ifCheck creation')

    elif (placeHolder[0] == "else"):
        #make labels in assembly 
        writeASM('else:')

        if (ifCheck == 'true'):
            elseCheck = 'false'
        elif (ifCheck == 'else'):
            elseCheck = 'true'
        else:
            print('Compiler: Error in else')

    elif (placeHolder[0] == "while"):
        #don't need to worry about writing error, because it will overwrite itself
        whileCheck = 'true'
        whileStatement = placeHolder
        #the address is the line its on + 1

        #statement at end of parser to add to whileCounter

        #check statement, if its active.
        #prints statement to assembly.txt
        var4 = 'cmp ' + placeHolder[1] + ', ' + placeHolder[3]
        writeASM(var4)

        if (placeHolder[2] == '<'): # while y = 3
            var4 = 'jl while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>'):
            var4 = 'jg while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '<='):
            var4 = 'jle while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>='):
            var4 = 'jge while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter
            
        elif (placeHolder[2] == '!='):
            var4 = 'jne while'      #maybe have it re write this later
            writeASM(var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '='):
            var4 = 'je while'
            writeASM(var4)  #can put at end of if statement to make shorter 

        else:
            var4 = 'jmp end'
            writeASM(var4)  #can put at end of if statement to make shorter

        writeASM('while:')  #label for asm jump

        #while Check will go to 'true' or 'false' depends on statement
        if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
            if (placeHolder[2] == '>'):
                if (a > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (a < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (a >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (a <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (a == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (a == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'b'):
            if (placeHolder[2] == '>'):
                if (b > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (b < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (b >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (b <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (b == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (b == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'c'):
            if (placeHolder[2] == '>'):
                if (c > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (c < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (c >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (c <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (c == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (c == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')      
            
        elif(placeHolder[1] == 'x'):
            if (placeHolder[2] == '>'):
                if (x > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (x < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (x >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (x <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (x == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (x == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'y'):
            if (placeHolder[2] == '>'):
                if (y > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (y < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (y >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (y <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (y == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (y == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'z'):
            if (placeHolder[2] == '>'):
                if (z > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (z < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (z >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (z <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (z == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (z == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')

        else:
            print('Compiler: Error for whileCheck creation')

    elif (placeHolder[0] == "print"):   #also needs to be added to the assemlby conversion : print y : 0 1
        print(placeHolder[1])   #might need if statement for 

    else:
        print("Error for Parser")

    #while counter, to keep track of whats to be repeated
    if (whileCheck == 'true'): #Should be fine here, maybe move to top if need : possibly conflict with 1st time use
        #counts to keep track of where at
        whileCounter = whileCounter + 1

        #whileStatement #stores while statement at line to check later : Ex. while y > 4 : 0 1 2 3

        placeHolder = whileStatement #moves while statment in to check for while statment
        if (placeHolder[1] == 'a'): # while y > 0 : 0 1 2 3
            if (placeHolder[2] == '>'):
                if (a > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (a < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (a >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (a <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (a == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (a == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'b'):
            if (placeHolder[2] == '>'):
                if (b > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (b < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (b >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (b <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (b == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (b == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif (placeHolder[1] == 'c'):
            if (placeHolder[2] == '>'):
                if (c > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (c < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (c >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (c <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (c == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (c == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')      
            
        elif(placeHolder[1] == 'x'):
            if (placeHolder[2] == '>'):
                if (x > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (x < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (x >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (x <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (x == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (x == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'y'):
            if (placeHolder[2] == '>'):
                if (y > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (y < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (y >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (y <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (y == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (y == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')
            
        elif(placeHolder[1] == 'z'):
            if (placeHolder[2] == '>'):
                if (z > placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<'):
                if (z < placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '>='):
                if (z >= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '<='):
                if (z <= placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '='):
                if (z == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            elif (placeHolder[2] == '!='):
                if (z == placeHolder[3]):
                    whileCheck = 'true' 
                else:
                    whileCheck = 'false'

            else:
                print('Error in If statements')

        else:
            print('Compiler: Error for whileCheck creation')

            #checks if statment is still true after each line, if it is. Keep going, otherwise it changes whileCheck to false
        
    else: 
        whileCounter = 0

    return 0

#---------------------------------------------------------------------
#Start to run stuff together
#---------------------------------------------------------------------
def projectCompiler():
    global whileCheck, whileCounter, ifCheck, elseCheck, fileName, regChanges
    while (i >= 21):    #i = line number currently on
        #how do I know how long he file is?
        
        #function to check file number
        indentCheck = checkIndent(fileName, i)

        if (indentCheck == '\t'):  #implement indent checker
            betaParser(i)

        elif (whileCheck == 'true'):
            #resets while so that the lineCounterASMR and whileCounter are back where they started
            lineCounterASMR = lineCounterASMR - whileCounter #resets linecounterASMR to where while conversion started
            i = i - whileCounter - 1 # -1 because this check is an i : resets i to go back to HLC line
        
        else:
            #if this ends up in a funcion add global varibales
            #reset so they dont mistake them
            ifCheck = 'false'
            whileCheck = 'false'
            elseCheck = 'false'

            betaParser(i)
            print('Loop Error')
            


    
        
        

        #at the end, print out the variables results
        i = i + 1   #Loop ends here and restarts
    
    
    regChanges = regCheck()   #make sure it checks in the correct loop
    modReg.append(regChanges)
    

    #make array that stores all HLC lines according to assembly line conversion
    #instead of .txt
    return 0

