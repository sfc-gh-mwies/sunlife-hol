![sunlife-snowflake](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/img/sunlife-snowflake.png?raw=true)
> # Sunlife HOL Day 2 - Cortex + Data Ops

## Snowpark + Snowflake ML
* Create a new database with your <firtname>_<lastname> in the title
Download [Snowpark-ML.ipynb](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/Day2/Zero-to-Snowpark/Snowpark-ML.ipynb)
* In your Snowflake account, navigate to Projects > Notebooks and click the dropdown next to [+] Notebook in the top right corner > "import from .ipynb file"
* Use the database you just created, and the PUBLIC schema
* Import the downloaded file, and we will begin to step through the cells

## Basic Cortex Built-in Features Via Streamlit!
* In your Snowflake account, navigate to Projects > Streamlit and click the [+] Streamlit button
* Choose an "app title", select the database you just created (you can use the PUBLIC schema) and choose the warehouse SNOWPARK_HOL_VWH
* Navigate to [SKO_HOP_Cortex_SiS_BUILD_1.py](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/Day2/Zero-to-Snowpark/SKO_HOP_Cortex_SiS_BUILD_1.py) and copy the code
* "Edit" your streamlit app and paste in the python code
* Now we should be able to explore the cortex features that come out of the box with Snowflake using a simple Streamlit app interface

## Devops Part 1
[Database Change Management with Terraform and GitHub](https://quickstarts.snowflake.com/guide/devops_dcm_terraform_github)
### PREREQUISITES
* Ensure that you have a github account with [credentials set up on your laptop](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) -- alternatively, you may be able to use codespaces if you're familiar with that option
* Create a [Terraform account](https://app.terraform.io/signup/account?_fsi=hU5Zx4LY&_fsi=hU5Zx4LY)
* Create a blank Git repo, with only a README file, and clone the repo to your laptop
### Important Notes About the Quickstart Guide
* This is a public Snowflake Quickstart, which we'll modify slightly as we go
* **In step 4** When creating variables, choose "environment variable", not the default "Terraform Vairable"
* **In step 5** replace;
    * "actions/checkout@v2" --> "actions/checkout@v4" 
    * "hashicorp/setup-terraform@v1" --> "hashicorp/setup-terraform@v3"
* **In step 6** replace "demo_db" with "demo_db_\<firstname\>_\<lastname\>"

## Devops Part 2
Open the Quickstart Guide [Getting Started with Devops in Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_devops_in_snowflake/#0) in a new tab
* You may use Codespaces as described in the Quickstart, **OR** install VS Code and the [Snowflake Extension](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc)
### Important Notes About the Quickstart Guide
* **YOU WILL NEED TO SUFFIX ALL DATABASES IN THE CODE REPO WITH YOUR \<firstname\>_\<lastname\>
    * ```CREATE DATABASE IF NOT EXISTS QUICKSTART_COMMON_<firstname>_<lastname>;```
    * ```CREATE OR REPLACE DATABASE QUICKSTART_PROD_<firstname>_<lastname>;```
    * Do this everywhere in the lab that you see "QUICKSTART_PROD" and "QUICKSTART_COMMON" i.e. each "use schema" statement
* **YOU WILL NOT CREATE A NEW WAREHOUSE -- YOU WILL NEED TO USE SNOWPARK_HOL_VWH INSTEAD
* ```USE WAREHOUSE SNOWPARK_HOL_VWH;```
* **YOU WILL NEED TO CHANGE ALL REFERENCES TO THE "ACCOUNTADMIN" ROLE TO "SNOWPARK_HOL_ROLE"
* **IN STEP 1, YOU WILL NEED TO SUFFIX THE API INTEGRATION AND NOTIFICATION INTEGRATION WITH YOUR  \<firstname\>_\<lastname\>
    * ```CREATE OR REPLACE API INTEGRATION git_api_integration_<firstname>_<lastname>;```
    * ```CREATE OR REPLACE NOTIFICATION INTEGRATION email_integration_<firstname>_<lastname>;```
* **In Step 4** We will import the data sets as a group, using a user with ACCOUNTADMIN access
