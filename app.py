# Police Stops Dataset Streamlit 
import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt
from PIL import Image 

#Title
st.title(" Police Stops Interactive Insights ")

st.balloons()

#Project objective
st.header("Project Objective:")
st.write("In this project, I have conducted a data analysis on a Police Stops dataset.")
st.write("The main objective is to explore police stop data to gain insights into driver demographics, including age, gender, and race.")  
st.write("- It aims to identify areas of improvement,")
st.write("- To find potential biases in stops based on age, gender, or race,")
st.write("- To visualize and communicate police stop data in an accessible manner for the public.")

#Image
image=Image.open("Police Stops Image.png")
resized_image = image.resize((650,590))  
st.image(resized_image)

#Dataset overview
column_descriptions = [
    "📅 **stop_date**: Date of the stop",
    "⏰ **stop_time**: Time of the stop",
    "🚹 **driver_gender**: Gender of the driver",
    "🎂 **driver_age_raw**: Year of birth of the driver",
    "👤 **driver_age**: Age of the driver",
    "🌎 **driver_race**: Race of the driver",
    "📜 **violation_raw**: Raw violation description.",
    "⚖️ **violation**: Processed violation category.",
    "🔍 **search_conducted**: Indicates if a search was conducted.",
    "🕵️ **search_type**: Type of search conducted",
    "📄 **stop_outcome**: Outcome of the stop (e.g., citation, warning)",
    "🚔 **is_arrested**: Indicates if the driver was arrested.",
    "⏳ **stop_duration**: Duration of the stop (in minutes)",
    "💊 **drugs_related_stop**: Indicates if the stop related to drugs",
    "👶 **driver_age_cat**: Age category of the driver (e.g., Young Adults, Adults)",
    "📆 **year**: Year of the stop",
    "📆 **Month**: Month of the stop"
]

# Display each description using a loop
st.header("Dataset Overview:")
st.subheader("This dataset contains 65535 rows and 15 columns")
for description in column_descriptions:
    st.write(description)


#Upload dataset
df=pd.read_csv("Police Stops Data.csv")

#Show Basics of Dataset
st.subheader("The sample of the dataset is as follows: ")
st.write(df.head())

#QUCK  OVERVIEW METRICS
#st.subheader("Quick dataset Overview:")
#total_stops=len(df)
#avg_age=df['driver_age'].mean()
#minors_percent=(df[df['driver_age']<18].shape[0]/len(df))*100
#avg_stop_duration = df['stop_duration'].mean()
#most_common_outcome = df['stop_outcome'].mode()[0]  # Mode gives the most frequent value

#colm_1,colm_2,colm_3,colm_4=st.columns(4)
#with colm_1:
 #   st.metric("**Average Age**",f"{int(avg_age)}")
#with colm_2:
 #   st.metric("**Percent of minors**:",f"{minors_percent:.2f}%")
#with colm_3:
  #  st.metric("**Average stop duration**",f"{avg_stop_duration:.2f}")
#with colm_4:
 #   st.metric("**Top stop outcome**",str(most_common_outcome))


#SIDEBAR
#Shape button in sidebar
if st.sidebar.button("Shape of the data:"):
  st.sidebar.subheader(df.shape)

#sidebar checkbox null %
st.sidebar.header("Null values ")
total_cells=df.shape[0]*df.shape[1]
null_values=df.isnull().sum().sum()
null_value_percent= (null_values/total_cells)*100
st.sidebar.write(f"Total null values:**{null_values}**")
if st.sidebar.checkbox("Check total null value percent"):
   st.sidebar.write(f"Percentage of null values: **{null_value_percent:.2f}%**")


#SIDEBAR filter by YEAR of data
st.sidebar.header("Select Year of Data")
df['stop_date']=pd.to_datetime(df['stop_date'], format='%m/%d/%Y',errors='coerce')
df['year']=df['stop_date'].dt.year.fillna(0).astype(int) #to remove years in decimal 2007.0 to only year and no NAN valu as option
selected_year=st.sidebar.selectbox("Select Year", df['year'].unique())
filtered_data = df[df['year'] == selected_year]
st.sidebar.write(f"Data for year {selected_year}")
st.sidebar.write(filtered_data)


#Checkbox for data summary 
st.subheader("Data Summary")
missing_percent = (df.isna().sum()/len(df))
summary_df=pd.DataFrame({
    "Data Types": df.dtypes,
    "Unique Values": df.nunique(),
    "Missing values": df.isna().sum(),
    "Missing (%)":(missing_percent*100).round(2)
})
col1, col2 = st.columns([1,3])
with col1:
 data_summary_button= st.button("Dataset Summary")
with col2:
    if data_summary_button:
     st.write("Dataset Summary:")
     st.dataframe(summary_df)


