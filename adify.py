import streamlit as st
# from utils import PrepProcesor, columns 
import os 
import openai
import os
from dotenv import load_dotenv
from apikey import apikey
from PIL import Image

load_dotenv(".env")
os.environ['OPENAI_API_KEY'] = apikey
openai.api_key = apikey

st.title('🦜 Adify App 🦜')


companyName = st.text_input("Company Name","mango jazan")
client = st.selectbox('ServiceType',('Product Owner', 'Service Provider'))
offer = st.text_input("what do you offer in 2 words", "mango fruit")
campaignsGoals = st.multiselect('Campaign Goals',['Enter a new market', 'Reaching mew cutomers', 'Increase sales', 'Replace old product'])
selected_campaignsGoals = ", ".join(campaignsGoals)
region = st.multiselect('Targeted region in Saudi Arabia',['Eastern Region', 'Central Region', 'Northern Region', 'Northwest Region',
                                                           'Midwest Region', 'Southwest regions'])
selected_regions = ", and ".join(region)
timeline = st.slider("Campaign duration in weeks",1,52)

gender = st.radio("Targeted audience gender",['male','female','male and female'])
age = st.slider("Targeted Age range", value=[18,60])
selected_age = str(age[0])+ ' to ' + str(age[1])
budget = st.number_input("Budget", 1000)
# media = st.checkbox('Preferred Social media platform','Twitter 🐦','Facebook','Snapchat 👻','Tiktok 🎵', 'instagram 📸')
sumbit = st.button('Submit')
script_prompt = """I am {client} and I offer {offer} and my company name is {company}, I am looking to {selected_campaignsGoals} to target {gender} between the age of {selected_age} in {selected_regions} of Saudi Arabia.
      Create me an engaging campaign as a social media post to be for {timeline} weeks and within the budget of {budget} Saudi riyals.
      I want the campaign to be in the format of: 
      1- The best suitable platform: (just the name of the platform)
      2- The best timing of the year: (just the date/months)
      3- The caption of the campaign post based on the platform: (be as creative as possible emojie is a plus)
      4- The strategy to enter a new market: ( I am a marketing expert, I will send the exact text to my client, write for me five action items, each one is less than 25 words)(indecate this part with strategy:)""".format(
        client=client,
        offer=offer,
        company=companyName,
        selected_campaignsGoals=selected_campaignsGoals,
        selected_age=selected_age,
        selected_regions=selected_regions,
        budget=budget,
        gender=gender,
        timeline=timeline
    )
# valdating the info
substring = script_prompt.split('.', 2)[:2]
visual_part = '.'.join(substring)
visual_prompt = visual_part + " using 10 words only write me an image description that will be great for the advertisement."
translation_prompt = "That's great! now translate the first answer you sent me above to be in informal Saudi Arabic"

if sumbit:
    # openai.api_key = 
### OPEN AI API REQUEST

    script_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": script_prompt}],
    temperature=0.7, 
    max_tokens=1000
    )
    gen_script = script_response["choices"][0]["message"]["content"]

    visual_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  
    messages=[
            # {"role": "user", "content": script_prompt.split('.')[0]},
            {"role": "user", "content": visual_prompt},
            ],
    temperature=0.9, 
    max_tokens=80
    )

    gen_visual = visual_response["choices"][0]["message"]["content"]

    translation_response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  
    messages=[
            {"role": "user", "content": gen_script},
            {"role": "user", "content": translation_prompt}
        ],
    temperature=0.7, 
    max_tokens=1000
    )
    gen_translation = translation_response["choices"][0]["message"]["content"]

    image_gen = openai.Image.create(
    prompt = gen_visual,
    n=1,
    size="1024x1024"
    )
    image_url = image_gen["data"][0]["url"]
    gen_script_parts = gen_script.split('Strategy')



    with st.expander("See The English Version"):
            # st.header("English Version")
        st.write(gen_script_parts[0])
        st.image(
            image_url,
            width=400, # Manually Adjust the width of the image as per requirement
        )
        st.write('Strategy'+ gen_script_parts[1])

    with st.expander("See The Arabic Version"):
            # st.header("Arabic Version")
        st.write(gen_translation)
        st.image(
            image_url,
            width=400, # Manually Adjust the width of the image as per requirement
        )