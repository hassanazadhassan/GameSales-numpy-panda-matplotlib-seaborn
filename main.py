import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import lineStyles

df = pd.read_csv("VideoGamesSales.csv")
df = df.drop_duplicates()
df['Region'] = df['Region'].fillna('North') #Publisher
df['Publisher'] = df['Publisher'].fillna('Nintendo')
# df = df[df['Region'].isnull()] #To check null value by column name region
df["NA_Sales"] = df["NA_Sales"].replace('[$]','',regex=True)
df["Country"] =df["Country"].replace({"USA":"United States"})
df["Country"] = df["Country"].str.title()
df = df.rename(columns={'NA_Sales': 'National Sales', 'Global_Sales': 'Global Sales',
                        'NA_Profit': 'National Profit', 'Global_Profit': 'Global Profit'})
df["National Sales"] = pd.to_numeric(df["National Sales"], errors="coerce")

sale_cap = df["National Sales"].quantile(0.95)
df["National Sales"] = np.where(df["Global Sales"] > sale_cap,  sale_cap, df['National Sales'])

National_Sales = df.groupby(['Region', 'Country'])["National Sales"].sum().reset_index().sort_values(by="National Sales", ascending=True)

#Bar Plot
# fig = plt.figure(figsize=(14,6))
# sns.barplot(data=National_Sales, x='Region', y='National Sales', hue='Country', palette='coolwarm')
# plt.title('National Sales by Region and Country', fontweight='bold')
# plt.xlabel('Region', fontweight='bold')
# plt.ylabel('National Sales', fontweight='bold')
# plt.show()

#Box Plot
# fig = plt.figure(figsize=(8, 5))
# sns.boxplot(data=df, x='Country', y='National Sales', hue='Genre', showmeans=True, palette='coolwarm',
#             meanprops={'marker':'s',
#                        'markerfacecolor': 'white',
#                        'markersize' : 5,
#                        'markeredgecolor': 'red'
#
# })
# plt.title('National Sales by Country', fontweight='bold')
# plt.xlabel('Country', fontweight='bold')
# plt.ylabel('National Sales', fontweight='bold')
# plt.show()


#Pie Chart
# Sales = df.groupby(['Country'])[["National Sales", 'Global Sales']].sum().reset_index()
# country = Sales['Country']
# national_sales = Sales['National Sales']
# global_sales = Sales['Global Sales']
#
# fig, axe = plt.subplots(1, 2, figsize=(10, 8))
#
# axe[0].pie(national_sales, labels=country, autopct='%1.1f%%', startangle=90)
# axe[0].set_title('National Sales by Country', fontweight='bold')
#
# axe[1].pie(global_sales, labels=country, autopct='%1.1f%%', startangle=80)
# axe[1].set_title('Global Sales by Country', fontweight='bold')
#
# plt.show()


yearly_sales = df.groupby("Year")[["National Sales", "Global Sales"]].sum().reset_index()

fig = plt.figure(figsize=(10, 6))

plt.plot(yearly_sales['Year'], yearly_sales["National Sales"], marker='o', linestyle='-', color='b', label='National Sales')

plt.plot(yearly_sales['Year'], yearly_sales["Global Sales"], marker='s', linestyle='--', color='g', label='Global Sales')

plt.title('National and Global Sales over the Year')
plt.xlabel('Year')
plt.ylabel('Sales')
plt.legend()

plt.grid(True)
plt.show()