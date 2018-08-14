from chalice import Chalice
from chalicelib import Queries
from chalicelib import create_file
from chalicelib import S3

import os
import pymysql
import logging

app = Chalice(app_name='bi_structure')
app.debug = True

logger = logging.getLogger()
logger.setLevel(logging.INFO)

@app.route('/')
def index():
    data = False
    return {'hello': data}

@app.lambda_function()
def mysql_csv_to_s3(event, context):
    result    = False
    query     = Queries()
    s3        = S3()
    companies = query.companies()
    tables    = query.tables()
    for company in companies:
        for table in tables:
            data     = query.data_from_db(company, table)
            filename = company[2] + '_' + table[0]+'.csv'
            filepath = create_file(data, filename)
            result   = s3.save_to_bucket(filepath, company[4] + os.environ['bucket_prefix'] + filename)

    return {'csv_files': result}

@app.lambda_function()
def s3_to_mysql(event, context):
    data      = False
    query     = Queries()
    s3        = S3()
    companies = query.companies()
    tables    = query.tables()

    for company in companies:
        for table in tables:
            filename = company[2] + '_' + table[0]+'.csv'
            content  = s3.retrieve_file(company[4] + os.environ['bucket_prefix'] + filename)
            data     = query.insert_data_csv_db(company, table, content)

    return {'hello': data}