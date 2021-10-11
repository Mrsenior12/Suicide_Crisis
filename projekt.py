import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pycountry
from scipy import stats

df = pd.read_csv("master.csv")
df["age"] = df['age'].replace({'5-14 years': '05-14 years'})
df = df.rename(columns={' gdp_for_year ($) ':'gdp_for_year','gdp_per_capita ($)':'gdp_per_capita'},inplace=False)
df.pop("suicides/100k pop")
df.pop("country-year")
df.pop("HDI for year")
print(df.head())
print(df.shape)
print(df.info())
print(df.any().isna())
df_for_year = df.groupby("year").agg('sum','suicides_no')
df_for_year['suicides_per_100k'] = df_for_year['suicides_no']/df_for_year["population"] * 100000
print(df_for_year.head())

sns.lineplot(x = "year",y="suicides_per_100k",data=df_for_year)
plt.ylabel("Suicides per 100K")
plt.grid(linestyle="--")
plt.title("Suicides vs Year")
plt.show()
# As we can se on this plot 'suicide rate for 100k' worldwide, was quite high.
# After 1987 we can see 30% increase in 'suicide rate for 100k'. We can say that increase was caused by change of the political system around the world.
# Another factor of that increase might be economic crisis. There are many factors which might or might not caused this increase. 
# After 1995 we can see that 'suicide rate for 100k' slowly decreased itself
# It's hard to predict future 'suicide rate for 100k', due to many factors which may occure in the future.

df_for_year_sex = df.groupby(["sex","year"])['suicides_no','population'].sum()
df_for_year_sex["suicides_per_100k"] = df_for_year_sex["suicides_no"]/df_for_year_sex['population'] * 100000
df_for_year_sex = df_for_year_sex.sort_values("year")

sns.lineplot(x="year",y="suicides_per_100k",hue="sex",data=df_for_year_sex,style="sex",markers=["o","o"],dashes=False)
plt.ylabel("Suicides per 100K")
plt.grid(linestyle="--")
plt.title("Suicides for Gender vs Year")
plt.show()
# As we can see on that plot, it doesn't matter which year it is, 'suicide rate for 100k' for men is more than 2.5 times higher than for women.
# It might be caused by enviromental preassure which states that men must be very successful or they have to be the head of the family. 

df_for_age = df.groupby(["year","age"])['suicides_no','population'].sum()
df_for_age['suicides_per_100k'] = df_for_age['suicides_no']/df_for_age['population'] * 100000
age = df['age'].unique()

plt.figure(figsize=(9,6))
sns.lineplot(x="year",y="suicides_per_100k",hue="age",data=df_for_age,style="age",markers=['o' for i in range(len(age))],dashes=False)
plt.xticks(rotation=45)
plt.ylabel("Suicides per 100K")
plt.grid(linestyle="--")
plt.title("Suicides for Age vs Year")
plt.show()
# As we can see on this plot 'suicide rate for 100k' gets higher with age. That's why we can say that 'age' is one of many factors of suicides.

df_for_generation = df.groupby(['year','generation'])['suicides_no','population'].sum()
df_for_generation['suicides_per_100k'] = df_for_generation['suicides_no']/df_for_generation['population'] * 100000
generations = df['generation'].unique()

plt.figure(figsize=(9,6))
sns.lineplot(x='year',y='suicides_per_100k',hue="generation",data=df_for_generation,style="generation",markers=['o' for i in range(len(generations))],dashes=False)
plt.ylabel("Suicides per 100K")
plt.grid(linestyle="--")
plt.title("Suicides for generation vs Year")
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

plt.figure(figsize=(9,10))
sns.barplot(x=country_suicide[:20],y=country_list[:20],palette="GnBu")
plt.yticks(rotation=45)
plt.ylabel("Countrie")
plt.xlabel("Suicides per 100k")
plt.title("20 countries with highest suicides per 100k")
plt.grid(linestyle="--")
plt.show()

df_total1 = pd.DataFrame(df_total)
df_total1 = df_total1.rename(columns={0:'suicides_per_100k_for_year'},inplace=False).reset_index()
df_top_10 = df_total1[df_total1['country'].isin(country_list[:10])]
top_10_country = df_top_10['country'].unique()
fig,axa1 = plt.subplots(1,2,figsize=(12,10))
sns.lineplot(ax=axa1[0],x='year',y='suicides_per_100k_for_year',hue='country',data=df_top_10,style='country',markers=['o' for i in range(10)],dashes=False)
axa1[0].grid(linestyle="--")
axa1[0].set_ylabel("Suicides per 100K")
axa1[0].set_title("Cuicides vs Year")
# As we can se on this plot most of coutries from Top 10 were members of Soviet Union
# It should be clearly that suicide rate per 100k for these countries is high
# due to economic and democratic transfer which occured in former Soviet Union countries between 1990 and 2000.
# Although there are many studies which mentions alcoholism,economic hardship depression as another factors of higher rate of suicide.
# But as far as I know no one accepted as the main factor of that trend.

df_gdp = df.groupby(["country","year"])["gdp_per_capita"].mean()

for country in top_10_country[:10]:
    axa1[1].plot(df_gdp[country].index,df_gdp[country].values, label=country, marker="o")
