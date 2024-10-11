# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

import requests
ingredients_list = st.multiselect ( 
    'Choose up to 5 ingredients: '
    ,my_dataframe 
    ,max_selections =5 
    )

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ''

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'], iloc[0]
        st.write ('the search value for ', fruit_chosen, ' is ', search_on, ',')
        
      #  fruityvice_response =  requests.get("https://fruityvice.com/api/fruit/watermelon")
        st.subheader(fruit_chosen + 'Nutrition Infomation')
        fruityvice_response = requests.get ("https://fruityvice.com/api/fruit/" + fruit_chosen)
        #fruityvice_response =  requests.get("https://fruityvice.com/api/fruit/watermelon")
        st.text(fruityvice_response)
        #fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width = True)

  #  my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
   #         values ('""" + ingredients_string + """')"""
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

   # st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
