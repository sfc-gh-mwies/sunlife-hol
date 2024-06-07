/*-----------------------------------------------------------------------------
Hands-On Lab: Data Engineering with Snowpark
Script:       08_orchestrate_jobs.sql
Author:       Jeremiah Hansen
Last Updated: 2023-11-22 by Mike Wies
-----------------------------------------------------------------------------*/

-- SNOWFLAKE ADVANTAGE: Tasks (with Stream triggers)
-- SNOWFLAKE ADVANTAGE: Task Observability

USE ROLE SNOWPARK_HOL_ROLE;
USE WAREHOUSE SNOWPARK_HOL_VWH;
USE SCHEMA SNOWPARK_HOL_DB.HARMONIZED;


-- ----------------------------------------------------------------------------
-- Step #1: Create the tasks to call our Python stored procedures
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TASK <FIRSTNAME>_<LASTNAME>_ORDERS_UPDATE_TASK
WAREHOUSE = SNOWPARK_HOL_VWH
WHEN
  SYSTEM$STREAM_HAS_DATA('<FIRSTNAME>_<LASTNAME>_POS_FLATTENED_V_STREAM')
AS
CALL SNOWPARK_HOL_DB.HARMONIZED.<FIRSTNAME>_<LASTNAME>_ORDERS_UPDATE_SP();

CREATE OR REPLACE TASK <FIRSTNAME>_<LASTNAME>_DAILY_CITY_METRICS_UPDATE_TASK
WAREHOUSE = SNOWPARK_HOL_VWH
AFTER <FIRSTNAME>_<LASTNAME>_ORDERS_UPDATE_TASK
WHEN
  SYSTEM$STREAM_HAS_DATA('<FIRSTNAME>_<LASTNAME>_ORDERS_STREAM')
AS
CALL SNOWPARK_HOL_DB.ANALYTICS.<FIRSTNAME>_<LASTNAME>_DAILY_CITY_METRICS_UPDATE_SP();


-- ----------------------------------------------------------------------------
-- Step #2: Execute the tasks
-- ----------------------------------------------------------------------------

ALTER TASK <FIRSTNAME>_<LASTNAME>_DAILY_CITY_METRICS_UPDATE_TASK RESUME;
EXECUTE TASK <FIRSTNAME>_<LASTNAME>_ORDERS_UPDATE_TASK;


-- ----------------------------------------------------------------------------
-- Step #3: Monitor tasks in Snowsight
-- ----------------------------------------------------------------------------

/*---
-- https://docs.snowflake.com/en/user-guide/ui-snowsight-tasks.html



-- Alternatively, here are some manual queries to get at the same details
SHOW TASKS;

-- Task execution history in the past day
SELECT *
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY(
    SCHEDULED_TIME_RANGE_START=>DATEADD('DAY',-1,CURRENT_TIMESTAMP()),
    RESULT_LIMIT => 100))
ORDER BY SCHEDULED_TIME DESC
;

-- Scheduled task runs
SELECT
    TIMESTAMPDIFF(SECOND, CURRENT_TIMESTAMP, SCHEDULED_TIME) NEXT_RUN,
    SCHEDULED_TIME,
    NAME,
    STATE
FROM TABLE(INFORMATION_SCHEMA.TASK_HISTORY())
WHERE STATE = 'SCHEDULED'
ORDER BY COMPLETED_TIME DESC;

-- Other task-related metadata queries
SELECT *
  FROM TABLE(INFORMATION_SCHEMA.CURRENT_TASK_GRAPHS())
  ORDER BY SCHEDULED_TIME;

SELECT *
  FROM TABLE(INFORMATION_SCHEMA.COMPLETE_TASK_GRAPHS())
  ORDER BY SCHEDULED_TIME;
---*/