#Get CSV
import pandas as pd

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
df = pd.read_csv(url, error_bad_lines=False)
df.to_csv('vaccinations.csv')

#Create Hyperfile
from tableauhyperapi import Connection, HyperProcess, SqlType, TableDefinition, \
    escape_string_literal, escape_name, NOT_NULLABLE, Telemetry, Inserter, CreateMode, TableName

with HyperProcess(Telemetry.SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, 'vaccinations.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        vaccinations_table = TableDefinition(
            table_name = "vaccinations", 
            columns =[
                TableDefinition.Column('id', SqlType.text()),
                TableDefinition.Column('location', SqlType.text()),
                TableDefinition.Column('iso_code', SqlType.text()),
                TableDefinition.Column('date', SqlType.date()),
                TableDefinition.Column('total_vaccinations', SqlType.big_int()),
                TableDefinition.Column('people_vaccinated', SqlType.big_int()),
                TableDefinition.Column('people_fully_vaccinated', SqlType.big_int()),
                TableDefinition.Column('daily_vaccinations_raw', SqlType.big_int()),
                TableDefinition.Column('daily_vaccinations', SqlType.big_int()),
                TableDefinition.Column('total_vaccinations_per_hundred', SqlType.double()),
                TableDefinition.Column('people_vaccinated_per_hundred', SqlType.double()),
                TableDefinition.Column('people_fully_vaccinated_per_hundred', SqlType.double()),
                TableDefinition.Column('daily_vaccinations_per_million', SqlType.big_int()),
            ])
        print("The table is defined.")
        connection.catalog.create_table(vaccinations_table)
        path_to_csv = "vaccinations.csv"
        count_in_vaccinations_table = connection.execute_command(
                command=f"COPY {vaccinations_table.table_name} from {escape_string_literal(path_to_csv)} with "
                f"(format csv, NULL '', delimiter ',', header)")
        
        print("The data was added to the table.")
    print("The connection to the Hyper extract file is closed.")
print("The HyperProcess has shut down.")

#Publish to Tableau Server
import tableauserverclient as TSC

#Authentication
#https://tableau.github.io/server-client-python/docs/api-ref#authentication
tableau_auth = TSC.TableauAuth('admin', 'password', site_id='')
server = TSC.Server('http://localhost', use_server_version=True)
with server.auth.sign_in(tableau_auth):
    print("Sign in Sucessfull")
    
    # create project item
    new_project = TSC.ProjectItem(name='Tableua Demo Project', content_permissions='LockedToProject', description='Interview Demo Project created with API')
    
    # create the project
    new_project = server.projects.create(new_project)
    print("Project Created")
    
    #get Project ID
    #https://community.tableau.com/s/question/0D54T000006B4SPSA0/how-to-get-the-projectid-from-the-tableau-server
    found = [proj for proj in TSC.Pager(server.projects) if proj.name == 'Tableua Demo Project']
    project_id = found[0].id
    print("Project ID Set")
    
    #define path to hyper file
    path_to_hyper = "vaccinations.hyper"
    
    # Use the project id to create new datsource_item
    new_datasource = TSC.DatasourceItem(project_id)
    
    # publish data source (specified in file_path)
    new_datasource = server.datasources.publish(new_datasource, path_to_hyper, 'CreateNew')
    print("Data Source Published")
    
    server.auth.sign_out()
    print("Signed Out")
