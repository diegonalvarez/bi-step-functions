import os
from .mysql import MySql
from datetime import datetime, timedelta

class Queries(object):

    def companies(self):
        mysql = MySql(os.environ['aurora_host'], os.environ['aurora_username'], os.environ['aurora_password'], os.environ['aurora_db_name'])
        conn  = mysql.connect()
        query = "SELECT companies.*, companies_configurations.configuration_value FROM companies INNER JOIN companies_configurations ON companies.company_id = companies_configurations.retail_id WHERE status = 1"
        data  = True
        try:
            with conn.cursor() as cur:
                cur.execute(query)
                data = []
                for row in cur:
                    data.append(row)
                cur.close()
            conn.close()
        except Exception, e:
            print str(e)
        return data;

    def tables(self):
        mysql = MySql(os.environ['aurora_host'], os.environ['aurora_username'], os.environ['aurora_password'], os.environ['aurora_db_name'])
        conn  = mysql.connect()
        query = "SELECT name, query_select, params_select, query_insert, params_insert FROM tables WHERE status = 1"
        data  = True

        try:
            with conn.cursor() as cur:
                cur.execute(query)
                data = []
                for row in cur:
                    data.append(row)
                cur.close()
            conn.close()
        except:
            print ('Database Error')

        return data;

    def data_from_db(self, company, table):
        mysql  = MySql(os.environ['rds_host'], os.environ['rds_username'], os.environ['rds_password'], os.environ['rds_db_name'])
        conn   = mysql.connect()
        query  = table[1]
        data   = True

        date      = datetime.today() - timedelta(days=int(float(company[5])))
        where_var = table[2].replace("date", date.strftime('%Y-%m-%d'))

        try:
            with conn.cursor() as cur:
                cur.execute(query, (eval(where_var)))
                data = []
                for row in cur:
                    data.append(row)
                cur.close()
            conn.close()
        except Exception, e:
            print str(e)

        return data;

    def insert_data_csv_db(self, company, table, content):
        mysql = MySql(os.environ['aurora_host'], os.environ['aurora_username'], os.environ['aurora_password'], os.environ['project_alias']+ '_' + company[4])
        conn  = mysql.connect()
        insert_params = ''
        comma         = ''
        res = False
        with conn.cursor() as cur:
            try:
                for idx, row in enumerate(content):
                    if idx % 30000 == 0 :
                        comma      = ''
                        if idx != 0:
                            insert_sql =  table[3] + insert_params
                            res        = cur.execute(insert_sql)
                            conn.commit()
                            insert_params = ''
                            pass
                        pass
                    else :
                        comma = ','
                    insert_params = insert_params + comma + eval(table[4])
                insert_sql =  table[3] + insert_params
                res        = cur.execute(insert_sql)
                conn.commit()
            except:
                print ('Empty File')
        cur.close()
        conn.close()
        return res;