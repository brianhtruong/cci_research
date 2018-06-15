# cci_research

##### We are working to quantify a) the current state of tenant protections coverage in California, and b) hypothetical tenant protections coverage scenarios under reform. The two tenant protections we are looking at are (1) rent stabilization, which caps the amount a landlord can increase a tenant’s rent (usually tied to inflation), and (2) Just Cause for Evictions protections, which makes it so legally landlords can only evict tenants for specific “just causes” listed in the law. 

#### HOW TO QUANTIFY (GENERAL STEPS)
1. Import into ZCountyExtracts.sqlite the county of interest from ZMainBldg.sqlite with SQL
2. Group unique record among different years of a parcel for the newest record using ImportParcelID and LoadID
3. Add Subsidized column to county dataset and save dataset (using my utils package)
4. Commit initial data cleaning process for city in county of interest (using my utils package)
5. Apply quantification procedures based on stipulations of Rent Control and JCE policies

#### HOW TO QUANTIFY (IN-DEPTH STEPS)
1. Create EML account at eml.berkeley.edu and wait several days for account to be approved and created
2. Download and Install Microsoft Desktop Remote
3. Add desktop connection (remote access with MDR GUI to a Unix VM environment) using account information and one of the hostname users from the EML computing grid, and connect
4. Store critical or private files in personal account or create an account directory on the File Systems /scratch/public to store larger files
5. Download ZMainBldg.sqlite and ZCountyExtracts.sqlite from Berkeley Box
6. Use the terminal and cd into / then /scratch/public/account_name, and type sqlite3 ZMainBldg.sqlite
7. Apply SQL query to create a new table group based on county of interest
8. Link this new county table into ZCountyExtracts.sqlite
9. Using SQLite again on this county table, group unique record among different years of a parcel for the newest record using ImportParcelID and LoadID
10. Apply euclidean algorithm in order to identify subsidized parcels from the CHPC data to the Zillow data using my utils package
11. Apply my data cleaning function from my utils package. This will remove vacant properties, fix units to appropriate/estimated values, select residential buildings, and more. This will give more accurate unit approximations
12. Apply quantification procedures based on stipulations of Rent Control and JCE policies from the JC and RC inventory or using research

Contact me for information on the process of the creation of ZMainBldg.sqlite or anything else at
brian-truong@berkeley.edu
