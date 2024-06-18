import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df=pd.read_csv("startup_clean1.csv")
df["date"]=pd.to_datetime(df["date"],format='mixed',errors="coerce")
df["year"]=df["date"].dt.year
st.set_page_config(layout="wide",page_title="Startup_Analysis")
df["month"] = df["date"].dt.month
def overall_analysis():
    st.title("Overall Analysis")
    #total invested amount
    total=round(df["amount"].sum())
    max_funding=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby("startup")["amount"].sum().mean()
    num_startup=df["startup"].nunique()

    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total",str(total)+" Cr")
    with col2:
        st.metric("Max",str(max_funding)+" Cr")
    with col3:
        st.metric("Total",str(round(avg_funding))+" Cr")
    with col4:
        st.metric("Total",str(num_startup))


    st.subheader("MoM Graph")
    select_opt=st.selectbox("Select Type",["Total","Count"])
    if select_opt=="Total":
        temp_df = df.groupby(["year", "month"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "month"])["amount"].count().reset_index()

    temp_df["x_axis"] = temp_df["month"].astype(str) + "-" + temp_df["year"].astype(str)
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df["x_axis"],temp_df["amount"])
    st.pyplot(fig3)


def load_investor_details(select_investor):
    st.title(select_investor)
    lastdf=df[df["investors"].str.contains(select_investor)].head()[["date","startup","vertical","city","round","amount"]]
    st.subheader("Recent 5 investment")
    st.dataframe(lastdf)
    col1,col2=st.columns(2)
    with col1:
      big_ser=df[df["investors"].str.contains(select_investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
      st.subheader("Biggest Investment")
      fig,ax=plt.subplots()
      ax.bar(big_ser.index,big_ser.values)
      st.pyplot(fig)
    with col2:
        vertical_ser=df[df["investors"].str.contains(select_investor)].groupby("vertical")["amount"].sum().sort_values(ascending=False)
        st.subheader("Sectors invested in")
        fig1, ax1= plt.subplots()
        ax1.pie(vertical_ser,labels=vertical_ser.index,autopct="%0.01f%%")
        st.pyplot(fig1)

    #year on year investment
    year_ser=df[df["investors"].str.contains(select_investor)].groupby("year")["amount"].sum()
    st.subheader("YoY Investment")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_ser.index,year_ser.values)
    st.pyplot(fig2)

st.sidebar.title("Startup Funding Analysis")
option=st.sidebar.selectbox("Select One",["Overall Analysis","Startup","Investor"])






#main structure
if option=="Overall Analysis":
        overall_analysis()

elif option=="Startup":
    st.sidebar.selectbox("Select Startup", sorted(df["startup"].unique()))
    btn1=st.sidebar.button("find startup details")
    st.title("Startup Analysis")

else:
    selected_investor=st.sidebar.selectbox("Select Startup", sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("find investor details")
    if btn2:
        load_investor_details(selected_investor)


