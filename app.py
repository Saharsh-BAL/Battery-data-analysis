


# %%
import openai
import pickle
import numpy as np
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()


# Set Azure OpenAI details.
openai_deployment = 'gpt-4.1'  # Azure OpenAI deployment name
openai_api_key =  os.getenv.API_KEY
openai_end_pt =   os.getenv.END_POINT
openai_api_version = '2025-01-01-preview'  

# Initialize Azure OpenAI client
openai.api_base = openai_end_pt
openai.api_key = openai_api_key
openai.api_version = openai_api_version


# In[2]:


# Function to generate SQL query using OpenAI
def llm_answer(query, max_words, df_data):
    client = openai.AzureOpenAI(
        azure_endpoint=openai_end_pt,  
        api_key=openai_api_key,  
        api_version=openai_api_version,
    )



    user_prompt = f"Context: {df_data}\n\nQuery: {query}."

    input_prompt = [
        {'role': 'system', 'content': f'''You are a quality assurance professional in a manufacturing organization and your role is to analyze battery failures in their products and provide insights on root causes. Analyze the provided dataset to identify trends, patterns, and potential issues related to replaced or failed batteries. Provide a detailed analysis based on the specified dataset columns, with your thought process and data, examples to back it up.
---

To complete this analysis:
- **Explore Key Features**: Consider columns such as battery production dates, replaced counts, BIN capacities, BMS suppliers, configurations, battery ages when replaced, and charge cycles to identify significant factors affecting replacements or failures.  
- **Identify Patterns**: Look for correlations between battery failures and variables like brand, battery supplier, VIN, vehicle production/distribution dates, usage patterns (e.g., kms driven, charge cycles), and assembly specifics like BIN Assembly Line or Rev.  
- **Evaluation**: Evaluate the reliability or lifespan of batteries based on their ages, configurations, and conditions under which replacements occurred. Identify any trends across production batches, suppliers, or other contributing factors.  
- **Provide Evidence**: Use data-driven backing for conclusions, specifying metrics, trends, or visualized examples where appropriate.
---

# Steps  

1. **Data Cleaning & Preparation**:  
   - Examine and clean "missing data" or anomalies across all features.  
   - Standardize formats for dates (e.g., `Veh Production Date`, `Latest battery replace Date`, `BIN Mfg Date`) to analyze aging trends.  

2. **Descriptive Statistics Analysis**:  
   - Aggregate counts by key fields like `BIN Pack Supplier`, `BIN BMS Supplier`, `Brand`, etc.  
   - Identify patterns by grouping data (e.g., common failure periods during lifetime, charge cycle correlation, etc.).  

3. **Feature Correlation Analysis**:  
   - Correlate age and usage statistics (e.g., `Org BIN Age when Replaced`, `KMS Org BIN Replaced`, `Charge Cycles Org BIN`) to failure/replacement rates.  
   - Analyze the `Replaced Count` trends by attributes like `BIN BMS Supplier`, `BIN Battery Config`, and `BIN Mfgr`.  

4. **Detailed Trend Exploration**:  
   - Examine specific bottlenecks such as correlations between specific `BIN Rev` and high failure rates or recurrent issues with `BIN Assembly Line`.  
   - Analyze sales-to-failure trends by evaluating `Vehicle Dispatch Date`, `Sold to`, `EOL Date (Exittime)`, and associated `Replace Counts`.  

5. **Data Segmentation**:
   - Tag and group data into key segments, such as specific brand-SKU combinations, certain regional suppliers, or BIN configurations. Drill into issues for patterns in these groups.  

6. **Recommendations**:
   - Based on analytical findings, produce actionable recommendations for potential root causes and preventive measures.

---

# Output Format  

Provide a **detailed text report** in the following structure:  

1. **Introduction**: Brief explanation of the dataset and objectives.  
2. **Key Observations**: Highlight the main insights, patterns, and trends (e.g., age-based failure patterns, supplier-related issues). Break this into subpoints for clarity.  
3. **Reasoning**: Provide evidence-based reasoning for conclusions using patterns, data-backed thresholds, or calculated trends.  
4. **Conclusions**: Summarize findings and specify any critical root causes identified.  
5. **Recommendations**: Provide suggested next steps such as further analysis, supplier-specific investigations, policy changes, or operational improvements.

---

# Notes  

- Focus on identifying **actionable insights** while avoiding vague conclusions. 
- Do not provide illustrative numbers 
- Do not provide Hypothetical Aggregation. Generate aggregation and provide actual calculated data insights.
- Do not include direct outputs like JSON or code snippets in the analysis but reference specific columns appropriately to back findings.  
- Ensure the reasoning provided is **data-driven** and avoids assumptions not inferred from the dataset's features. 
 

                                       Generate answers in max tokens = {max_words}'''},
        {'role' : 'user', 'content' : user_prompt}
    ]

    # Send request to OpenAI
    response = client.chat.completions.create(
        model=openai_deployment,
        messages=input_prompt,
        temperature=0,
        max_tokens = int(1.2 * max_words)
    )


    #return assistant_reply
    return response.choices[0].message.content


# In[ ]:


# df_dict = pd.read_csv('Service_Data_Dictionary.csv')
# df_table = pd.read_csv('Service_Data_Dictionary_tables.csv')
df_data = pd.read_csv('Battery_Data_Short.csv')

def generate_answer(user_query, max_words):
    answer = llm_answer(user_query, max_words, df_data)
    return answer

def user_input(user_question):
    response=generate_answer(user_query = user_question,
                           max_words = 5000)
    st.write(response)

st.set_page_config(page_title="Ask the Battery Data Analyst",page_icon=":books:")
st.header("Ask a Question about Chetak Battery Failures ")

user_question=st.text_input("Ask a Question from Chetak Battery Failures")
if user_question:
    user_input(user_question)


