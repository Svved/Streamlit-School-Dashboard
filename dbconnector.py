import streamlit as st
import pandas as pd
from funzioni import *

@st.cache_data
def get_calendar1():
    # 1°anno
    # data import
    try:
        data = pd.read_csv('./data/Calendario AI&DS - biennio 2023-25 - Calendario 1° anno.csv', skiprows=3, sep=';').dropna()
        data.drop(columns=['Dalle', 'Alle', 'Dettagli'], inplace=True)
        data.rename(columns={'Formatore (ROL)': 'Docente', 'Tot. Ore': 'ore', 'Data': 'data'}, inplace=True)
        # Apply the conversion function to the 'ore' column
        data['ore'] = data['ore'].apply(convert_to_float_hours)
        return data
    except Exception as e:
        return print(f'Errore {e} in import di get_calendar1!')

def get_calendar():  # Load data
    # 1°anno
    # data import
    try:
        data = pd.read_csv('./data/Calendario AI&DS - biennio 2023-25 - Calendario 2° anno.csv', skiprows=7)
        data = data.dropna()
        data.rename(columns={'Orario': 'inizio', 'Unnamed: 3': 'fine'}, inplace=True)
        data['Modulo'] = data['Modulo'].astype('int')
        data['inizio'] = data['inizio'].str.replace(',', '.').astype(float)
        data['fine'] = data['fine'].str.replace(',', '.').astype(float)
        data['Ore'] = data['Ore'].str.replace(',', '.').astype(float)
        data['Data'] = pd.to_datetime(data['Data'], format='%d/%m/%Y')
        return data
    except Exception as e:
        return print(f'Errore {e} in import di get_calendar!')

def get_grades():  # Load data
    # import dati sui voti
    try:
        data = pd.read_excel('./data/Valutazioni_Presenze.xlsx', sheet_name='Valutazioni', skiprows=3)[:-2]
        unnamed = []
        for col in data.columns:
            if (col.startswith('Unnamed')):
                unnamed.append(col)
        data.drop(columns=unnamed, inplace=True)
        data.set_index('Cognome Nome', drop=True, inplace=True)
        return data
    except Exception as e:
        return print(f'Errore {e} in import di get_grades!')

def get_absences():
    #import dati sulle presenze
    try:
        data = pd.read_excel('data/Valutazioni_Presenze.xlsx', sheet_name='Presenze', skiprows=2)[:-2]
        data.set_index('Cognome Nome', drop=True, inplace=True)
        data = data.dropna()
        return data
    except Exception as e:
        return print(f'Errore {e} in import di get_absences!')