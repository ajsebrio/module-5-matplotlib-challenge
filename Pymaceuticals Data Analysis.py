#!/usr/bin/env python
# coding: utf-8

# # Pymaceuticals Inc.
# ---
# 
# ### Analysis
# - Overall, the mouse sample size distribution is even in terms of sex: 51% male and 49% female. The weight and age vary, which is a good distribution to determine if these variables are a factor in the efficacy of the drug they are being treated with. Targeting a specific weight or age group will limit the scope of the study, which would then limit the number of intended users.
# 
# 
# - The drugs Capomulin and Ramicane, show a decrease of tumor size over the course of 45 days, which suggests that they are effective drugs in reducing the tumor volume. 
# 
# 
# - The drug, Infubinol, shows an increase in volume of tumor within 45 days of the study, which suggests it has a negative effect by increasing the tumor volume. In addition, there is an outlier when determining the distribution of the final tumor volume (mm3) across each drug treatment. This could mean this mouse sample did not react in the same behavior as the other mouse samples treated with Infubinol, a documentation error, or contaminant. The cause of the outlier is indeterminant. 
# 
# 
# - Based on the summary statistics of each drug, Capomulin and Ramicane show the lowest values for variance, standard deviation, and standard error of the means (SEM). A low value for these statistics means low variability across each mice sample being treated with these drugs, which may suggest these drugs are stable and able to reproduce consistent results.
# 
# 
# - Ketapril has the greatest standard deviation, variance, and standard error of means, which suggests there is too much variability between each mouse treated with this drug. This may not be the best choice, since the drug does not show stability across the mouse samples treated with Ketapril.
# 
# 
# - There is a positive linear regression between weight and average tumor volume with a coefficient of correlation value of 0.85. The two are dependent variables. In other words, the greater the weight (g) of the mouse, the greater the tumor volume (mm3). 
# 
# 
# - In conclusion, Capomulin and Ramicane are drugs showing promising results for treating squamous cell carcinoma (SCC) in mice by decreasing the tumor volume over time.
# 

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st

# Study data files
mouse_metadata_path = "data/Mouse_metadata.csv"
study_results_path = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata_path)
study_results = pd.read_csv(study_results_path)

# Combine the data into a single DataFrame
combined_data_df = pd.merge(study_results, mouse_metadata, how="left", on="Mouse ID")

# Display the data table for preview
combined_data_df.head()


# In[2]:


# Checking the number of mice.
number_mice = len(combined_data_df["Mouse ID"].unique())
number_mice


# In[3]:


# Our data should be uniquely identified by Mouse ID and Timepoint
# Get the duplicate mice by ID number that shows up for Mouse ID and Timepoint. 
duplicated_mouse_ids = combined_data_df[combined_data_df.duplicated(subset=["Mouse ID", "Timepoint"])]["Mouse ID"].unique()
duplicated_mouse_ids


# In[4]:


# Optional: Get all the data for the duplicate mouse ID. 
duplicated_mouse_dataset = combined_data_df[combined_data_df["Mouse ID"] == "g989"]
duplicated_mouse_dataset


# In[5]:


# Create a clean DataFrame by dropping the duplicate mouse by its ID.
clean_combined_data = combined_data_df[combined_data_df["Mouse ID"].isin(duplicated_mouse_ids) == False]
clean_combined_data


# In[6]:


# Checking the number of mice in the clean DataFrame.
len(clean_combined_data["Mouse ID"].unique())


# ## Summary Statistics

# In[7]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen



# Use groupby and summary statistical methods to calculate the following properties of each drug regimen: 
# mean, median, variance, standard deviation, and SEM of the tumor volume. 
# Assemble the resulting series into a single summary DataFrame.

mean_tumor_volume = clean_combined_data.groupby(["Drug Regimen"])["Tumor Volume (mm3)"].mean()
median_tumor_volume = clean_combined_data.groupby(["Drug Regimen"])["Tumor Volume (mm3)"].median()
var_tumor_volume = clean_combined_data.groupby(["Drug Regimen"])["Tumor Volume (mm3)"].var()
std_tumor_volume = clean_combined_data.groupby(["Drug Regimen"])["Tumor Volume (mm3)"].std()
sem_tumor_volume = clean_combined_data.groupby(["Drug Regimen"])["Tumor Volume (mm3)"].sem()

tumor_volume_summary = pd.DataFrame({"Mean Tumor Volume" : mean_tumor_volume,
                                     "Median Tumor Volume" : median_tumor_volume,
                                     "Tumor Volume Variance" : var_tumor_volume,
                                     "Tumor Voume Sdt. Dev." : std_tumor_volume,
                                     "Tumor Volume Std. Err." : sem_tumor_volume
                                    })

tumor_volume_summary



# In[8]:


# A more advanced method to generate a summary statistics table of mean, median, variance, standard deviation,
# and SEM of the tumor volume for each regimen (only one method is required in the solution)

# Using the aggregation method, produce the same summary statistics in a single line
tumor_volume_summary2 = clean_combined_data.groupby("Drug Regimen").agg({"Tumor Volume (mm3)":["mean", "median", "var", "std", "sem"]})
tumor_volume_summary2


# ## Bar and Pie Charts

