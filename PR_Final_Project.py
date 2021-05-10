#!/usr/bin/env python
# coding: utf-8

# ### Project Description
# Terrorism is a disease which has been stuck with us since forever. Our project aims to analyse terrorist activities which have been carried out throughout the world since 1970 till 2017. We plan to do this by analysing the below mentioned datasets which will give us a deep insight into what, how and where the terrorist activities were carried out through these years.
# 
# Hypothesis:
# 
# 1) We expect to see a decrease in terrorist activities in first world countries(USA, UK, France) as compared to third world countries(Pakistan, Bangladesh, India) due to advancement in technology since 1970s.
# 
# 2) Attackers who assassinated government officials were holding non-immigrant visas.
# 
# 3) Unmarried people of ages between 20-35 are more likely to commit terrorist activities as compared to people not categorized in the above criteria.
# 
# We can further analyse this dataset further to see what kind of weapons were used to carry out acts of terrorism in different countries and whether the perpetrators were charged or not.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from io import StringIO
from mpl_toolkits.axes_grid1 import Divider, Size
import doctest

warnings.filterwarnings('ignore')


# In[97]:


def load_terrorism_file(filename: str) -> pd.DataFrame: #has country,target type
    """
        Load a file efficiently, retaining only the most useful columns & rows.
        Uses Pandas read_csv() with its compression='infer' option.
        
        param filename : terrorism file
        return : dataframe of terrorism file
    """
    
    csv_columns = ['eventid','iyear','imonth','iday','approxdate','extended','resolution','country','country_txt','region','region_txt','provstate','city','latitude','longitude','specificity','vicinity','location','summary','crit1','crit2','crit3','doubtterr','alternative','alternative_txt','multiple','success','suicide','attacktype1','attacktype1_txt','attacktype2','attacktype2_txt','attacktype3','attacktype3_txt','targtype1','targtype1_txt','targsubtype1','targsubtype1_txt','corp1','target1','natlty1','natlty1_txt','targtype2','targtype2_txt','targsubtype2','targsubtype2_txt','corp2','target2','natlty2','natlty2_txt','targtype3','targtype3_txt','targsubtype3','targsubtype3_txt','corp3','target3','natlty3','natlty3_txt','gname','gsubname','gname2','gsubname2','gname3','gsubname3','motive','guncertain1','guncertain2','guncertain3','individual','nperps','nperpcap','claimed','claimmode','claimmode_txt','claim2','claimmode2','claimmode2_txt','claim3','claimmode3','claimmode3_txt','compclaim','weaptype1','weaptype1_txt','weapsubtype1','weapsubtype1_txt','weaptype2','weaptype2_txt','weapsubtype2','weapsubtype2_txt','weaptype3','weaptype3_txt','weapsubtype3','weapsubtype3_txt','weaptype4','weaptype4_txt','weapsubtype4','weapsubtype4_txt','weapdetail','nkill','nkillus','nkillter','nwound','nwoundus','nwoundte','property','propextent','propextent_txt','propvalue','propcomment','ishostkid','nhostkid','nhostkidus','nhours','ndays','divert','kidhijcountry','ransom','ransomamt','ransomamtus','ransompaid','ransompaidus','ransomnote','hostkidoutcome','hostkidoutcome_txt','nreleased','addnotes','scite1','scite2','scite3','dbsource','INT_LOG','INT_IDEO','INT_MISC','INT_ANY','related']
    
    columns_wanted = ['iyear','country_txt','attacktype1_txt','targtype1_txt']
    
    df = pd.read_csv('terrorism.csv',
                    compression='infer',
                    names=csv_columns,
                    usecols=columns_wanted,
                    )
    
    df['iyear'] = pd.to_numeric(df['iyear'], errors='coerce')
    
    return df


# In[53]:


terrorism_data


# In[39]:


