import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm

st.write("安全库存和再订货水平测算!")

# 输入过去12个月的消耗历史，采购交货期和期望的服务水平
with st.sidebar:
    Month = [st.number_input(f'Month{i}', value=0, min_value=0) for i in range(1, 13)]
    period = st.number_input('期间', value=1, min_value=1, max_value=12)
    LeadTime = st.number_input('采购提前期（Day）')
    ServiceLevel = st.slider('服务水平', 0.80, 0.99)

# 处理历史消耗数据
demand = pd.DataFrame({'Month': range(1, period+1), 'Demand': Month[:period]})

# 计算预测消耗
forecast_demand = demand['Demand'].sum() / period

# 计算安全库存和再订货点
Lead_Time_Demand = forecast_demand * (LeadTime/30)
Standard_Deviation = demand['Demand'].std()
Service_Factor = norm.ppf(ServiceLevel)
Lead_Time_Factor = np.sqrt(LeadTime/30)
Safety_Stock = Standard_Deviation * Service_Factor * Lead_Time_Factor
Reorder_Point = Safety_Stock + Lead_Time_Demand

# 输出结果
st.subheader('Input Data')
st.write('消耗数', demand)
st.write('采购提前期（Day）', LeadTime)
st.write('服务水平', ServiceLevel)
st.write('期间', period)

st.subheader('测算安全库存和再订货点')
st.write('标准差', round(Standard_Deviation, 2))
st.write('安全库存', round(Safety_Stock, 2))
st.write('再订货点', round(Reorder_Point, 2))