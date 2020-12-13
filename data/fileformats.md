# Format of Data

<h2> Forest Fire Data </h2>

Forest Fire Data must be a .csv file containing the columns in the example table
below. All values should be **floating point values** with the exception of month and day,
which should be **strings** (lowercase only) with their first three letters. For example,
**"March"** should be written as **"mar"** and **"Friday"** should be written as **"fri"**.
Example set with one row:


 X | Y | month | day | FFMC | DMC | DC | ISI | temp | RH | wind | rain | area
-- | - | ----- | --- | ---- | --- | -- | --- | ---- | -- | ---- | ---- | ----
8 | 6 | sep | tue | 91 | 129.5 | 63.6 | 7 | 13.1 | 63 | 5.4 | 0 | 0

<h2> Temperature Data </h2>

Temperature Data should be a .csv file containing the columns in the example table
below. Dates should be in the format **year-month-day**, temperatures and error should be
**floating point values**, and city/country are **strings**.
Example set with one row:

 date | temperature | error | city | country | latitude | longitude
----- | ----------- | ----- | ---- | ------- | -------- | ---------
1753-01-01 | 7.106 | 5.358 | Amadora | Portugal | 39.38N | 8.32W
