import streamlit as st
import pandas as pd
from streamlit_calendar import calendar


@st.cache_resource(show_spinner=False)
def create_calendar(df):
    # Convertir columna de fechas a tipo datetime
    df['date'] = pd.to_datetime(df['date'])
    # Crear una lista de eventos en el formato que streamlit-calendar requiere
    events = []
    for index, row in df.iterrows():
        event = {
            "title": row['event'],
            "start": row['date'].strftime('%Y-%m-%dT%H:%M:%S'),
            "end": row['date'].strftime('%Y-%m-%dT%H:%M:%S')
        }
        events.append(event)
    calendar_options = {
        "editable": "true",
        "selectable": "true",
        'views': {
        'listDay': { 'buttonText': 'Día' },
        'listWeek': { 'buttonText': 'Semana' },
        'listMonth': { 'buttonText': 'Mes' },
        'today':{ 'buttonText': 'Hoy' }
        },
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "listDay,listWeek,listMonth",
        },
        "slotMinTime": "06:00:00",
        "slotMaxTime": "18:00:00",
        "initialView": "listMonth",
        "resourceGroupField": "building",
        'buttonText':{'today':'Hoy'},
        'locale': 'es',
    }
    # Mostrar el calendario usando streamlit-calendar
    return calendar(events=events, options=calendar_options)
st.title("Calendario en Formato de Lista")

df = pd.read_csv('Calendar/calendar_events.csv')
create_calendar(df)
