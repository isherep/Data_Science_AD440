# What percentage of Hispanics identify as White?
print(100 * states["hispanic_white"].sum() / states["hispanic"].sum())

# Set list of Hispanic race column names
hispanic_races = [
                  "hispanic_white",
                  "hispanic_black", "hispanic_aian",
                  "hispanic_asian", "hispanic_pacific",
                  "hispanic_other", "hispanic_multiracial"
                  ]

# What percentage of Hispanics identify as each race?
print(100 * states[hispanic_races].sum() / states["hispanic"].sum())


# What percentage of Hispanics identify as each race?
print(100 * states[hispanic_races].sum() / states["hispanic"].sum())

# Create a deep copy of only the Hispanic race columns
states_hr = states[hispanic_races].copy()

# Calculate percentages for all columns in the date frame
for race in hispanic_races:
    states_hr[race] = 100 * states_hr[race] / states["hispanic"]

# View the result
print(states_hr.head())



'''
    Create a boxplot by setting the data parameter to the name of the data frame. (orient = "h" will plot the boxplots horizontally.)
    Using squeeze, show the state with the largest value in column hispanic_white.
    Using squeeze, show the state with the smallest value in column hispanic_other.
    Notice that very few Hispanics identify as Asian, but one state is a high outlier. Using squeeze, show the state with the largest value in column hispanic_asian.
    '''
# Import seaborn and matplotlib.plt
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Create a boxplot
sns.boxplot(data = states_hr, orient = "h")
plt.show()

# Show states with extreme values in various columns
print(states_hr.nlargest(1, "hispanic_white").squeeze())
print(states_hr.nsmallest(1, "hispanic_other").squeeze())
print(states_hr.nlargest(1, "hispanic_asian").squeeze())

'''
    In this exercise, you will construct an API request to retrieve the average family size and median age for all states in the United States. The data will come from Summary File 1 of the 2010 Decennial Census.
    
    requests has been imported for you.
'''
# Build base URL
HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])

# Specify Census variables and other predicates
get_vars = ["NAME", "P013001", "P037001"]
predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "state:*"

# Execute the request, examine text of response object
r = requests.get(base_url, params=predicates)
print(r.text)




'''
    In this exercise you will load data from an API response object into a pandas data frame. You will assign user-friendly column names and convert the values from strings to appropriate data types.
    
    After creating the data frame, run the sample code to create a scatterplot to visualize the relationship between average family size and median age in the United States.
    
    requests and pandas (as pd) have already been imported. A response object r is loaded.
'''

# Import seaborn
import seaborn as sns
sns.set()

# Construct the data frame
col_names = ["name", "median_age", "avg_family_size", "state"]
states = pd.DataFrame(columns = col_names, data = r.json()[1:])

# Convert each column with numeric data to an appropriate type
states["median_age"] = states["median_age"].astype(float)
states["avg_family_size"] = states["avg_family_size"].astype(float)

# Scatterplot with regression line
sns.lmplot(x = "avg_family_size", y = "median_age", data = states)
plt.show()

'''
    In this exercise, you will investigate where juvenile offenders are incarcerated. This exercise introduces the concept of "group quarters" populations, which includes college dorms, correctional facilities, nursing homes, military bases, etc.
    
    You will visualize the percentage, by state, of incarcerated minor males in adult correctional facilities. The variables to request are:
    
    PCT021005 - Male: Under 18 years: Institutionalized population: Correctional facilities for adults
    PCT021015 - Male: Under 18 years: Institutionalized population: Juvenile facilities: Correctional facilities intended for juveniles
    requests has been imported. The base_url for the API request has been defined.
    
    pandas and seaborn have been imported using the usual aliases.
    
'''

# Specify variables and execute API request
get_vars = ["NAME", "PCT021005", "PCT021015"]
predicates["get"] = ",".join(get_vars)
r = requests.get(base_url, params=predicates)

# Construct data frame
col_names = ["name", "in_adult", "in_juvenile", "state"]
states = pd.DataFrame(columns=col_names, data=r.json()[1:])
states[["in_adult", "in_juvenile"]] = states[["in_adult", "in_juvenile"]].astype(int)

