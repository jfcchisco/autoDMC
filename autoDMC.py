# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 10:14:59 2023

@author: CHJ2LIZ
"""

import cv2
import json
import numpy as np

class stitchClass:
    def __init__(self, X, Y, dmcCode, dmcName, R, G, B, symbol):
        self.X = X
        self.Y = Y        
        self.dmcCode = dmcCode
        self.dmcName = dmcName
        self.R = R
        self.G = G
        self.B = B
        self.symbol = symbol

class colorClass:
    def __init__(self, newCode, count):
        self.code = newCode["code"]
        self.name = newCode["name"]
        self.R = newCode["R"]
        self.G = newCode["G"]
        self.B = newCode["B"]
        self.hexCode = newCode["hexCode"]
        self.count = count


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
    
def isNewColor(newColor, colors):
    for color in colors:
        if(color.code == newColor["code"]):
            return False
    return True


def reduceColors(colors, stitches, th):
    colors.sort(key=lambda x: x.count)
    
    
    while True:
        if(colors[0].count >= th):
            return colors, stitches
        
        colorToChange = colors[0]        
        colors.pop(0)
        
        absDiff=1000
        for color in colors:
            newDiff = abs(color.R - colorToChange.R) + abs(color.G - colorToChange.G) + abs(color.B - colorToChange.B)
            if(newDiff < absDiff):
                absDiff=newDiff
                newColor = color
                
        #Change all stitches to newColor
        for stitch in stitches:
            if(stitch.dmcCode == colorToChange.code):
                stitch.dmcCode = newColor.code
                stitch.dmcName = newColor.name
                stitch.R = newColor.R
                stitch.G = newColor.G
                stitch.B = newColor.B
                
                for color in colors:
                    if(color.code == newColor.code):
                        color.count += 1
        
        colors.sort(key=lambda x: x.count)
        
        
        
def assignSymbols(colors, stitches):
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwxyz!$%&/()=?+-#:_*.,;^°01234567890ABCDEFGHIJKLMNOPQRS"
    symbols = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", 
               "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", 
               "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", 
               "U", "V", "W", "Y", "Z", "a", "b", "c", "d", "e", 
               "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
               "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", 
               "z", "!", "$", "%", "&", "/", "(", ")", "=", "?", 
               "+", "-", "#", ":", "_", "*", ".", ",", ";", "^", 
               "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
               "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
               "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
               ]
    colors.sort(key=lambda x: x.count, reverse=True)
    
    i=0
    for color in colors:
        for stitch in stitches:
            if(stitch.dmcCode == color.code):
                stitch.symbol = symbols[i]
        i += 1
        
    return stitches
        
        
        
    
    
stitches = []
colors = []

dmcCodes = parseJson("C:/Users/chj2liz/Documents/Python/AutoDMC/dmc_codes.json")

img = cv2.imread("C:/Users/chj2liz/Pictures/Screenpresso/2023-10-18_09h54_23.jpg")
rows, cols = img.shape[:2]

#print(rows, cols)

newHeight = 100
box = int(rows/newHeight)
newWidth = int(cols/box)
rowsLeftOut = rows - newHeight*box 
colsLeftOut = cols - newWidth*box

#print(newHeight, newWidth)
#print(rowsLeftOut, colsLeftOut)
#print(rows/newHeight, box)


startRow = int(rowsLeftOut/2)
startCol = int(colsLeftOut/2)

x=0
y=0




for y in range(newHeight):
    for x in range(newWidth):
        
        #Box for loop
        r=0
        g=0
        b=0
        for i in range(box):
            for j in range(box):
                pixelColor = img[y*box+j+startRow, x*box+i+startCol]
                #print(x*box+i+startCol, y*box+j+startRow, color)
                b += pixelColor[0]
                g += pixelColor[1]
                r += pixelColor[2]
        b = int(b/(box*box))
        g = int(g/(box*box))
        r = int(r/(box*box))
        
        newCode = getClosestDMC(dmcCodes, r, g, b)
        
        stitches.append(stitchClass(x, y, newCode["code"], newCode["name"], newCode["R"], newCode["G"], newCode["B"], ""))
        
        if(isNewColor(newCode, colors)):
            colors.append(colorClass(newCode, 1))
        else:
            for color in colors:
                if(color.code == newCode["code"]):
                    color.count += 1
                
        
        
        
        #outFile.write(",\n")
        
print(len(stitches)) 
print(len(colors))

colors, stitches = reduceColors(colors, stitches, 1)  
stitches = assignSymbols(colors, stitches)

print(len(stitches)) 
print(len(colors))

outFile = open('out.json', 'w')
outFile.write("[\n")

for stitch in stitches:
    outFile.write("{\t\"X\":" + str(stitch.X) + ",\n")
    outFile.write("\t\"Y\":" + str(stitch.Y) + ",\n")
    outFile.write("\t\"dmcCode\":\"" + stitch.dmcCode + "\",\n")
    outFile.write("\t\"dmcName\":\"" + stitch.dmcName + "\",\n")
    outFile.write("\t\"R\":" + str(stitch.R) + ",\n")
    outFile.write("\t\"G\":" + str(stitch.G) + ",\n")
    outFile.write("\t\"B\":" + str(stitch.B) + ",\n")
    outFile.write("\t\"symbol\":\"" + stitch.symbol + "\"\n}")
    if(stitch.Y==newHeight-1 and stitch.X==newWidth-1): 
        outFile.write("\n")
    else: 
        outFile.write(",\n")

outFile.write("]")               
outFile.close()

#Create file to view
box = 10
image = np.zeros((newHeight*box, newWidth*box, 3), np.uint8)

for stitch in stitches:
    image = cv2.rectangle(image, (stitch.X*10, stitch.Y*10), (stitch.X*10+box, stitch.Y*10+box), (stitch.B, stitch.G, stitch.R), -1)

#cv2.imshow('Image', image)
cv2.imwrite("image.jpg", image)