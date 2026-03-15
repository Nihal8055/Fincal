import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

# Page Config
st.set_page_config(page_title="FinCal Pro", layout="wide")
st.title("🚀 FinCal Pro – AI Wealth Architect")

# Sidebar Inputs
with st.sidebar:

    st.header("📊 Investment Inputs")

    sip = st.number_input("Monthly SIP ₹", value=10000, step=1000)
    years = st.slider("Investment Duration (Years)",1,40,20)
    return_rate = st.slider("Expected Annual Return %",5,25,12)
    stepup = st.slider("Annual Step-Up %",0,20,10)

    goal = st.number_input("Financial Goal Target ₹", value=10000000)

    inflation = st.slider("Inflation Rate %",3,10,6)

    st.markdown("---")

    st.header("🧠 Risk Profile")

    risk = st.selectbox(
        "Risk Appetite",
        ["Low","Medium","High"]
    )

    st.markdown("---")

    st.header("🔥 FIRE Calculator")

    monthly_exp = st.number_input(
        "Monthly Expense ₹",
        value=30000
    )

# SIP Calculation Engine
def sip_calculator(sip,rate,years,stepup):

    months = years*12
    m_rate = rate/12/100

    balance = 0
    invested = 0
    curr_sip = sip

    data=[]

    for m in range(1,months+1):

        balance=(balance+curr_sip)*(1+m_rate)
        invested+=curr_sip

        if m%12==0:

            yr=m//12

            real_value = balance/((1+inflation/100)**yr)

            data.append({
                "Year":yr,
                "Wealth":balance,
                "Invested":invested,
                "RealValue":real_value
            })

            curr_sip += curr_sip*(stepup/100)

    df=pd.DataFrame(data)

    return df,balance,invested

df,wealth,invested = sip_calculator(
    sip,return_rate,years,stepup
)

# Dashboard Metrics
c1,c2,c3=st.columns(3)

c1.metric("Total Investment",f"₹{invested:,.0f}")
c2.metric("Projected Wealth",f"₹{wealth:,.0f}")
c3.metric(
    "Today's Purchasing Power",
    f"₹{wealth/((1+inflation/100)**years):,.0f}"
)

# Goal Tracker
st.subheader("🎯 Goal Progress")

progress=min(wealth/goal,1.0)

st.progress(progress)

st.write(f"{progress*100:.1f}% of your goal achieved")

# Compounding Pie Chart
st.subheader("📊 Magic of Compounding")

fig_pie=px.pie(
    names=["Invested Amount","Interest Earned"],
    values=[invested,wealth-invested],
    hole=0.5
)

st.plotly_chart(fig_pie,use_container_width=True)

# Wealth Growth Graph
st.subheader("📈 Wealth Projection")

fig=go.Figure()

fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["Wealth"],
    name="Future Value"
))

fig.add_trace(go.Scatter(
    x=df["Year"],
    y=df["RealValue"],
    name="Inflation Adjusted"
))

fig.update_layout(
    template="plotly_dark",
    hovermode="x unified"
)

st.plotly_chart(fig,use_container_width=True)

# Monte Carlo Simulation
st.subheader("🎲 Monte Carlo Simulation")

def monte_carlo(sip,years,avg_return,simulations=1000):

    months=years*12
    results=[]

    for i in range(simulations):

        bal=0

        for m in range(months):

            r=np.random.normal(avg_return/12/100,0.04)

            bal=(bal+sip)*(1+r)

        results.append(bal)

    return results

sim=monte_carlo(
    sip,
    years,
    return_rate
)

fig_mc=px.histogram(
    sim,
    nbins=40,
    title="Wealth Distribution"
)

st.plotly_chart(fig_mc)

# FIRE Calculator
st.subheader("🔥 FIRE Calculator")

fire_target = monthly_exp*12*25

st.write(
    f"Required Corpus for Financial Independence: ₹{fire_target:,.0f}"
)

if wealth>=fire_target:

    st.success(
        "You can achieve Financial Independence!"
    )

else:

    st.warning(
        "Increase investments to reach FIRE."
    )

# Portfolio Allocation
st.subheader("📊 Recommended Portfolio")

if risk=="High":

    alloc={
        "Equity":80,
        "Debt":10,
        "Gold":10
    }

elif risk=="Medium":

    alloc={
        "Equity":60,
        "Debt":30,
        "Gold":10
    }

else:

    alloc={
        "Equity":30,
        "Debt":60,
        "Gold":10
    }

fig_alloc=px.pie(
    names=list(alloc.keys()),
    values=list(alloc.values())
)

st.plotly_chart(fig_alloc)

# Tax Estimator
st.subheader("💰 Tax Estimation")

profit = wealth-invested

ltcg=max((profit-100000)*0.10,0)

st.write(
    f"Estimated Long Term Capital Gain Tax: ₹{ltcg:,.0f}"
)

# Live Market Data
st.subheader("📈 Live Stock / ETF Tracker")

ticker=st.text_input(
    "Enter Stock Symbol",
    "AAPL"
)

data=yf.download(
    ticker,
    period="1y"
)

if not data.empty:
    data.columns = data.columns.get_level_values(0)

    fig_stock = px.line(
        data,
        y="Close",
        title=f"{ticker} Price"
    )

    st.plotly_chart(fig_stock)

# new feture add now for detecting your gole complite

from sklearn.linear_model import LinearRegression

st.subheader("🧠 AI Wealth Predictor")

years_data = df["Year"].values.reshape(-1,1)
wealth_data = df["Wealth"].values

model = LinearRegression()
model.fit(years_data, wealth_data)

future_year = st.slider("Predict Future Year", years, years+20, years+5)

prediction = model.predict([[future_year]])

st.write(f"Predicted Wealth in {future_year} years:")

st.success(f"₹{prediction[0]:,.0f}")


# Net Worth Tracker
st.subheader("💎 Net Worth Tracker")

stocks=st.number_input("Stocks ₹",0)
crypto=st.number_input("Crypto ₹",0)
cash=st.number_input("Cash ₹",0)
realestate=st.number_input("Real Estate ₹",0)
networth=stocks+crypto+cash+realestate
st.metric(
    "Total Net Worth",
    f"₹{networth:,.0f}"
)
fig_net=px.pie(
    names=[
        "Stocks",
        "Crypto",
        "Cash",
        "Real Estate"
    ],
    values=[
        stocks,
        crypto,
        cash,
        realestate
    ]
)
st.plotly_chart(fig_net)
# Data Table + Export
with st.expander("📄 Yearly Breakdown"):

    st.dataframe(df)

    st.download_button(
        "Download CSV Report",
        df.to_csv(index=False),
        "FinCal_Report.csv"
    )
    
# ab ye batayega ki konsa mutual fund le 
st.subheader("📊 Mutual Fund Suggestions")

if risk == "High":

    funds = [
        "Quant Small Cap Fund",
        "Nippon Small Cap Fund",
        "Axis Midcap Fund"
    ]

elif risk == "Medium":

    funds = [
        "Parag Parikh Flexi Cap",
        "UTI Nifty 50 Index Fund"
    ]

else:

    funds = [
        "HDFC Balanced Advantage",
        "ICICI Conservative Hybrid"
    ]

for fund in funds:
    st.write("✔️",fund)
    # new feature ke liye hai
 