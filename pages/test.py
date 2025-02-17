import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from funzioni import *
from dbconnector import *

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

try:
    tab1, tab2, tab3 = st.tabs(["Lezioni", "Valutazioni", "ITS's Heroes"])
    # Data ETL
    data1 = get_calendar1()
    data = get_calendar()
    grades = get_grades()
    absences = get_absences()
        
    with tab1:
        tab1.subheader('')
        # Display the chart in Streamlit
        tab1.title('Distribuzione Ore Lezioni')
        # Create a radio button to select the data source
        selected_data = tab1.radio("Seleziona Anno", ("1° Anno", "2° Anno"),horizontal=True)

        # Choose the appropriate data based on the selection
        if selected_data == "1° Anno":
            hours_by_docente = data1.groupby('Docente')['ore'].sum()
        else:
            hours_by_docente = data.groupby('Docente')['Ore'].sum()

        # Calculate total hours
        total_hours = hours_by_docente.sum()

        # Sorting the hours
        hours_by_docente = hours_by_docente.sort_values(ascending=False)

        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=hours_by_docente.index,
            values=hours_by_docente.values,
            hole=0.5  # This creates a donut chart
        )])

        # Update layout to add total hours in center
        fig.update_layout(
            annotations=[{
                'text': f'Total Hours:\n{total_hours}',
                'x': 0.5,
                'y': 0.5,
                'font_size': 22,
                'showarrow': False
            }],
            width=1200,
            height=600
        )
        
        tab1.plotly_chart(fig)
        tab1.divider()

        # Create a bar plot with color-coding and legend
        # Create the bar chart
        fig_bar = go.Figure(data=[go.Bar(
            x=hours_by_docente.index,
            y=hours_by_docente.values,
            text=hours_by_docente.values,  # Show the values on top of bars
            textposition='outside',  # Automatically position the text
            name='Ore per Docente'  # Legend name
        )])

        # Update layout for better readability
        fig_bar.update_layout(
            font_size=18,
            xaxis_title='Docenti',
            yaxis_title='Ore',
            width=1200,
            height=600,
            xaxis={'tickangle': 45},  # Rotate x-axis labels for better readability
            showlegend=False,  # Show the legend
            margin=dict(t=50, b=50, l=50, r=50),  # Increase margins
        )
        # Adjust the y-axis range to ensure labels are not cut off
        max_value = hours_by_docente.max()
        fig_bar.update_yaxes(range=[0, max_value + 10])  # Add some space above the highest bar

        tab1.title('Ore per Docente')
        # Display the bar chart in Streamlit
        tab1.plotly_chart(fig_bar)
        tab1.divider()

    
    with tab2:
        tab2.subheader('')
        # Display mean grades
        mean_grades_students = grades.T.mean().sort_values(ascending=False).reset_index()
        mean_grades_students.columns = ['Studente', 'Media Voti']  # Rename columns

        mean_grades_teachers = grades.mean().sort_values(ascending=False).dropna().reset_index()
        mean_grades_teachers.columns = ['Docente', 'Media Voti']  # Rename columns

        percentuale_assenze = absences['% presenza su ore svolte'].sort_values(ascending=False).reset_index()
        percentuale_assenze.columns = ['Studente', '% Assenze']  # Rename columns

        # Create visualizations using the new function
        col1, col2 = tab2.columns([3,1])
        with col1:
            st.header('Media Voti Studenti')
            fig_students = create_bar_chart(mean_grades_students, 'Studente', 'Media Voti', 'Media Voti per Studente')
            st.plotly_chart(fig_students, use_container_width=True)
        with col2:
            st.header('')
            st.dataframe(mean_grades_students, width=500, height=600)
            
        st.divider()
        
        col3, col4 = tab2.columns([1,3])
        with col3:
            st.header('')
            st.dataframe(mean_grades_teachers, width=500)
        with col4:
            st.header('Media Voti Docenti')
            fig_teachers = create_bar_chart(mean_grades_teachers, 'Docente', 'Media Voti', 'Media Voti per Docente')
            st.plotly_chart(fig_teachers, use_container_width=True)
            
        st.divider()
        
        col5, col6 = tab2.columns([3,1])
        with col5:
            st.header('Percentuale Assenze')
            fig_absences = create_bar_chart(
                percentuale_assenze, 
                'Studente', 
                '% Assenze', 
                'Percentuale Assenze',
                ref_line=0.8  # Add reference line at 80%
            )
            st.plotly_chart(fig_absences, use_container_width=True)
        with col6:
            st.header('')
            st.dataframe(percentuale_assenze, width=500)
        
    
        tab2.divider()
        
        st.title("Student Grade Report Card")
        # Create a dropdown selector for students and teachers
        docenti = grades.columns
        studenti = grades.index
        # Create a container inside tab2 for the dropdown selectors and result 
        # Create two columns for side-by-side dropdown selectors
        col1, col2 = st.columns(2)
        
        # Display the student dropdown in the first column
        with col1:
            select_studente = st.selectbox("Select a Student:", studenti)
        # Display the teacher dropdown in the second column
        with col2:
            select_docente = st.selectbox("Select a Teacher:", docenti)
         
        # Get the grade for the selected student and teacher
        voto = grades.loc[select_studente, select_docente]
        st.write(f"Il voto di {select_studente} con {select_docente} è : {voto}! Way To GO!")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.subheader("Dettaglio Voti")
            student_grades = grades.loc[select_studente]
            st.dataframe(
                student_grades.reset_index().rename(columns={
                    'index': 'Docente',
                    select_studente: 'Voto'
                }),
                width=400,
                height=500,
            )
        with col2:
            st.subheader("Grafico Voti")
            st.plotly_chart(create_student_grade_chart(student_grades), use_container_width=True, height=700)
            
        # Display the report card using Markdown
        st.markdown(create_report_card(grades, select_studente), unsafe_allow_html=True)

        st.divider()
    
    with tab3:
        tab3.header('ITS\'s Heroes')
        col1, col2, col3 = st.columns(3)
        # metrica media peggiore
        nome_worst = str(list(grades.T.mean().sort_values().reset_index().iloc[0])[0])
        worst_mean = str(list(grades.T.mean().sort_values().reset_index().iloc[0])[1])
        col1.metric("Media Inferiore", f"{nome_worst}", '-'+ worst_mean ,border=True )
        # metrica assense
        most_absent = str(list(absences['% presenza su ore svolte'].sort_values().reset_index().iloc[0])[0])
        most_absent_percent = str(list(absences['% presenza su ore svolte'].sort_values().reset_index().iloc[0])[1])
        col3.metric("Assenze Top", most_absent,'-' + most_absent_percent,border=True)
        # metrica rapporto assenze più alte/media voti migliore
        # Join the grades and absences DataFrames
        absences_grades = grades.join(absences, on='Cognome Nome')
        # Calculate the mean of grades
        absences_grades['Media'] = absences_grades.mean(axis=1)
        # Ensure the '% presenza su ore svolte' is numeric
        absences_grades['% presenza su ore svolte'] = pd.to_numeric(absences_grades['% presenza su ore svolte'], errors='coerce')
        # Calculate performance
        absences_grades['performance'] = absences_grades['Media'] / absences_grades['% presenza su ore svolte']
        # Get the best performer
        best_performer = absences_grades['performance'].idxmax()  # Get the index of the max performance
        best_performance = absences_grades['performance'].max()  # Get the max performance value
        # Display the metrics
        col2.metric("Media/Assenza King", f"{best_performer}", f"{best_performance:.2f}", border=True)
        
        col4, col5, col6 = st.columns(3)
        # metrica media peggiore
        nome_best = str(list(grades.T.mean().sort_values(ascending=False).reset_index().iloc[0])[0])
        best_mean = str(list(grades.T.mean().sort_values(ascending=False).reset_index().iloc[0])[1])
        col4.metric("Media Migliore", f"{nome_best}", best_mean,border=True )
        # metrica assense
        least_absent = str(list(absences['% presenza su ore svolte'].sort_values(ascending=False).reset_index().iloc[0])[0])
        least_absent_percent = str(list(absences['% presenza su ore svolte'].sort_values(ascending=False).reset_index().iloc[0])[1])
        col6.metric("Presenze Top", least_absent,least_absent_percent,border=True)
        # metrica rapporto assenze più alte/media voti migliore
        # Join the grades and absences DataFrames
        absences_grades = grades.join(absences, on='Cognome Nome')
        # Calculate the mean of grades
        absences_grades['Media'] = absences_grades.mean(axis=1)
        # Ensure the '% presenza su ore svolte' is numeric
        absences_grades['% presenza su ore svolte'] = pd.to_numeric(absences_grades['% presenza su ore svolte'], errors='coerce')
        # Calculate performance
        absences_grades['performance'] = absences_grades['Media'] / absences_grades['% presenza su ore svolte']
        # Get the best performer
        worst_performer = absences_grades['performance'].idxmin()  # Get the index of the min performance
        worst_performance = absences_grades['performance'].min()  # Get the min performance value
        # Display the metrics
        col5.metric("Media/Assenza Jullar", f"{worst_performer}", '-' + str(worst_performance), border=True)

except Exception as e:
    tab1.error(f"An error occurred: {e}")
    tab2.error(f"An error occurred: {e}")
    tab3.error(f"An error occurred: {e}")


