from django.shortcuts import render
from graphos.sources.csv_file import CSVDataSource
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.morris import BarChart
import yaml
import csv








#with open('/Users/Rick/Desktop/sample_demographics.csv', 'r') as w:
#    income_group = {}
#    income_group_list = []
#    next(w)
#    data = csv.reader(w, delimiter=',')
#    for row in data:
#        if row[2] not in income_group:
#            income_group[row[2]] = 1
#        else:
#            income_group[row[2]] += 1
#    for key, value in sorted(income_group.iteritems(), key=lambda(k,v):(v,k)):
#        print "%s: %s" % (key,value)
#
#    for i, k in income_group.items():
#        in.come_group_list.append([i,k])
#        print income_group_list





#    with open("/Users/Rick/Desktop/Project/src/media/documents/2016/08/24/transaction_data.csv", 'r') as f:
#         csv_f = list(csv.reader(f,delimiter = ','))
#         new_list = []
#         J = csv_f[0].index('SALES_VALUE')
#         K = csv_f[0].index('WEEK_NO')
#         for i in range(len(csv_f)):
#             new_list.append(csv_f[i][J])
#             new_list.append(csv_f[i][K])
#    new_list = new_list[:5]
#
# Test CSV file
#    csv_file = open('/Users/Rick/Desktop/Project/test.csv')
def plot(request):
    '''   data = [
            ['Year', 'Sales', 'Expenses'],
            [2004, 1000, 400],
            [2005, 1170, 460],
            [2006, 660, 1120],
            [2007, 1030, 540]
        ]'''
    context = {}
    topHouseHoldList = []
    CustomerOverTimeDict = {}
    Weekly_list=[]

    with open('/Users/Rick/Desktop/segments/topHouseHoldList', 'r' ) as f:
        topHouseHoldList =  yaml.load(f)
    f.close()

    with open('/Users/Rick/Desktop/segments/CustomerOverTimeDict.yaml', 'r' ) as f:
        CustomerOverTimeDict = yaml.load(f)
        f.close()

    count = 0
    for household_key, WeekDict in CustomerOverTimeDict.items():
        if household_key in topHouseHoldList:
            Weekly_list = [['week_no', 'sales_value']]
            for week_no, sales_value in sorted(WeekDict.items(), key=lambda k:int(k[0])):
                # for each week number, It is appending value to 2 D List
                Weekly_list.append([week_no,sales_value])
            print"*"*30
            print "Customer :", household_key,"Week No:" , len(Weekly_list) - 1
            print"*"*30
            print household_key, Weekly_list

            data = Weekly_list
            # DataSource object
            data_source = SimpleDataSource(data)
            # Chart object
            chart = BarChart(data_source, options={'lineWidth': 50, 'smooth': False})
    #chart = LineChart(data_source)
            context['chart'+str(count)] = chart
            context['house'+str(count)]= household_key
            count = count+ 1
    return render(request, 'plot.html', context)



# Create your views here.