#NULL values heatmap
st.subheader("Heatmap of Missing Values")
fig,ax=plt.subplots(figsize=(10, 6))
sns.heatmap(df.isnull())
st.pyplot(fig)


#Data Cleaning and Pre-processing
st.header("Data Cleaning and Pre-processing")
st.write("* Dropping unnecessary columns i.e 'country_name' ")
df.drop(columns='country_name',inplace=True)
st.write("* Convert columns 'stop_date' and 'stop_time' from object to datetime format")
df['stop_date']=pd.to_datetime(df['stop_date'], format='%m/%d/%Y',errors='coerce').dt.date
df['stop_time']=pd.to_datetime(df['stop_time'],format='%H:%M').dt.time 
st.write(df.head(3))


#Button for MEAN of stop_duration
df['stop_duration'] = df['stop_duration'].map({'0-15 Min': 7.5, '16-30 Min': 24, '30+ Min': 45})

col1, col2 = st.columns([1,3])
with col1:
    mean_duration_button= st.button("Calculate mean of Stop duration:",key='mean_duration_button') #a
with col2:
    if mean_duration_button:
        mean_stop_duration= df['stop_duration'].mean()  #b
        st.write(f"The Mean of Stop duration is: **{mean_stop_duration:.2f}** minutes") #c


st.write("---")
#Search conducted analysis
st.subheader(" Search conducted analysis:")
search_conducted_values=df['search_conducted'].value_counts()
st.write(" If search is conducted then True, else False")
st.table(search_conducted_values)

st.write("Analysing when Search conducted is True further with respect to to Gender. ")
search_by_gender=df.groupby('driver_gender').search_conducted.sum()
fig,ax=plt.subplots()
search_by_gender.plot(kind='bar',color=('#FF99CC','#19B2FF'),edgecolor='black')
plt.title('Search conducted by Gender')
plt.xlabel('Gender')
plt.ylabel('Count')
ax.bar_label(ax.containers[0])
plt.xticks(rotation=0)
st.pyplot(fig)

Females_searched=(366/2479) *100
Males_searched=(2113/2479) *100 
st.write(f"**Females searched**: {Females_searched:.2f}%")
st.write(f"**Males searched**: {Males_searched:.2f}%")


#Selectbox FILTER by Race and Gender
st.subheader("Filter data according to Race and Gender")

col1,col2=st.columns([2,2])
with col1:
    selected_gender=st.selectbox("Select gender",df['driver_gender'].dropna().unique())
with col2:
    selected_race=st.selectbox("Select race",df['driver_race'].dropna().unique())
    data_sel_race_gender=df[(df['driver_race']==selected_race)& (df['driver_gender']==selected_gender)]
st.write(data_sel_race_gender)



# driver_race distribution pie chart BUTTON
col1,col2= st.columns([1,3])

with col1: 
    driver_race_dist_button=st.button("Driver Race distribution")
with col2:
    if driver_race_dist_button:
        race=df['driver_race'].value_counts()
        colors=['#FF9999','#FFCC99','#FFFF99','#CCFF99','#99FF99' ]
        fig,ax=plt.subplots()
        ax.pie(race,labels=race.index,autopct='%1.1f%%',wedgeprops={'edgecolor':'black'}, colors=colors)
        ax.set_title('Driver Race distribution', loc='center')
        plt.legend(loc='upper right')
        st.pyplot(fig)


st.subheader("Driver Gender and race ")
dist_gen_race=df.groupby('driver_gender').driver_race.value_counts()
st.table(dist_gen_race)

#VIOLATION BY RACE horizontal bar
st.subheader("Violation by Race")
violation_by_race=df.groupby(['driver_race','violation']).size().unstack(fill_value=0)
violation_by_race.plot(kind='barh',stacked=True,edgecolor='black')
plt.title('Violation by Race')
plt.xlabel('Count')
plt.ylabel('Race')
plt.grid(axis='x', linestyle='--')
st.pyplot(plt)


#Is arrested or not and stop out
st.subheader("Arrested or Not and the Outcome")
st.table(df.is_arrested.value_counts())

col1, col2=st.columns(2)
with col1:
    arrested_button= st.button("Arrested")         
with col2:
    not_arrested_button=st.button("Not Arrested")   
    
def show_arrested_data():
    arrested_df= df[df['is_arrested']==True].stop_outcome.value_counts()
    st.write("Arrested Data")
    st.dataframe(arrested_df)
def show_not_arrested_data():
    not_arrested_df= df[df['is_arrested']==False].stop_outcome.value_counts()
    st.write("Not Arrested Data")
    st.dataframe(not_arrested_df)

if arrested_button:
    with col1:
        show_arrested_data()
if not_arrested_button:
    with col2:
        show_not_arrested_data()


st.write("---")
#Age distribution DESCRIBE
st.subheader("Compare the age distribution for each violation")
viol_age_dist=df.groupby('violation').driver_age.describe()
st.write(viol_age_dist)

