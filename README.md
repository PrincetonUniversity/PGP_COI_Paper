# EIL Community of Interest Paper

This file describes the process taken to prepare results for the EIL COI paper

## Datasets

Flushing and Bayside maps
Flushing and Bayside shapefiles

New York census blocks
New York population

Greater Richmond COIs shapefile

Virginia census blocks
Virginia population

NY 1997 Congressional map
NY 2002 Congressional map
NY 2012 Congressional map

Virginia 2012 State Senate map
Virginia 2018 State Senate map
Princeton Gerrymandering Project's Reform map

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
