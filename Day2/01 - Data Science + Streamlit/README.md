![sunlife-snowflake](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/img/sunlife-snowflake.png?raw=true)
> # Sunlife HOL Day 2

## Cortex Part 1: Snowpark + Snowflake ML
* Create a new database with your \<firtname\>_\<lastname\> in the title
* Download [Snowpark-ML.ipynb](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/Day2/Zero-to-Snowpark/Snowpark-ML.ipynb)
* In your Snowflake account, navigate to Projects > Notebooks and click the dropdown next to [+] Notebook in the top right corner > "import from .ipynb file"
* Use the database you just created, and the PUBLIC schema
* Import the downloaded file, and we will begin to step through the cells

## Cortex Part 2: Basic Cortex Built-in Features Via Streamlit!
* In your Snowflake account, navigate to Projects > Streamlit and click the [+] Streamlit button
* Choose an "app title", select the database you just created (you can use the PUBLIC schema) and choose the warehouse SNOWPARK_HOL_VWH
* Navigate to [SKO_HOP_Cortex_SiS_BUILD_1.py](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/Day2/Zero-to-Snowpark/SKO_HOP_Cortex_SiS_BUILD_1.py) and copy the code
* "Edit" your streamlit app and paste in the python code
* Now we should be able to explore the cortex features that come out of the box with Snowflake using a simple Streamlit app interface
