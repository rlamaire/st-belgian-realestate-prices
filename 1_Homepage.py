import streamlit as st

#-----------------------------------------
#--------------- SETTINGS ----------------
page_title = 'Vastgoed App'
page_icon = ':house_with_garden:'
layout = 'wide'

#-------------- PAGE CONFIG --------------
st.set_page_config(page_title=page_title, page_icon=page_icon,layout=layout)

hide_st_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            # header {visibility: hidden;}
            </style>"""

st.markdown(hide_st_style, unsafe_allow_html=True)
#-------------------------------------------
#--------------- PAGE TITLE ----------------
st.title(page_title + ''+ page_icon)
#-------------------------------------------

    
       








