#!/usr/bin/env python
# coding: utf-8

# # LIVEBOOK PROJECT QUESTIONS

# In[ ]:


#Perform data quality assurance check on “events” (use Python here, you may need to do numeric encoding on “events”)

• Do events happen equally at different times of the day or are there patterns (give 
visualizations)?
• Analyze “a particular account_id” for insights on how the person uses the service at 
different times of the day (Visualizations)?
get_ipython().set_next_input('• Are there any gaps(missing data) in the record of any events');get_ipython().run_line_magic('pinfo', 'events')
get_ipython().set_next_input('• Are there any extreme outliers (class imbalances) in the number of events');get_ipython().run_line_magic('pinfo', 'events')
5. Ensure data quality assurance
• Fix bad data
• Correct any missing data/gaps
• Fix class imbalance in the “events”


# Quality check

# In[338]:


#reading in the dataset "livebook"
livebook = pd.read_csv(r"C:\Users\USER\Downloads\actions2load.csv\actions2load.csv")
livebook.head()


# In[339]:


livebook.shape


# In[308]:


#check the types of variables and other details
livebook.info()


# In[310]:


#check for missing values 
livebook.isnull().sum()


# In[311]:


#check for duplicates
livebook.duplicated().sum()


# In[313]:


#check the number of unique categories
livebook.nunique()


# In[314]:


# plot a graph with the cardinality of each variable:
livebook.nunique().plot.bar(figsize=(12,6))
plt.ylabel('Number of unique categories')
plt.xlabel('Variables')
plt.title('Cardinality')


# In[315]:


#check the categories of events on livebook
livebook['event_type'].unique()


# In[317]:


#check the frequency of each event and assign the value counts to a variable
freq_of_events = livebook['event_type'].value_counts()
freq_of_events


# In[319]:


#plot a graph to inspect the frequency of events on livebook 

fig = freq_of_events.sort_values(ascending=False).plot.bar()
fig.set_ylabel('Frequency')
fig.set_xlabel('Events')
fig.set_title('Frequency of events on livebook')


# In[324]:


#import onehotencoder to convert event_type to integers
from sklearn.preprocessing import OneHotEncoder
encoder = OneHotEncoder(categories='auto', drop='first', 
    sparse=False)


# In[325]:


livebook['event_type'] = encoder.fit_transform(livebook['event_type'].values.reshape(-1, 1))


# In[328]:


# drop the variable not needed
livebook.drop(['additional_data'], axis = 1, inplace=True)


# In[329]:


#check dataset for changes made
livebook.head()


# In[330]:


#check for mean and other details of numeric variables
livebook.describe()


# In[332]:


#check for distribution of data

livebook.hist(figsize=(8,4), bins=30, edgecolor="black")
plt.subplots_adjust(hspace=0.5, wspace=0.4)


# In[333]:


#check for correlation of the variables

plt.figure(figsize=(8,4))
corre = livebook.corr()
sns.heatmap(corre, annot= True, cmap="YlGnBu")


# # Question 1: Do events happen equally at different times of the day or are there patterns (give visualizations)?

# In[102]:


#Reading in the data 

livebook = pd.read_csv(r"C:\Users\USER\Downloads\actions2load.csv\actions2load.csv")
livebook.head()


# In[103]:


# converting event_time to datetime format in order to create a variable for hours

livebook['event_time']=pd.to_datetime(livebook['event_time'])


# In[107]:


# creating the variable hours

livebook['event_hours'] = livebook['event_time'].dt.hour


# In[108]:


# Checking the data for the new variable created

livebook.head()


# In[114]:


#value count of the event_hours variable

event_hour = livebook['event_hours'].value_counts()
event_hour


# In[134]:


#plotting a bar chart to visualize event hours

event_hour.plot.bar(figsize=(12,6))
plt.ylabel('Frequency')
plt.xlabel('Hour of the day')
plt.title('FREQUENCY OF EVENTS PER HOUR')


# In[106]:


#creating time periods function to get the time of day

def TimePeriod(hour):
    if 0 < hour < 6:
        period = "Dawn"
    elif 5 < hour < 12:
        period = "Morning"
    elif 11 < hour < 17:
        period = "Afternoon"
    elif 16 < hour < 20:
        period = "Evening"
    else:
        period = "Night"
    return period


# In[110]:


#applying the time periods function to event_hours variable

livebook['time of day'] = livebook['event_hours'].apply(TimePeriod)


# In[111]:


#checking the dataset for the new variable "time of day"

livebook.head()


# In[121]:


# Value count of time of day

time_of_day = livebook['time of day'].value_counts()


# In[122]:


#plot a graph to visualize events during different times of the day

time_of_day.plot.bar(figsize=(12,6))
plt.ylabel('Frequency')
plt.xlabel('time of day')
plt.title('EVENTS DURING DIFFERENT TIMES OF THE DAY')


