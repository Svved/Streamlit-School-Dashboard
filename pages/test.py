import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
import time

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

@st.cache_data
def convert_to_float_hours(time_str):
    # Split the time string into parts
    time_parts = time_str.split(':')
    
    # Handle HH:MM:SS (3 parts) and HH:MM (2 parts)
    if len(time_parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, time_parts)
    elif len(time_parts) == 2:  # HH:MM
        hours, minutes = map(int, time_parts)
        seconds = 0  # Default seconds to 0
    else:
        return None  # Handle unexpected format
    
    # Calculate total hours as a float
    total_hours = hours + minutes / 60 + seconds / 3600
    return total_hours

def get_calendar1():
    # 1°anno
    # data import
    data = pd.read_csv('./data/Calendario AI&DS - biennio 2023-25 - Calendario 1° anno.csv', skiprows=3).dropna()
    data.drop(columns=['Dalle', 'Alle', 'Dettagli'], inplace=True)
    data.rename(columns={'Formatore (ROL)': 'Docente', 'Tot. Ore': 'ore', 'Data': 'data'}, inplace=True)
    # Apply the conversion function to the 'ore' column
    data['ore'] = data['ore'].apply(convert_to_float_hours)
    return data

def get_calendar():  # Load data
    data = pd.read_csv('./data/Calendario AI&DS - biennio 2023-25 - Calendario 2° anno.csv', skiprows=7)
    data = data.dropna()
    data.rename(columns={'Orario': 'inizio', 'Unnamed: 3': 'fine'}, inplace=True)
    data['Modulo'] = data['Modulo'].astype('int')
    data['inizio'] = data['inizio'].str.replace(',', '.').astype(float)
    data['fine'] = data['fine'].str.replace(',', '.').astype(float)
    data['Ore'] = data['Ore'].str.replace(',', '.').astype(float)
    data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y')
    return data

def create_report_card(grades, select_studente):
            """
            Generate a Markdown-formatted report card for the selected student
            """
            # Get the student's grades
            student_grades = grades.loc[select_studente]
            
            report_card = f"""
            ## Summary Statistics

            - **Average Grade**: {student_grades.mean():.2f}
            - **Highest Grade**: {student_grades.max():.2f}
            - **Lowest Grade**: {student_grades.min():.2f}

            ## Performance Interpretation
            """
            
            # Add performance interpretation
            if student_grades.mean() >= 85:
                report_card += "⭐ **Excellent Performance!** Outstanding achievement across subjects. 👏"
            elif student_grades.mean() >= 70:
                report_card += "📚 **Very Good Performance!** Strong academic standing. Keep up the great work! 👍"
            elif student_grades.mean() >= 60:
                report_card += "✏️ **Good Performance.** Satisfactory academic progress. Room for improvement. 📈"
            else:
                report_card += "🆘 **Needs Improvement.** Consider additional support and study strategies. 📊"
            
            return report_card

def get_grades():  # Load data
    data = pd.read_excel('./data/Valutazioni_Presenze.xlsx', sheet_name='Valutazioni', skiprows=3)[:-2]
    unnamed = []
    for col in data.columns:
        if (col.startswith('Unnamed')):
            unnamed.append(col)
    data.drop(columns=unnamed, inplace=True)
    data.set_index('Cognome Nome', drop=True, inplace=True)
    return data

def get_absences():
    data = pd.read_excel('data/Valutazioni_Presenze.xlsx', sheet_name='Presenze', skiprows=2)[:-2]
    data.set_index('Cognome Nome', drop=True, inplace=True)
    data = data.dropna()
    return data

def countdown_timer(target_date):
    """Function to display a countdown timer."""
    countdown_placeholder = st.empty()  # Create a placeholder for the countdown

    while True:
        # Get the current time
        now = datetime.datetime.now()
        
        # Calculate the time remaining
        time_remaining = target_date - now
        
        # Check if the countdown has finished
        if time_remaining.total_seconds() <= 0:
            countdown_placeholder.write("Countdown finished!")
            break
        
        # Format the time remaining
        days, seconds = time_remaining.days, time_remaining.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        # Display the countdown
        countdown_placeholder.write(f"Time remaining until {target_date.strftime('%Y-%m-%d')}:")
        countdown_placeholder.write(f"{days} days, {hours:02}:{minutes:02}:{seconds:02}")
        
        # Wait for 1 second before updating
        time.sleep(1)

def create_bar_chart(df, x_col, y_col, title, ref_line=None):
    """Create a bar chart with consistent styling and optional reference line"""
    # Create figure for multiple traces
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=df[x_col],
        y=df[y_col],
        text=df[y_col].round(2),
        textposition='outside',
        name=title
    ))
    
    # Add reference line if specified
    if ref_line is not None:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=[ref_line] * len(df),
            mode='lines',
            name=f'Critical ({ref_line})',
            line=dict(color='red', dash='dash'),
        ))
    
    max_value = df[y_col].max()
    
    fig.update_layout(
        font_size=18,
        xaxis_title=x_col,
        yaxis_title=y_col,
        width=1200,
        height=600,
        xaxis={'tickangle': 45},
        showlegend=True,  # Show legend for reference line
        margin=dict(t=50, b=50, l=50, r=50),
    )
    
    # Add more padding above the highest bar to prevent label cutoff
    fig.update_yaxes(range=[0, max_value + (max_value * 0.1)])
    return fig

def create_student_grade_chart(student_grades):
    """Create a bar chart for individual student grades"""
    # Ensure we have a DataFrame with all grades
    if isinstance(student_grades, pd.Series):
        df = pd.DataFrame(student_grades).reset_index()
        df.columns = ['Docente', 'Voto']
    else:
        df = student_grades.reset_index()
    
    # Calculate mean
    mean_grade = df['Voto'].mean()
    
    # Create figure with bar chart
    fig = go.Figure()
    
    # Add bars
    fig.add_trace(go.Bar(
        x=df['Docente'],
        y=df['Voto'],
        text=df['Voto'].round(2),
        textposition='outside',
        name='Voti per Materia'
    ))
    
    # Add mean line
    fig.add_trace(go.Scatter(
        x=df['Docente'],
        y=[mean_grade] * len(df),
        mode='lines',
        name=f'Media ({mean_grade:.2f})',
        line=dict(color='red', dash='dash'),
    ))
    
    max_value = df['Voto'].max()
    
    fig.update_layout(
        title='Distribuzione Voti per Materia',
        font_size=18,
        xaxis_title='Docenti',
        yaxis_title='Voti',
        width=1200,
        height=600,
        xaxis={'tickangle': 45},
        showlegend=True,  # Show legend to display mean line label
        margin=dict(t=50, b=50, l=50, r=50),
    )
    
    # Add more padding above the highest bar
    fig.update_yaxes(range=[0, max_value + (max_value * 0.2)])
    return fig

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