# Calculate percentage of incarcerated male minors in adult facilities
states["pct_in_adult"] = 100 * states["in_adult"] / (states["in_adult"] + states["in_juvenile"])
states.sort_values(by = "pct_in_adult", ascending = False, inplace = True)
sns.stripplot(x = "pct_in_adult", y = "name", data = states)
plt.show()


'''
    In this exercise you will practice looking up geographic identifiers for major cities. The Census classifies cities and other municipalities as "places". You will find place codes using the Geographic Codes Lookup at the Missouri Census Data Center: https://census.missouri.edu/geocodes/
    
    The variables to request are place names and total population.
    
    The requests library has been imported and the base_url for the request is already set to request SF1 data for 2010.
'''
# Build dictionary of predicates
get_vars = ["NAME", "P001001"] # <- total population
predicates = {}
predicates["get"] = ",".join(get_vars)
predicates["for"] = "place:60000,61000"
predicates["in"] = "state:42"

# Execute the request
r = requests.get(base_url, params=predicates)

# Show the response text
print(r.text)

'''
    A Pennsylvania-based family advocacy nonprofit wants to find the average family size by Congressional district, so that they can call representatives from districts with relatively large families. For this exercise you will have to know the GEOID (ANSI Code) for Pennsylvania. If you don't remember it from a previous exercise, use the Geographic Codes Lookup at https://census.missouri.edu/geocodes/.
    
    The requests and pandas (as pd) packages have been imported. The base_url is defined, as is the predicates dictionary with the list of variables to request.
'''

# Build dictionary of predicates and execute the request
predicates["for"] = "congressional district:*"
predicates["in"] = "state:42"
r = requests.get(base_url, params=predicates)

# Construct the data frame
col_names = ["name", "avg_family_size", "state", "cd"]
cd = pd.DataFrame(columns=col_names, data=r.json()[1:])


# Print the head of the "avg_family_size" column
print(cd["avg_family_size"].head())

# Set data type and print
cd["avg_family_size"] = cd["avg_family_size"].astype(float)
print(cd)

'''
    ip Code Tabulation Areas
    In the marketing field, it is very common to want to know ZIP Code demographics. ZIP Code Tabulation Areas ("ZCTAs") are Census-defined equivalents to ZIP Codes that are built out of Census blocks. In this exercise you will request total population for all ZCTAs in the state of Alabama.
    
    In pandas, an index can be used to retrieve particular rows. The GEOIDs are suitable row identifiers. In this exercise you will set a multilevel index based on the state and ZCTA of each row.
    
    The requests and pandas packages have been imported. The base_url is defined, as is the predicates dictionary with the list of variables to request.
    '''

# Build dictionary of predicates and execute the request
predicates = {}
predicates["get"] = ",".join(["NAME", "P001001"])
predicates["for"] = "zip code tabulation area (or part):*"
predicates["in"] = "state:01"
r = requests.get(base_url, params=predicates)

# Construct the data frame
col_names = ["name", "total_pop", "state", "zcta"]
zctas = pd.DataFrame(columns=col_names, data=r.json()[1:])
zctas["total_pop"] = zctas["total_pop"].astype(int)

# Set multilevel index from GEOIDs and print the head
zctas.set_index(["state", "zcta"], inplace = True)
print(zctas.head())


'''
    Calculate Proportions
    Nationally, 55% of Hispanics identify as White and 35% identify as "Some Other Race". (You can run Line 2 in the code window to confirm this.) But there is substantial state-to-state variation, which we will now investigate. As a reminder, we will express proportions as percentages throughout this course.
    
    pandas has been imported, the data frame states is loaded with population counts by race and Hispanic origin. A list, hispanic_races, has names of columns with Hispanics by race data, and is shown in the console.
    '''
# What percentage of Hispanics identify as each race?
print(100 * states[hispanic_races].sum() / states["hispanic"].sum())

# Create a deep copy of only the Hispanic race columns
states_hr = states[hispanic_races].copy()

