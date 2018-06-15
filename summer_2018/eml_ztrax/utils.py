# function  to add subsidized or not
def add_subsidized(county, grouped=False, sql=False):
    import numpy as np
    import pandas as pd
    import sqlalchemy
    if sql:
        sqlite_uri = "sqlite:///ZCountyExtracts.sqlite"
        zce_engine = sqlalchemy.create_engine(sqlite_uri)
        print(zce_engine.table_names())
        sql_expr = "SELECT * FROM " + county + ";" 
        df = pd.read_sql(sql_expr, zce_engine)
        display(df.head())
    else:
        fields = ['RowID' ,'ImportParcelID' ,'FIPS' ,'State' ,'County' ,'ValueCertDate' ,'ExtractDate' ,'Edition' ,'ZVendorStndCode' ,'AssessorParcelNumber' ,'DupAPN' ,'ParcelSequenceNumber' ,'ParcelNumberTypeStndCode' ,'RecordSourceStndCode' ,'RecordTypeStndCode' ,'ConfidentialRecordFlag' ,'PropertyAddressSourceStndCode' ,'PropertyHouseNumber' ,'PropertyHouseNumberExt' ,'PropertyStreetPreDirectional' ,'PropertyStreetName' ,'PropertyStreetSuffix' ,'PropertyStreetPostDirectional' ,'PropertyFullStreetAddress' ,'PropertyCity' ,'PropertyState' ,'PropertyZip' ,'OriginalPropertyFullStreetAddress' ,'OriginalPropertyAddressLastline' ,'PropertyBuildingNumber' ,'PropertyZoningDescription' ,'PropertyZoningSourceCode' ,'CensusTract' ,'TaxIDNumber' ,'TaxAmount' ,'TaxYear' ,'TaxDelinquencyFlag' ,'TaxDelinquencyAmount' ,'TaxDelinquencyYear' ,'TaxRateCodeArea' ,'LegalLot' ,'LegalLotStndCode' ,'LegalOtherLot' ,'LegalBlock' ,'LegalSubdivisionCode' ,'LegalSubdivisionName' ,'LegalCondoProjectPUDDevName' ,'LegalBuildingNumber' ,'LegalUnit' ,'LegalSection' ,'LegalPhase' ,'LegalTract' ,'LegalDistrict' ,'LegalMunicipality' ,'LegalCity' ,'LegalTownship' ,'LegalSTRSection' ,'LegalSTRTownship' ,'LegalSTRRange' ,'LegalSTRMeridian' ,'LegalSecTwnRngMer' ,'LegalRecordersMapReference' ,'LegalDescription' ,'LegalNeighborhoodSourceCode' ,'NoOfBuildings' ,'LotSizeAcres' ,'LotSizeSquareFeet' ,'LotSizeFrontageFeet' ,'LotSizeDepthFeet' ,'LotSizeIRR' ,'LotSiteTopographyStndCode' ,'LoadID' ,'PropertyAddressMatchcode' ,'PropertyAddressUnitDesignator' ,'PropertyAddressUnitNumber' ,'PropertyAddressCarrierRoute' ,'PropertyAddressGeoCodeMatchCode' ,'PropertyAddressLatitude' ,'PropertyAddressLongitude' ,'PropertyAddressCensusTractAndBlock' ,'PropertyAddressConfidenceScore' ,'PropertyAddressCBSACode' ,'PropertyAddressCBSADivisionCode' ,'PropertyAddressMatchType' ,'PropertyAddressDPV' ,'PropertyGeocodeQualityCode' ,'PropertyAddressQualityCode' ,'SubEdition' ,'BatchID' ,'BKFSPID', 'RowID2' ,'NoOfUnits' ,'OccupancyStatusStndCode' ,'PropertyCountyLandUseDescription' ,'PropertyCountyLandUseCode' ,'PropertyLandUseStndCode' ,'PropertyStateLandUseDescription' ,'PropertyStateLandUseCode' ,'BuildingOrImprovementNumber' ,'BuildingClassStndCode' ,'BuildingQualityStndCode' ,'BuildingQualityStndCodeOriginal' ,'BuildingConditionStndCode' ,'ArchitecturalStyleStndCode' ,'YearBuilt' ,'EffectiveYearBuilt' ,'YearRemodeled' ,'NoOfStories' ,'TotalRooms' ,'TotalBedrooms' ,'TotalKitchens' ,'FullBath' ,'ThreeQuarterBath' ,'HalfBath' ,'QuarterBath' ,'TotalActualBathCount' ,'BathSourceStndCode' ,'TotalBathPlumbingFixtures' ,'RoofCoverStndCode' ,'RoofStructureTypeStndCode' ,'HeatingTypeorSystemStndCode' ,'AirConditioningTypeorSystemStndCode' ,'FoundationTypeStndCode' ,'ElevatorStndCode' ,'FireplaceFlag' ,'FirePlaceTypeStndCode' ,'FireplaceNumber' ,'WaterStndCode' ,'SewerStndCode' ,'MortgageLenderName' ,'TimeshareStndCode' ,'Comments' ,'StoryTypeStndCode']
        df = pd.read_csv(county+'.csv', sep=',', names=fields, header=None)
    
    # get most recent parcel
    #if ~grouped:
        #df = df.sort('LoadID', ascending=False).groupby('ImportParcelID', as_index=False).first()

    # Load CHPC which will help determine if property is subsidized
    chpc = pd.read_excel('chpc.xls', sheet_name='Cleaned')
    # Compare Address numbers and name 
    chpc['Address_Num'] = chpc['Address_Cleaned'].str.extract(r'(\d+)')
    chpc['Address_Name'] = chpc['Address_Cleaned'].str.extract(r'([^\d,-]\w+)').str.upper()
    # Merge based on euclidean distance
    chpc = chpc.dropna(subset=['Longitude', 'Latitude'])
    def merge_euclidean(table, eps=0.01):
        chpc_list = []
        table['merge_row'] = table.index.values
        for i, row in table.iterrows():
            chpc_subset = chpc.loc[((chpc.Longitude - row.PropertyAddressLongitude)**2 + (chpc.Latitude - row.PropertyAddressLatitude)**2 < eps) & (chpc.Address_Num == row.PropertyHouseNumber)]
            chpc_subset['merge_row'] = i
            chpc_list.append(chpc_subset)
        chpc_found = pd.concat(chpc_list)

        result = pd.merge(table, chpc_found, on='merge_row', how='left')
        return result
    df.to_csv(county+'.csv', sep='|', index=False)
    df = pd.read_csv(county+'.csv', sep='|')
    chpc_df = merge_euclidean(df, eps=0.0000001)
    chpc_df = (chpc_df.dropna(subset=['Longitude', 'Latitude']))
    # Going to add subsidez column now
    chpc_df = chpc_df[['ImportParcelID']]
    chpc_df['Subsidized'] = 'Y'
    df = pd.merge(df, chpc_df, on=['ImportParcelID'], how='left')
    value = {'Subsidized': 'N'}
    df.fillna(value=value, inplace=True)
    df.to_csv(county+'_v2.csv', sep='|', index=False)
    display(df.head())
    return df
    