if st.button("Understand the Stats"):
    explanation=(
    "**Count**: The highest count of violation is of 'Speeding' which is **37,120**. 'Seatbelt' violation has the smallest sample size of only 3.\n\n"
    "**Mean**:Highest mean age(40.36 years)is for 'Other' violation, while 'Equipment' violations have the lowest (31.68 years).\n\n"
    "**Standard Deviation**:(Shows how much the ages vary from the mean) Age variability is highest in 'Moving' violation.\n\n"
    "**Median(50%)**: The median age for 'Other' violations is the highest at 41 years and lowest for 'Seatbelt' violation 26.\n\n"
    "**Min**:The youngest age recorded in the dataset is 15 for 'moving violation' as well as 'Speeding'\n\n"
    "**Max**:The highest age was recorded for 'Speeding' at 88 years.\n\n")
    st.write(explanation)


st.subheader("Age distribution for Violation")
image = Image.open("Age violatn dist BOXPLOT.png")
st.image(image,use_container_width=True)
if st.button("Understand the Boxplot"):
    boxplot_detail= (
    "**Speeding**: Has a lot of older drivers showing up as outliers. Median age around 30.\n\n"
    "**Other violations**: Mostly older drivers, with the highest median age (about 41).\n\n"
    "**Equipment & Registration/Plates**: Mainly younger drivers, with typical ages around 28-30. Also has a lot of extreme outliers.\n\n"
    "**Moving Violation**: Ages vary widely, median around 35, with some older outliers.\n\n"
    "**Registration/plates**:Contains drivers with ages 25 to 40 ,with median age being 30. This too has a few outliers.\n\n"
    "**Seatbelt**: Very few cases, mostly younger drivers, median around 26.\n\n"
    "Older drivers are mostly in 'Other' and 'Moving violation', while younger drivers are more in 'Equipment' and 'Speeding' violations.\n\n")
    st.write(boxplot_detail)
    
    

st.subheader("5 Most common violations") 
col_a, col_b=st.columns([2,2])  
with col_a:
    st.write("Actual values in table format:")
    st.table(df.violation.value_counts().head(5))
with col_b:
    image=Image.open("top_5_violatns.png")
    st.image(image)
    

#FILTER by violation
st.subheader("Filter by violation")
viol_condition=st.selectbox("Select violation",df['violation'].dropna().unique())
viol_conditn_op=df[df['violation']==viol_condition]
st.write(viol_conditn_op)
    
    
#BUTTON to check analysis of Minors in the df
st.subheader("Check Analysis done for Minors stopped")

def show_minor_analysis():
    minor=df[df['driver_age']<18]
    
    total_minors=len(minor)
    st.write(f"Total minors in the dataset: **{total_minors}**")
    
    st.write(minor.head())
 
    st.write("**Violations by minors**")
    coll1,coll2=st.columns(2)
    minor_viol=minor.violation.value_counts()
    with coll1:
        st.table(minor_viol)
    with coll2:
        st.bar_chart(minor_viol)
    
    minors_stop_outcome=minor['stop_outcome'].value_counts()
    st.write("**Stop outcome of minors stopped**")
    st.table(minors_stop_outcome) #table
    
if st.button("Check Analysis of Minors stopped"):
   show_minor_analysis()



st.write("---")
#SEARCH CONDUCTED
st.subheader("Search conducted and stop outcome")
st.write("If Search conducted ***True***, if not ***False***")
search_conducted_stop_o=df.groupby('search_conducted').stop_outcome.value_counts()
st.table(search_conducted_stop_o)



#TOP 5 SEARCH TYPE radio button
st.subheader("Top Search Types")
selection=st.radio("Select Analysis",["Search Types Table","Search Types Chart"])
if selection== "Search Types Table":
    st.write("Most common Search Types")
    st.dataframe(df['search_type'].value_counts().head())

elif selection== "Search Types Chart":
    st.write("Most common Search Types")
    fig,ax=plt.subplots()
    top_5_search_types=df['search_type'].value_counts().head(5)
    plt.barh(top_5_search_types.index[::-1],top_5_search_types.values[::-1],color='#FF8000',edgecolor='black')
    plt.title('Top 5 search types')
    plt.xlabel('Count')
    plt.ylabel('Search types')
    st.pyplot(fig)


#Check drug related CHECKBOX
st.subheader("Drug related stop")
st.table(df.drugs_related_stop.value_counts())

if st.checkbox("Check % of stops which were drug related"):
    drug_related_percent= (518/len(df))*100
    st.write(f"Police stops which were drug related is **{drug_related_percent:.2f}%**")