def load_perp_file(filename: str) -> pd.DataFrame: 
    """
        Load a file efficiently, retaining only the most useful columns & rows.
        Uses Pandas read_csv() with its compression='infer' option.
        
        param filename : perps.csv
        return : dataframe of perps file
    """

    csv_columns = ['person_id','first_name','last_name','full_name','headshot','headshot_credit','gender','age','inv_informant','inv_public_tip','inv_community_or_family_tip','marital_status','terror_plot','terror_plot_2','plot_id','citizenship_status','charged_or_deceased','year_charged_or_deceased','date_charged','state_charged','state_charged_2','last_residency_state','last_residency_country','char_awlaki','char_contact_with_foreign_militant','char_overseas_military_training','char_us_military_experience','char_online_radicalization','targeted_jews_israel','targeted_military_installation']
    
    columns_wanted = ['first_name','last_name','full_name','age','citizenship_status','marital_status']
    
    df = pd.read_csv('perps.csv',
                    compression='infer',
                    names=csv_columns,
                    usecols=columns_wanted,
                    )   
    
    df['age'] = pd.to_numeric(df['age'],errors='coerce')

    return df


# In[54]:


perpetrators_data


# In[41]:


def load_income_file(filename: str) -> pd.DataFrame:
    """
        Cleaning and loading income file to get country, region and income
        
        param filename : CLASS.xls
        return : dataframe of income file    
    """
    
    xls = pd.ExcelFile(r"CLASS.xls")                   #https://stackoverflow.com/questions/2942889/reading-parsing-excel-xls-files-with-python
    sheetX = xls.parse(0, skiprows=5)
    sheetX = sheetX.rename(columns = {'x.2' : 'country_txt','x.5':'Region','x.6':'Income'})
    sheetX = sheetX[['country_txt','Region','Income']].head(218)
    
    return sheetX


# In[55]:


income_data


# In[43]:


def load_population_data(filename: str) -> pd.DataFrame:
    """
        Loading population data as per required column names for merging the files
        
        param filename : country_population.csv
        return : dataframe of country_population file
    """
    
    population_data = pd.read_csv('country_population.csv',names=['country_txt', 'Country Code', 'Indicator Name', 'Indicator Code',
   '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
   '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
   '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
   '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
   '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
   '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
   '2014', '2015', '2016'])  
    
    return population_data


# In[56]:


population_data


# ### Hypothesis 1

# In[45]:


def mergeCountryIncome(terrorism_data,income_data):
    """
        This function is used to merge terrorism_data with income_data to include the income column for testing our first hypothesis.
        param terrorism_data : dataframe of terrorism_data
        
        param income_data : dataframe of income_data
        return: dataFrame with country_txt and income columns from specified dataFrames in the function
    >>> data = {'iyear':['1971.0', '1972.0'],'country_txt':['Dominican Republic', 'United States'],'attacktype1_txt':['Assassination','Hostage Taking (Kidnapping)'],'targtype1_txt':['Private Citizens & Property','Business']}
    >>> data2 = {'country_txt':['Dominican Republic', 'United States'],'Region':['Central America & Caribbean','North America'],'Income':['Upper middle income', 'High income']}
    >>> df_test = pd.DataFrame(data)
    >>> df_test2 = pd.DataFrame(data2)
    >>> mergeCountryIncome(df_test,df_test2).head(1)[['country_txt','Income']]
         country_txt       Income
    0  United States  High income
    """
    
    terrorism_data = terrorism_data.iloc[1:]      # https://stackoverflow.com/questions/16396903/delete-the-first-three-rows-of-a-dataframe-in-pandas

    result = terrorism_data.merge(income_data, on='country_txt', how='left')
    
    return result
doctest.testmod()


# In[57]:


countryIncome


# In[6]:


def thirdWorldCountry(countryIncome):
    """
        This function takes the country names and returns two dataframes based on income groups

        param countryIncome: DataFrame of countries with their income groups
        return lowIncome: contains country names, regions and incomes of low income countries
        return lowIncomeCountries: contains year and count of low income countries
    >>> data = {'iyear':['1970.0','1971.0'],'Income':['Lower middle income','Low income'],'country_txt':['Dominican Republic','United States']}
    >>> test = pd.DataFrame(data)
    >>> thirdWorldCountry(test)
    (    iyear               Income         country_txt
    0  1970.0  Lower middle income  Dominican Republic
    1  1971.0           Low income       United States,         country_countL
    iyear                 
    1970.0               1
    1971.0               1)
    """

    options=['Lower middle income','Low income']

    lowIncome = countryIncome[countryIncome['Income'].isin(options)]

    lowIncomeCountries=lowIncome.groupby(['iyear']).agg(country_countL = ('country_txt','count'))
    
    return lowIncome,lowIncomeCountries