# In[9]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using Pandas.
drug_type_counts = clean_combined_data["Drug Regimen"].value_counts()
drug_type_counts.plot(kind="bar")
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.show()


# In[10]:


# Generate a bar plot showing the total number of rows (Mouse ID/Timepoints) for each drug regimen using pyplot.
drug_type_counts = clean_combined_data["Drug Regimen"].value_counts()
plt.bar(drug_type_counts.index.values, drug_type_counts.values)
plt.xlabel("Drug Regimen")
plt.ylabel("# of Observed Mouse Timepoints")
plt.xticks(rotation = 90)
plt.show()


# In[11]:


# Generate a pie plot showing the distribution of female versus male mice using Pandas
sex_count = clean_combined_data["Sex"].value_counts()
sex_count.plot(kind="pie", autopct="%1.1f%%")


# In[12]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
sex_counts = clean_combined_data["Sex"].value_counts()
plt.pie(sex_counts, labels = sex_counts.index.values, autopct="%1.1f%%")
plt.ylabel("Sex")
plt.show()



# ## Quartiles, Outliers and Boxplots

# In[13]:


# Calculate the final tumor volume of each mouse across four of the treatment regimens:  
# Capomulin, Ramicane, Infubinol, and Ceftamin

# Start by getting the last (greatest) timepoint for each mouse
max_tumor = clean_combined_data.groupby(["Mouse ID"])["Timepoint"].max()
max_tumor = max_tumor.reset_index()

# Merge this group df with the original DataFrame to get the tumor volume at the last timepoint
merged_data = max_tumor.merge(clean_combined_data, on=["Mouse ID", "Timepoint"], how="left")


# In[14]:


# Put treatments into a list for for loop (and later for plot labels)
treatment_list = ["Capomulin", "Ramicane", "Infubinol", "Ceftamin"]

# Create empty list to fill with tumor vol data (for plotting)
tumor_volume_list = []

# Calculate the IQR and quantitatively determine if there are any potential outliers. 
for drug in treatment_list:
    
    # Locate the rows which contain mice on each drug and get the tumor volumes
    final_tumor_volume = merged_data.loc[merged_data["Drug Regimen"] == drug, "Tumor Volume (mm3)"]

    
    # add subset 
    tumor_volume_list.append(final_tumor_volume)

    
    # Determine outliers using upper and lower bounds
    quartiles = final_tumor_volume.quantile([0.25, 0.5, 0.75])
    lowerq = quartiles[0.25]
    upperq = quartiles[0.75]
    iqr = upperq - lowerq
    lower_bound = lowerq - (1.5 * iqr)
    upper_bound = upperq + (1.5 * iqr)
    
    outliers = final_tumor_volume.loc[(final_tumor_volume < lower_bound) | (final_tumor_volume > upper_bound)]
    
    print(f"{drug}'s potential outliers {outliers}")


# In[15]:


# Generate a box plot that shows the distrubution of the tumor volume for each treatment group.
orange_out = dict(markerfacecolor="red", markersize=10)
plt.boxplot(tumor_volume_list, labels = treatment_list, flierprops = orange_out)
plt.ylabel("Final Tumor Volume (mm3)")
plt.show()


# ## Line and Scatter Plots

# In[16]:


# Generate a line plot of tumor volume vs. time point for a single mouse treated with Capomulin
capomulin_table = clean_combined_data[clean_combined_data["Drug Regimen"] == "Capomulin"]
mousedata = capomulin_table[capomulin_table["Mouse ID"] == "l509"]

plt.plot(mousedata["Timepoint"], mousedata["Tumor Volume (mm3)"])
plt.title("Capomulin treatment of mouse 1509")
plt.xlabel("Timepoint (days)")
plt.ylabel("Tume Volume (mm3)")

plt.show()


# In[17]:


# Generate a scatter plot of mouse weight vs. the average observed tumor volume for the entire Capomulin regimen

capomulin_table2 = clean_combined_data[clean_combined_data["Drug Regimen"] == "Capomulin"]
capomulin_average = capomulin_table2.groupby(["Mouse ID"])
capomulin_average = capomulin_average.mean(numeric_only=True)

plt.scatter(capomulin_average["Weight (g)"], capomulin_average["Tumor Volume (mm3)"])
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")

plt.show()


# ## Correlation and Regression

# In[18]:


# Calculate the correlation coefficient and a linear regression model 
# for mouse weight and average observed tumor volume for the entire Capomulin regimen

corr = st.pearsonr(capomulin_average["Weight (g)"], capomulin_average["Tumor Volume (mm3)"])
print(f"The correlation between mouse weight and the average tumor volume is {round(corr[0],2)}")

model = st.linregress(capomulin_average["Weight (g)"], capomulin_average["Tumor Volume (mm3)"])
slope = model[0]
b = model [1]
y_values = capomulin_average["Weight (g)"] * slope + b

plt.scatter(capomulin_average["Weight (g)"], capomulin_average["Tumor Volume (mm3)"])
plt.plot(capomulin_average["Weight (g)"], y_values, color="red")
plt.xlabel("Weight (g)")
plt.ylabel("Average Tumor Volume (mm3)")
plt.show()


# In[ ]:




