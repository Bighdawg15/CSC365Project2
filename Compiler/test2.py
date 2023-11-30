#---------------------------------------------------------------
#varibales/imports
#---------------------------------------------------------------
#file imports for functions
import ASM
import betaCompiler
import CSV

#---------------------------------------------------------------
#here to test certain functions seperately
#---------------------------------------------------------------


#import pathlib
#t = pathlib.Path(__file__) # get the path of the current file
#print(t)


#C:\Users\harle\OneDrive\Documents\GitHub\CSC-365--Project-2\Compiler\Outputs\assembly.txt
p = 0

fileName = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\HighLevelCode.txt")
fileName2 = ("C:\\Users\harle\OneDrive\Documents\GitHub\CSC365Project2\Compiler\Outputs\Assembly.txt")




#'C:\\Users\harle\OneDrive\Documents\GitHub\CSC-365--Project-2\Compiler\Outputs\assembly.txt'     #r'C:/Users/harle/OneDrive/Documents/GitHub/CSC-365--Project-2/Compiler/assembly.txt'
lenG = CSV.lineCount(fileName2)

while(p < lenG):
    ASM.assembler(fileName2, p)
    p = p + 1


    #Assembler:
    #puts 0000 as end of all : it store while space as slot 2 :|
    #doesn't handle indents