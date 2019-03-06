def main():
    print("hello world")
    binaryString1 = convertBooleanListToBinaryString([False,False, True,False,True])
    print(binaryString1)
    booleanArray1 = convertBinaryStringToBooleanList(binaryString1)
    print(booleanArray1)

    binaryString2 = convertBooleanListToBinaryString([False, True, True, False, True])
    print(binaryString2)
    booleanArray2 = convertBinaryStringToBooleanList(binaryString2)
    print(booleanArray2)

    ten = '01010'
    twelve = '01100'
    print(andTwoBinaryStrings(binaryString1,binaryString2))
    print(convertIntegerToBooleanList(andTwoBinaryStrings(binaryString1, binaryString2)))


    testList=['alpha:True','beta:False','gamma:True']
    print(filterOutBooleanList(testList,':'))


def convertBooleanListToBinaryString(booleanList):
    return ''.join(['1' if x else '0' for x in booleanList])

def convertIntegerToBooleanList(integer):
    print(str(integer))
    stringed = format(integer,"036b")
    return convertBinaryStringToBooleanList(stringed)

def convertBinaryStringToBooleanList(binaryString):
    booleanList=[]
    for bit in binaryString:
        if bit=='1': booleanList.append(True)
        else: booleanList.append(False)
    return booleanList

def andTwoBinaryStrings(string1, string2):
    return int(string1,2) & int(string2,2)

def filterOutBooleanList(listToFilter, delimiter):
    booleanValuesList = []
    for item in listToFilter:
        time, value = item.split(delimiter)
        if(value.lower() == 'false'):
            booleanValuesList.append(False)
        else:
            booleanValuesList.append(True)
    return booleanValuesList

if __name__ == "__main__":
    main()
