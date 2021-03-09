# EIL Community of Interest Paper

This file describes the process taken to prepare results for the EIL COI paper

## Datasets

[Flushing](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/New%20York/Flushing.zip) and [Bayside](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/New%20York/Bayside.zip) shapefiles

[New York census blocks](https://catalog.data.gov/dataset/tiger-line-shapefile-2014-2010-state-new-york-2010-census-block-state-based-shapefile)
[New York population](https://github.com/PrincetonUniversity/PGP_COI_Paper/tree/master/Data/New%20York/Blocks)

[NY 1997 Congressional map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/New%20York/NY%20District%20Maps/1997.zip)
[NY 2002 Congressional map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/New%20York/NY%20District%20Maps/2002.zip)
[NY 2012 Congressional map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/New%20York/NY%20District%20Maps/2012.zip)

[Greater Richmond COIs shapefile](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/Virginia/Richmond%20COIs.zip)

[Virginia census blocks](https://www2.census.gov/geo/pvs/tiger2010st/51_Virginia/51/tl_2010_51_tabblock10.zip)
[Virginia population](https://github.com/PrincetonUniversity/PGP_COI_Paper/tree/master/Data/Virginia/blocks)


[Virginia 2012 State Senate map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/Virginia/unconstitutional%20map.zip)
[Virginia 2018 State Senate map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/Virginia/court%20ordered%20map.zip)
[Princeton Gerrymandering Project's Reform map](https://github.com/PrincetonUniversity/PGP_COI_Paper/blob/master/Data/Virginia/reform%20map.zip)

## Processing

__Flushing and Bayside__

Using QueensCOIs.py, New York population is merged into census blocks, and then
labels are given to all census blocks in one of the two COIS.
Next, labels from each map are assigned to these blocks, and we calculate the
proportion of population in pieces of the COIs split by each set of congressional districts.

__Greater Richmond__

Using coi_splitting_VA.py, Virginia's 2010 census blocks are given labels when they are
part of any of the Greater Richmond COIs in our dataset. They are then given labels
for each of the three maps we are considering, and the proportion of population in
each split of each community is calculated and recorded.

##Calculations

All calculations of different splitting metrics were done in this [google sheet](https://docs.google.com/spreadsheets/d/1iPqaEaam9to_p9xZTHkQTkGv7PEYO036Agnc11oNWHk/edit#gid=0). Only population proportions for each of the splits are needed for any of these calculations.