doctest.testmod()


# In[58]:


thirdWorldIncome


# In[59]:


thirdWorldCountries


# In[9]:


def firstWorldCountry(countryIncome):
    """
        This function takes the country names and returns two dataframes based on income groups

        param countryIncome: DataFrame of countries with their income groups
        return highIncome: contains country names, regions and incomes of high income countries
        return highIncomeCountries: contains year and count of high income countries
    >>> data = {'iyear':['1970.0','1971.0'],'Income':['Upper middle income','High income'],'country_txt':['Dominican Republic','United States']}
    >>> test = pd.DataFrame(data)
    >>> firstWorldCountry(test)
    (    iyear               Income         country_txt
    0  1970.0  Upper middle income  Dominican Republic
    1  1971.0          High income       United States,         country_countH
    iyear                 
    1971.0               1)
    """
    
    options=['High income','Upper middle income']

    highIncome = countryIncome[countryIncome['Income'].isin(options)]

    highIncomeCountries=highIncome.groupby(['iyear']).agg(country_countH = ('country_txt','count'))
    
    highIncomeCountries = highIncomeCountries.iloc[1:]

    
    return highIncome,highIncomeCountries
doctest.testmod()


# In[60]:


firstWorldIncome


# In[61]:


firstWorldCountries


# In[12]:


def lowIncomePopulation(thirdWorldCountries,population_data):
    
    """
        This function calculates population of low income countries year wise
        
        param thirdWorldCountries: contains country names, regions and incomes of third world income countries
        param population_data: dataframe of country_population file
        return h_stack: dataframe of population of required countries by each year
    """
    
    lowIncomePop = thirdWorldCountries.merge(population_data, on='country_txt', how='left')
    
    lowIncomePopln = lowIncomePop.drop_duplicates('country_txt')
    
    reqCol = lowIncomePopln[['country_txt','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']]
    
    reqCol.T                   #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html
    
    #https://www.geeksforgeeks.org/loop-or-iterate-over-all-or-certain-columns-of-a-dataframe-in-python-pandas/
    c=[]
    d=[]
    for (columnName, columnData) in reqCol.iteritems():            
        c.append(columnName)
        d.append(columnData.values.sum())

    dfreq = pd.DataFrame(c,columns = ['iyear'])
    dfreq1 = pd.DataFrame(d,columns = ['Population_low'])
    
    horizontal_stack = pd.concat([dfreq, dfreq1], axis=1)
    horizontal_stack = horizontal_stack.iloc[1:]  
    
    h_stack = horizontal_stack.dropna()
    
    return h_stack


# In[62]:


twcountriesPercentPop


# In[14]:


def highIncomePopulation(firstWorldCountries,population_data):
    
    """
        This function calculates population of high income countries year wise
        
        param firstWorldCountries: contains country names, regions and incomes of first world income countries
        param population_data: dataframe of country_population file
        return h_stack: dataframe of population of required countries by each year
    """
    
    highIncomePop = firstWorldCountries.merge(population_data, on='country_txt', how='left')

    highIncomePopln = highIncomePop.drop_duplicates('country_txt')
    
    
    reqCol = highIncomePopln[['country_txt','1970','1971','1972','1973','1974','1975','1976','1977','1978','1979','1980','1981','1982','1983','1984','1985','1986','1987','1988','1989','1990','1991','1992','1993','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']]
    
    reqCol.T          #https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.transpose.html
    
    #https://www.geeksforgeeks.org/loop-or-iterate-over-all-or-certain-columns-of-a-dataframe-in-python-pandas/
    a=[]
    b=[]
    for (columnName, columnData) in reqCol.iteritems():
        a.append(columnName)
        b.append(columnData.values.sum())

    dfreqL = pd.DataFrame(a,columns = ['iyear'])
    dfreqL1 = pd.DataFrame(b,columns = ['Population_high'])
    
    horizontal_stack = pd.concat([dfreqL, dfreqL1], axis=1)
    horizontal_stack = horizontal_stack.iloc[1:] 
    

    h_stack = horizontal_stack.dropna()
    return h_stack


# In[63]:


fwcountriesPercentPop


# In[16]:


def percentFirstWorldCountries(sumPopulationBYearHigh,firstWorldCountries):
    
    """
        This function calculates the division of terrorist activites and total population of countries according to years
        
        param sumPopulationBYearHigh: dataframe of population of required first world countries by each year
        param firstWorldCountries: dataframe of first world country_population file
        return percentfwc: dataframe containing division of terrorist activities by population by year
    """

    sumPopulationBYearHigh['iyear'] = pd.to_numeric(sumPopulationBYearHigh['iyear'], errors='coerce')   #https://stackoverflow.com/questions/15891038/change-column-type-in-pandas

    percentfwc = pd.merge(firstWorldCountries,sumPopulationBYearHigh, on='iyear')

    percentfwc['division_high'] = (percentfwc['country_countH']/percentfwc['Population_high'])*100
        
    return percentfwc


# In[64]:


percentFWCountries


# In[18]:


def percentThirdWorldCountries(sumPopulationBYearlow,thirdWorldCountries):
    
    """
        This function calculates the division of terrorist activites and total population of countries according to years
        
        param sumPopulationBYearlow: dataframe of population of required third world countries by each year
        param thirdWorldCountries: dataframe of third world country_population file
        return percenttwc: dataframe containing division of terrorist activities by population by year
    """
   
    sumPopulationBYearlow['iyear'] = pd.to_numeric(sumPopulationBYearlow['iyear'], errors='coerce')  #https://stackoverflow.com/questions/15891038/change-column-type-in-pandas   
    
    percenttwc = pd.merge(thirdWorldCountries,sumPopulationBYearlow,  on='iyear')
    
    percenttwc['division_low'] = (percenttwc['country_countL']/percenttwc['Population_low'])*100
        
    return percenttwc


# In[65]:


percentTWCountries


# In[99]:


def chartPrepData(percentFWCountries,percentTWCountries):
    """
        Merging files based on year to plot chart
        
        param percentFWCountries: dataframe containing division of terrorist activities by population by year for first world countries
        param percentTWCountries: dataframe containing division of terrorist activities by population by year for third world countries
        return result: Dataframe year wise with division of terrorist activities and population
    >>> data = {'iyear':['1970.0','1971.0'],'division_low':['1.34918e-06','9.18405e-05']}
    >>> data2 = {'iyear':['1970.0','1971.0'],'division_high':['3.02327e-05','9.73395e-05']}
    >>> test = pd.DataFrame(data)
    >>> test2 = pd.DataFrame(data2)
    >>> chartPrepData(test,test2)
        iyear division_low division_high
    0  1970.0  1.34918e-06   3.02327e-05
    1  1971.0  9.18405e-05   9.73395e-05
    """
    
    result = percentFWCountries.merge(percentTWCountries, on='iyear', how='inner')
    
    return result

doctest.testmod()


# In[66]:


percentBothType


# In[67]:


#plots the terrorism count of first and third world countries  

#https://stackabuse.com/change-figure-size-in-matplotlib/

x = percentBothType['iyear']
y = percentBothType['division_low']
z = percentBothType['division_high']
plt.figure(figsize=(20, 10))
plt.plot(x, y)
plt.plot(x, z)
plt.xlabel("Years",fontsize=20)
plt.ylabel("Percent Population Involved in Terrorist Activities",fontsize=15)
plt.plot(x, y, "-b", label="Third World COuntries")
plt.plot(x, z, "-r", label="First World COuntries")
plt.legend(loc="upper center")

plt.grid()
plt.show()


# ### Hypothesis 2

# In[23]:


def citizenship(terrorism_data,terrorists_data):
    """
    This function is used to merge terrorism_data with terrorists_data to include the citizenship_status column for testing our second hypothesis.

    param terrorism_data:dataframe of terrorism file
    param terrorists_data: dataframe of terrorists file
    return: dataFrame with citizenship_status and targtype1_txt columns from specified dataFrames in the function.
        
    >>> data = {'iyear':['1970.0', '1980.0'],'country_txt':['Dominican Republic', 'test'],'attacktype1_txt':['Assassination','Assassination2'],'targtype1_txt':['Government (Diplomatic)','Government (Diplomatic)2']}

    >>> data2 = {'column_a':['167', '168'],'citizenship_status':['abc', 'pqr'],'full_name':['pqr','asd'],'country_txt':['Dominican Republic', 'test']}
    >>> df_test = pd.DataFrame(data)
    >>> df_test2 = pd.DataFrame(data2)
    >>> citizenship(df_test,df_test2).head(1)[['iyear','country_txt','citizenship_status']]
        iyear         country_txt citizenship_status
    0  1970.0  Dominican Republic                abc
   """

    citizenshipStatus = pd.merge(terrorism_data,terrorists_data,how='inner', on='country_txt')
    
    return citizenshipStatus

