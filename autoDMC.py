# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:14:59 2023

@author: CHJ2LIZ
"""

import cv2
import json

def parseJson(jsonFile):
    with open(jsonFile) as f:
        d = json.load(f)
    print('Loaded: ', jsonFile)
    return d 

def getClosestDMC(codes, r, g, b):
    absDiff = 1000
    newCode = {}
    for code in codes:
        newDiff = abs(r-code["R"])+abs(g-code["G"])+abs(b-code["B"])
        if(newDiff < absDiff):
            absDiff=newDiff
            newCode = code
            
    return newCode
        

dmcCodes = parseJson("C:/Users/chj2liz/Documents/Python/AutoDMC/dmc_codes.json")

img = cv2.imread("C:/Users/chj2liz/Pictures/Chrysanthemum.jpg")
rows, cols = img.shape[:2]

print(rows, cols)

newHeight = 100
box = int(rows/newHeight)
newWidth = int(cols/box)
rowsLeftOut = rows - newHeight*box 
colsLeftOut = cols - newWidth*box

print(newHeight, newWidth)
print(rowsLeftOut, colsLeftOut)
print(rows/newHeight, box)


startRow = int(rowsLeftOut/2)
startCol = int(colsLeftOut/2)

x=0
y=0


outFile = open('out2.json', 'w')
outFile.write("[\n")

for y in range(newHeight):
    for x in range(newWidth):
        
        #Box for loop
        r=0
        g=0
        b=0
        for i in range(box):
            for j in range(box):
                color = img[y*box+j+startRow, x*box+i+startCol]
                #print(x*box+i+startCol, y*box+j+startRow, color)
                b += color[0]
                g += color[1]
                r += color[2]
        b = int(b/(box*box))
        g = int(g/(box*box))
        r = int(r/(box*box))
        
        newCode = getClosestDMC(dmcCodes, r, g, b)
        
        outFile.write("{\t\"X\":" + str(x) + ",\n")
        outFile.write("\t\"Y\":" + str(y) + ",\n")
        outFile.write("\t\"dmcCode\":\"" + newCode["code"] + "\",\n")
        outFile.write("\t\"dmcName\":\"" + newCode["name"] + "\",\n")
        outFile.write("\t\"R\":" + str(newCode["R"]) + ",\n")
        outFile.write("\t\"G\":" + str(newCode["G"]) + ",\n")
        outFile.write("\t\"B\":" + str(newCode["B"]) + ",\n")
        outFile.write("\t\"symbol\":\"\"\n},\n")
        
        
        
print(dmcCodes[0]["code"])    
        
        #print(x, y, r, g, b)
outFile.write("]")               
    
outFile.close()