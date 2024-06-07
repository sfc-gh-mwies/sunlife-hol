USE ROLE SNOWPARK_HOL_ROLE;
USE WAREHOUSE SNOWPARK_HOL_VWH;
USE SNOWPARK_HOL_DB.ANALYTICS;

/* REPLACE YOUR NAME IN THIS LINE */
CREATE FUNCTION <firstname>_<lastname>_INCH_TO_MILLIMETER_UDF(f float)
/*---------------------------------*/

returns float
language python
runtime_version = '3.8'
handler = 'main'
as
$$
def main(temp_f: float) -> float:
  return (temp_f * 25.4)
$$;


/* REPLACE YOUR NAME IN THIS LINE */
SELECT <firstname>_<lastname>_INCH_TO_MILLIMETER_UDF(1);
/*---------------------------------*/