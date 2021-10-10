import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pycountry
from scipy import stats

df = pd.read_excel("master.xlsx")
df["age"] = df['age'].replace({'5-14 years': '05-14 years'})
print(df.head())
print(df.shape)
print(df.info())
print(df.any().isna())
df_for_year = df.groupby("year").agg('sum','suicides_no')
df_for_year['suicides_per_100k'] = df_for_year['suicides_no']/df_for_year["population"] * 100000
print(df_for_year.head())
sns.lineplot(x = "year",y="suicides_per_100k",data=df_for_year)
plt.show()
# As we can se on this plot 'suicide rate for 100k' worldwide, was quite high.
# After 1987 we can see 30% increase in 'suicide rate for 100k'. We can say that increase was caused by change of the political system around the world.
# Another factor of that increase might be economic crisis. There are many factors which might or might not caused this increase. 
# After 1995 we can see that 'suicide rate for 100k' slowly decreased itself
# It's hard to predict future 'suicide rate for 100k', due to many factors which may occure in the future.

df_for_year_sex = df.groupby(["sex","year"])['suicides_no','population'].sum()
df_for_year_sex["suicides_per_100k"] = df_for_year_sex["suicides_no"]/df_for_year_sex['population'] * 100000
df_for_year_sex = df_for_year_sex.sort_values("year")
sns.lineplot(x="year",y="suicides_per_100k",hue="sex",data=df_for_year_sex,style="sex",markers=["o","o"])
plt.grid()
plt.show()
# As we can see on that plot, it doesn't matter which year it is, 'suicide rate for 100k' for men is more than 2.5 times higher than for women.
# It might be caused by enviromental preassure which states that men must be very successful or they have to be the head of the family. 

df_for_age = df.groupby(["year","age"])['suicides_no','population'].sum()
df_for_age['suicides_per_100k'] = df_for_age['suicides_no']/df_for_age['population'] * 100000
age = df['age'].unique()
plt.figure(figsize=(9,6))
sns.lineplot(x="year",y="suicides_per_100k",hue="age",data=df_for_age,style="age",markers=['o' for i in range(len(age))],dashes=False)
plt.xticks(rotation=45)
plt.grid()
plt.show()
# As we can see on this plot 'suicide rate for 100k' gets higher with age. That's why we can say that 'age' is one of many factors of suicides.

df_for_generation = df.groupby(['year','generation'])['suicides_no','population'].sum()
df_for_generation['suicides_per_100k'] = df_for_generation['suicides_no']/df_for_generation['population'] * 100000
generations = df['generation'].unique()
plt.figure(figsize=(9,6))
sns.lineplot(x='year',y='suicides_per_100k',hue="generation",data=df_for_generation,style="generation",markers=['o' for i in range(len(generations))],dashes=False)
plt.grid()
plt.show()
# As we can see the highest rate of suicides per 100k before 2000 has 'G.I Generation' which is also known as WW2 Generation.
# The rate is so high due to worldwide depression before WW2, income, profit,taxes and so on.
# So this generation experianced economic and social turmoil.
# It's very intresting, since 'suicide rate per 100k' for Generation X and Milenials increase step by step.
# That rate increases rapidly once the average age of generation is over 20.
# Does it mean that chance of suicide by young person rise when they are more independant of parents?
# Lets take a look and see if having healthy family have impact on 'suicide rate per 100k'

# To do this I want to check how many countris do we have in our dataset.
# Than I will calculate the suicide rate per 100k 
df1 = df.groupby("country")['suicides_no'].sum()
country_names = list(df1.index.get_level_values(0))
print(len(country_names))
# as we can see we have 101 coutries, now I will check using pycountry if all names of coutries are corect
# firstly i will make dictionary with every country and their code, i will use alpha_3 code
countries = []
for country in pycountry.countries:
    countries.append(country.name)

country_not_in_list = []
for i in country_names:
    if i not in countries:
        print(i)
        country_not_in_list.append(i)

df.replace('Saint Vincent and Grenadines','Saint Vincent and the Grenadines',inplace=True)
df.replace('Republic of Korea','Korea, Republic of',inplace=True)
df.replace('Macau','Macao',inplace=True)
df.replace('Czech Republic','Czechia',inplace=True)

# Finaly we can jump to visualization of suicide rate per 100k for every country.
df_suicide = df.groupby(["country",'year'])["suicides_no"].sum()
df_population = df.groupby(["country","year"])['population'].sum()
df_sum = df_suicide.sort_values(ascending=True) * 100000
df_pop = df_population.sort_values(ascending=False)
df_total = df_sum/df_pop

country_dict = {}
for country in df_total.index.get_level_values(0):
    if country not in country_dict.keys():
        country_dict[country] = df_total[country].mean()
    else:
        pass

tup = list(country_dict.items())
tup.sort(key=lambda x:x[1],reverse=True)
country_list = [a[0] for a in tup]
country_suicide = [a[1] for a in tup]

plt.figure(figsize=(8,32))
sns.barplot(x=country_suicide[:20],y=country_list[:20],palette="GnBu")
plt.yticks(rotation=45)
plt.ylabel("countrie")
plt.xlabel("suicides per 100k")
plt.title("20 countries with highest suicides per 100k")
plt.grid()
plt.show()


df_total = pd.DataFrame(df_total)
df_total = df_total.rename(columns={0:'suicides_per_100k_for_year'},inplace=False).reset_index()
df_top_10 = df_total[df_total['country'].isin(country_list[:10])]
plt.figure(figsize=(9,32))
sns.lineplot(x='year',y='suicides_per_100k_for_year',hue='country',data=df_top_10,style='country',markers=['o' for i in range(10)],dashes=False)
plt.grid()
plt.show()
# As we can se on this plot most of coutries from Top 10 were members of Soviet Union
# It should be clearly that suicide rate per 100k for these countries is high
# due to economic and democratic transfer which occured in former Soviet Union countries between 1990 and 2000.
# Although there are many studies which mentions alcoholism,economic hardship depression as another factors of higher rate of suicide.
# But as far as I know no one which is the main factor of that trend.

df_new = pd.read_excel("master1.xlsx")
df_merged = df_top_10.merge(df_new,on='country',how='left')
df_merged = df_merged.rename(columns={' gdp_for_year ($) ':'gdp_for_year','gdp_per_capita ($)':'gdp_per_capita'},inplace=False)
print(df_merged["country"].unique())
print(df_merged["gdp_for_year"])

df_gdp_for_year = df_merged.groupby(['country','year']).agg('mean','gdp_per_capita')
#sns.lineplot(x=df_gdp_for_year.index.get_level_values(1),y="gdp_per_capita",hue=df_gdp_for_year.index.get_level_values(0),data=df_gdp_for_year)
#plt.show()