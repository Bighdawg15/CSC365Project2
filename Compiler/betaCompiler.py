#-----------------------------------------------------------------------------------------------------
#Rules                  : Not very helpful
#-----------------------------------------------------------------------------------------------------
#Lines 1,2: Variables are declare at the top of the program. First unsigned, then signed. 
#           All variables are implicitly of type 8-bit integer. No need to declare that.  
#           Only 3 unsigned variables are allowed: a, b, c.  
#           Only 3 signed variables are allowed: x, y, z. 
#Lines 4-9: One assignment is performed per line. Don’t write b = 0, x = 4 etc 
#Lines 5,6,12,14: The four arithmetic operations allowed are + - * / 
#Line 6: A single line can have max of two arithmetic operations. Operators are evaluated left to right. 
#        For example, Line 6 means c = (b * a) / 10 
#Line 6: Only the integer part of an operation is preserved. So the output of Line 6 right-side is (18*3)/10 = 5 
#Lines 11,16: Two types of conditional structures are allowed: if-else and while loop. No nested structures. 
#Lines 11-21: Indentation indicates whether a line is inside an if-else or a while loop 
#Lines 11,16: Only a single relational operator is allowed in if and while statements. 
#             So if x > 10 && y < 5 is not allowed. 
#Lines 17-21: The print command is the only mechanism to output a value. 
#             There is no user input command, i.e. a cin equivalent 

#-----------------------------------------------------------------------------------------------------
#NOTES:
#-----------------------------------------------------------------------------------------------------
#If a varible was signed or unsigned. Would i need to have a manual check for if its outside of that number range so that it gives an error message?



#-----------------------------------------------------------------------------------------------------
#variables/imports
#-----------------------------------------------------------------------------------------------------
import re

#other files with needed functions
import ASM
import CSV

lineCounterASM = '' #their are 389 uses of this function, that I'll clean up later



i = 0
lineCounterASMR = 0 #for the ASM
whileCheck = 'false'
ifCheck = 'false'
elseCheck = 'false'
#lineCounterComp = 0 #for the HLC
#lineCounterM = 0 #machine code
indentCheck = 'false'
fileName = 'test.txt'

#only positive                  Range: 0 to 255  (unsigned)
a = 0
b = 0
c = 0

#both positive and negative     Range: -128 to 127  (Signed)
x = 0
y = 0
z = 0

#registers
#eax = 0
#ebx = 0
#ecx = 0
#edx = 0

#placeHolder registers (to check for changes)
eax2 = 0
ebx2 = 0
ecx2 = 0
edx2 = 0



#------------------------------------------------------------------
#Storage Management for Assembly
#------------------------------------------------------------------
stackCounter = 0

class Stack:
    def __init__(self):
        self.stack = [] #blank array to represent

    def push(self, register):
        stackCounter = stackCounter + 1 #To know where things located
        self.stack.append(register)

    def pop(self):
        stackCounter = stackCounter - 1 #To know where things are located
        if len(self.stack) < 1:
            return None
        return self.stack.pop()

    #stack = Stack() #create stack

    #stack.push('eax') #push variable

    #stack.pop()  #pop : output %eax : last in



#Memory:
    #eax = 0001
    #ebx = 0002
    #ecx = 0003
    #edx = 0004
    #a = 0005
    #b = 0006
    #c = 0007
    #x = 0008
    #y = 0009
    #z = 0010
    #line 0 = 0011 -> Increments up for storage
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

