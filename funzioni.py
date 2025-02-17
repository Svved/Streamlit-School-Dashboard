import streamlit as st
import datetime 
import time


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