import streamlit as st
import plotly.graph_objects as go
import datetime 
import time
import pandas as pd

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
        
def create_report_card(grades, select_studente):
            """
            Generate a Markdown-formatted report card for the selected student
            """
            # Get the student's grades
            student_grades = grades.loc[select_studente]
            
            report_card = f"""
            ## Riassunto

            - **Media**: {student_grades.mean():.2f}
            - **Voto più alto**: {student_grades.max():.2f}
            - **Voto più basso**: {student_grades.min():.2f}

            ## Commento su performance:
            """
            
            # Add performance interpretation
            if student_grades.mean() >= 85:
                report_card += "⭐ **Performance Eccellente!** Ottimi risultati tutto tondo. 👏"
            elif student_grades.mean() >= 70:
                report_card += "📚 **Performance Molto Buona!** Buona prestazione accademica. Continua così! 👍"
            elif student_grades.mean() >= 60:
                report_card += "✏️ **Performance Buona.** Soddisfacente prestazione accademica. C'è un'ottima possibilità di miglioramento. 📈"
            else:
                report_card += "🆘 **Da Migliorare.** Da considerarsi supporto esterno e cambio metodologie di studio. 📊"
            
            return report_card
        
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
    if ref_line is not None and ref_line == 0.8:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=[ref_line] * len(df),
            mode='lines',
            name=f'Limite ({ref_line})',
            line=dict(color='red', dash='dash'),
            opacity=0.80
        ))
    elif ref_line is not None:
        fig.add_trace(go.Scatter(
            x=df[x_col],
            y=[ref_line] * len(df),
            mode='lines',
            name=f'Media ({ref_line})',
            line=dict(color='yellow', dash='dash'),
            opacity=0.80
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
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.75
        ),
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
        line=dict(color='yellow', dash='dash'),
        opacity=0.80
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
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.95
        ),
        margin=dict(t=50, b=50, l=50, r=50),
    )
    
    # Add more padding above the highest bar
    fig.update_yaxes(range=[0, max_value + (max_value * 0.2)])
    return fig