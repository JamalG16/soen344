def main():
    print("hello world")
    binaryString = convertBooleanListToBinaryString([True,False,True])
    print(binaryString)
    booleanArray = convertBinaryStringToBooleanList(binaryString)
    print(booleanArray)


def convertBooleanListToBinaryString(booleanList):
    return ''.join(['1' if x else '0' for x in booleanList])

def convertBinaryStringToBooleanList(binaryString):
    booleanList=[]
    for bit in binaryString:
        if bit=='1': booleanList.append(True)
        else: booleanList.append(False)
    return booleanList


if __name__ == "__main__":
    main()