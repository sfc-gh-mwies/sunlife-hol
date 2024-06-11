USE ROLE FROSTBYTE_HOL_ROLE;

USE WAREHOUSE SNOWPARK_HOL_VWH;

-- Separate database for git repository
CREATE DATABASE IF NOT EXISTS QUICKSTART_COMMON_<firstname>_<lastname>;


-- API integration is needed for GitHub integration
CREATE OR REPLACE API INTEGRATION git_api_integration_<firstname>_<lastname>
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/<insert GitHub username>') -- INSERT YOUR GITHUB USERNAME HERE
  ENABLED = TRUE;


-- Git repository object is similar to external stage
CREATE OR REPLACE GIT REPOSITORY quickstart_common.public.quickstart_repo_<firstname>_<lastname>
  API_INTEGRATION = git_api_integration_<firstname>_<lastname>
  ORIGIN = '<insert URL of forked GitHub repo>'; -- INSERT URL OF FORKED REPO HERE


CREATE OR REPLACE DATABASE QUICKSTART_PROD_<firstname>_<lastname>;


-- To monitor data pipeline's completion
CREATE OR REPLACE NOTIFICATION INTEGRATION email_integration_<firstname>_<lastname>
  TYPE=EMAIL
  ENABLED=TRUE;


-- Database level objects
USE DATABASE QUICSTART_PROD_<firstname>_<lastname>;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;


-- Schema level objects
CREATE OR REPLACE FILE FORMAT bronze.json_format TYPE = 'json';
CREATE OR REPLACE STAGE bronze.raw;


-- Copy file from GitHub to internal stage
copy files into @bronze.raw from @quickstart_common.public.quickstart_repo/branches/main/data/airport_list.json;
