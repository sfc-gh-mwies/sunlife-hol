# Import python packages
import pandas as pd
import streamlit as st
from snowflake.snowpark.context import get_active_session

##########################################
#             Page | Session
##########################################

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# from PIL import Image
# image = Image.open('basic.png')
# st.image(image, width=600)

# Title
st.title(":snowflake: Snowflake Cortex: Unstructured Batch Data Processing Assistant :snowflake:")
st.caption(
    f"""Welcome! 
    This demo uses Snowflake Cortex LLM functions to extract desired information from unstructured data.
    
    The application can help you:
        1. Translates text from an indicated or detected source language to a target language
        2. Detect the overall sentiment of the text
        3. Generate a brief summary of the text
    """)
st.write(" ")
option = st.selectbox('Which option would you like: ', ("Translate Text","Detect Sentiment","Summarize Text"))

# Get the current credentials
session = get_active_session()

##########################################
#       Cortex Function: TRANSLATE
##########################################

if option == "Translate Text":
    placeholder_prompt = ("La vie, voyez-vous, ça n'est jamais si bon ni si mauvais qu'on croit. Et si on la vivait sans amertume, sans faire de mal à personne, en aidant un peu ses voisins, en donnant son obole, en étant doux [...]")
    prompt_input = st.text_input("What text would you like to translate?", placeholder = placeholder_prompt)
    if prompt_input== "":
        st.write('Please enter text to translate.')
    else:
        st.write(f'Your text with {len(prompt_input)} characters will be translated to English.')
        quest_q = f'''select snowflake.cortex.translate('{prompt_input.replace("'", "''")}', '', 'en') as translation;'''
        output_translation = session.sql(quest_q).to_pandas()['TRANSLATION'][0]
        st.write("Your ❄️ :blue[**Snowflake Cortex Translated**] ❄️ Results: ")
        st.write(output_translation)

##########################################
#       Cortex Function: SENTIMENT
##########################################

elif option == "Detect Sentiment":
    placeholder_prompt = ("It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light[...] (...)")
    prompt_input = st.text_input("What text would you like to detect sentiment?", placeholder = placeholder_prompt)
    if prompt_input== "":
        st.write('Please enter text to detect sentiment.')
    else:
        st.write(f'Your English text with {len(prompt_input)} characters will be scored between -1 (most negative) to 1 (most positive) with 0 being neutral.')
        quest_q = f"""select snowflake.cortex.sentiment('{prompt_input.replace("'", "''")}') as sentiment;"""
        df_sql = session.sql(quest_q).to_pandas()
        sentiment_value = float(df_sql.iloc[0,0])
        st.write("The ❄️ :blue[**Snowflake Cortex Analyzed Sentiment**] ❄️ is: ", sentiment_value)
     
        if sentiment_value < -0.5:
            st.write(f'The tone of your English text with {len(prompt_input)} characters is very negative.')
        elif sentiment_value < -0:
            st.write(f'The tone of your English text with {len(prompt_input)} characters is fairly negative.')
        elif sentiment_value > 0.5:
            st.write(f'The tone of your English text with {len(prompt_input)} characters is very positive.')
        elif sentiment_value > 0:
            st.write(f'The tone of your English text with {len(prompt_input)} characters is fairly positive.')
        else:
            st.write(f'The tone of your English text with {len(prompt_input)} characters is neutral.')

#########################################
#       Cortex Function: SUMMARIZE
##########################################

else:
    placeholder_prompt = ("In the realm of artificial intelligence, Generative AI stands as a groundbreaking frontier that promises to revolutionize the way machines create content. At its core, Generative AI encompasses [...]")

    prompt_input = st.text_input("What text would you like to summarize?", placeholder = placeholder_prompt)
    if prompt_input== "":
        st.write('Please enter text to summarize.')
    else:
        st.write(f'Your English text with {len(prompt_input)} characters will be summarized.')
        quest_q = f'''select snowflake.cortex.summarize('{prompt_input.replace("'", "''")}') as summary;'''
        output_summary = session.sql(quest_q).to_pandas()['SUMMARY'][0]
        st.write("The ❄️ :blue[**Snowflake Cortex Summarized Text**] ❄️ is: ")
        st.write(output_summary)
