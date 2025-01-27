# Import required packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import hashlib

# Title and Description
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Step 1: Fetch Fruit Options from Snowflake
try:
    fruit_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
    fruit_pd_df = fruit_df.to_pandas()  # Convert Snowpark DataFrame to Pandas
    st.dataframe(data=fruit_pd_df, use_container_width=True)
except Exception as e:
    st.error("Failed to fetch fruit options from Snowflake.")
    st.exception(e)
    st.stop()

# Step 2: Multiselect for Ingredient Selection
try:
    fruit_names = fruit_pd_df["FRUIT_NAME"].tolist()  # Extract fruit names
    selected_ingredients = st.multiselect("Choose up to 5 ingredients:", fruit_names, max_selections=5)
except Exception as e:
    st.error("Error while rendering the ingredient selection.")
    st.exception(e)
    st.stop()

# Step 3: Order Form (Name + Ingredients)
name_on_order = st.text_input("Enter your name for the order:")
if selected_ingredients and name_on_order:
    # Hash the selected ingredients
    ingredients_string = " ".join(selected_ingredients)
    ingredients_hash = hashlib.sha256(ingredients_string.encode("utf-8")).hexdigest()
    
    st.write("Selected Ingredients:", selected_ingredients)
    st.write("Ingredients Hash:", ingredients_hash)

    # Step 4: Insert Order into Snowflake
    if st.button("Submit Order"):
        try:
            insert_query = f"""
                INSERT INTO smoothies.public.orders (ingredients, name_on_order, order_filled, hash_ing, order_ts)
                VALUES ('{ingredients_string}', '{name_on_order}', FALSE, {int(ingredients_hash, 16)}, CURRENT_TIMESTAMP)
            """
            session.sql(insert_query).collect()
            st.success(f"Order placed successfully for {name_on_order}!")
        except Exception as e:
            st.error("Failed to insert the order into the database.")
            st.exception(e)

# Step 5: Nutrition Information (Optional)
if selected_ingredients:
    for fruit in selected_ingredients:
        try:
            search_on = fruit_pd_df.loc[fruit_pd_df['FRUIT_NAME'] == fruit, 'SEARCH_ON'].iloc[0]
            response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
            
            if response.status_code == 200:
                st.subheader(f"{fruit} Nutrition Information")
                st.json(response.json())
            else:
                st.warning(f"Could not fetch nutrition information for {fruit}.")
        except Exception as e:
            st.error(f"Error fetching nutrition data for {fruit}.")
            st.exception(e)
