#------------------------------------------------------------------------------
# Hands-On Lab: Data Engineering with Snowpark
# Script:       06_orders_process_sp/app.py
# Author:       Jeremiah Hansen, Caleb Baechtold
# Last Updated: 2024-01-02 by Mike Wies
#------------------------------------------------------------------------------

# SNOWFLAKE ADVANTAGE: Python Stored Procedures

#import time
import snowflake.snowpark as snowpark
from snowflake.snowpark import Session
#import snowflake.snowpark.types as T
import snowflake.snowpark.functions as F
#from snowflake.snowpark.functions import col

def main(session: Session) -> str:
   ######## ADD YOUR NAME HERE ########
    username = '<firstname>_<lastname>'.upper()
   ####################################  
    # Create the ORDERS table and ORDERS_STREAM stream if they don't exist
    if not table_exists(session, schema='HARMONIZED', name=username+'_ORDERS'):
        create_orders_table(session,username)
        create_orders_stream(session,username)

    # Process data incrementally
    merge_order_updates(session,username)
#    session.table('SNOWPARK_HOL_DB.HARMONIZED.ORDERS').limit(5).show()

    return f"Successfully processed ORDERS"


def table_exists(session, schema='', name=''):
    exists = session.sql("SELECT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}') AS TABLE_EXISTS".format(schema, name)).collect()[0]['TABLE_EXISTS']
    return exists

def create_orders_table(session,username):
    _ = session.sql("CREATE TABLE SNOWPARK_HOL_DB.HARMONIZED."+username+"_ORDERS LIKE SNOWPARK_HOL_DB.HARMONIZED."+username+"_POS_FLATTENED_V").collect()
    _ = session.sql("ALTER TABLE SNOWPARK_HOL_DB.HARMONIZED."+username+"_ORDERS ADD COLUMN META_UPDATED_AT TIMESTAMP").collect()

def create_orders_stream(session,username):
    _ = session.sql("CREATE STREAM SNOWPARK_HOL_DB.HARMONIZED."+username+"_ORDERS_STREAM ON TABLE SNOWPARK_HOL_DB.HARMONIZED."+username+"_ORDERS").collect()

def merge_order_updates(session,username):
    # COMMENT OUT IF NO PERMISSION TO ALTER WAREHOUSE
    #_ = session.sql('ALTER WAREHOUSE SNOWPARK_HOL_VWH  SET WAREHOUSE_SIZE = XLARGE WAIT_FOR_COMPLETION = TRUE').collect()

    source = session.table('SNOWPARK_HOL_DB.HARMONIZED.'+username+'_POS_FLATTENED_V_STREAM')
    target = session.table('SNOWPARK_HOL_DB.HARMONIZED.'+username+'_ORDERS')

    # TODO: Is the if clause supposed to be based on "META_UPDATED_AT"?
    cols_to_update = {c: source[c] for c in source.schema.names if "METADATA" not in c}
    metadata_col_to_update = {"META_UPDATED_AT": F.current_timestamp()}
    updates = {**cols_to_update, **metadata_col_to_update}

    # merge into DIM_CUSTOMER
    target.merge(source, target['ORDER_DETAIL_ID'] == source['ORDER_DETAIL_ID'], \
                        [F.when_matched().update(updates), F.when_not_matched().insert(updates)])

    # COMMENT OUT IF NO PERMISSION TO ALTER WAREHOUSE
    #_ = session.sql('ALTER WAREHOUSE SNOWPARK_HOL_VWH  SET WAREHOUSE_SIZE = XSMALL').collect()


