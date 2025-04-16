import plotly.express as px
import streamlit as st
import pandas as pd
import preprocesser,helper
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np
helper import get_country_athlete_count
from helper import get_medal_counts


from * import preprocesser
st.sidebar.title('Olympics Analysis')
st.sidebar.image('./images/olympics 1.png')
user_menu = st.sidebar.radio(
    'Select An Option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete Wise Analysis')
)
df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')
df = preprocesser.preprocess(df,df_region)

if user_menu=='Medal Tally':
    st.sidebar.title('Medal Tally')
    year,country = helper.get_country_year(df)
    selectec_year =st.sidebar.selectbox('Select Year',year)
    selected_country =st.sidebar.selectbox('Select Country',country)
    medal_tally = helper.fetch_medal_tally(df,selectec_year,selected_country)
    if selectec_year=='Overall' and selected_country =='Overall':
        st.title('Overall Tally')
    if selectec_year!='Overall' and selected_country =='Overall':
        st.title(f'Overall Tally In Year {selectec_year}')
    if selectec_year=='Overall' and selected_country !='Overall':
        st.title(f'Overall Tally Of Country {selected_country}')
    if selectec_year !='Overall' and selected_country !='Overall':
        st.title(f'Overall Tally Of {selected_country} In Year {selectec_year}')
    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title('Top Statistics')
    athletes=df.Name.unique().shape[0]
    country=df.region.unique().shape[0]
    events=df.Event.unique().shape[0]
    sports=df.Sport.unique().shape[0]
    cities=df.City.unique().shape[0]
    editions=df.Year.unique().shape[0]-1
    
    col1,col2,col3,=st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)
    col1,col2,col3,=st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(country)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    
    st.title('Participating Nations Over The Year')
    nations_over_time_df = helper.data_over_time(df,'region','countries')
    fig = px.line(nations_over_time_df,x='year',y='countries')
    st.plotly_chart(fig)
    st.title('Events Over The Year')
    nations_over_time_df = helper.data_over_time(df,'Event','events')
    fig = px.line(nations_over_time_df,x='year',y='events')
    st.plotly_chart(fig)
    st.title('Athlet Over The Year')
    nations_over_time_df = helper.data_over_time(df,'Name','athletes')
    fig = px.line(nations_over_time_df,x='year',y='athletes')
    st.plotly_chart(fig)
    st.title('No Of Events Overtime Of Sports')
    fig,ax = plt.subplots(figsize=(25,20))
    x =df.drop_duplicates(['Year','Sport','Event'])
    ax =sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int),annot=True)
    st.pyplot(fig)
    st.title('Most Successful Players')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport =  st.selectbox('Select A Sport',sport_list)
    st.table(helper.most_successful(df,selected_sport))
    
if user_menu == 'Country-Wise Analysis':
    year,country = helper.get_country_year(df)
    country = country[1:]
    selected_country = st.sidebar.selectbox('Select Country',country)
    st.title('Medal Analysis Of {}'.format(selected_country))
    country_df = helper.year_wise_medal_tally(df,selected_country)
    fig = px.line(country_df,x='Year',y=['Gold','Silver','Bronze'],color_discrete_sequence=['Gold', 'Silver','#cd7f32'])
    st.plotly_chart(fig)
    try :
        st.title('{} Sport Heatmap'.format(selected_country))
        sport_country_df = helper.country_event_heatmap(df,selected_country)
        fig,ax = plt.subplots(figsize=(25,20))
        sns.heatmap(sport_country_df,annot=True)
        st.pyplot(fig)
    except:
        st.text("{} Not Win Any Game So Heatmap Can't Be Show".format(selected_country))
    st.title('Most Successful Player In {}'.format(selected_country))
    top_temp_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top_temp_df)






