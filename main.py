import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from funzioni import *
from dbconnector import *

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

try:
    tab1, tab2, tab3, tab4 = st.tabs(["Lezioni", "Valutazioni", "Presenze", "ITS's Heroes"])
    
    # Data Loading
    data1 = get_calendar1()
    data = get_calendar()
    grades = get_grades()
    absences = get_absences()
        
    with tab1:
        #tab1.subheader('')
        selected_data = tab1.radio("", ("1° Anno", "2° Anno"),horizontal=True)
        # Create a title for the chart
        tab1.header('Distribuzione Ore Lezioni ' + str(selected_data))
        
        # Choose the appropriate data based on the selection
        if selected_data == "1° Anno":
            hours_by_docente = data1.groupby('Docente')['ore'].sum()
        else:
            hours_by_docente = data.groupby('Docente')['Ore'].sum()

        # Calculate total hours
        total_hours = hours_by_docente.sum()

        # Sorting the hours
        hours_by_docente = hours_by_docente.sort_values(ascending=False)
        mean_hours = hours_by_docente.mean()
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=hours_by_docente.index,
            values=hours_by_docente.values,
            hole=0.5,# This creates a donut chart

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
            width=100,
            height=600,
            showlegend=True,
            legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
            ),
        )
        
        tab1.plotly_chart(fig, use_container_width=True,  height=700)
        
        
        #tab1.divider()
        # Create a bar plot with color-coding and legend
        # Create the bar chart
        fig_bar = go.Figure(data=[go.Bar(
            x=hours_by_docente.index,
            y=hours_by_docente.values,
            text=hours_by_docente.values,  # Show the values on top of bars
            textposition='outside',  # Automatically position the text
            name='Ore per Docente'  # Legend name
        )])

        # Add mean line
        fig_bar.add_trace(go.Scatter(
            x=hours_by_docente.index,  # Use the same x-axis values as bars
            y=[mean_hours] * len(hours_by_docente),  # Repeat mean value for each x point
            mode='lines',
            name=f'Media ({mean_hours:.2f})',
            line=dict(color='yellow', dash='dash'),
            opacity=0.80
        ))
        
        # Update layout for better readability
        fig_bar.update_layout(
            font_size=18,
            xaxis_title='Docenti',
            yaxis_title='Ore',
            width=1200,
            height=600,
            xaxis={'tickangle': 45},  # Rotate x-axis labels for better readability
            showlegend=True,  # Show the legend
            margin=dict(t=50, b=50, l=50, r=50),  # Increase margins
        )
        # Adjust the y-axis range to ensure labels are not cut off
        max_value = hours_by_docente.max()
        fig_bar.update_yaxes(range=[0, max_value + 10])  # Add some space above the highest bar

        # Display the bar chart in Streamlit
        tab1.plotly_chart(fig_bar, use_container_width=True,  height=700)
        
        tab1.divider()

    
    with tab2:
        
        #tab2.subheader('')
        # Display mean grades
        mean_grades_students = grades.T.mean().sort_values(ascending=False).reset_index()
        mean_grade = grades.T.mean().mean().round(2)   # Calculate the mean of all grades
        mean_grades_students.columns = ['Studente', 'Media Voti']  # Rename columns

        mean_grades_teachers = grades.mean().sort_values(ascending=False).dropna().reset_index()
        mean_grade_techer = grades.mean().mean().round(2)
        mean_grades_teachers.columns = ['Docente', 'Media Voti']  # Rename columns


        # Create visualizations using the new function
        col1, col2 = tab2.columns([3,1])
        with col1:
            st.header('Media Voti Studenti')
            fig_students = create_bar_chart(mean_grades_students, 'Studente', 'Media Voti', 'Media Voti per Studente',ref_line= mean_grade) 
            st.plotly_chart(fig_students, use_container_width=True,  height=700)
        with col2:
            st.header('')
            st.dataframe(mean_grades_students, width=400, height=500)
            
        st.divider()
        
        col3, col4 = tab2.columns([1,3])
        with col3:
            st.header('')
            st.dataframe(mean_grades_teachers, width=400,height=500)
        with col4:
            st.header('Media Voti Docenti')
            fig_teachers = create_bar_chart(mean_grades_teachers, 'Docente', 'Media Voti', 'Media Voti per Docente', ref_line= mean_grade_techer)
            st.plotly_chart(fig_teachers, use_container_width=True, height=700)
            
        st.divider()
        
        
        st.title("Pagellina Studente")
        # Create a dropdown selector for students and teachers
        docenti = grades.columns
        studenti = grades.index
        # Create a container inside tab2 for the dropdown selectors and result 
        # Create two columns for side-by-side dropdown selectors
        col1, col2 = st.columns(2)
        
        # Display the student dropdown in the first column
        with col1:
            select_studente = st.selectbox("Selezionare Studente:", studenti)
        # Display the teacher dropdown in the second column
        with col2:
            select_docente = st.selectbox("Selezionare Docente:", docenti)
         
        # Get the grade for the selected student and teacher
        voto = grades.loc[select_studente, select_docente]
        st.write(f"Il voto di {select_studente} con {select_docente} è : {voto}!")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Grafico Voti")
            student_grades = grades.loc[select_studente]
            student_mean = student_grades.mean().round(2)
            st.plotly_chart(create_student_grade_chart(student_grades), use_container_width=True, height=700)
        with col2:
            st.subheader("Dettaglio Voti")
            st.dataframe(
                student_grades.reset_index().rename(columns={
                    'index': 'Docente',
                    select_studente: 'Voto'
                }),
                width=400,
                height=500,
            )
            
        # Display the report card using Markdown
        st.markdown(create_report_card(grades, select_studente), unsafe_allow_html=True)

        st.divider()
    
    
    with tab3:    
        percentuale_assenze = absences['% presenza su ore svolte'].sort_values(ascending=False).reset_index()
        percentuale_assenze.columns = ['Studente', '% Assenze']  # Rename columns
        
        col1, col2 = tab3.columns([3,1])
        with col1:
            st.header('Percentuale di Assenza Studenti')
            fig_absences = create_bar_chart(
                percentuale_assenze, 
                'Studente', 
                '% Assenze', 
                'Percentuale Assenze',
                ref_line=0.8  # Add reference line at 80%
            )
            st.plotly_chart(fig_absences, use_container_width=True, height=700)
        with col2:
            st.header('')
            st.dataframe(percentuale_assenze,  width=400,height=500)

        st.divider()
        
        
    with tab4:
        
        tab4.header('ITS\'s Heroes')
        
        col1, col2, col3 = tab4.columns(3)
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
        
        col4, col5, col6 = tab4.columns(3)
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
        
        col7, col8, col9 = tab4.columns(3)
        # professore con più ore 
        teacher_name_most_hours = hours_by_docente.idxmax()
        teacher_number_most_hours = hours_by_docente.max()
        highest_mean_prof = mean_grades_teachers.iloc[0][0]
        highest_mean_vote= mean_grades_teachers.iloc[0][1]
        lowest_mean_prof = mean_grades_teachers.iloc[-1][0]
        lowest_mean_vote= mean_grades_teachers.iloc[-1][1]
        col7.metric("Prof. Media + Bassa", f"{lowest_mean_prof}", '-' + str(lowest_mean_vote),border=True )
        col8.metric("Prof. Con + Ore", f"{teacher_name_most_hours}", teacher_number_most_hours,border=True )
        col9.metric("Prof. Media + Bassa", f"{lowest_mean_prof}", lowest_mean_vote,border=True )
        
        col10, col11, col12 = tab4.columns(3)
        teacher_name_most_hours = hours_by_docente.idxmin()
        teacher_number_most_hours = hours_by_docente.min()
        highest_mean_prof = mean_grades_teachers.iloc[0][0]
        highest_mean_vote= mean_grades_teachers.iloc[0][1]
        lowest_mean_prof = mean_grades_teachers.iloc[-1][0]
        lowest_mean_vote= mean_grades_teachers.iloc[-1][1]
        col10.metric("Prof. Media + Alta", f"{highest_mean_prof}", highest_mean_vote,border=True )
        col12.metric("Prof. Media + Alta", f"{highest_mean_prof}", highest_mean_vote,border=True )
        col11.metric("Prof. Con - Ore", f"{teacher_name_most_hours}", '-'+ str(teacher_number_most_hours),border=True )

except Exception as e:
    tab1.error(f"An error occurred: {e}")
    tab2.error(f"An error occurred: {e}")
    tab3.error(f"An error occurred: {e}")