doctest.testmod()


# In[68]:


citizenshipStatus


# In[70]:


### To check who Nonimmigrant visa holders targeted the most.

options=['Nonimmigrant Visa']

res_4 = citizenshipStatus[citizenshipStatus['citizenship_status'].isin(options)]

target_type=res_4.groupby(['targtype1_txt']).agg(cit_count = ('citizenship_status','count'))


x = target_type.index.tolist()
y = target_type['cit_count']

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(x,y)
plt.xticks(rotation=90)
plt.show()


# In[28]:


def displayPlots(citizeshipStatus):
    countries=['United Kingdom','France','Pakistan','Bangladesh','Qatar']

    for i in countries:


        options1=[i]
        options=['Nonimmigrant Visa']

        citizenstatus=citizenshipStatus[citizenshipStatus['country_txt'].isin(options1)]

        res_4 = citizenstatus[citizenstatus['citizenship_status'].isin(options)]

        target_type=res_4.groupby(['targtype1_txt']).agg(cit_count = ('citizenship_status','count'))


        x = target_type.index.tolist()
        y = target_type['cit_count']

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(x,y)
        plt.xticks(rotation=90)
        ax.set_title(i)
        plt.show()


# In[71]:


displayPlots(citizenshipStatus)


# ### Hypothesis 3

# In[30]:


def age(citizenshipStatus,perpetrators_data):
    
    """
        This function is used to merge citizenshipStatus with perpetrators_data to include the age column for testing our third hypothesis.
        
        param citizenshipStatus: dataframe of terrorists file
        param perpetrators_data: dataframe of perps file
        return age_df: dataFrame with age and marital_status columns from specified dataFrames in the function
    >>> data = {'iyear':['1970.0', '1972.0'],'country_txt':['Dominican Republic', 'United States'],'targtype1_txt':['Government (Diplomatic)','Government (Diplomatic)2'],'citizenship_status':['Nonimmigrant Visa','Permanent Resident']}
    >>> data2 = {'age':['33.0', '39.0'],'citizenship_status':['Nonimmigrant Visa','Permanent Resident']}
    >>> df_test = pd.DataFrame(data)
    >>> df_test2 = pd.DataFrame(data2)
    >>> age(df_test,df_test2).head(1)[['age','citizenship_status']]
        age citizenship_status
    0  33.0  Nonimmigrant Visa
    """
    age_df = pd.merge(citizenshipStatus, perpetrators_data, how='inner', on='citizenship_status')
    
    return age_df


# In[72]:


ageBins


# In[73]:



ageBins['bin'] = pd.cut(ageBins['age'], bins = [0,10,20,30,40,50,60,70,80],labels = [10,20,30,40,50,60,70,80])

ageBins.head()

options=['Unmarried']

res_1 = ageBins[ageBins['marital_status'].isin(options)]

res_2 = res_1.groupby(['bin']).agg(count = ('marital_status','count'))

x = res_2.index.tolist()
y = res_2['count']

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(x,y)
ax.set_title('World')
plt.show()


# In[33]:


def displayAgePlots(ageBinsFilter):
    """
        This function is used to return a pandas series that denotes the age bins of terrorists.
        Age data retrieved from: 
        Age Groups and their respective count:
            
        bin:count
        0-9:0
        10-19:7799
        20-29:19415
        30-39:3263
        40-49:0
        50-59:392
        60-69:572
        70-80:0
        
        :param ageBins:Filters the dataframe based on countries mentioned.
        :param res_1:Filters the dataframe based on marital status (unmarried) as mentioned. 
        :param res_2:Counts the number of unmarried terrorists by age-group. 
        :param row: Denotes that the operation has to be performed across rows
        
        

        """
    
    countries=['United Kingdom','France','Pakistan','Bangladesh','Qatar']
    for i in countries:
        
        options=[i]

        ageBins = ageBinsFilter[ageBinsFilter['country_txt'].isin(options)]
        
        ageBins['bin'] = pd.cut(ageBins['age'], bins = [0,10,20,30,40,50,60,70,80],labels = [10,20,30,40,50,60,70,80])

        ageBins.head()

        options=['Unmarried']

        res_1 = ageBins[ageBins['marital_status'].isin(options)]

        res_2 = res_1.groupby(['bin']).agg(count = ('marital_status','count'))

        x = res_2.index.tolist()
        y = res_2['count']
        
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.bar(x,y)
        ax.set_title(i)
        plt.show()
        


