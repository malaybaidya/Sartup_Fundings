import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

df=pd.read_csv("startup_clean1.csv")
df["date"]=pd.to_datetime(df["date"],format='mixed',errors="coerce")
df["year"]=df["date"].dt.year
st.set_page_config(layout="wide",page_title="Startup_Analysis")
df["month"] = df["date"].dt.month

#Title
st.sidebar.title("Startup Funding Analysis")
option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])


def overall_analysis():
    st.title("Overall Analysis")
    #total invested amount
    total=round(df["amount"].sum())
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby("startup")["amount"].sum().mean()
    num_startup=df["startup"].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total Amount",str(total)+" Cr")
    with col2:
        st.metric("Max Amount",str(max_funding)+" Cr")
    with col3:
        st.metric("Avg Amount",str(round(avg_funding))+" Cr")
    with col4:
        st.metric("Total Startup",str(num_startup))


    st.subheader("MoM Graph")
    select_opt=st.selectbox("Select Type",["Total","Count"])
    if select_opt=="Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
        temp_df["x_axis"] = temp_df["month"].astype(str) + "-" + temp_df["year"].astype(str)
        fig = px.line(temp_df, x="x_axis", y="amount",title="Amount of Money Invested in Every Month in Cr")
        st.plotly_chart(fig)
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()
        temp_df["x_axis"] = temp_df["month"].astype(str) + "-" + temp_df["year"].astype(str)
        fig = px.line(temp_df, x="x_axis", y="amount",labels={"amount":"no_of_investment"},title="Total Number of Investment in Every Month")
        st.plotly_chart(fig)

    #city wise funding
    st.subheader("City wise funding")
    temp1 = df.groupby("city")["amount"].sum().reset_index()
    temp2 = temp1[temp1['amount'] != 0]
    fig2 = px.bar(temp2, x="city", y="amount")
    st.plotly_chart(fig2)
    #top startup
    top_startup = df.groupby(["year", "startup"])["amount"].sum().reset_index().sort_values(["year", "amount"], ascending=[True,False]).drop_duplicates("year", keep="first")
    st.subheader("Top Startups in Every year")
    st.dataframe(top_startup)

def load_investor_details(select_investor):
    st.title(select_investor)
    lastdf=df[df["investors"].str.contains(select_investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Recent 5 investment")
    st.dataframe(lastdf)
    col1,col2=st.columns(2)
    col3, col4 = st.columns(2)
    with col1:
      big_ser=df[df["investors"].str.contains(select_investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
      st.subheader("Biggest Investment")
      fig1 = px.pie(big_ser, names=big_ser.index, values=big_ser.values)
      st.plotly_chart(fig1)
    with col2:
        vertical_ser=df[df["investors"].str.contains(select_investor)].groupby("vertical")["amount"].sum().sort_values(ascending=False)
        st.subheader("Sectors invested in")
        fig2=px.pie(vertical_ser,names=vertical_ser.index,values=vertical_ser.values)
        st.plotly_chart(fig2)
    with col3:
        city_ser2 = df[df["investors"].str.contains(select_investor)].groupby("city")["startup"].count().sort_values(ascending=False)
        st.subheader("Cities invested in")
        fig3 = px.pie(city_ser2, names=city_ser2.index,values=city_ser2.values)
        st.plotly_chart(fig3)
    with col4:
        round_ser2 = df[df["investors"].str.contains(select_investor)].groupby("round")["startup"].count().sort_values(ascending=False)
        st.subheader("Stages invested in")
        fig4 = px.pie(round_ser2, names=round_ser2.index, values=round_ser2.values)
        st.plotly_chart(fig4)
    #year on year investment
    year_ser=df[df["investors"].str.contains(select_investor)].groupby("year")["amount"].sum()
    st.subheader("YoY Investment")

    fig4=px.line(year_ser,x=year_ser.index,y=year_ser.values,labels={"y":"amount"})
    st.plotly_chart(fig4)



def startup_analysis(startup_name):
    st.title(startup_name)
    col1, col2 = st.columns(2)
    col3, col4, col5= st.columns(3)
    #founder
    with col1:
      st.subheader("Founders")
      founders = df[df["startup"] == startup_name]["investors"].values[0]
      st.markdown(" - "+founders)
    #Industry
    with col3:
       st.subheader("Industry")
       industry = df[df["startup"] == startup_name]["vertical"].values[0]
       st.markdown(" - " + industry)
    # sub-Industry
    with col4:
        st.subheader("Sub Industry")
        sub_industry = df[df["startup"] == startup_name]["subvertical"].values[0]
        st.markdown(" - " + sub_industry)
    with col5:
        st.subheader("Location")
        location = df[df["startup"] == startup_name]["city"].values[0]
        st.markdown(" - " + location)




#main structure
if option=="Overall Analysis":
        overall_analysis()

elif option=="Startup":
    select_startup=st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique()))
    btn1=st.sidebar.button("Find startup details")
    st.subheader("Startup Analysis")
    if btn1:
      startup_analysis(select_startup)

else:
    selected_investor=st.sidebar.selectbox("Select Startup", sorted(set(df["investors"].str.split(", ").sum())))
    btn2 = st.sidebar.button("Find investor details")
    st.subheader("Investor Analysis")
    if btn2:
        load_investor_details(selected_investor)


