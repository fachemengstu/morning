import streamlit as st
import pandas as pd
import numpy as np
from pandas.io.sas import sas7bdat
import sas7bdat
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
st.title("Summary analysis on the ECL dataset  ")
st.sidebar.title("Summary analysis on the ECL dataset ")

st.markdown("This application is streamlit dashboard to analysze the ECl Dataset for Banca Ifis  ")
st.sidebar.markdown("This application is streamlit dashboard to analysze the ECl Dataset for banca ifis")
# Read data from the 'Ead_dis_rating_March' sheet in an Excel file and save as CSV
df1= ('Y:\RISK_SM\Stage_Futsum\Total_Summary_Dec&Mar.xlsx')

@st._cache_data(persist=True)
def load_data():
    data = pd.read_excel(df1, sheet_name='SummaryTable', engine='openpyxl')
    data=data.to_csv('C:/Users/fmuche/Downloads/RatingModels79.csv', index=False)
    data=pd.read_csv('C:/Users/fmuche/Downloads/RatingModels79.csv')
    return data
data = load_data()
#data2 = load_data()
#st.write(data2)
if st.checkbox("** click Here To see the Ecl dataset for December 2022 **" , False):

    #Rating_models = data.loc[(data['DESC_SOTTOMODELLO'].isin(['Small Business', 'Corporate ML', 'Corporate Small']))]
    rating_model = data.groupby(by="DESC_SOTTOMODELLO").sum(numeric_only=True)[["EAD_CURRENT"]]
    business_area = data.groupby(by="business_area").sum(numeric_only=True)[["EAD_CURRENT"]]
    #Rating_modelsAgg=Rating_models.groupby(by="DESC_SOTTOMODELLO").sum(numeric_only=True)[["EAD_CURRENT"]]
    #Rating_modelsAgg_busness = Rating_models.groupby(by="business_area").sum(numeric_only=True)[["EAD_CURRENT"]]
    st.subheader('ECL dataset')
    st.write(data)
    st.write(data.shape)
    st.subheader('Dataset for the rating models')
    #st.write(Rating_models)
    #st.write(Rating_models.shape)
    st.subheader('The columns we have in the dataset')
    st.write(data.columns)
    st.subheader('The sum of Ead_current by Models ')
    st.write(rating_model)
    st.subheader('The sum Ead_current by Business Area')
    st.write(business_area)
    st.subheader('The aggregate Ead_current for Rating Models ')
    #st.write(Rating_modelsAgg)
    st.subheader('The aggregate Ead_current for Rating Models by Business Area')
    #st.write(Rating_modelsAgg_busness)
    #st.write(data2)


#st.sidebar.subheader("Show Me EAD value for rating Rating Models")
#sum_ead_value=st.sidebar.radio('DESC_SOTTOMODELLO',('Corporate ML','Corporate Small','Small Business'))
#st.sidebar.markdown(data.query(data['total_ead_current_Dec']=='sum_ead_value').sum())


st.sidebar.markdown('EAD_value by business area and rating models')
select=st.sidebar.selectbox('Visualization type', ['Histogram','pie chart'],key='1')

#rating_model=pd.DataFrame({'DESC_SOTTOMODELLO':data.index,'tot_ead_current_mar':data.values})
st.markdown('### total ead by rating model for Mach')
if not st.sidebar.checkbox("Hide",True):
    if select=='Histogram':
       fig=px.bar(data,x='DESC_SOTTOMODELLO',y='EAD_CURRENT',color='DESC_SOTTOMODELLO',height=500,width=800)
       #percent=st.sidebar.slider('Percentage',0,100,100)
       #for i, val in enumerate(data['EAD_CURRENT'].values):
           #plt.text(i,val,"{:.2f}%".format(val/data['DESC_SOTTOMODELLO'].sum()*100),fontsize=10)
           #fig.update_traces(marker_color=percent)
       st.plotly_chart(fig)


    else:
        fig=px.pie(data,values='EAD_CURRENT',names='DESC_SOTTOMODELLO')
        st.plotly_chart(fig)

st.sidebar.markdown('EAD_value by business area ')
select=st.sidebar.selectbox('Visualization type', ['Histogram','pie chart'],key='2')
if not st.sidebar.checkbox("Hide",True ,key='3'):
    st.markdown('### total ead by business  area for Mach')
    if select == "Histogram":
        fig1=px.bar(data,x='business_area',y='EAD_CURRENT',color='business_area',height=600)
        st.plotly_chart(fig1)
    else:
        fig1=px.pie(data,values='EAD_CURRENT',names='business_area')
        st.plotly_chart(fig1)

st.subheader("Ead distribution for different months")
choice= st.sidebar.multiselect('Pick different months',('Feburary','March','December'),key='4')
if len(choice)>0:
    choice_data=data[data.REPORTING_DT.isin(choice)]
    fig_choice=px.histogram(choice_data , x='REPORTING_DT', y='EAD_CURRENT', histfunc='sum', color='DESC_SOTTOMODELLO',
                            facet_col='DESC_SOTTOMODELLO',labels={'Rating_model':'EAD_CURRENT'}, height=600, width=800)
    st.plotly_chart(fig_choice)


