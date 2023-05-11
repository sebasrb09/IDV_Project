import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache
def load_data():

    data = pd.read_excel('data/WBL-1971-2023-Dataset.xlsx',sheet_name=1)
    data['id_temp'] = data.sort_values('Region').groupby(['Region','Economy']).ngroup()
    data['id_reg'] = data.sort_values('Region').groupby(['Region']).ngroup()
    years = data['Report Year'].unique()
    return data,years

data,years = load_data()



group_vars = ['South Asia','East Asia & Pacific','Middle East & North Africa',
 'Sub-Saharan Africa','Latin America & Caribbean','Europe & Central Asia', 'High income: OECD',
 ]
dfg = pd.DataFrame({'Region':group_vars})
dfg['dummy'] = dfg.index
data = pd.merge(data, dfg, on = 'Region', how='left')

grouped = data.groupby(['Report Year','Region'], as_index=False)['WBL INDEX'].mean()

st.title('Women Business and the Law Index Data')

st.write('Gender inequality is a global issue that affects economic outcomes and social well-being. Despite progress in some areas, women still face significant barriers to accessing economic opportunities, particularly in the areas of labor force participation, entrepreneurship, and pay equity. Women, Business and the Law 2023 is a report made by the World Bank where they measure women economic opportunities. The Women, Business and the Law data provides valuable information on the legal barriers that women face in different countries and regions, including restrictions on their ability to work and own property, unequal pay, and limitations on their ability to start and manage businesses. Data goes from 1971 to 2023, so there are 52 years of data, from 190 different countries. This amount of data can be difficult to analyze for researchers and also to the general public.')

st.subheader('WBL Index development over years per region')
fig = px.line(grouped, x='Report Year', y='WBL INDEX', color='Region')
st.plotly_chart(fig)

st.write('In the next visualization, you can see the evolution of the WBL Index over the years. A higher value means a better score for the country in terms of Women Economic Opportunities.')

hover_data_cols_main = "WBL INDEX"
hover_data_cols = ["WBL INDEX",'MOBILITY', 'WORKPLACE', 'PAY',
                                          'MARRIAGE','PARENTHOOD','ENTREPRENEURSHIP',
                                          'ASSETS','PENSION','Region']

fig = px.choropleth(data,
                    locations="Economy",
                    locationmode='country names',
                    color=hover_data_cols_main, 
                    hover_name = hover_data_cols_main,
                    hover_data = hover_data_cols,
                    color_continuous_scale = px.colors.sequential.Purpor,
                    animation_frame='Report Year',
                    range_color=(0, 100)
               )

fig.update_layout(coloraxis_colorbar_x=-0.15,height=600,width=500)

st.plotly_chart(fig, use_container_width=True,height=600,width=500)

st.subheader('Evaluation per Year')
st.write('The different categories have coorelations between them. In the following plot, you can select a year, and see how they are related to the overall index score and according to the region.')

year = st.slider(label='Select the year',min_value=1971,max_value=2023,step=1,value=1971)

data_fil = data[data['Report Year'] == year]

##fig = px.parallel_coordinates(data_fil, color="WBL INDEX",
##                              dimensions=['MOBILITY', 
#                                         'MARRIAGE','PARENTHOOD','ENTREPRENEURSHIP', 'WORKPLACE',
#                                          'ASSETS','PENSION','PAY'],
#                              color_continuous_scale=px.colors.sequential.thermal,
#                              title = f'WBL Index Based on the Categories for the Year {year}')

##st.plotly_chart(fig, use_container_width=True)

st.write('In the following plot, you can choose one or more regions and see how their categories score behave and relate')

fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = data_fil['dummy'],
                   colorscale = 'Jet'),
        dimensions = list([
            dict(range = [0,100],
                 label = 'MOBILITY', values = data_fil['MOBILITY']),
            dict(range = [0,100],
                 label = 'WORKPLACE', values = data_fil['WORKPLACE']),
            dict(range = [0,100],
                 label = 'PAY', values = data_fil['PAY']),
            dict(range = [0,100],
                 label = 'MARRIAGE', values = data_fil['MARRIAGE']),
            dict(range = [0,100],
                 label = 'PARENTHOOD', values = data_fil['PARENTHOOD']),
            dict(range = [0,100],
                 label = 'ENTREPRENEURSHIP', values = data_fil['ENTREPRENEURSHIP']),
            dict(range = [0,100],
                 label = 'ASSETS', values = data_fil['ASSETS']),
            dict(range = [0,100],
                 label = 'PENSION', values = data_fil['PENSION']),
            dict(range=[0,data_fil['dummy'].max()],
                       tickvals = dfg['dummy'], ticktext = dfg['Region'],
                       label='REGION', values=data_fil['dummy']),
            dict(range = [0,100],
                 label = 'WBL INDEX', values = data_fil['WBL INDEX']),
            ]
        )
    )
)

fig.update_layout(height=500,width=500,
                  title={
        'text': f"WBL Index Based on the Categories for the Year {year} According to the Region",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},)

st.plotly_chart(fig, use_container_width=True,height=600,width=500)




dict_cat = {'MOBILITY':[8,9,10,11],
            'WORKPLACE':[13,14,15,16], 
            'PAY':[18,19,20,21,],
            'MARRIAGE':[23,24,25,26,27],
            'PARENTHOOD':[29,31,32,34,38],
            'ENTREPRENEURSHIP':[40,41,42,43],
            'ASSETS':[45,46,47,48,49],
            'PENSION':[51,52,53,54]}

st.subheader('Filter by category')
st.write('There are many questions that were used to calculate the WBL Index. In the following visualization, it is possible to filter by category and select a question from it. With the time bar in the bottom, you can visualize how the world has evolved in that particular question.')

option1 = st.selectbox(
    'Which category would you like to filter?',
    dict_cat.keys())

ques_cols = data.iloc[:, dict_cat[option1]].columns

option = st.selectbox(
    f'Which specific question of the {option1} category would you like to visualize?',
    ques_cols)

hover_data_cols_df = option

fig = px.choropleth(data,
                    locations="Economy",
                    locationmode='country names',
                    color=hover_data_cols_df, 
                    hover_name = hover_data_cols_df,
                    hover_data = [hover_data_cols_df],
                    color_discrete_map={
                        "No":  px.colors.qualitative.Set2[1],
                        "Yes": px.colors.qualitative.Set2[0]},
                    animation_frame='Report Year'
               )
#fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
st.plotly_chart(fig, use_container_width=True)