st.write("---")
#Age categories tabs
age_bins=[15,19,31,60,89]
age_labels=["Minor","Young Adults","Adults","Seniors"]
df['driver_age_cat']=pd.cut(df['driver_age'],bins=age_bins,labels=age_labels,right=False)

st.subheader("Age categories")
tab1, tab2,tab3,tab4=st.tabs(["Minor","Young Adults","Adults","Seniors"])

with tab1:
    st.write("**Data for Minors**: *Ages 15 to 18*")
    minor_df=df[df['driver_age_cat']=='Minor']
    st.dataframe(minor_df)
    
with tab2:
    st.write("**Data for Young Adults**: *Ages 19 to 30*")
    young_adults_data = df[df['driver_age_cat'] == 'Young Adults']
    st.dataframe(young_adults_data)
    
with tab3:
    st.write("**Data for Adults**: *Ages 31 to 59*")
    adults_data = df[df['driver_age_cat'] == 'Adults']
    st.dataframe(adults_data)

with tab4:
    st.write("**Data for Seniors**: *Ages 60 to 89*")
    seniors_data = df[df['driver_age_cat'] == 'Seniors']
    st.dataframe(seniors_data)


#Driver age categories BAR CHART and HISTOGRAM
coll1,coll2=st.columns(2)
with coll1:
    st.write("Driver Age categories")

    age_cat_counts = df['driver_age_cat'].value_counts().sort_index()

    fig,ax=plt.subplots()
    plt.bar(age_cat_counts.index,age_cat_counts.values, edgecolor='#7300E6',color='#00FFAA')
    plt.title('Driver age categories')
    plt.xlabel('Age Categories')
    plt.ylabel('Ages')
    plt.tight_layout()
    st.pyplot(fig)     
with coll2:
    st.write("Driver Age Histogram")
    fig,ax=plt.subplots()
    plt.hist(df['driver_age'],bins=30,color='skyblue', edgecolor='black')
    plt.title('Driver age distribution Histogram')
    plt.xlabel('Driver Age')
    plt.ylabel('Number of Drivers')
    plt.grid(axis='y', linestyle='--', alpha=0.8)
    st.pyplot(fig)



#stop outcome by VIOLATION table and barchart 
st.write("---")
st.subheader("Stop Outcomes for different Violations")

tab_1, tab_2=st.tabs(["Table","Bar Chart"])
with tab_1:
    stop_out_viol=df.groupby('violation').stop_outcome.value_counts()
    st.dataframe(stop_out_viol)
with tab_2:
    stop_outcome_by_violation=df.groupby(['violation','stop_outcome']).size().unstack(fill_value=0) #2nd col will be unstacked made into column
    fig,ax =plt.subplots()
    stop_outcome_by_violation.plot(kind='bar',stacked=True, ax=ax)
    plt.title('Stop outcomes for different Violations')
    plt.xlabel('Violation')
    plt.ylabel('Stop Outcome')
    plt.grid(axis='y', linestyle='--', alpha=0.8)
    st.pyplot(fig)
    
#HEATMAP for Violations vs stop_outcomes    
st.write("**Heatmap showing Stop Outcomes for different Violations**")   
pivot_df = df.groupby(['violation', 'stop_outcome']).size().unstack(fill_value=0)

fig,ax=plt.subplots()
sns.heatmap(pivot_df, annot=True, fmt='d', cmap='YlGnBu', cbar=True)
plt.title('Heatmap of Stop Outcomes by Violation Type')
plt.xlabel('Stop Outcome')
plt.ylabel('Violation Type')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)
    

# YEARS, MONTHS(LINE BAR) in tabs
st.subheader("Police stops over time")

tabb1,tabb2= st.tabs(["Stops over the Years","Stops over the Months"])
with tabb1: 
    df['stop_date']=pd.to_datetime(df['stop_date'])
    df['year']=df['stop_date'].dt.year
       
    yearly_stops= df['year'].value_counts().sort_index()
    fig, ax=plt.subplots()
    plt.plot(yearly_stops.index,yearly_stops.values, marker='o',color='blue')
    plt.title('Number of Police Stops Over the Years')
    plt.xlabel('Years')
    plt.ylabel('Number of Stops')
    plt.tight_layout()
    plt.grid(True)
    st.pyplot(fig)
    
with tabb2:
    image=Image.open("stops_in_months.png")
    st.image(image,use_container_width=True)

#Count of stops in each year
choose_year = st.radio("Select Year", ['2005','2006', '2007', '2008', '2009', '2010', '2011', '2012'])  
count_stops = len(df[df['year'] == int(choose_year)])  # Convert the selected year to an integer to match the df format
st.write(f"Number of Police stops in {choose_year}: **{count_stops}**")


#Feedback 
st.write("---")
st.subheader("Feedback on the Website")
st.markdown(" For feedback and suggestions, feel free to reach out at")
st.markdown("📧aditishetti9060@gmail.com")


