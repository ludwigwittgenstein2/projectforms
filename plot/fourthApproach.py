#fourthApproach for finding lower trend in Top list

import yaml
import sys
import csv

customerSaleDict = {}
customerQuarterSalesDict = {}
topCompleteHouseHoldList = []

def readCSV():
    global customerSaleDict
    global customerQuarterSalesDict
    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
        for row in data:
            salesValue = (round(float(row[5])))

            if row[0] not in customerSaleDict:
                customerSaleDict[row[0]] = salesValue
            else:
                customerSaleDict[row[0]] += salesValue

            if row[0] not in customerQuarterSalesDict:
                customerQuarterSalesDict[row[0]]= {}
                customerQuarterSalesDict[row[0]][0] = 0
                customerQuarterSalesDict[row[0]][1] = 0
                customerQuarterSalesDict[row[0]][2] = 0
                customerQuarterSalesDict[row[0]][3] = 0

                if int(row[9]) >= 0 and int(row[9]) <26:
                    customerQuarterSalesDict[row[0]][0] = salesValue
                elif int(row[9]) >= 26 and int(row[9]) <51:
                    customerQuarterSalesDict[row[0]][1] = salesValue
                elif int(row[9]) >=51 and int(row[9]) < 76:
                    customerQuarterSalesDict[row[0]][2] = salesValue
                elif int(row[9]) >= 76 and int (row[9]) < 103:
                    customerQuarterSalesDict[row[0]][3] = salesValue
                else:
                    continue
            else:
                if int(row[9]) >= 0 and int(row[9]) <26:
                    customerQuarterSalesDict[row[0]][0] += salesValue
                elif int(row[9]) >= 26 and int(row[9]) <51:
                    customerQuarterSalesDict[row[0]][1] += salesValue
                elif int(row[9]) >=51 and int(row[9]) < 76:
                    customerQuarterSalesDict[row[0]][2] += salesValue
                elif int(row[9]) >= 76 and int (row[9]) < 103:
                    customerQuarterSalesDict[row[0]][3] += salesValue
                else:
                    continue
    f.close()

with open("/Users/Rick/Desktop/segments/customerSaleDict.yaml", 'w') as f:
    f.write(yaml.dump(customerSaleDict,default_flow_style=False))
f.close()

with open("/Users/Rick/Desktop/segments/customerQuarterSalesDict.yaml", 'w' ) as f:
    f.write(yaml.dump(customerQuarterSalesDict,default_flow_style=False))
f.close()

def buildBottomList():
    global topCompleteHouseHoldList
    for houseHoldKey, salesValue in sorted(customerSaleDict.items(), key=lambda k:k[1]):
        topCompleteHouseHoldList.append(houseHoldKey)
    print topCompleteHouseHoldList

with open('/Users/Rick/Desktop/segments/topCompleteHouseHoldList', 'wb' ) as f:
    f.write(yaml.dump(topCompleteHouseHoldList,default_flow_style=False))
f.close()


def selectDecreaseTrendCustomer():
    with open("/Users/Rick/Desktop/segments/selectDecreaseTrendCustomer.yaml", 'r' ) as f:
        customerQuarterSalesDict =  yaml.load(f)
    f.close()

    with open('/Users/Rick/Desktop/segments/topCompleteHouseHoldList', 'r' ) as f:
        topCompleteHouseHoldList  = yaml.load(f)
    f.close()

    count = 0
    for houseHoldKeyValue in topCompleteHouseHoldList:
        for houseHoldKey, quarterDict in customerQuarterSalesDict.items():
            if houseHoldKeyValue == houseHoldKey:
                if count == 10:
                    break
                Quarterly_list = [['week_no', 'sales_value']]
                if (( quarterDict[0] <= quarterDict[1] ) and ( quarterDict[1] <= quarterDict[2] ) and ( quarterDict[2] <= quarterDict[3] )):
                    for quarterNo, salesValue in sorted(quarterDict.items(), key=lambda k:int(k[0])):
                        Quarterly_list.append([quarterNo, salesValue])
                    print houseHoldKey, Quarterly_list
                    count +=1

def main():
    readCSV()
    buildBottomList()
    selectDecreasedTrendCustomer()
if __name__ =="__main__":
    main()