elif selected == "Country vs Country Analysis":
    st.title("🏳️‍🌈 Country vs Country Comparison")

    countries = df['region'].dropna().unique().tolist()
    countries.sort()

    col1, col2 = st.columns(2)
    with col1:
        country1 = st.selectbox("Select First Country", countries)
    with col2:
        country2 = st.selectbox("Select Second Country", countries)

    if country1 == country2:
        st.warning("Please select two different countries.")
    else:
        # Total Athletes
        col3, col4 = st.columns(2)
        with col3:
            count1 = get_country_athlete_count(df, country1)
            st.metric(label=f"{country1} - Total Athletes", value=count1)
        with col4:
            count2 = get_country_athlete_count(df, country2)
            st.metric(label=f"{country2} - Total Athletes", value=count2)

        # Medal Comparison
        st.subheader("🥇 Medal Comparison")
        medal_df = compare_countries_medal_count(df, country1, country2)
        st.dataframe(medal_df)

        fig1, ax1 = plt.subplots()
        medal_df.plot(kind='bar', ax=ax1, color=['#1f77b4', '#ff7f0e'])
        ax1.set_ylabel("Count")
        ax1.set_title("Medal Count")
        st.pyplot(fig1)

        # Year-wise Medal Trend
        st.subheader("📈 Year-wise Medal Trend")
        trend1 = get_country_medal_trend(df, country1)
        trend2 = get_country_medal_trend(df, country2)

        trend_df = pd.DataFrame({country1: trend1, country2: trend2}).fillna(0)
        st.line_chart(trend_df)

        # Sports Participation
        st.subheader("🏋️ Sports Participation (Top 10)")
        sport1 = get_country_sport_participation(df, country1).head(10)
        sport2 = get_country_sport_participation(df, country2).head(10)

        col5, col6 = st.columns(2)
        with col5:
            st.markdown(f"### {country1}")
            fig2, ax2 = plt.subplots()
            sns.barplot(y=sport1.index, x=sport1.values, palette='Blues_d', ax=ax2)
            ax2.set_xlabel("Count")
            st.pyplot(fig2)

        with col6:
            st.markdown(f"### {country2}")
            fig3, ax3 = plt.subplots()
            sns.barplot(y=sport2.index, x=sport2.values, palette='Oranges_d', ax=ax3)
            ax3.set_xlabel("Count")
            st.pyplot(fig3)

        # Top 5 Medal-Winning Sports
        st.subheader("🏆 Top 5 Sports by Medal Wins")
        top_sport1 = get_country_top_sports(df, country1)
        top_sport2 = get_country_top_sports(df, country2)

        col7, col8 = st.columns(2)
        with col7:
            st.markdown(f"### {country1}")
            st.bar_chart(top_sport1)

        with col8:
            st.markdown(f"### {country2}")
            st.bar_chart(top_sport2)








if user_menu == 'Athlete Wise Analysis':
    
    st.title('Distrubution Of Age')
    player_df =df.drop_duplicates(['Name','region'])
    x1 =player_df['Age'].dropna()
    x2= player_df[player_df['Medal']=='Gold']['Age'].dropna()
    x3= player_df[player_df['Medal']=='Silver']['Age'].dropna()
    x4= player_df[player_df['Medal']=='Bronze']['Age'].dropna()
    fig =ff.create_distplot([x1,x2,x3,x4],['Age Distribution','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.plotly_chart(fig)
    
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                    'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                    'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                    'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                    'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                    'Tennis', 'Golf', 'Softball', 'Archery',
                    'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                    'Rhythmic Gymnastics', 'Rugby Sevens',
                    'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Won Gold Medal')
    st.plotly_chart(fig)
    
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Won Silver Medal')
    st.plotly_chart(fig)
    
    x = []
    name = []
    for sport in famous_sports:
        temp_df = player_df[player_df['Sport'] == sport]
        temp_df=temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna()
        if temp_df.shape[0] != 0:
            x.append(temp_df)
            name.append(sport)

    fig =ff.create_distplot(x,name,show_hist=False,show_rug =False)
    fig.update_layout(autosize=False,width=880,height=600)
    st.header('Distribution Of Age With Respect To Sport Who Bronze Medal')
    st.plotly_chart(fig)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport =  st.selectbox('Select A Sport',sport_list)
    temp_df = helper.create_v_height(df,selected_sport)
    fig,ax = plt.subplots(figsize=(20,20))
    ax =sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=350)
    st.pyplot(fig)

    st.title('Men Vs Women Participation')
    final =helper.men_vs_women(df)
    fig = px.line(final,x='Year',y=['Female','Male'])
    fig.update_layout(autosize=False,width=880,height=600)
    st.plotly_chart(fig)
    
    



# from helper import get_country_athlete_count
# from helper import get_medal_counts

