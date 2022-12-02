import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

st.title("********* Udemy Courses *********")

@st.cache
def load_data():
    data = pd.read_csv('udemy_course_info.csv')
    return data

def main():
    data = load_data()
    st.header("**** List of Top Courses Curated for you ****")

    category = st.sidebar.selectbox("Course Category(s)", data['category'].unique())
    if category:
        data = data[data.category.isin([category])]

    subcategory = st.sidebar.selectbox("Course Subcategory(s)", data['subcategory'].unique())
    if subcategory:
        data = data[data.subcategory.isin([subcategory])]

    topics = st.sidebar.selectbox("Course Topic(s)", data['topic'].unique())
    if topics:
        data = data[data.topic.isin([topics])]

    language = st.sidebar.multiselect("Course Language(s)",data['language'].unique())
    if language:
        data = data[data.language.isin(language)]

    paid = st.sidebar.multiselect("Paid Course",data['is_paid'].unique())
    if paid:
        data = data[data.is_paid.isin(paid)]

    filter_scatter = st.sidebar.radio(
        "Show Linear Regression",
        ["No", "Yes"]
    )
    data_filter_scatter = data

    filter_bar_chart = st.sidebar.radio(
        "Top Courses On The Basis Of  👇",
        ["avg_rating", "num_reviews", "num_subscribers"]
    )

    if filter_bar_chart:
        column_name = filter_bar_chart
        data = data.sort_values(by=[column_name], ascending=False)

    data1=data
    total_rows = 0
    if data.size >= 10:
        data = data.head(10)
        total_rows = 10
    else:
        total_rows = data.size

    filter_show_data = st.sidebar.radio(
        "Display Data In Table",
        ["No", "Yes"]
    )

    st.header("*********************************************")
    st.subheader("** Bar Chart for Top Courses **")
    bar_chart_data = pd.DataFrame(
        data,
    columns=["instructor_name","title","avg_rating", "num_reviews", "num_subscribers"])
    st.bar_chart(bar_chart_data, x="title", y=column_name)

    val=data.groupby(['is_paid']).size()
    st.header("*********************************************")
    st.subheader("** Paid versus Free Courses **")
    if len(val) > 1:
        fig, ax = plt.subplots()
        plt.figure(figsize=(2, 2))
        ax.pie(val,
                labels=['Free', 'Paid'],
                autopct='%1.1f%%',
                startangle=90, colors=['green', 'red'],
                textprops={'size': 8},
                wedgeprops={"edgecolor": "white",
                            'linewidth': 1,
                            'antialiased': True})
        ax.plot(val)
        st.pyplot(fig)
    else:
        fig, ax = plt.subplots()
        plt.figure(figsize=(2, 2))
        if bool(data['is_paid'].values[0]) == True:
            ax.pie(val,
                    labels=['All Selected Courses are Paid'],
                    autopct='%1.1f%%',
                    startangle=90, colors=['red'],
                    textprops={'size': 8},
                    wedgeprops={"edgecolor": "white",
                                'linewidth': 1,
                                'antialiased': True})
        else:
            ax.pie(val,
                    labels=['All Selected Courses are Free'],
                    autopct='%1.1f%%',
                    startangle=90, colors=['green'],
                    textprops={'size': 8},
                    wedgeprops={"edgecolor": "white",
                                'linewidth': 1,
                                'antialiased': True})
        ax.plot(val)
        st.pyplot(fig)

    x1 = "http://udemy.com"
    count = 0

    st.header("*********************************************")
    st.subheader("** Details of Top Courses **")
    for x,y,z,a in zip(data.course_url, data.title, data.instructor_name, data.instructor_url):
        count = count + 1
        x = x1 + x
        a = x1 + a
        st.markdown(str(count) + ") Course Title : " + y +
                     " [Show Course on Udemy](%s)." % x +
                    " This course is created by " + z +
                   " [Show Instructor's Profile on Udemy](%s)" % a)

    if filter_scatter == "Yes":
        x=data_filter_scatter['num_subscribers']
        y=data_filter_scatter['avg_rating']
        slope, intercept, r, p, std_err = stats.linregress(x,y)
        val = slope * x + intercept
        st.header("*********************************************")
        st.subheader("** Linear Regression Chart **")
        st.subheader("Linear Regression Relation = " + str(r))
        def myfunc(x):
            return slope * x + intercept
        mymodel = list(map(myfunc, x))
        fig, ax = plt.subplots()
        plt.xlabel("Number of Subscibers")
        plt.ylabel("Average Rating")
        ax.scatter(x,y,color="green")
        ax.plot(x, mymodel)
        st.pyplot(fig)

    #if st.checkbox('Show Data'):
    if filter_show_data == "Yes":
        st.header("*********************************************")
        st.subheader("** Data Table **")
        st.dataframe(data)

if __name__ == '__main__':
    main()
