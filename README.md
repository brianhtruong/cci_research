# cci_research

##### We are working to quantify a) the current state of tenant protections coverage in California, and b) hypothetical tenant protections coverage scenarios under reform. The two tenant protections we are looking at are (1) rent stabilization, which caps the amount a landlord can increase a tenant’s rent (usually tied to inflation), and (2) Just Cause for Evictions protections, which makes it so legally landlords can only evict tenants for specific “just causes” listed in the law. 

#### HOW TO QUANTIFY (GENERAL STEPS)
1. Import into ZCountyExtracts.sqlite the county of interest from ZMainBldg.sqlite with SQL
2. Group unique record among different years of a parcel for the newest record using ImportParcelID and LoadID
3. Add Subsidized column to county dataset and save dataset (using my utils package)
4. Commit initial data cleaning process for city in county of interest (using my utils package)
5. Apply quantification procedures based on stipulations of Rent Control and JCE policies
