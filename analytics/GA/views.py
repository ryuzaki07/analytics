from django.shortcuts import render
import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json
from  GA.forms import DateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from GA.models import Datevssessionsmodel
from GA.models import  Newvisitormodel,Repeatedvisitormodel


SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'
VIEW_ID = '244458600'



def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics



#{'expression': 'ga:sessions'} -> metrics
#{'name': 'ga:date'} -> dimensions
#y m d
#2021-06-08
def get_report(analytics, pageTokenVar,start_date,end_date,dimensions,metrics):
    print(start_date)
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{"startDate": start_date, "endDate": end_date}],
                    'metrics': [metrics],
                    'dimensions': [dimensions],
                    'pageSize': 10000,
                    'pageToken': pageTokenVar,
                    'samplingLevel': 'LARGE'
                }]
        }
    ).execute()


def handle_report(analytics, pagetoken, rows,start_date,end_date,dimensions,metrics):
    response = get_report(analytics, pagetoken,start_date,end_date,dimensions,metrics)
    res = json.dumps(response)
   
    # Header, Dimentions Headers, Metric Headers
    columnHeader = response.get("reports")[0].get('columnHeader', {})
    
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get(
        'metricHeader', {}).get('metricHeaderEntries', [])
    #print(columnHeader)
    #print(dimensionHeaders)
    #print(metricHeaders)
    # Pagination
    pagetoken = response.get("reports")[0].get('nextPageToken', None)

    # Rows
    rowsNew = response.get("reports")[0].get('data', {}).get('rows', [])
    rows = rows + rowsNew
    #print("len(rows): " + str(len(rows)))

    # Recursivly query next page
    if pagetoken != None:
        return handle_report(analytics, pagetoken, rows)
    else:
        # nicer results
        nicerows = []
        for row in rows:
            dic = {}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                dic[header] = dimension

            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    if ',' in value or ',' in value:
                        dic[metric.get('name')] = float(value)
                    else:
                        dic[metric.get('name')] = float(value)
            nicerows.append(dic)
       
        return nicerows

def query(request):
   
    return render(
        request,
        'index.html')


def DateVsSessionsFormView(request):
    context={
        'form':DateForm
    }
    return render(request,'datesvssessions.html',context)

def UsertypeFormView(request):
    context={
        'form':DateForm
    }
    return render(request,'usertype.html',context)



def DateVsSessionsView(request):
    if request.method == "POST":

       
        form = DateForm(request.POST)
    
     
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            dimensions={'name': 'ga:date'}
            metrics={'expression': 'ga:sessions'}
            analytics = initialize_analyticsreporting()
            global dfanalytics
            dfanalytics = []

            rows = []
            rows = handle_report(analytics, '0', rows,start_date,end_date,dimensions,metrics)
            print(rows)
            data=rows[0]
            print(type(data))
            for row in rows:
                print(row["ga:date"])
                date_time_obj = datetime.strptime(row["ga:date"], '%Y%m%d')
                str=int(row["ga:sessions"])
                print(date_time_obj.date())
                print(str)
                check=Datevssessionsmodel.objects.filter(date=date_time_obj.date()).exists()
                
                if check:
                    obj=Datevssessionsmodel.objects.get(date=date_time_obj.date())
                    obj.sessions=str
                    obj.save()
                
                else:
                    obj=Datevssessionsmodel(date=date_time_obj.date(),sessions=str)
                    obj.save()
               
            dfanalytics = pd.DataFrame(list(rows))
           
    return HttpResponseRedirect(reverse('query')) 


def UsertypeView(request):
    if request.method == "POST":

       
        form = DateForm(request.POST)
    
     
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            dimensions=[{'name': 'ga:userType'},{'name':'ga:date'}]
            metrics={'expression': 'ga:avgSessionDuration'}
            analytics = initialize_analyticsreporting()
            global dfanalytics
            dfanalytics = []

            rows = []
            rows = handle_report(analytics, '0', rows,start_date,end_date,dimensions,metrics)
        
            for row in rows:
                print(row)
                date_time_obj = datetime.strptime(row["ga:date"], '%Y%m%d')
                str=float(row["ga:avgSessionDuration"])
                visitor=row["ga:userType"]
                
                if visitor=='New Visitor':
                    obj=Newvisitormodel(date=date_time_obj.date(),visitor="New Visitor",time=str)
                    obj.save()
                
                else:
                    obj=Repeatedvisitormodel(date=date_time_obj.date(),visitor="Returning Visitor",time=str)
                    print("yes")
                    obj.save()
                
                '''
                check=Usertypemodel.objects.filter(date=date_time_obj.date()).filter(visitor=visitor).filter(time=str).exists()
                if not check:
                    obj=Usertypemodel(date=date_time_obj.date(),visitor=visitor,time=str)
                    obj.save()
                    print(obj)
                    
                    obj=Usertypemodel.objects.get(date=date_time_obj.date())
                    print(obj)
                    v=obj.visitor
                    print(v)
                    if v==visitor:
                        obj.time=str
                        obj.save()
                    
                    else:
                        obj=Usertypemodel(date=date_time_obj.date(),visitor=visitor,time=str)
                        obj.save()
                        print(obj)

                    
                    check2=Usertypemodel.objects.filter(date=date_time_obj.date()).filter(visitor=visitor).exists()
                    if check2:
                        obj=Usertypemodel.objects.get(date=date_time_obj.date(),visitor=visitor)
                        obj.time=str
                        obj.save()
                    
                    else:
                        obj=Usertypemodel.objects.get(date=date_time_obj.date())
                        obj.visitor=visitor
                        obj.time=str
                        obj.save()
                    
                
                else:
                    obj=Usertypemodel(date=date_time_obj.date(),visitor=visitor,time=str)
                    obj.save()
                    print(obj)
                '''
                #print(row["ga:date"])
                
                #type=row["ga:userType"]
                #print(type)
                #print(date_time_obj.date())
                #print(str)
                #check=Datevssessionsmodel.objects.filter(date=date_time_obj.date()).exists()
                '''
                if check:
                    obj=Datevssessionsmodel.objects.get(date=date_time_obj.date())
                    obj.visitor=str
                    obj.save()
                
                else:
                    obj=Datevssessionsmodel(date=date_time_obj.date(),sessions=str)
                    obj.save()
                '''
            dfanalytics = pd.DataFrame(list(rows))
        model=Newvisitormodel.objects.all()
        print(model)
    
    
    
    
    
    return HttpResponseRedirect(reverse('query')) 
