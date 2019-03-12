Any files meeting the below criteria place in the "sounding_tables" folder will be loaded into the UI 

Tank Naming Conventions / File Names are as follows

TYPE followed by 2 digit number and position

e.g.

BALLAST 01P.csv
BALLAST 01S.csv
BALLAST 01C.csv

Valid TYPES

BALLAST
FO
DO
SLUDGE
BILGE
GW
BW
GREY WATER
BLACK WATER

files must be .csv format and can be produced easily and edited in excel, they must be formatted as follows

Trim followed by trim options
sounding in cm followed by value in m3, currently only trim 0 is accepted

e.g.

Trim,0
0,0.1
1,0.2
2,0.3
3,0.5
4,0.6
5,0.7
6,0.8
7,0.9