# Calculate percentages for all columns in the date frame
for race in hispanic_races:
    states_hr[race] = 100 * states_hr[race] / states["hispanic"]

# View the result
print(states_hr.head())



'''
    Zip Code Tabulation Areas
    In the marketing field, it is very common to want to know ZIP Code demographics. ZIP Code Tabulation Areas ("ZCTAs") are Census-defined equivalents to ZIP Codes that are built out of Census blocks. In this exercise you will request total population for all ZCTAs in the state of Alabama.
    
    In pandas, an index can be used to retrieve particular rows. The GEOIDs are suitable row identifiers. In this exercise you will set a multilevel index based on the state and ZCTA of each row.
    
    The requests and pandas packages have been imported. The base_url is defined, as is the predicates dictionary with the list of variables to request.
    '''
# Build dictionary of predicates and execute the request
predicates = {}
predicates["get"] = ",".join(["NAME", "P001001"])
predicates["for"] = "zip code tabulation area (or part):*"
predicates["in"] = "state:01"
r = requests.get(base_url, params=predicates)

# Construct the data frame
col_names = ["name", "total_pop", "state", "zcta"]
zctas = pd.DataFrame(columns=col_names, data=r.json()[1:])
zctas["total_pop"] = zctas["total_pop"].astype(int)

# Set multilevel index from GEOIDs and print the head
zctas.set_index(["state", "zcta"], inplace = True)
print(zctas.head())


# Chapter 2

# Loop over years 2011 to 2017
for year in range(2011, 2018):
    base_url = "/".join([HOST, str(year), dataset])
    r = requests.get(base_url, params=predicates)
    df = pd.DataFrame(columns=col_names, data=r.json()[1:])
    # Add column to df to hold year value, append df to collector dfs
    df["year"] = year
    dfs.append(df)

# Concatenate all data frames, fix column type
states = pd.concat(dfs)
states["median_home_value"] = states["median_home_value"].astype(int)

sns.lineplot("year", "median_home_value", data = states)
plt.show()


'''
   2. Health Insurance Coverage
    The Affordable Care Act went into effect in 2014. One of its goals was to increase health insurance coverage among healthy young adults. Has health insurance coverage among 19-25 year olds changed with the passage of the Affordable Care Act? Let's calculate the percentage point change in coverage by state. Then plot the change against the initial percent covered rate.
    
    ACS Table B27022 - "Health Insurance Coverage Status By Sex By Enrollment Status For Young Adults Aged 19 To 25" has been loaded. Columns names (printed to the console) indicate breakdowns by sex (m/f), school enrollment (school/noschool) and insurance (insured/uninsured).
    
    As a reminder, we are using percentages throughout this course.
    
    pandas and seaborn have been imported using the usual aliases.
    
    
    Calculate the percentage insured as 100 times the insured_total, divided by the total population
    Create a pivot table states_pvt with rows representing states (index = "state"), columns as years (columns = "year"), and values as "pct_insured"
    Calculate the change in percentage insured by subtracting pct_insured_2013 from pct_insured_2017
    Plot the change in insurance rate (y) against the rate in 2013 (x)
    
    '''

# Calculate percent insured
states["insured_total"] = states["m_school_insured"] +  states["m_noschool_insured"] + states["f_school_insured"] + states["f_noschool_insured"]
states["pct_insured"] = 100 * states["insured_total"] / states["total"]

# Pivot the table and rename the columns
states_pvt = states.pivot(index = "state", columns = "year", values = "pct_insured")
states_pvt.columns = ["pct_insured_2013", "pct_insured_2017"]

# Calculate the change in insurance rates 2013 to 2017
states_pvt["pct_insured_change"] = states_pvt["pct_insured_2017"] - states_pvt["pct_insured_2013"]

# Plot the change against initial (2013) insurance rates
sns.lmplot(x = "pct_insured_2013", y = "pct_insured_change", data = states_pvt)
plt.show()

