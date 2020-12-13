# Format of Data

First Header | Second Header
------------ | -------------
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column

Forest Fire Data must be a .csv file containing the following columns:
X,Y,month,day,FFMC,DMC,DC,ISI,temp,RH,wind,rain,area
X | Y | month | day | FFMC | DMC | DC | ISI | temp | RH | wind | rain | area
Content from cell 1 | Content from cell 2
Content in the first column | Content in the second column

All values should be floating point values with the exception of month and day,
which should be strings lowercase only with the first three letters. For example,
"March" should be written as "mar" and "Friday" should be written as "fri".
Example row:

8,6,sep,tue,91,129.5,692.6,7,13.1,63,5.4,0,0

Temperature Data should be a .csv file containing the following columns:
date,temperatures,error,city,country,latitude,longitude

Dates should be in the format year-month-day, temperatures and error should be
floating point values, and city/country are strings.
Example row:

1753-01-01,7.106,5.358,Amadora,Portugal,39.38N,8.32W