# Q1 Answer: As we can see from the hours and time of day graphs, events do not happen equally at dfferent times of the day. 
# From the "event_hour" graph, the highest number of events happen around 2pm while the least number of events happen around 11pm.
# From the 'time of day graph', most events happen in the afternoon and in the morning while less events happen during the evening and at dawn. 

# # Question 2: Analyze “a particular account_id” for insights on how the person uses the service at different times of the day (Visualizations)?

# In[255]:


#read in the dataset
livebook = pd.read_csv(r"C:\Users\USER\Downloads\actions2load.csv\actions2load.csv")
livebook.head()


# In[139]:


#check the account_id variable

livebook['account_id']


# In[273]:


#check the spread of events based on account_ids
events_per_accounts = pd.crosstab(livebook['account_id'],livebook['event_type'])
events_per_accounts


# In[256]:


#check number of unique account IDs
livebook['account_id'].nunique()


# In[258]:


#do a value count of events carried out by each account_id
livebook['account_id'].value_counts()


# In[269]:


#drop the columns not needed 
livebook.drop(['product_id','additional_data'], axis=1, inplace=True)
livebook.head()


# In[275]:


#pick the account_id with the highest events for analysis and assign it to a variable
acct_analysed = livebook[livebook["account_id"] == '6bb61e3b7bce0931da574d19d1d82c88']
acct_analysed


# In[277]:


acct_analysed = acct_analysed.reset_index()


# In[284]:


acct_analysed['event_type'].nunique()


# In[299]:


acct_eventcount = acct_analysed['event_type'].value_counts()
acct_eventcount


# In[302]:


fig = acct_eventcount.sort_values(ascending=False).plot.bar()
fig.set_ylabel('count')
fig.set_xlabel('event_type')
fig.set_title('Event counts')


# In[296]:


eventtime_of_account = pd.crosstab(acct_analysed['event_time'],acct_analysed['event_type'])


# In[297]:


eventtime_of_account


# In[306]:


acct_analysed.hist(figsize=(8,4), edgecolor="black")
plt.subplots_adjust(hspace=0.5, wspace=0.4)


# # Question 3: Are there any gaps(missing data) in the record of any events?

# In[138]:


# checking the dataset

livebook.head()


# In[125]:


livebook.isnull().sum()


# In[133]:


Perc_of_missing_data = livebook.isnull().mean()
Perc_of_missing_data


# In[212]:


#plotting a bar chart to visualize missing data

Perc_of_missing_data.plot.bar(figsize=(8,4))
plt.ylabel('Percentage of missing data')
plt.xlabel('Variables')
plt.title('QUANTIFYING MISSING DATA')


# Answer: There are no missing gaps or data in the record of any events, which are in event_time and event_type. 
#         The only variable with missing data is additional_data.

# # Question 4: Are there any extreme outliers (class imbalances) in the number of events?

# In[151]:


#check the number of unique categories in event_type
livebook['event_type'].nunique()


# In[48]:


#check the unique values in event_type

livebook['event_type'].unique()


# In[51]:


#count the number of times each event was carried out

livebook['event_type'].value_counts()


# In[206]:


#plot a graph to visualize the events count


fig = livebook['event_type'].value_counts().plot.bar()
fig.set_title('Frequency of event types')

event_type_count.plot.bar(figsize=(12,6))
plt.ylabel('count')
plt.xlabel('events')
plt.title('EVENTS COUNT')


# In[280]:


#assign the events value count to a variable
event_type_count = livebook['event_type'].value_counts()


# In[281]:


#reset the index and assign to a variable
event_count = event_type_count.to_frame().reset_index()


# In[282]:


#assign columns to event_count

event_count.columns = ["event_type","count"]
x = event_count['event_type']
y = event_count['count']


# In[283]:


event_count


# In[236]:


#use boxplot to check for outliers
import seaborn as sns

sns.boxplot(y=event_count['count'])
plt.title('Boxplot')


# In[239]:


plt.boxplot(event_count['count'])


# # Question 5: Ensure data quality assurance
# • Fix bad data
# • Correct any missing data/gaps
# • Fix class imbalance in the “events”

# In[157]:


#reading in the dataset again to check for bad data and missing data
livebook = pd.read_csv(r"C:\Users\USER\Downloads\actions2load.csv\actions2load.csv")
livebook.head()


# In[158]:


#drop the variable not needed
livebook.drop(['additional_data'], axis=1, inplace=True)


# In[159]:


#check the dataset after dropping the variable not needed
livebook.head()


# In[ ]:


#drop duplicated rows in the dataset
livebok.drop_duplicates()


# In[220]:


# Fix class imbalance in the events

# define function to remove outliers
def drop_outlier(data,var):
    q1, q3 = np.percentile(data[var], [25, 75])
    iqr = q3 - q1
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr
    data = data[data[var]< upper]
    data = data[data[var]> lower]
    data.reset_index(drop=True, inplace = True)
    return data


# In[241]:


#drop outliers in events
event_count = drop_outlier(event_count, 'count') 


# In[250]:


#check the event count again

sns.boxplot(x = event_count['count'], y = event_count['event_type'])
plt.title('Boxplot')
plt.show