'''
    4.Plotting Margins of Error over Time
    In this exercise you will inspect changing home prices in Philadelphia, PA, using a line plot with error bars. The data come from ACS 1-year sample Table B25077. The estimates and margin of error for each year from 2011 to 2017 have been downloaded and concatenated into a pandas data frame named philly. ACS table variables for the estimate and margin of error have been renamed to median_home_value and median_home_value_moe, respectively. (See the data frame in the console.)
    
    pandas has been imported as pd.
    '''

# Import graphics packages
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

# Calculate and inspect Relative Margin of Error
philly["rmoe"] = 100 * philly["median_home_value_moe"] / philly["median_home_value"]
print(philly)

# Create line plot with error bars of 90% MOE
plt.errorbar("year", "median_home_value", yerr = "median_home_value_moe", data = philly)
plt.show()


# Import graphics packages
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt

# Calculate and inspect Relative Margin of Error
philly["rmoe"] = 100 * philly["median_home_value_moe"] / philly["median_home_value"]
print(philly)

# Create line plot with error bars of 90% MOE
plt.errorbar("year", "median_home_value", yerr = "median_home_value_moe", data = philly)
plt.show()

'''

    Set x1 to the current year median home value, and x2 to the median home value for the prior year (current year minus 1)
    Set se_x1 to the current year MOE of the median home value divided by Z_CRIT, and se_x2 to the same calculation for the prior year
    Use Python's ternary operator (result1 if condition else result2) to return the empty string if the absolute value of z is greater than Z_CRIT, and otherwise return "not "

'''
# Set the critical Z score for 90% confidence, prepare message
Z_CRIT = 1.645
msg = "Philadelphia median home values in {} were {}significantly different from {}."
for year in range(2012, 2018):
    # Assign current and prior year's median home value to variables
    x1 = int(philly[philly["year"] == year]["median_home_value"])
    x2 = int(philly[philly["year"] == year - 1]["median_home_value"])
    
    # Calculate standard error as 90% MOE / critical Z score
    se_x1 = float(philly[philly["year"] == year]["median_home_value_moe"] / Z_CRIT)
    se_x2 = float(philly[philly["year"] == year - 1]["median_home_value_moe"] / Z_CRIT)
    
    # Calculate two-sample z-statistic, output message if greater than critical Z score
    z = (x1 - x2) / sqrt(se_x1**2 + se_x2**2)
    print(msg.format(year, "" if abs(z) > Z_CRIT else "not ", year - 1))

'''
    Significance of Difference of Proportions
    
    Bike commuting is still uncommon, but Washington, DC, has a decent share. It has increased by over 1 percentage point in the last few years, but is this a statistically significant increase? In this exercise you will calculate the standard error of a proportion, then a two-sample Z-statistic of the proportions.
    
    The formula for the standard error (SE) of a proportion is:
    
    SEP=1NSE2n−P2SE2N‾‾‾‾‾‾‾‾‾‾‾‾‾√
    
    The formula for the two-sample Z-statistic is:
    
    Z=x1−x2SE2x1+SE2x2‾‾‾‾‾‾‾‾‾‾‾√
    
    The data frame dc is loaded. It has columns (shown in the console) with estimates (ending "_est") and margins of error (ending "_moe") for total workers and bike commuters.
    
    The sqrt function has been imported from the numpy module.
'''
# Set the critical Z score for 90% confidence
Z_CRIT = 1.645

# Calculate share of bike commuting
dc["bike_share"] = dc["bike_est"] / dc["total_est"]

# Calculate standard errors of the estimate from MOEs
dc["se_bike"] = dc["bike_moe"] / Z_CRIT
dc["se_total"] = dc["total_moe"] / Z_CRIT
dc["se_p"] = sqrt(dc["se_bike"]**2 - dc["bike_share"]**2 * dc["se_total"]**2) / dc["total_est"]

# Calculate the two sample statistic between 2011 and 2017
Z = (dc[dc["year"] == 2017]["bike_share"] - dc[dc["year"] == 2011]["bike_share"]) / \
    sqrt(dc[dc["year"] == 2017]["se_p"]**2 + dc[dc["year"] == 2011]["se_p"]**2)
print(Z_CRIT < Z)
