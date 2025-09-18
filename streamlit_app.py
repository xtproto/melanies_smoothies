# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize your Order!")
st.write("Choose the fruits you want in your custom Order!")

# option = st.selectbox(
#     'What is your favorite fruit?',
#      ('', 'Banana', 'Strawberries', 'Peaches'))

# st.write('Your favorite fruits is:', option)

name_on_order = st.text_input('Name on Smoothie')
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))


#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
    ,max_selections = 5
)

if ingredients_list:
    # st.write('Your favorite fruits is:', ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients, name_on_order)
        values ('"""+ ingredients_string + """', '"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit to Order')

    success_string = 'Your Smoothie is ordered, ' + name_on_order + '!'

    if time_to_insert:
    #if ingredients_string:
        session.sql(my_insert_stmt).collect()

        st.success(success_string, icon="✅")

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

