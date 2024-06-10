![sunlife-snowflake](https://github.com/sfc-gh-mwies/sunlife-hol/blob/main/img/sunlife-snowflake.png?raw=true)
> # Sunlife HOL Day 2 - Cortex + Data Ops

## AGENDA

### Devops Part 1
[Database Change Management with Terraform and GitHub](https://quickstarts.snowflake.com/guide/devops_dcm_terraform_github)
#### PREREQUISITES
* Ensure that you have a github account with [credentials set up on your laptop](https://docs.github.com/en/get-started/getting-started-with-git/caching-your-github-credentials-in-git) -- alternatively, you may be able to use codespaces if you're familiar with that option
* Create a [Terraform account](https://app.terraform.io/signup/account?_fsi=hU5Zx4LY&_fsi=hU5Zx4LY)
* Create a blank Git repo, with only a README file, and clone the repo to your laptop
#### Important Notes About the Quickstart Guide
* This is a public Snowflake Quickstart, which we'll modify slightly as we go
* **In step 4** When creating variables, choose "environment variable", not the default "Terraform Vairable"
* **In step 5** replace;
    * "actions/checkout@v2" --> "actions/checkout@v4" 
    * "hashicorp/setup-terraform@v1" --> "hashicorp/setup-terraform@v3"
* **In step 6** replace "demo_db" with "demo_db_\<firstname\>_\<lastname\>"

### Devops Part 2
[Getting Started with Devops in Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_devops_in_snowflake)
#### PREREQUISITES
* VS Code and the [Snowflake Extension](https://marketplace.visualstudio.com/items?itemName=snowflake.snowflake-vsc)
#### Important Notes About the Quickstart Guide
* This is also a public Snowflake Quickstart. Again, we'll modify slightly as we go
* In the Overview, it says you need ACCOUNTADMIN access -- you can use your regular HOL role
* **SUFFIX ALL DATABASE OBJECTS IN THE CODE REPO WITH YOUR** \<firstname\>_\<lastname\>
* **In Step 3** While editing the SQL script, replace;
    * "USE ROLE ACCOUNTADMIN" with "USE ROLE SNOWPARK_HOL_ROLE"
    * Replace the entire "CREATE WAREHOUSE" statement with "USE WAREHOUSE SNOWPARK_HOL_VWH"
* **In Step 4** We will import the data sets as a group, using a user with ACCOUNTADMIN access
* 
