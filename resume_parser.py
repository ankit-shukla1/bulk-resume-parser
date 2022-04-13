#!/usr/bin/env python
# coding: utf-8

# In[199]:


import spacy  # nlp
import pdfminer  # pdf2txt
import re  # regex
import os  # file manip
import pandas as pd  # csv - tabular


# In[200]:


import pdf2txt


# In[201]:


# converting pdf to text
def convert_pdf(f):
    output_filename = os.path.basename(os.path.splitext(f)[0]) + ".txt"
    output_filepath = os.path.join("output/txt/", output_filename)
    pdf2txt.main(args=[f, "--outfile", output_filepath])
    print(output_filepath + " saved successfully")
    return open(output_filepath, encoding="utf8").read()


# In[202]:


# load the language model
nlp = spacy.load("en_core_web_sm")


# In[203]:


# dictionary for output
result_dict = {"name": [], "phone": [], "email": [], "skills": []}
names = []
phones = []
emails = []
skills = []


# In[204]:


# Phone Number RegEx Credit : https://stackoverflow.com/questions/3868753/find-phone-numbers-in-python-script/3868861


# In[205]:


def parse_content(text):
    skillset = re.compile("python|java|sql|hadoop|tableau")
    phone_num = re.compile(
        "((?:\+\d{2}[-\.\s]??|\d{4}[-\.\s]??)?(?:\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}))"
    )
    doc = nlp(text)

    #     for word in doc.ents:
    #         print(word, end = " ")
    #         print(word.label_)
    name = [entity.text for entity in doc.ents if entity.label_ == "PERSON"][0]
    print(name)
    email = [word for word in doc if word.like_email == True][0]
    print(email)
    phone = str(re.findall(phone_num, text.lower()))
    skills_list = re.findall(skillset, text.lower())
    unique_skills_list = str(set(skills_list))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skills_list)
    print("Extraction Completed Successfully")


# In[206]:


for file in os.listdir("resumes/"):
    if file.endswith(".pdf"):
        print("Reading....." + file)
        txt = convert_pdf(os.path.join("resumes/", file))
        parse_content(txt)


# In[207]:


# Assign values in the dictionary

result_dict["name"] = names
result_dict["phone"] = phones
result_dict["email"] = emails
result_dict["skills"] = skills


# In[208]:


result_df = pd.DataFrame(result_dict)
print(result_df)


# In[209]:


result_df.to_csv("output/csv/parsed_resumes.csv")
