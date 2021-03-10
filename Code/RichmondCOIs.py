
import geopandas as gpd
import maup
import pandas as pd

# load in block file and add population
blocks = gpd.read_file('./Blocks/tl_2010_51_tabblock10.shp')

pop = pd.read_csv('./Census/DECENNIALSF12010.P1_data_with_overlays_2021-03-01T113113.csv')

blocks['GEOID2'] = blocks['GEOID10'].map(lambda x:'1000000US'+x)
blocks = blocks.merge(pop, left_on='GEOID2', right_on='geoid', how='left')

# oad in COIs
richmond = gpd.read_file('./COI/Richmond COIs/Richmond COIs.shp')

# import maps
enacted = gpd.read_file('./COI/unconstitutional map/enacted.shp')

court = gpd.read_file('./COI/court ordered map/New_Map.shp')

reform = gpd.read_file('./COI/reform map/reform.shp')

# change crs 
proj_crs = richmond.crs

blocks = blocks.to_crs(proj_crs)
enacted = enacted.to_crs(proj_crs)
court = court.to_crs(proj_crs)
reform = reform.to_crs(proj_crs)

court['geometry'] = court['geometry'].buffer(0)
enacted['geometry'] = enacted['geometry'].buffer(0)
reform['geometry'] = reform['geometry'].buffer(0)

plan_dict = {'enacted':enacted,
             'court':court,
             'reform':reform}

# find blocks within each COI
for index,coi in richmond.iterrows():
    print(coi['entry_name'], str(coi['id']))
    coi_col = 'coi_' + str(coi['id'])
    coi_gdf = gpd.GeoDataFrame(pd.DataFrame(coi).transpose()).set_geometry('geometry').set_crs(proj_crs)
    coi_gdf_b = coi_gdf
    coi_gdf_b['geometry'] = coi_gdf_b['geometry'].buffer(35)
    blocks_within = gpd.sjoin(blocks, coi_gdf_b, op='within')
    blocks_within[coi_col] = True
    blocks[coi_col] = blocks_within[coi_col]


# create district columns for each map
plan_dict['court']['DistNum'] = plan_dict['court']['District_1'].map(lambda x:str(x).zfill(3))
plan_dict['enacted']['DistNum'] = plan_dict['enacted']['HOUSE_TA_6'].map(lambda x:str(x).zfill(3))
plan_dict['reform']['DistNum'] = plan_dict['reform']['DISTRICT_N'].map(lambda x:str(x).zfill(3))

plan_dict['court'].set_index('DistNum', inplace=True)
plan_dict['enacted'].set_index('DistNum', inplace=True)
plan_dict['reform'].set_index('DistNum', inplace=True)

# assign blocks to map districts
blocks['court'] = maup.assign(blocks, plan_dict['court'])
blocks['enacted'] = maup.assign(blocks, plan_dict['enacted'])
blocks['reform'] = maup.assign(blocks, plan_dict['reform'])

# isolate the blocks in richmond COIs
richmond_blocks = blocks.loc[(blocks['coi_1'] == True )|
                             (blocks['coi_2'] == True )|
                             (blocks['coi_3'] == True )|
                             (blocks['coi_4'] == True )|
                             (blocks['coi_5'] == True )|
                             (blocks['coi_6'] == True )|
                             (blocks['coi_7'] == True )|
                             (blocks['coi_8'] == True )|
                             (blocks['coi_9'] == True )|
                             (blocks['coi_10'] == True )|
                             (blocks['coi_11'] == True )|
                             (blocks['coi_12'] == True )|
                             (blocks['coi_13'] == True )]

# save COI blocks
richmond_blocks.to_file('./COI/richmond_all_blocks.shp')

# generate dataframe of COI population splits
coi_splits_df = pd.DataFrame(columns=['coi_id','coi_name','court', 'reform', 'enacted'])
pops_dict = {}

for i in range(1,14):
    coi_dict = {}
    coi_id = 'coi_' + str(i)
    coi_name = richmond.iloc[i-1]['entry_name']
    cur_blocks = richmond_blocks.loc[richmond_blocks[coi_id] == True]
    print('{0} blocks in {1} ({2})'.format(str(len(cur_blocks['GEOID10'])), coi_name, coi_id))
    #court
    cur_pops_court = cur_blocks.groupby('court').agg({'tot':'sum', 'GEOID10':'count'})
    court_list = list(cur_pops_court['tot'])
    coi_dict['court'] = court_list
    #enacted
    cur_pops_enacted = cur_blocks.groupby('enacted').agg({'tot':'sum', 'GEOID10':'count'})
    enacted_list = list(cur_pops_enacted['tot'])
    coi_dict['enacted'] = enacted_list
    #reform
    cur_pops_reform = cur_blocks.groupby('reform').agg({'tot':'sum', 'GEOID10':'count'})
    reform_list = list(cur_pops_reform['tot'])
    coi_dict['reform'] = reform_list
    #update coi dict
    pops_dict[coi_id] = coi_dict
    coi_splits_df = coi_splits_df.append({
     'coi_id':coi_id,
     'coi_name':coi_name,
     'court': court_list,
     'enacted': enacted_list,
     'reform': reform_list
     }, ignore_index=True)

# save COI splits
coi_splits_df.to_csv('./COI/richmond_pop_splits.csv')    

