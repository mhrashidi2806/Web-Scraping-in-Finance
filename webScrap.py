#!/usr/bin/env python
# coding: utf-8

# # Find the location of each row , Y

# In[172]:


import fitz  # PyMuPDF
import pandas as pd

# Open the PDF file
pdf_file = 'LinaHan.pdf'
doc = fitz.open(pdf_file)

# Find all occurrences of the search phrase
search_phrase = 'For all items subject'
search_positions = []
for page in doc:
    text_instances = page.search_for(search_phrase)
    search_positions.extend(text_instances)

# Extract the x and y coordinates of each search position
coords = [(pos[0], pos[1]) for pos in search_positions]

# Create a dataframe of the search phrase and its coordinates
df = pd.DataFrame({'text': [search_phrase] * len(search_positions),
                   'x': [c[0] for c in coords],
                   'y': [c[1] for c in coords]})

# Print the dataframe
print(df)


# In[173]:


import pandas as pd
import numpy as np

# Create a sample dataframe
df1 = pd.DataFrame({'numbers': df.iloc[:,2]})

# Split the dataframe into groups
groups = np.split(df1.numbers.values, np.where(np.diff(df1.numbers) < 0)[0] + 1)

# Create a new dataframe with each group as a column
max_len = max([len(g) for g in groups])
new_df = pd.DataFrame([g.tolist() + [0]*(max_len-len(g)) for g in groups]).T

# Rename columns
new_df.columns = [f"group_{i+1}" for i in range(len(groups))]
#Change the sort
#for col in new_df.columns:
    #new_df[col] = new_df[col].sort_values(ascending=False).values

for col in new_df.columns:
    index_of_first_zero = np.argmax(new_df[col] == 0)
    if index_of_first_zero > 0:
        new_df.at[index_of_first_zero, col] = 710
print(new_df)


# # find X 

# In[174]:




numbers = [0, 184, 297.76, 364.76, 431.76, 509]

# create a pandas dataframe with 6 rows and one column
df2 = pd.DataFrame({'numbers': numbers})
print(df2)


# # build the table

# In[175]:


import fitz
import pandas as pd

# create an empty dataframe with 5 columns
main_df = pd.DataFrame(columns=['Country', 'Entity', 'License requirement', 'License review policy', 'FEDERAL REGISTER citation'], index=range(1064))

# Open the PDF file and get the first page
with fitz.open('LinaHan.pdf') as pdf:
    # Get the pages
    for k in range(76):
        page = pdf[k] 
    
        # Define the dimensions of the rectangular region as a fraction of the page dimensions
        for j in range(14):
            for i in range(5):#We should replace the number of row of new_df

                # Calculate the coordinates of the rectangular region
                x1, y1, x2, y2 = df2.iloc[i],new_df.iloc[j,k]-.05,df2.iloc[i+1],new_df.iloc[j+1,k]
                # Open the cropped PDF file and extract the text   
                rect = fitz.Rect(x1, y1, x2, y2)  
                extracted_text = page.get_text("text", clip=rect) 
                main_df.iloc[14*k+j,i]  = extracted_text


main_df


# # Final table

# In[176]:


main_df = main_df.replace('', np.nan).dropna(how='all', subset=main_df.columns)
main_df = main_df.replace( np.nan,'')
main_df


# # Find all Aliases

# In[177]:


import re

# define a function to extract the aliases from the text
def extract_aliases(text):
    pattern = r'aliases:(.*)'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        return None

# apply the function to the column containing the text and create a new column "aliases" with the extracted values
main_df['aliases'] = main_df['Entity'].apply(extract_aliases)


# # CSV

# In[178]:


main_df.to_csv('ResearchData.csv', index=False)