# # Country vs Country Analysis
# st.title("Country vs Country Analysis")

# # Load and preprocess data
# df = pd.read_csv('athlete_events.csv')
# region_df = pd.read_csv('noc_regions.csv')
# df = df.merge(region_df, on='NOC', how='left')

# # Drop rows with missing 'region' or 'Medal'
# df = df.dropna(subset=['region', 'Medal'])

# # Get list of unique countries
# countries = df['region'].dropna().unique()
# countries.sort()

# # Country selection
# col1, col2 = st.columns(2)
# with col1:
#     country1 = st.selectbox("Select First Country", countries)
# with col2:
#     country2 = st.selectbox("Select Second Country", countries)

# if country1 == country2:
#     st.warning("Please select two different countries.")
# else:
#     # Get medal counts
#     medals_c1 = get_medal_counts(df, country1)
#     medals_c2 = get_medal_counts(df, country2)

#     # Create DataFrame for visualization
#     medal_df = pd.DataFrame({
#         'Medal': ['Gold', 'Silver', 'Bronze'],
#         country1: [medals_c1['Gold'], medals_c1['Silver'], medals_c1['Bronze']],
#         country2: [medals_c2['Gold'], medals_c2['Silver'], medals_c2['Bronze']]
#     })

#     # Melt the DataFrame for seaborn
#     medal_df_melted = medal_df.melt(id_vars='Medal', var_name='Country', value_name='Count')

#     # Plotting
#     fig, ax = plt.subplots(figsize=(10, 6))
#     sns.barplot(data=medal_df_melted, x='Medal', y='Count', hue='Country', ax=ax)
#     ax.set_title(f'Medal Comparison: {country1} vs {country2}')
#     st.pyplot(fig)





# if user_menu == 'Country vs Country Analysis':
#     st.title("Detailed Country vs Country Analysis")

#     countries = df['region'].dropna().unique().tolist()
#     countries.sort()

#     col1, col2 = st.columns(2)
#     with col1:
#         country1 = st.selectbox("Select First Country", countries)
#     with col2:
#         country2 = st.selectbox("Select Second Country", countries)

#     if country1 == country2:
#         st.warning("Please select two different countries.")
#     else:
#         col3, col4 = st.columns(2)

#         with col3:
#             st.subheader(f"Athletes from {country1}")
#             count1 = get_country_athlete_count(df, country1)
#             st.metric(label="Total Athletes", value=count1)

#         with col4:
#             st.subheader(f"Athletes from {country2}")
#             count2 = get_country_athlete_count(df, country2)
#             st.metric(label="Total Athletes", value=count2)

#         # 🥇 Medal Count Comparison
#         st.subheader("Medal Count Comparison")
#         medal_df = compare_countries_medal_count(df, country1, country2)
#         st.dataframe(medal_df)
#         medal_df.plot(kind='bar')
#         st.pyplot(plt)

#         # 📊 Year-wise Medal Trend
#         st.subheader("Medal Trend Over Years")
#         trend1 = get_country_medal_trend(df, country1)
#         trend2 = get_country_medal_trend(df, country2)

#         medal_trend_df = pd.DataFrame({country1: trend1, country2: trend2})
#         st.line_chart(medal_trend_df.fillna(0))

#         # 🏋️ Sport Participation
#         st.subheader("Sports Participation Count")
#         sp1 = get_country_sport_participation(df, country1).head(10)
#         sp2 = get_country_sport_participation(df, country2).head(10)

#         fig, ax = plt.subplots(figsize=(12, 5))
#         sns.barplot(x=sp1.index, y=sp1.values, color='blue', label=country1)
#         sns.barplot(x=sp2.index, y=sp2.values, color='orange', label=country2)
#         plt.legend()
#         plt.xticks(rotation=45)
#         st.pyplot(fig)

#         # 🔝 Top Performing Sports
#         st.subheader("Top 5 Sports by Medal Wins")
#         top1 = get_country_top_sports(df, country1)
#         top2 = get_country_top_sports(df, country2)

#         col5, col6 = st.columns(2)
#         with col5:
#             st.markdown(f"**{country1}**")
#             st.bar_chart(top1)
#         with col6:
#             st.markdown(f"**{country2}**")
#             st.bar_chart(top2)
