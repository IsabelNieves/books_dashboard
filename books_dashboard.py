import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.colors
import numpy as np
import textwrap

#Define the set-up for background 
def set_background_color(color):
    """
    Function to set the background color of the application.
    """
    # Generate custom CSS code
    css_code = f"""
    <style>
    .stApp {{
        background-color: {color};
    }}
    </style>
    """
    # Render the CSS code
    st.markdown(css_code, unsafe_allow_html=True)

# Configure page layout and change background color
st.set_page_config(layout="wide", page_title="Books_dashboard")

# set the coulor 
set_background_color('#ede4bb')  # Change the value to your desired color

# Add the content you want for the first container (e.g., title)
st.markdown("<h1 style='text-align: center; color: #873e23;'>Let's talk about Books Ratings </h1>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1,3])


# Add content to the first column.
with col1:
    st.markdown(
    """
    <style>
    div.image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    div.image-container img {
        max-width: 100%;
        max-height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("<div class='image-container'>", unsafe_allow_html=True)
    st.image("https://amboy.lib.il.us/wp-content/uploads/2022/06/summer-reading.jpg", use_column_width=False, width=500)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    

# Add content to the second column
with col2:

    # Add the content you want for the first container (e.g., title)
    st.markdown("<h1 style='text-align: center; color: #873e23;'>Let's talk about Books Ratings </h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: #873e23; font-size: 26px;'>Have you ever lost a lot of time thinking about the next book you will read? Save time. Here we will talk about the rating of readers around the world.</h1>", unsafe_allow_html=True)



#read the dataset
df=pd.read_csv("./books_raiting.csv")

# Create two columns for the first two containers
col3, col4 = st.columns(2)

# container in column 3
with col3:
    st.markdown("<div style='width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        div.st-ai, div.st-cu {
            margin-top: -30px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Calculate total users per country
    users_per_country = df.groupby("Country_Code")["user_id"].count().reset_index()
    users_per_country.rename(columns={"user_id": "Total_Users"}, inplace=True)

    # Create a new dataset with information for the chart
    new_df = users_per_country[["Country_Code", "Total_Users"]].merge(df[["Country_Code", "country"]], on="Country_Code").drop_duplicates()

    # Display the new dataset
    print(new_df.head())

    # Define the base color
    base_color = '#edc9c0'  # For example, red

    # Define color degradations
    color_degradations = ['#edc9c0', '#c34b2c']  # For example, lighter shades of red

    # Combine the base color and color degradations
    colors = [base_color] + color_degradations

    # Create the custom color scale
    custom_colors = plotly.colors.make_colorscale(colors)

    # Generate the choropleth map with the custom color scale
    fig = px.choropleth(new_df,
                    locations="Country_Code",
                    color="Total_Users",
                    hover_name="country",
                    color_continuous_scale=custom_colors,  # Use the custom color scale
                    projection="natural earth")

    fig.update_layout(
    title='Readers per country',
    title_font=dict(color='#873e23', family='Arial, bold', size=30),
    title_x=0.0,
    plot_bgcolor='#ede4bb',
    paper_bgcolor='#ede4bb',
    autosize=True
)

    fig.update_coloraxes(colorbar=dict(  
    tickfont=dict(color='#873e23')  # Color of the tick labels
))

    # Show the fig
    st.plotly_chart(fig)
  

# Second container in column 2
with col4:
    st.markdown("<div style='width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        div.st-ai, div.st-cu {
            margin-top: -30px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
  # count the total per generation
    age = df['Generation'].value_counts().to_frame().reset_index()
    age.columns = ['Generation', 'count']
    age['count'] = age['count'].astype(int)


    colors = ["#377576", "#59a6ba", "#c34b2c", "#c7a93b"]

# Create the pie plot using  Plotly Express
    fig = px.pie(age, values='count', names='Generation', hole=0.3,
             labels={'Generation': 'Age Category', 'Count': 'Number Of People'},
             color_discrete_sequence=colors)
   

    fig.update_traces(textfont_size=18)
    
    

    fig.update_layout(
    yaxis=dict(autorange="reversed", showgrid=False),
    xaxis=dict(showgrid=False),
    title='Generation Distribution',
    title_font=dict(color='#873e23', family='Arial, bold', size=30),
    title_x=0.0,
    plot_bgcolor='#ede4bb',
    paper_bgcolor='#ede4bb',
    autosize=True,
    legend_font=dict(size=20, color='#873e23'),
    legend_title_font=dict(size=18, color='#873e23')
    
) 

# Show the graph
    st.plotly_chart(fig)

# Third container occupying the entire screen

def load_data():
    df_books_sum = df.groupby(by=['title'])['rating'].sum().to_frame().reset_index().rename(columns={'title': 'title', 'rating': 'total_rating'})
    df_books_sum = df_books_sum.sort_values(by='total_rating', ascending=False)
    
    df_books_count = df.groupby(by=['title'])['rating'].count().to_frame().reset_index().rename(columns={'title': 'title', 'rating': 'count_rating'})
    df_books_count = df_books_count.sort_values(by='count_rating', ascending=False)
    
    df_books_merge = pd.merge(df_books_sum, df_books_count, on='title')[0:50]
    df_books_merge['rate'] = df_books_merge['total_rating'] / df_books_merge['count_rating']
    df_books_merge = df_books_merge.sort_values(by='rate', ascending=False)
    
    df_books_merge1 = df_books_merge[df_books_merge['count_rating'] > 75]
    df_books_merge1 = df_books_merge1.sort_values(by='rate', ascending=False)[0:10]
    
    # Add column "wrapped_title"
    df_books_merge1['wrapped_title'] = df_books_merge1['title'].apply(wrap_title)
    return df_books_merge1

def wrap_title(title):
    wrapped_title = textwrap.wrap(title, width=20)
    return '<br>'.join(wrapped_title)

def plot_bar_chart(df_books_merge1):
    colors = ["#377576", "#59a6ba", "#c34b2c", "#c7a93b", "#99d0c0", "#f3f3f4", "#ca9065", "#b5cebc", "#c5a094", "#63bcaf"]
    
    fig = go.Figure(go.Bar(
        x=df_books_merge1['wrapped_title'],
        y=df_books_merge1['rate'],
        marker={'color': colors, 'colorscale': 'cividis'},
        textposition="outside",
    ))
    
    fig.update_layout(
        yaxis=dict(showgrid=False,tickfont=dict(color='#873e23'),range=[8.2, 9.3] ),
        xaxis=dict(showgrid=False, tickangle=45, tickfont=dict(size=16,color="#873e23")),
        title_text='Best Books Ratings',
        xaxis_title="Book",
        xaxis_title_font=dict(color='#873e23',family='Arial, bold',size=16),
        yaxis_title="Avg Rating",
        yaxis_title_font=dict(color='#873e23',family='Arial, bold',size=16),
        title_font=dict(color='#873e23', family='Arial, bold', size=30),
        title_x=0.0,
        plot_bgcolor="#ede4bb",
        width=1400,
        height=600,
        paper_bgcolor='#ede4bb'
    )
    
    return fig

# Load the data
df_books_merge1 = load_data()

# Creat3 the plot
fig1 = plot_bar_chart(df_books_merge1)

# Show the plot
st.plotly_chart(fig1)



# Create two more columns for the last two containers
col5, col6 = st.columns(2)

# 
with col5:
    st.markdown(
        "<div style='width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>",
        unsafe_allow_html=True
    )
    # Add the content you want for the fourth container
    df_book_name = df.title.value_counts().reset_index()[:10]
    df_book_name.columns = ['title', 'count']
    

    fig = go.Figure(go.Bar(
    x=df_book_name['count'],
    y=df_book_name['title'],
    orientation='h',
    marker={'color': "#c7a93b"},
    textposition="outside",
))

    fig.update_layout(
    yaxis=dict(autorange="reversed", showgrid=False,tickfont=dict(color='#873e23')),
    xaxis=dict(showgrid=False,tickfont=dict(color='#873e23')),
    title='Most voted books (TOP 10)',
    title_font=dict(color='#873e23', family='Arial, bold', size=30),
    title_x=0.0,
    plot_bgcolor='#ede4bb',
    paper_bgcolor='#ede4bb',
    autosize=True,

)

# Show the plot
    st.plotly_chart(fig)




# container in column 6
with col6:
    st.markdown(
        "<div style='width: 100%; height: 100%; display: flex; flex-direction: column; justify-content: center; align-items: center;'>",
        unsafe_allow_html=True
    )
    # Add the content you want for the fifth container
    df_author_name = df['author'].value_counts()[:10].reset_index()
    df_author_name.columns = ['author', 'count']
    colors = ["#377576", "#59a6ba", "#c34b2c", "#c7a93b", "#99d0c0", "#f3f3f4", "#ca9065", "#b5cebc", "#c5a094", "#63bcaf"]

    fig = go.Figure(go.Bar(
    x=df_author_name['author'],
    y=df_author_name['count'],
    marker={'color': "#63bcaf",
            'colorscale': 'cividis'},
    textposition="outside",
))


    fig.update_layout(
    yaxis=dict(showgrid=False,tickfont=dict(color='#873e23')),
    xaxis=dict(showgrid=False,tickfont=dict(color='#873e23')),
    title_text='TOP 10 Reviewed Book Author',
    xaxis_title="Author", 
    xaxis_title_font=dict(color='#873e23',family='Arial, bold',size=16),
    yaxis_title="Count",
    yaxis_title_font=dict(color='#873e23',family='Arial, bold',size=12),
    title_font=dict(color='#873e23',  family='Arial, bold',size=30),
    title_x=0.0,
    plot_bgcolor="#ede4bb",
    paper_bgcolor='#ede4bb', 
    autosize=True,

)
    st.plotly_chart(fig)



