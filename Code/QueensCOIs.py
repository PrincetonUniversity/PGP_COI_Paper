
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, LineString
from shapely.ops import split
import numpy as np
import sys
sys.path.append('./GitHub/gerrymander-geoprocessing/areal_interpolation')
import areal_interpolation as ai

#load in block file and add population
blocks = gpd.read_file ('.2010 Census Block shapefiles/NY/tl_2014_36_tabblock10.shp')
blocks.GEOID10 = blocks.GEOID10.astype(np.int64)

pop = pd.read_csv('./Blocks/NY2010pop.csv')
blocks = blocks.merge(pop, on =['GEOID10'])

#load in COIS
flushing = gpd.read_file('./COI shapefiles/Flushing/Flushing.shp')
proj_crs = flushing.crs
blocks = blocks.to_crs(proj_crs)

bayside = gpd.read_file('./COI shapefiles/Bayside/Bayside.shp')
bayside = bayside.to_crs(proj_crs)

#make COIs out of blocks
f_blocks = ai.aggregate(blocks, flushing, target_columns=['Community'])[0]
f_blocks = f_blocks.loc[f_blocks.Community == 'Flushing']
f_blocks.to_file('./COI shapefiles/Flushing/FlushingBlocks.shp')

b_blocks = ai.aggregate(blocks, bayside, target_columns=['Community'])[0]
b_blocks = b_blocks.loc[b_blocks.Community == 'Bayside']
b_blocks.to_file('./COI shapefiles/Bayside/BaysideBlocks.shp')


######################################################

#load in blocks
flushing = gpd.read_file('/Users/hwheelen/Desktop/COI shapefiles/Flushing/FlushingBlocks.shp')
bayside = gpd.read_file('/Users/hwheelen/Desktop/COI shapefiles/Bayside/BaysideBlocks.shp')

flushing = flushing.to_crs(proj_crs)
bayside = bayside.to_crs(proj_crs)
#load in maps

map1 = gpd.read_file('./NY District Maps/1997/Queens1997CD.shp') #1997 map

map2 = gpd.read_file('./NY District Maps/2002/Queens2002CD.shp') #2002 map

map3 = gpd.read_file('./NY District Maps/2012/Queens2012CD.shp') #2012 map

map1 = map1.to_crs(proj_crs)
map2 = map2.to_crs(proj_crs)
map3 = map3.to_crs(proj_crs)

#aggregate map1 
agg_f1 = ai.aggregate(flushing, map1, target_columns=['DISTRICT'])[0]
agg_b1 = ai.aggregate(bayside, map1, target_columns=['DISTRICT'])[0]

agg_f1['Dist1997'] = agg_f1['DISTRICT']
agg_b1['Dist1997'] = agg_b1['DISTRICT']

#aggregate map2
agg_f2 = ai.aggregate(agg_f1, map2, target_columns=['DISTRICT'])[0]
agg_b2 = ai.aggregate(agg_b1, map2, target_columns=['DISTRICT'])[0]

agg_f2['Dist2002'] = agg_f2['DISTRICT']
agg_b2['Dist2002'] = agg_b2['DISTRICT']
#aggregate map3
agg_f3 = ai.aggregate(agg_f2, map3, target_columns=['DISTRICT'])[0]
agg_b3 = ai.aggregate(agg_b2, map3, target_columns=['DISTRICT'])[0]

agg_f3['Dist2012'] = agg_f3['DISTRICT']
agg_b3['Dist2012'] = agg_b3['DISTRICT']

#save these shapefiles
agg_f3.to_file('./COI shapefiles/Flushing/FlushingBlocks_with_dists.shp')
agg_b3.to_file('./COI shapefiles/Bayside/BaysideBlocks_with_dists.shp')

#sum pops in 
#97
flushing_dict97 = {}

for dist in agg_f3['Dist1997'].unique():
    df = agg_f3.loc[agg_f3['Dist1997'] == dist]
    pop = df.tot.sum()
    flushing_dict97[dist] = pop
#02
flushing_dict02 = {}

for dist in agg_f3['Dist2002'].unique():
    df = agg_f3.loc[agg_f3['Dist2002'] == dist]
    pop = df.tot.sum()
    flushing_dict02[dist] = pop    

#12
flushing_dict12 = {}

for dist in agg_f3['Dist2012'].unique():
    df = agg_f3.loc[agg_f3['Dist2012'] == dist]
    pop = df.tot.sum()
    flushing_dict12[dist] = pop
    
#sum pops in bayside
#97
bayside_dict97 = {}

for dist in agg_b3['Dist1997'].unique():
    df = agg_b3.loc[agg_b3['Dist1997'] == dist]
    pop = df.tot.sum()
    bayside_dict97[dist] = pop

#02
bayside_dict02 = {}

for dist in agg_b3['Dist2002'].unique():
    df = agg_b3.loc[agg_b3['Dist2002'] == dist]
    pop = df.tot.sum()
    bayside_dict02[dist] = pop

#97
bayside_dict12 = {}

for dist in agg_b3['Dist2012'].unique():
    df = agg_b3.loc[agg_b3['Dist2012'] == dist]
    pop = df.tot.sum()
    bayside_dict12[dist] = pop

print('Flushing 97',flushing_dict97)
print('Flushing 02',flushing_dict02)
print('Flushing 12',flushing_dict12)
 
print('Bayside 97',bayside_dict97)
print('Bayside 02',bayside_dict02)
print('Bayside 12',bayside_dict12)

print('1997',flushing_dict97,bayside_dict97 )
print('2002',flushing_dict02,bayside_dict02 )
print('2012',flushing_dict12,bayside_dict12 )

#save shapefiles
flushing['Community'] = 'Flushing'
flush = flushing.dissolve(by = 'Community',aggfunc='sum')
flush = flush.buffer(.1)
flush.to_file('./COI shapefiles/Flushing/Flushing.shp')

bayside['Community'] = 'Bayside'
bay = bayside.dissolve(by = 'Community',aggfunc='sum')
bay = bay.buffer(.1)
bay.to_file('./COI shapefiles/Bayside/Bayside.shp')

        