#-----------------------------------------------------
#writeASM fucntion (for HLC to ASM)
#-----------------------------------------------------
def writeASM (lineCounterASM, new_line):    #doeslinCounterASM need to be imported?
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
        writeASM(lineCounterASM, var4)

    elif (temp == 5): #y = a + b : 0 1 2 3 4 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(lineCounterASM, var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(lineCounterASM, var4)

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

        writeASM(lineCounterASM, var4)
        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(lineCounterASM, var4)

    elif (temp == 7): #y = a + b - c : 0 1 2 3 4 5 6 
        var4 = 'mov eax, ' + placeHolder[2]
        writeASM(lineCounterASM, var4)
        var4 = 'mov ebx, ' + placeHolder[4]
        writeASM(lineCounterASM, var4)
        var4 = 'mov ebc, ' + placeHolder[6]
        writeASM(lineCounterASM, var4)
        
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
        writeASM(lineCounterASM, var4)

        var4 = 'mov ' + placeHolder[0] + ', eax'
        writeASM(lineCounterASM, var4)

    else:
        print('justPrint: Temp Error')

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
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                a = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                a = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                a = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                a = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                a = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov a, eax')

            else:
                eax = placeHolder[2]
                a = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov a, eax')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[2] == 'a'):
                eax = a
                b = eax
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                b = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                b = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                b = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                b = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                b = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov b, eax')

            else:
                eax = placeHolder[2]
                b = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov b, eax')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[2] == 'a'):
                eax = a
                c = eax
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                c = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                c = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                c = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                c = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                c = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov c, eax')

            else:
                eax = placeHolder[2]
                c = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov c, eax')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[2] == 'a'):
                eax = a
                x = eax
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                x = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                x = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                x = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                x = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                x = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov x, eax')

            else:
                eax = placeHolder[2]
                x = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov x, eax')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[2] == 'a'):
                eax = a
                y = eax
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                y = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                y = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                y = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                y = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                y = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov y, eax')

            else:
                eax = placeHolder[2]
                y = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov y, eax')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[2] == 'a'):
                eax = a
                z = eax
                writeASM(lineCounterASM, 'mov eax, a')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[2] == 'b'):
                eax = b
                z = eax
                writeASM(lineCounterASM, 'mov eax, b')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[2] == 'c'):
                eax = c
                z = eax
                writeASM(lineCounterASM, 'mov eax, c')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[2] == 'x'):
                eax = x
                z = eax
                writeASM(lineCounterASM, 'mov eax, x')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[2] == 'y'):
                eax = y
                z = eax
                writeASM(lineCounterASM, 'mov eax, y')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[2] == 'z'):
                eax = z
                z = eax
                writeASM(lineCounterASM, 'mov eax, z')
                writeASM(lineCounterASM, 'mov z, eax')

            else:
                eax = placeHolder[2]
                z = eax
                var4 = 'mov eax, ' + placeHolder[2]
                writeASM(lineCounterASM, var4)
                writeASM(lineCounterASM, 'mov z, eax')

        else:
            print('Compiler: Error for temp3 in abc')

    elif (temp == 5): #basic math : 0 1 2 3 4 : y = a + b
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM(lineCounterASM, 'mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM(lineCounterASM, 'mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM(lineCounterASM, 'mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM(lineCounterASM, 'mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM(lineCounterASM, 'mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM(lineCounterASM, 'mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(lineCounterASM, var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM(lineCounterASM, 'mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM(lineCounterASM, 'mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM(lineCounterASM, 'mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM(lineCounterASM, 'mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM(lineCounterASM, 'mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM(lineCounterASM, 'mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(lineCounterASM, var4)

        #does arithmetic and writes to txt assembly conversion

        if (placeHolder[0] == 'a'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                a = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                a = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                a = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov a, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                a = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov a, eax')

            else:
                print('Compiler: Error for Operator type in abc')
                
        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                b = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                b = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                b = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov b, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                b = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov b, eax')

            else:
                print('Compiler: Error for Operator type in abc')                

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                c = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                c = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                c = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov c, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                c = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov c, eax')

            else:
                print('Compiler: Error for Operator type in abc')   

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                x = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                x = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                x = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov x, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                x = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov x, eax')

            else:
                print('Compiler: Error for Operator type in abc')            

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                y = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                y = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                y = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov y, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                y = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov y, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                eax = eax + ebx
                z = eax
                writeASM(lineCounterASM, 'add eax eax ebx')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[3] == '-'):
                eax = eax - ebx
                z = eax
                writeASM(lineCounterASM, 'sub eax eax ebx')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[3] == '*'):
                eax = eax * ebx
                z = eax
                writeASM(lineCounterASM, 'mult eax eax ebx')
                writeASM(lineCounterASM, 'mov z, eax')

            elif (placeHolder[3] == '/'):
                eax = eax / ebx
                z = eax
                writeASM(lineCounterASM, 'div eax eax ebx')
                writeASM(lineCounterASM, 'mov z, eax')

            else:
                print('Compiler: Error for Operator type in abc')

        else:
            print ('Compiler: Error at temp5 abc')

    elif (temp == 7): #2 types for the math : Y = X + Z + 3 : 0 1 2 3 4 5 6
        #move varible to register eax
        if (placeHolder[2] == 'a'): 
            eax = a
            writeASM(lineCounterASM, 'mov eax, a')
        elif (placeHolder[2] == 'b'):
            eax = b
            writeASM(lineCounterASM, 'mov eax, b')
        elif (placeHolder[2] == 'c'):
            eax = c
            writeASM(lineCounterASM, 'mov eax, c')
        elif (placeHolder[2] == 'x'):
            eax = x
            writeASM(lineCounterASM, 'mov eax, x')
        elif (placeHolder[2] == 'y'):
            eax = y
            writeASM(lineCounterASM, 'mov eax, y') 
        elif (placeHolder[2] == 'z'):
            eax = z
            writeASM(lineCounterASM, 'mov eax, z')
        else:
            eax = placeHolder[2]
            var4 = 'mov eax, ' + placeHolder[2]
            writeASM(lineCounterASM, var4)

        #move varible to register ebx
        if (placeHolder[4] == 'a'):
            ebx = a
            writeASM(lineCounterASM, 'mov ebx, a')
        elif (placeHolder[4] == 'b'):
            ebx = b
            writeASM(lineCounterASM, 'mov ebx, b')
        elif (placeHolder[4] == 'c'):
            ebx = c
            writeASM(lineCounterASM, 'mov ebx, c')
        elif (placeHolder[4] == 'x'):
            ebx = x
            writeASM(lineCounterASM, 'mov ebx, x')
        elif (placeHolder[4] == 'y'):
            ebx = y
            writeASM(lineCounterASM, 'mov ebx, y')
        elif (placeHolder[4] == 'z'):
            ebx = c
            writeASM(lineCounterASM, 'mov ebx, z')
        else:
            ebx = placeHolder[4]
            var4 = 'mov ebx, ' + placeHolder[4]
            writeASM(lineCounterASM, var4)
    
        #move varible to register ecx
        if (placeHolder[6] == 'a'):
            ecx = a
            writeASM(lineCounterASM, 'mov ecx, a')
        elif (placeHolder[6] == 'b'):
            ecx = b
            writeASM(lineCounterASM, 'mov ecx, b')
        elif (placeHolder[6] == 'c'):
            ecx = c
            writeASM(lineCounterASM, 'mov ecx, c')
        elif (placeHolder[6] == 'x'):
            ecx = x
            writeASM(lineCounterASM, 'mov ecx, x')
        elif (placeHolder[6] == 'y'):
            ecx = y
            writeASM(lineCounterASM, 'mov ecx, y')
        elif (placeHolder[6] == 'z'):
            ecx = c
            writeASM(lineCounterASM, 'mov ecx, z')
        else:
            ecx = placeHolder[6]
            var4 = 'mov ecx, ' + placeHolder[6]
            writeASM(lineCounterASM, var4)       
    
        #does double arithmetic and converts to assembly
        if (placeHolder[0] == 'a'): # Y = X + Z + 3 : 0 1 2 3 4 5 6
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    a = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    a = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    a = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    a = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    a = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    a = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    a = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    a = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    a = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    a = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    a = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    a = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    a = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    a = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    a = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    a = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic parta')

        elif (placeHolder[0] == 'b'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    b = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    b = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    b = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    b = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    b = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    b = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    b = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    b = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    b = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    b = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    b = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    b = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    b = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    b = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    b = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    b = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov b, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partb')

        elif (placeHolder[0] == 'c'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    c = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    c = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    c = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    c = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    c = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    c = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    c = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    c = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    c = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    c = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    c = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    c = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    c = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    c = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    c = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    c = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov c, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partc')

        elif (placeHolder[0] == 'x'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    x = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    x = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    x = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    x = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    x = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    x = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    x = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    x = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov a, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    x = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    x = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    x = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    x = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    x = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    x = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    x = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    x = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov x, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partx')

        elif (placeHolder[0] == 'y'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    y = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    y = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    y = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    y = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    y = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    y = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    y = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    y = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    y = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    y = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    y = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    y = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    y = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    y = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    y = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    y = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov y, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic party')

        elif (placeHolder[0] == 'z'):
            if (placeHolder[3] == '+'):
                if (placeHolder[5] == '+'):
                    eax = eax + ebx + ecx
                    z = eax
                    writeASM(lineCounterASM, 'addadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax + ebx - ecx
                    z = eax
                    writeASM(lineCounterASM, 'addsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax + ebx * ecx
                    z = eax
                    writeASM(lineCounterASM, 'addmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax + ebx / ecx
                    z = eax
                    writeASM(lineCounterASM, 'adddiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')

            elif (placeHolder[3] == '-'):
                if (placeHolder[5] == '+'):
                    eax = eax - ebx + ecx
                    z = eax
                    writeASM(lineCounterASM, 'subadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax - ebx - ecx
                    z = eax
                    writeASM(lineCounterASM, 'subsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax - ebx * ecx
                    z = eax
                    writeASM(lineCounterASM, 'submult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax - ebx / ecx
                    z = eax
                    writeASM(lineCounterASM, 'subdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '*'):
                if (placeHolder[5] == '+'):
                    eax = eax * ebx + ecx
                    z = eax
                    writeASM(lineCounterASM, 'multadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax * ebx - ecx
                    z = eax
                    writeASM(lineCounterASM, 'multsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax * ebx * ecx
                    z = eax
                    writeASM(lineCounterASM, 'multmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax * ebx / ecx
                    z = eax
                    writeASM(lineCounterASM, 'multdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            elif (placeHolder[3] == '/'):
                if (placeHolder[5] == '+'):
                    eax = eax / ebx + ecx
                    z = eax
                    writeASM(lineCounterASM, 'divadd eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '-'):
                    eax = eax / ebx - ecx
                    z = eax
                    writeASM(lineCounterASM, 'divsub eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '*'):
                    eax = eax / ebx * ecx
                    z = eax
                    writeASM(lineCounterASM, 'divmult eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                elif (placeHolder[5] == '/'):
                    eax = eax / ebx / ecx
                    z = eax
                    writeASM(lineCounterASM, 'divdiv eax eax ebx ecx')
                    writeASM(lineCounterASM, 'mov z, eax')

                else:
                    print('Compiler: Error in temp7 equations')
            
            else:
                print('Compiler: Error in a double arithmetic partz')

        else:
            print('Compiler: Error in temp7')

    else:
        print("MathStuff: Temp Length is not right")

    return eax, ebx, ecx, edx, a, b, c, x, y, z

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
        writeASM(lineCounterASM, var4)       #FINISH Unsigned
        var4 = placeHolder[2] + ' dd $'
        writeASM(lineCounterASM, var4)
        var4 = placeHolder[3] + ' dd $'
        writeASM(lineCounterASM, var4)

    elif (placeHolder[0] == "signed"):
        var4 = placeHolder[1] + ' dd $'
        writeASM(lineCounterASM, var4)       #FINISH Signed
        var4 = placeHolder[2] + ' dd $'
        writeASM(lineCounterASM, var4)
        var4 = placeHolder[3] + ' dd $'
        writeASM(lineCounterASM, var4)

    elif (placeHolder[0] == "a" or "b" or "c" or "x" or "y" or "z"): #only positive range: 0 to 255
        #check lenght to figure out whats happening
        #3 = declaration, 5 = regular arithmetic, 7 = double arithmetic


        #do I have something check varibles for range, then output an error and convert them to how itd read in that situation?
        #like -12 reads as so and so for signed so it converts to binary -> 1's compliment -> converts to python to be stored


        #do if statements to check how many signed and unsigned varibales
        #actually, maybe put the changing of varibale at the end of the loop as a function
        mathStuff(placeHolder)    

    elif (placeHolder[0] == "if"): #Ex. y = 12 or y <= 3 : 1 2 3
        #worry about indentation
        #check for specific variable
        #check for type: <, >, <=, >=, =, !=
        
        #Checks for variable, then sign, then it uses the statement to create a variable that changes whats read
        #ifCheck: Can = 'true' or 'else'

        #how does it remember the address for jump
        #maybe incorporate with the counting system
        #typically creaets labels and jumps from that


        #prints statement to assembly.txt
        var4 = 'cmp ' + placeHolder[1] + ', ' + placeHolder[3]
        writeASM(lineCounterASM, var4)

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
        writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter
        writeASM(lineCounterASM, 'if:')

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
    #if statments off by one placeholder

    elif (placeHolder[0] == "else"):
        #make labels in assembly 
        writeASM(lineCounterASM, 'else:')

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
        writeASM(lineCounterASM, var4)

        if (placeHolder[2] == '<'): # while y = 3
            var4 = 'jl while'      #maybe have it re write this later
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>'):
            var4 = 'jg while'      #maybe have it re write this later
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '<='):
            var4 = 'jle while'      #maybe have it re write this later
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '>='):
            var4 = 'jge while'      #maybe have it re write this later
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter
            
        elif (placeHolder[2] == '!='):
            var4 = 'jne while'      #maybe have it re write this later
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter

        elif (placeHolder[2] == '='):
            var4 = 'je while'
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter 

        else:
            var4 = 'jmp end'
            writeASM(lineCounterASM, var4)  #can put at end of if statement to make shorter

        writeASM(lineCounterASM, 'while:')  #label for asm jump

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






            #checks if statment is still true after each line, if it is. Keep going , otherwise it changes whileCheck to false
        
    else: 
        whileCounter = 0


    return 0

#---------------------------------------------------------------------
#Start to run stuff
#---------------------------------------------------------------------

#i = 0   #Define  i, which is correspondent to line #
#indentCheck = 'false'
#ifCheck = 'false'
#whileCheck = 'false'

#how to get variables outside of functions



#probably make a function that runs all
while (i >= 21):    #i = line number currently on
    #how do I know how long he file is?
    
    #function to check file number
    checkIndent(fileName, i)

    if (indentCheck == '\t'):  #implement indent checker
        betaParser(i)

    elif (whileCheck == 'true'):
        #resets while so that the lineCounterASMR and whileCounter are back where they started
        lineCounterASMR = lineCounterASMR - whileCounter #resets linecounterASMR to where while conversion started
        i = i - whileCounter - 1 # -1 because this check is an i : resets i to go back to HLC line
       

    else:
        #if this ends up in a funcion add global varibales
        ifCheck = 'false'
        whileCheck = 'false'
        elseCheck = 'false'

        betaParser(i)
        print('Loop Error')
        #reset so they dont mistake them
        

        #lineCounterComp = lineCounterComp + 1   #increments lines instead of trying to do them
        #betaParser(i)   #Parse line
                        #Function to conver to assembly, also prints conversion to text file
                        #Converts ASM to Machine Code (Just a loop to check each assembly line conversion and printing to seperate text file)

    #make csv file in here, line by line
    
    #might be easier in the function
    regCheck()   #make sure it checks in the correct loop

    #might need to make seperate counters for both the assembly and the compiler

    #at the end, print out the variables results
    i = i + 1   #Loop ends here and restarts

