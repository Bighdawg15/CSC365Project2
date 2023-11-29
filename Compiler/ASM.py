#---------------------------------------------------
#Stack stuff (Allows pushing and poping onto a stack)
#---------------------------------------------------
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

#How it works:

#create a stack
    #stack = Stack() 

#Push registers to the stack
    #stack.push('eax')
    #stack.push('ebx')
    #stack.push('ecx')

#How to Pop registers from the stack (just an example)
    #print(stack.pop())  # Outputs: %ecx
    #print(stack.pop())  # Outputs: %ebx
    #print(stack.pop())  # Outputs: %eax



#Memory:
    #eax = 0001
    #ebx = 0002
    #ecx = 0003
    #edx = 0004
    #line 0 = 0011 -> Increments up for storage

#---------------------------------------------------
#Variables
#---------------------------------------------------
import re

lineCounter = 0 #here till error is fixed with all writeBack functions
lineCounterM = 0 #count lines for MACHINE CODE
array = {}
i = 1

#---------------------------------------------------
#writeBack Function (Writes to new txt file)
#---------------------------------------------------
def writeBack (lineCounter, new_line):  #can't just append 1 line apparently
    global lineCounterM #global, other counter was mistake, too far gone
    lineCounterM = lineCounterM + 1   #increment machine lines as added
    #new_line = 'This is the new text for line 3\n'

    #reads all lines
    with open('machine.txt', 'r') as f:
        lines = f.readlines()

    #modify specific line
    if lineCounterM - 1 < len(lines):
        lines[lineCounterM - 1] = new_line
    else:
        lines.append(new_line)  # Append the new line if the file has fewer lines

    #write all lines back to the file
    with open('machine.txt', 'w') as f:
        f.writelines(lines)

    return 0

#-----------------------------------------------------
def assembler(i):
    #Incrementing is temporary, their is one in the other file
    #lineCounter = lineCounter + 1   #increments for each line : REMOVE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    with open('assembly.txt', 'r') as g:    #opens file that is going to be converted
        line2 = g.readlines()   #saves whole value to varuable
        line2b = line2[i]   #saves specified line to variable
        line2c = re.split('[, ]', line2b) #splits line up at whitespaces and ,        {If this doesnt work do 'line2b.split() + line2b.split(',')}

    if (line2c[0] == "a"):  #Check the varibles
        writeBack(lineCounter, 'FF 0005')    #FF (Variable) 0000 (Memory Location)

    elif (line2c[0] == "b"):
        writeBack(lineCounter, 'FF 0006')

    elif (line2c[0] == "c"):
        writeBack(lineCounter, 'FF 0007')

    elif (line2c[0] == "x"):
        writeBack(lineCounter, 'FF 0008')

    elif (line2c[0] == "y"):
        writeBack(lineCounter, 'FF 0009')

    elif (line2c[0] == "z"):
        writeBack(lineCounter, 'FF 0010')

    elif (line2c[0] == "mov"): 
        #this is where I'd add in a check for if a register was changed
        var1 = line2c[1]
        var2 = line2c[2]
    
        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        elif (var1 == "a"):
            var1 = '0005 '
        elif (var1 == "b"):
            var1 = '0006 '
        elif (var1 == "c"):
            var1 = '0007 '
        elif (var1 == "x"):
            var1 = '0008 '
        elif (var1 == "y"):
            var1 = '0009 '
        elif (var1 == "z"):
            var1 = '0010 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        elif (var2 == "a"):
            var2 = '0005 '
        elif (var2 == "b"):
            var2 = '0006 '
        elif (var2 == "c"):
            var2 = '0007 '
        elif (var2 == "x"):
            var2 = '0008 '
        elif (var2 == "y"):
            var2 = '0009 '
        elif (var2 == "z"):
            var2 = '0010 '
        else:
            var2 = '0000 '  #representation for just numbers


        var4 = '00 ' + var1 + var2 
        writeBack(lineCounter, var4)

    elif (line2c[0] == "add"):  # add xxxx xxxx xxxx : 0 1 2 3
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'A ' + var1 + var2 + var3
        writeBack(lineCounter, var4)
       
    elif (line2c[0] == "sub"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'B ' + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "mult"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'C ' + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "div"):
        var1 = line2c[1]
        var2 = line2c[2]
        var3 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'D ' + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "addadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AA ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "addsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AB ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "adddiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AC ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "addmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'AD ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "subadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BA ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "subsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BB ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "submult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BC ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "subdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'BD '+ var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "multadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CA '+ var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "multsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CB ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "multmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CC ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "multdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'CD ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "divadd"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DA ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "divsub"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DB ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "divmult"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DC ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "divdiv"):
        var0 = line2c[1]
        var1 = line2c[2]
        var2 = line2c[3]
        var3 = line2c[4]

        #Statments to check for certain registers
        if (var0 == "eax"):
            var0 = '0001 '
        elif (var0 == "ebx"):
            var0 = '0002 '
        elif (var0 == "ecx"):
            var0 = '0003 '
        elif (var0 == "edx"):
            var0 = '0004 '
        else:
            var1 = '0000 '

        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '

        if (var3 == "eax"):
            var3 = '0001'
        elif (var3 == "ebx"):
            var3 = '0002'
        elif (var3 == "ecx"):
            var3 = '0003'
        elif (var3 == "edx"):
            var3 = '0004'
        else:
            var3 = '0000'

        var4 = 'DD ' + var0 + var1 + var2 + var3
        writeBack(lineCounter, var4)

    elif (line2c[0] == "cmp"):
        var1 = line2c[2]
        var2 = line2c[3]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000 '
        
        if (var2 == "eax"):
            var2 = '0001 '
        elif (var2 == "ebx"):
            var2 = '0002 '
        elif (var2 == "ecx"):
            var2 = '0003 '
        elif (var2 == "edx"):
            var2 = '0004 '
        else:
            var2 = '0000 '


        var4 = 'CC ' + var1 + var2
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jmp"):
        var4 = 'E0 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jl"):
        var4 = 'E1 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jle"):
        var4 = 'E2 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jg"):
        var4 = 'E3 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jge"):
        var4 = 'E4 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "jne"):
        var4 = 'E5 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "je"):
        var4 = 'E6 ' + line2c[1]
        writeBack(lineCounter, var4)

    elif (line2c[0] == "push"):
        var1 = line2c[1]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000'   #Might actual cause an error

        var4 = 'FA ' + var1
        writeBack(lineCounter, var4)

    elif (line2c[0] == "pop"):
        var1 = line2c[1]

        #Statments to check for certain registers
        if (var1 == "eax"):
            var1 = '0001 '
        elif (var1 == "ebx"):
            var1 = '0002 '
        elif (var1 == "ecx"):
            var1 = '0003 '
        elif (var1 == "edx"):
            var1 = '0004 '
        else:
            var1 = '0000'   #Might actual cause an error

        var4 = 'FF' + var1
        writeBack(lineCounter, var4)

    elif (line2c[0] == ""): #checks for blank lines : Don't know if we actually need this
        writeBack(lineCounter, "")

    elif (line2c[0].endswith == ":"):
        global array
        array.append(lineCounterM)


    else:
        #error handling
        print("Error at assembler at line ", lineCounterM)
    

    #idea of putting a blank row for csv indication : writeBack(lineCounter, '')
    return 0

