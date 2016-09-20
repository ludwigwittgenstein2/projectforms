#!/usr/bin/python

#fourthApproach for finding lower trend in Top list
import yaml
import sys
import csv

customerSaleDict = {}
customerQuarterSaleDict = {}
topCompleteHouseHoldList = []

def readCSV():
    global customerSaleDict
    global customerQuarterSaleDict
    with open("/Users/Rick/Desktop/CSV/transaction_data2.csv", 'r') as f:
        data = csv.reader(f, delimiter=',')
        next(data)
        for row in data:
            saleValue = (round(float(row[5])))

            if row[0] not in customerSaleDict:
                customerSaleDict[row[0]] = saleValue
            else:
                customerSaleDict[row[0]] += saleValue

            if row[0] not in customerQuarterSaleDict:
                customerQuarterSaleDict[row[0]]= {}
                customerQuarterSaleDict[row[0]][0] = 0
                customerQuarterSaleDict[row[0]][1] = 0
                customerQuarterSaleDict[row[0]][2] = 0
                customerQuarterSaleDict[row[0]][3] = 0

                if int(row[9]) >= 0 and int(row[9]) <26:
                    customerQuarterSaleDict[row[0]][0] = saleValue
                elif int(row[9]) >= 26 and int(row[9]) <51:
                    customerQuarterSaleDict[row[0]][1] = saleValue
                elif int(row[9]) >=51 and int(row[9]) < 76:
                    customerQuarterSaleDict[row[0]][2] = saleValue
               	else:
                    customerQuarterSaleDict[row[0]][3] = saleValue
            else:
                if int(row[9]) >= 0 and int(row[9]) <26:
                    customerQuarterSaleDict[row[0]][0] += saleValue
                elif int(row[9]) >= 26 and int(row[9]) <51:
                    customerQuarterSaleDict[row[0]][1] += saleValue
                elif int(row[9]) >=51 and int(row[9]) < 76:
                    customerQuarterSaleDict[row[0]][2] += saleValue
                else:
                    customerQuarterSaleDict[row[0]][3] += saleValue
    f.close()

    with open("/Users/Rick/Desktop/segments/customerSaleDict.yaml", 'w') as f:
		f.write(yaml.dump(customerSaleDict,default_flow_style=False))
    f.close()

    with open("/Users/Rick/Desktop/segments/customerQuarterSaleDict.yaml", 'w' ) as f:
		f.write(yaml.dump(customerQuarterSaleDict,default_flow_style=False))
    f.close()

def buildCompleteTopCustomer():
    global topCompleteHouseHoldList
    for houseHoldKey, saleValue in sorted(customerSaleDict.items(), key=lambda k:k[1]):
        topCompleteHouseHoldList.append(houseHoldKey)
    print topCompleteHouseHoldList

    with open('/Users/Rick/Desktop/segments/topCompleteHouseHoldList', 'wb' ) as f:
		f.write(yaml.dump(topCompleteHouseHoldList,default_flow_style=False))
    f.close()


def selectCustomerOverTrend():

    with open("/Users/Rick/Desktop/segments/customerQuarterSaleDict.yaml", 'r' ) as f:
        customerQuarterSaleDict =  yaml.load(f)
    f.close()

    with open('/Users/Rick/Desktop/segments/topCompleteHouseHoldList', 'r' ) as f:
        topCompleteHouseHoldList  = yaml.load(f)
    f.close()

    moreSpentOverTime = []
    lessSpentOverTime = []

	for houseHoldKeyValue in topCompleteHouseHoldList:
        for houseHoldKey, quarterDict in customerQuarterSaleDict.items():
            if houseHoldKeyValue == houseHoldKey:
                moreSpentOverTime.append(houseHoldKey)
				Quarterly_list = [['week_no', 'Sale_value']]
                if (( quarterDict[0] <= quarterDict[1] ) and ( quarterDict[1] <= quarterDict[2] ) and ( quarterDict[2] <= quarterDict[3] )):
                    for quarterNo, saleValue in sorted(quarterDict.items(), key=lambda k:int(k[0])):
                        Quarterly_list.append([quarterNo, saleValue])
                        print houseHoldKey, Quarterly_list

	for houseHoldKeyValue in topCompleteHouseHoldList:
        for houseHoldKey, quarterDict in customerQuarterSaleDict.items():
            if houseHoldKeyValue == houseHoldKey:
                lessSpentOverTime.append(houseHoldKey)
				Quarterly_list = [['week_no', 'Sale_value']]
                if (( quarterDict[0] >= quarterDict[1] ) and ( quarterDict[1] >= quarterDict[2] ) and ( quarterDict[2] >= quarterDict[3] )):
                    for quarterNo, saleValue in sorted(quarterDict.items(), key=lambda k:int(k[0])):
                        Quarterly_list.append([quarterNo, saleValue])
                        print houseHoldKey, Quarterly_list


    with open('/Users/Rick/Desktop/segments/moreSpentOverTime.yaml', 'w' ) as f:
		f.write(yaml.dump(moreSpentOverTime,default_flow_style=False))
    f.close()

	with open('/Users/Rick/Desktop/segments/lessSpentOverTime.yaml', 'w' ) as f:
		f.write(yaml.dump(lessSpentOverTime,default_flow_style=False))
    f.close()

def main():
    readCSV()
	buildCompleteTopCustomer()
	selectCustomerOverTrend()
if __name__ =="__main__":
    main()
0
