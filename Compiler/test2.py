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
fileName = 'c:\\Users\harle\OneDrive\Documents\GitHub\CSC-365--Project-2\Compiler\Outputs\test.txt'
#'C:\\Users\harle\OneDrive\Documents\GitHub\CSC-365--Project-2\Compiler\Outputs\assembly.txt'     #r'C:/Users/harle/OneDrive/Documents/GitHub/CSC-365--Project-2/Compiler/assembly.txt'
lenG = CSV.lineCount(fileName)

while(p < lenG):
    ASM.assembler(fileName, p)
    p = p + 1