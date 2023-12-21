# Tableau Server information

import tableauserverclient as TSC
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from io import StringIO
from version import VERSION

# Tableau Server information
server = 'http://SampleServer.com/'
username = ''
password = ''
site = '' # optional

# Workbook Information
workbook_name = 'YOUR WORKBOOK NAME'
project_name = 'YOUR PROJECT NAME'
view_name = ['VIEW1_NAME', 'VIEW2_NAME', 'VIEW3_NAME']  # Replace with the actual view name 

# Sign in to Tableau Server
tableau_auth = TSC.TableauAuth(username, password)
server = TSC.Server(server)

with server.auth.sign_in(tableau_auth):
    # Get the project ID
    all_projects, _ = server.projects.get()
    project_id = next((project.id for project in all_projects if project.name == project_name), None)

    if not project_id:
        raise Exception(f"Project '{project_name}' not found.")

    # Get the workbook ID
    request_options = TSC.RequestOptions(pagesize=1000)
    all_workbooks = list(TSC.Pager(server.workbooks, request_options))
    # all_workbooks, _ = server.workbooks.get()
    workbook_id = next((workbook.id for workbook in all_workbooks if workbook.name == workbook_name and workbook.project_id == project_id), None)

    print('workbook_id:', workbook_id)

    if not workbook_id:
        raise Exception(f"Workbook '{workbook_name}' not found in project '{project_name}'.")

    # Get the view ID
    all_views = list(TSC.Pager(server.views, request_options))
    # all_views, _ = server.views.get(workbook_id)
    view_id = {}
    for v in view_name:
        view_id[v] = next((view.id for view in all_views if view.name == v), None)

    print('view_id:', view_id)

    if not view_id:
        raise Exception(f"View '{view_name}' not found in workbook '{workbook_name}'.")

# Get the crosstab data - WIP
    # csv_export_url = f"{server}/views/{view_id}/data"

    # response = requests.get(csv_export_url, auth=(username, password))

    # # Save the crosstab data to a CSV file
    # with open(f"{workbook_name}_{view_name}_crosstab.csv", 'w', newline='') as csvfile:
    #     csvfile.write(response.text)


# Sign out from Tableau Server
server.auth.sign_out()
