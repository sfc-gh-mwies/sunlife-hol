# The Snowpark package is required for Python Worksheets. 
# You can add more packages by selecting them using the Packages control and then importing them.
#------------------------------------------------------------------------------
# Masterclass: Data Engineering with Snowpark
# Author:       Jeremiah Hansen, Caleb Baechtold
# Last Updated: 2024-01-02 by Mike Wies
#------------------------------------------------------------------------------

# SNOWFLAKE ADVANTAGE: Snowpark DataFrame API
# SNOWFLAKE ADVANTAGE: Streams for incremental processing (CDC)
# SNOWFLAKE ADVANTAGE: Streams on views

import snowflake.snowpark as snowpark
import snowflake.snowpark.functions as F
from snowflake.snowpark.functions import col

def main(session: snowpark.Session): 
       
   ######## ADD YOUR NAME HERE ########
    username = '<firstname>_<lastname>'.upper()
   ####################################  
    create_pos_view(session, username)
    create_pos_view_stream(session, username)  
    tableName = 'SNOWPARK_HOL_DB.HARMONIZED.'+username+'_POS_FLATTENED_V'
    dataframe = session.table(tableName).limit(1000)
    return dataframe


def create_pos_view(session, username):
    session.use_schema('SNOWPARK_HOL_DB.HARMONIZED')
    order_detail = session.table("SNOWPARK_HOL_DB.RAW_POS.ORDER_DETAIL").select(F.col("ORDER_DETAIL_ID"), \
                                                                F.col("LINE_NUMBER"), \
                                                                F.col("MENU_ITEM_ID"), \
                                                                F.col("QUANTITY"), \
                                                                F.col("UNIT_PRICE"), \
                                                                F.col("PRICE"), \
                                                                F.col("ORDER_ID"))
    order_header = session.table("SNOWPARK_HOL_DB.RAW_POS.ORDER_HEADER").select(F.col("ORDER_ID"), \
                                                                F.col("TRUCK_ID"), \
                                                                F.col("ORDER_TS"), \
                                                                F.to_date(F.col("ORDER_TS")).alias("ORDER_TS_DATE"), \
                                                                F.col("ORDER_AMOUNT"), \
                                                                F.col("ORDER_TAX_AMOUNT"), \
                                                                F.col("ORDER_DISCOUNT_AMOUNT"), \
                                                                F.col("LOCATION_ID"), \
                                                                F.col("ORDER_TOTAL"))
    truck = session.table("SNOWPARK_HOL_DB.RAW_POS.TRUCK").select(F.col("TRUCK_ID"), \
                                                F.col("PRIMARY_CITY"), \
                                                F.col("REGION"), \
                                                F.col("COUNTRY"), \
                                                F.col("FRANCHISE_FLAG"), \
                                                F.col("FRANCHISE_ID"))
    menu = session.table("SNOWPARK_HOL_DB.RAW_POS.MENU").select(F.col("MENU_ITEM_ID"), \
                                                F.col("TRUCK_BRAND_NAME"), \
                                                F.col("MENU_TYPE"), \
                                                F.col("MENU_ITEM_NAME"))
    franchise = session.table("SNOWPARK_HOL_DB.RAW_POS.FRANCHISE").select(F.col("FRANCHISE_ID"), \
                                                        F.col("FIRST_NAME").alias("FRANCHISEE_FIRST_NAME"), \
                                                        F.col("LAST_NAME").alias("FRANCHISEE_LAST_NAME"))
    location = session.table("SNOWPARK_HOL_DB.RAW_POS.LOCATION").select(F.col("LOCATION_ID"))

    t_with_f = truck.join(franchise, truck['FRANCHISE_ID'] == franchise['FRANCHISE_ID'], rsuffix='_f')
    oh_w_t_and_l = order_header.join(t_with_f, order_header['TRUCK_ID'] == t_with_f['TRUCK_ID'], rsuffix='_t') \
                                .join(location, order_header['LOCATION_ID'] == location['LOCATION_ID'], rsuffix='_l')
    final_df = order_detail.join(oh_w_t_and_l, order_detail['ORDER_ID'] == oh_w_t_and_l['ORDER_ID'], rsuffix='_oh') \
                            .join(menu, order_detail['MENU_ITEM_ID'] == menu['MENU_ITEM_ID'], rsuffix='_m')
    final_df = final_df.select(F.col("ORDER_ID"), \
                            F.col("TRUCK_ID"), \
                            F.col("ORDER_TS"), \
                            F.col('ORDER_TS_DATE'), \
                            F.col("ORDER_DETAIL_ID"), \
                            F.col("LINE_NUMBER"), \
                            F.col("TRUCK_BRAND_NAME"), \
                            F.col("MENU_TYPE"), \
                            F.col("PRIMARY_CITY"), \
                            F.col("REGION"), \
                            F.col("COUNTRY"), \
                            F.col("FRANCHISE_FLAG"), \
                            F.col("FRANCHISE_ID"), \
                            F.col("FRANCHISEE_FIRST_NAME"), \
                            F.col("FRANCHISEE_LAST_NAME"), \
                            F.col("LOCATION_ID"), \
                            F.col("MENU_ITEM_ID"), \
                            F.col("MENU_ITEM_NAME"), \
                            F.col("QUANTITY"), \
                            F.col("UNIT_PRICE"), \
                            F.col("PRICE"), \
                            F.col("ORDER_AMOUNT"), \
                            F.col("ORDER_TAX_AMOUNT"), \
                            F.col("ORDER_DISCOUNT_AMOUNT"), \
                            F.col("ORDER_TOTAL"))
    final_df.create_or_replace_view(username+'_POS_FLATTENED_V')

def create_pos_view_stream(session, username):
    session.use_schema('SNOWPARK_HOL_DB.HARMONIZED')
    _ = session.sql('CREATE STREAM '+username+'_POS_FLATTENED_V_STREAM \
                        ON VIEW '+username+'_POS_FLATTENED_V \
                        SHOW_INITIAL_ROWS = TRUE').collect()

def test_pos_view(session,username):
    session.use_schema('SNOWPARK_HOL_DB.HARMONIZED')
    tv = session.table(username+'_POS_FLATTENED_V')
    tv.limit(5).show()

