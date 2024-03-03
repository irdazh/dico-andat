import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')


# Load cleaned data
bike = pd.read_csv("dashboard/hour.csv")

# prepare the dataset
bike_hourly = bike.groupby(by="hr").agg({"cnt":"mean"}).reset_index()
bike_daily = bike.groupby(by="dteday").agg({"weekday":"mean", "cnt":"sum"})
bike_weekly = bike_daily.groupby(by="weekday").mean()
bike_monthly = bike.groupby(by="mnth")[["cnt"]].sum()

bike_weather = bike.groupby("weathersit")[["cnt"]].sum()


# give header and sub header
st.header('Bike Sharing :sparkles:')

st.subheader('How\'s your day? Here\'s daily bikes\' shared!')
# first daily pesepeda
fig, ax = plt.subplots(figsize=(16, 8))
bike_daily.cnt.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Quantity") 
st.pyplot(fig)

st.text("Lots of bikers do bike in March 'till August. From the above graph, we could also see a visible increment from 2011 to 2012.")

# weather condition
st.subheader('Does weather matter? I\'d say so!')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(bike_weather.cnt)
ax.set_xlabel("Weather Condition (4 is extreme!)")
ax.set_ylabel("Sum of Bikers") 
st.pyplot(fig)


# weather condition part 2
st.subheader('Who would\'ve gone in a hot, humid day!!!')

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.scatterplot(data=bike, x="temp", y="cnt", s=5, legend=False)
    ax.set_ylabel("# Bikers")
    ax.set_xlabel("Temperature")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
          item.set_fontsize(35)

    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.scatterplot(data=bike, x="hum", y="cnt", legend=False)
    ax.set_ylabel("# Bikers")
    ax.set_xlabel("Humidity")
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label] +
             ax.get_xticklabels() + ax.get_yticklabels()):
          item.set_fontsize(35)    
    st.pyplot(fig)

# the best day to bike
st.subheader('When to Bike?')


def iterize(ax):
    for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
          item.set_fontsize(10)   

fig, axes = plt.subplots(ncols=3, nrows=1, figsize=(15, 15), sharey=False)
axes = axes.ravel()

sns.lineplot(bike_hourly.cnt, ax=axes[0])
axes[0].set_ylabel("# Bikers")
axes[0].set_xlabel("Hour")
iterize(axes[0]) 

sns.barplot(bike_weekly.cnt, ax=axes[1])
axes[1].set_ylabel(None)
axes[1].set_xlabel("Week")
iterize(axes[1]) 

sns.barplot(bike_monthly.cnt, ax=axes[2])
axes[2].set_ylabel(None)
axes[2].set_xlabel("Month")
iterize(axes[2])

st.pyplot(fig)