# In[74]:


displayAgePlots(ageBins)


# In[78]:


def terrorRegion(terrorism_data,income_data):
    """
    This function merges the terrorism data frame with income data frame to get the region
    
    param terrorism_data: terrorism data for all countries over years
    param income_data: income data for all countries with regions
    return reg_df: merged data frame of both file
    return res_df: count of region accoridng to terrorist activities
    
    >>> data = {'iyear':['1970.0', '1972.0'],'country_txt':['Dominican Republic', 'United States']}
    >>> data2 = {'Region':['Asia', 'Africa'],'income':['Low','High'],'country_txt':['Dominican Republic', 'United States']}
    >>> df_test = pd.DataFrame(data)
    >>> df_test2 = pd.DataFrame(data2)
    >>> terrorRegion(df_test,df_test2)
    (    iyear         country_txt  Region income
    0  1970.0  Dominican Republic    Asia    Low
    1  1972.0       United States  Africa   High,         count_region
    Region              
    Africa             1
    Asia               1)
    """    
    reg_df = pd.merge(terrorism_data, income_data, how='left', on='country_txt')

    res_df = reg_df.groupby(['Region']).agg(count_region = ('iyear','count'))
    
    return reg_df,res_df


# In[75]:


x = terror.index.tolist()
y = terror['count_region']

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(x,y)
plt.xticks(rotation=90)
plt.show()


# In[81]:


attacks = ['Bombing/Explosion','Assassination','Armed Assault','Hijacking']
for j in attacks:
    options=[j]
    res_df1 = terror_act[terror_act['attacktype1_txt'].isin(options)]
    res_df = res_df1.groupby(['Region']).agg(count_region = ('iyear','count'))
    x = res_df.index.tolist()
    y = res_df['count_region']

    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(x,y)
    ax.set_title(j)
    plt.xticks(rotation=90)
    plt.show()


# In[79]:


#main function
if __name__ == '__main__' :
    
    
    # Loading Data
    
    terrorism_data = load_terrorism_file('terrorism.csv')              # Loading Terrorism data for all countries
    perpetrators_data = load_perp_file('perps.csv')                    # age, marital, cit status
    terrorists_data = pd.read_csv('terrorists.csv')                    # country and cit status
    income_data = load_income_file('CLASS.xls')                        # has income for first and third world countries
    population_data = load_population_data('country_population.csv')   # has population data for each country year wise
    
    
    # Hypothesis 1
    countryIncome = mergeCountryIncome(terrorism_data,income_data)
    
    firstWorldIncome,firstWorldCountries= firstWorldCountry(countryIncome)
    thirdWorldIncome,thirdWorldCountries= thirdWorldCountry(countryIncome)
    
    
    fwcountriesPercentPop = highIncomePopulation(firstWorldIncome,population_data)
    twcountriesPercentPop = lowIncomePopulation(thirdWorldIncome,population_data)
    
    percentFWCountries = percentFirstWorldCountries(fwcountriesPercentPop,firstWorldCountries)
    percentTWCountries = percentThirdWorldCountries(twcountriesPercentPop,thirdWorldCountries)
    
    percentBothType = chartPrepData(percentFWCountries,percentTWCountries)
   

    # Hypothesis 2
    terrorists_data = terrorists_data.rename(columns={'country': 'country_txt'})
    terrorists_data['country_txt'].replace({'United States of America':'United States'},inplace=True)
    citizenshipStatus = citizenship(terrorism_data,terrorists_data)
    
    
    # Hypothesis 3
    ageBins=age(citizenshipStatus,perpetrators_data)
    
    # Testing further analysis for regions where most terror activities occured.
    terror_act,terror = terrorRegion(terrorism_data,income_data)

