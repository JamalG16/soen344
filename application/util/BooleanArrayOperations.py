# def filterOutBooleanList(listToFilter, delimiter):
#     booleanValuesList = []
#     for item in listToFilter:
#         time, value = item.split(delimiter)
#         if(value.lower() == 'false'):
#             booleanValuesList.append(False)
#         else:
#             booleanValuesList.append(True)
#     return booleanValuesList

def filterOutBooleanList(listToFilter):
    booleanValuesList=[]
    for item in listToFilter:
        if 'false' in item.lower():
            booleanValuesList.append(False)
        else:
            booleanValuesList.append(True)
    return booleanValuesList


def getCommonTimeslots(timeslot1, timeslot2):
    booleanList1 = filterOutBooleanList(timeslot1)
    booleanList2 = filterOutBooleanList(timeslot2)
    commonList=[]
    for x in range(len(booleanList1)):
        commonList.append(booleanList1[x]==booleanList2[x])
    return commonList

def concatenateBooleanLists(booleanList1, booleanList2):
    concatenatedBooleanList = []
    for x in range(len(booleanList1)):
            concatenatedBooleanList.append(booleanList1[x] | booleanList2[x])
    return concatenatedBooleanList
