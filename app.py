import streamlit as st
import pandas as pd
import random
import os
from streamlit_gsheets import GSheetsConnection

# File paths
excel_file = r'data.xlsx'

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
votes_df = conn.read(ttl=0)
votes_df = votes_df.dropna()

# Function to save a vote
def save_vote(idu1,idu2, option1, option2, chosen_option, chosen_option_audio):
    global votes_df
    new_vote = {'IDU1':idu1, 'IDU2':idu2, 'Option1': option1, 'Option2': option2, 
                'ChosenOption': chosen_option, 'ChosenOptionAudio':chosen_option_audio,
                'Timestamp': pd.Timestamp.now()}
    new_vote = pd.DataFrame(new_vote, index=[0])
    votes_df = pd.concat([votes_df,new_vote], ignore_index=True)
    votes_df = conn.update(data=votes_df)

# Load the Excel file
df = pd.read_excel(excel_file)
df['rnd'] = df['d3rec'].apply(lambda x: 1 if pd.isna(x) else 0) 
df = df.dropna(subset=['d3_']) # Assuming 'd3_' is the column with the text

# Function to randomly select two different options
def get_random_options():
    rnd_0 = df[df['rnd'] == 0].sample()
    rnd_1 = df[df['rnd'] == 1].sample()
    options = pd.concat([rnd_0, rnd_1]).sample(frac=1).reset_index(drop=True) # Randomize order
    return options

# Streamlit app layout
st.title('Applicazione di Voto')

# Display random options using columns for side-by-side layout
options = get_random_options()

st.write("## Opzione 1")
st.write(options['d3_'][0])
if st.button("Vota per l'opzione 1", key='vote1'):        
    save_vote(options['IDU'][0],options['IDU'][1], options['d3_'][0], 
                options['d3_'][1], 1,options['rnd'][0])
     

st.write("## Opzione 2")
st.write(options['d3_'][1])
if st.button("Vota per l'opzione 2", key='vote2'):        
    save_vote(options['IDU'][0],options['IDU'][1], options['d3_'][0], 
                options['d3_'][1], 2, options['rnd'][1])
    
st.write("## Pari")
st.write("Vota per nessuna delle due opzioni")
# Draw option
if st.button("Pari", key='draw'):    
    save_vote(options['IDU'].iloc[0], options['IDU'].iloc[1], options['d3_'].iloc[0], 
            options['d3_'].iloc[1], 3, 3)  