def clean_city(county, city):
    import numpy as np
    import pandas as pd
    data_dict = pd.read_excel('ZAsmt_DataDictionary_2016-01.xlsx', sheet_name='LandUse', header=5, usecols=np.arange(4))
    residential = data_dict[data_dict['Prefix Code Classification'].isin(['RI', 'RR'])]
    R = residential['StndCode']
    progress = np.linspace(0, 100, 7)[1:]
    df = county[county.PropertyCity == city]
    print(str(round(progress[0], 2))+'%', 'current number:', df.NoOfUnits.sum())
    # Include only Residentials
    df = df[df['PropertyLandUseStndCode'].isin(R)]
    print(str(round(progress[1], 2))+'%', 'current number:', df.NoOfUnits.sum())
    # Remove vacant
    df = df[~df['PropertyCountyLandUseDescription'].str.contains('VAC')]
    print(str(round(progress[2], 2))+'%', 'current number:', df.NoOfUnits.sum())
    medians = df.groupby('PropertyLandUseStndCode')['NoOfUnits'].median()
    import math
    def fix_units(r):
        code = r['PropertyLandUseStndCode']
        units = r['NoOfUnits']
        # return median if 0 or NaN
        if units == 0.0 or math.isnan(units):
            return medians[code]
        elif code == 'RI101': # duplex
            return 2.0
        elif code == 'RI102': # triplex
            return 3.0
        elif code == 'RI103': # quad
            return 4.0
        elif code == 'RI104' and units < 5.0:
            return medians[code]
        elif code == 'RI105' and units < 100.0:
            return medians[code]
        elif code == 'RI106' and units < 5.0:
            return medians[code]
        
        return r['NoOfUnits']
    df['NoOfUnits'] = df.apply(fix_units, axis=1)
    print(str(round(progress[3], 2))+'%', 'current number:', df.NoOfUnits.sum())
    # Fill nans with 1 for now
    value = {'NoOfUnits': 1}
    df.fillna(value=value, inplace=True)
    print(str(round(progress[4], 2))+'%', 'current number:', df.NoOfUnits.sum())
    # Fill 0's with 1 for now
    df = df.replace({'NoOfUnits': {0: 1}}) 
    print(str(round(progress[5], 2))+'%', 'current number:', df.NoOfUnits.sum())
    return df