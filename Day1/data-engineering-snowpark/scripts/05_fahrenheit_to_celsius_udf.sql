USE ROLE SNOWPARK_HOL_ROLE;
USE WAREHOUSE SNOWPARK_HOL_VWH;
USE SNOWPARK_HOL_DB.ANALYTICS;

/* REPLACE YOUR NAME IN THIS LINE */
CREATE FUNCTION <firstname>_<lastname>_FAHRENHEIT_TO_CELSIUS_UDF (i int)
/*---------------------------------*/

returns int
language python
runtime_version = '3.8'
handler = 'main'
as
$$
def main(temp_f: float) -> float:
  return (float(temp_f) - 32) * (5/9)
$$;


SELECT <firstname>_<lastname>_FAHRENHEIT_TO_CELSIUS_UDF(90);