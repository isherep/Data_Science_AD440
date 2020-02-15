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
