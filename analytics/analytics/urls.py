"""analytics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('GA/', include('GA.urls'))

]
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='GA/', permanent=True)),
]










'''
import pandas as pd
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import json

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'client_secrets.json'
VIEW_ID = '244458600'


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)
    return analytics

# Get one report page


def get_report(analytics, pageTokenVar):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '3daysAgo', 'endDate': 'yesterday'}],
                    'metrics': [{'expression': 'ga:sessions'}],
                    'dimensions': [{'name': 'ga:browser'}],
                    'pageSize': 10000,
                    'pageToken': pageTokenVar,
                    'samplingLevel': 'LARGE'
                }]
        }
    ).execute()


def handle_report(analytics, pagetoken, rows):
    response = get_report(analytics, pagetoken)
    #res = json.dumps(response)
    print(type(response))
    # print(type(response))
    # Header, Dimentions Headers, Metric Headers
    columnHeader = response.get("reports")[0].get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])
    metricHeaders = columnHeader.get(
        'metricHeader', {}).get('metricHeaderEntries', [])

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
                        dic[metric.get('name')] = int(value)
            nicerows.append(dic)
        print(nicerows)
        print(type(nicerows))
        data = nicerows[0]
        print(data)
        print(type(data))
        #result = json.loads(nicerows)
        # print(type(result))
        return nicerows

# Start


def main():
    analytics = initialize_analyticsreporting()

    global dfanalytics
    dfanalytics = []

    rows = []
    rows = handle_report(analytics, '0', rows)

    dfanalytics = pd.DataFrame(list(rows))


if __name__ == '__main__':
    main()
'''