axa1[1].set_xlabel("year")
axa1[1].set_ylabel("GDP per capita")
axa1[1].yaxis.tick_right()
axa1[1].legend(prop={"size":11})
axa1[1].yaxis.set_label_position("right")
axa1[1].grid(linestyle="--")
axa1[1].set_title("GDP vs Year")
plt.tight_layout()
plt.show()
# As we can see on this image 'GDP per capit' for every country between 1985 and 2000 didn't changed as much as I thought. 
# In other words, economic situation in these countries were stagnant. We can see that 'GDP_per_capita' started to grow after 2002, 
# but there is drop in GPD_per_capita after 2008 due to financial crisis which occured that year.
# Now I want to now if there is relationship between GDP_per_capita and suicides_rate

fig,axa2 = plt.subplots(2,1,figsize=(12,12))
for country in top_10_country[:10]:
    sns.regplot(ax=axa2[0],x=df_gdp[country].values,y=df_total[country].values,label=country)
axa2[0].set_xlim(0,30000)
axa2[0].set_xlabel("GDP per capita")
axa2[0].set_ylabel("Rate of suicides for 100K")
axa2[0].grid(linestyle="--")
axa2[0].set_title("Suicides vs GDP")
axa2[0].legend()

corr_dict = {}
for country in top_10_country[:10]:
    slope,intercept,r_value,p_value,std_value = stats.linregress(df_gdp[country].values,df_total[country].values)
    corr_dict[country] = float(r_value)

sns.barplot(ax=axa2[1],x=list(corr_dict.keys()),y=list(corr_dict.values()),palette = "YlOrRd")
axa2[1].xaxis.set_tick_params(rotation=90)
axa2[1].set_xlabel("Country")
axa2[1].set_ylabel("Correlation coeff.")
axa2[1].set_title("GDP vs suicides for 100k")
plt.show()
# On the top image we can see for with increase of GDP_per_capita rate of suicides are getting lower.
# We can see on the bottom image that the suicide rate is strongly correlated to the GDP_per_capita of top10 countries.
# Now i would like to see if other countries have the same trend.

corr_dict = {}
p_val_dict = {}
for country in country_list[:]:
    slope,intercept,r_value,p_value,std_value = stats.linregress(df_gdp[country].values,df_total[country].values)
    corr_dict[country] = float(r_value)
    p_val_dict[country] = float(p_value)

gdp_tup = list(corr_dict.items())
gdp_tup.sort(key = lambda x:x[1],reverse=False)
gdp_rel = {a[0]:a[1] for a in gdp_tup}

plt.figure(figsize=(16,10))
sns.barplot(x=list(gdp_rel.keys()),y=list(gdp_rel.values()),palette="YlOrRd")
plt.xticks(rotation=90)
plt.xlabel("Country")
plt.ylabel("Correlation coeff.")
plt.title("GDP vs suicides")
plt.show()
# The lower correlation coefficient the higher inpact GDP_per_capita has on suicides rate.
# We can see that for the most countries in our dataset we have negative correlation, which means in these countries
# increase of GDP_per_capita resulted in a lowering suicides rate.
# There are some countries where correlation was equal to 0 or higher than 0, which was quite big surprise for me.
# because it means that in some countries increas of GDP_per_capita resulted in increase of suicide rate.

# Now i will see which countries have Strong or Very Strong negative correlation and which have Very Strong positive correlation
negative_relation_gdp = {a:b for a,b in gdp_rel.items() if b <= -0.6}
print(len(negative_relation_gdp))
for i in negative_relation_gdp.items():
    print(i)
# We can see that almost one third of countries have Strong or Very Strong negative correlation

positive_relation = {a:b for a,b in gdp_rel.items() if b >= 0.6}
positive_relation_tup = list(positive_relation.items())
positive_relation_tup.sort(key=lambda x:x[1],reverse=True)
positive_relation_gdp = {a[0]:a[1] for a in positive_relation_tup}

print(len(positive_relation_gdp))
for i in positive_relation_gdp.items():
    print(i)

# Now I wil plot GDP_per_capita and suicide rate for 100k the same way as I did with top10 countires with highest suicide rate

bottom_10 = list({a:b for a,b in positive_relation_gdp.items()})

fig,axa3 = plt.subplots(1,2,figsize=(15,10))
for country in bottom_10[:10]:
    axa3[0].plot(df_gdp[country].index,df_gdp[country].values,label=country,marker="o")
axa3[0].set_xlabel("Year")
axa3[0].set_ylabel("GDP per capita")
axa3[0].grid(linestyle="--")
axa3[0].legend()
axa3[0].set_title("GDP vs Year")

for country in bottom_10[:10]:
    axa3[1].plot(df_gdp[country].index,df_total[country].values,label=country,marker="o")
axa3[1].set_xlabel("Year")
axa3[1].set_ylabel("Suicides for 100K")
axa3[1].yaxis.tick_right()
axa3[1].yaxis.set_label_position("right")
axa3[1].legend(prop={"size":10})
axa3[1].grid(linestyle="--")
axa3[1].set_title("Suicides vs Year")
plt.tight_layout()
plt.show()
# First thing we can see is GDP per capita and Suicides for 100K of Korea are growing faster than in other countries.
# Does it mean there is social problem which led to this situation? Let's see

Korea = df[df["country"] == "Korea, Republic of"]
Korea_suicides = Korea.groupby(["year","age"])["suicides_no"].sum()*100000
Korea_population = Korea.groupby(["year","age"])["population"].sum()
Korea_rate = Korea_suicides/Korea_population
df_korea = pd.DataFrame(Korea_rate)
df_korea = df_korea.rename(columns={0:'suicides_per_100k_for_age'},inplace=False).reset_index()

plt.figure(figsize=(10,10))
sns.barplot(x="year",y="suicides_per_100k_for_age",hue="age",ci=None,data=df_korea)
plt.show()