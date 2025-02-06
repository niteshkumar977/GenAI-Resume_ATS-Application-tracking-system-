# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Read the *.pdf files one by one and then analyze the content

import openai
import PyPDF2
import os
import pandas as pd
import regex as re
import streamlit as st


# # FUNCTION TO EXTRACT TEXT FROM PDF FILE

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        totalPages = len(reader.pages)
        text = ''
        for page_num in range(0, totalPages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


# # FUNCTION TO GIVE EXECUTIVE SUMMARY OF THE RESUME IN TEXT FORMAT WHICH CONSISTS OF NAME, CONTACT NO.,EMAIL ID,PROFILE WEBSITE LINK,EXPERIENCE,SKILLS & QUALIFICATIONS

# +
#from openai import OpenAI
##from config import OPENAI_API_KEY

# Initialize OpenAI API
openai.api_key = 'OPENAI API'



def analyze_pdf_content(pdf_text):
    response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
        
        messages=[
         {
        "role": "assistant",
        "content":  "Provide the executive summary of the resume of Nitesh Kumar covering name,contact no,email ID,url,experience,skills and qualifications in 500 words. Please don't put any initiation and ending '**' all data in single line of text,Name to displayed in CAPITAL LETTERS ONLY",
    },
    {
        "role": "user",
        "content":  "Name: ABC,Contact No: 9999999999,Email ID: abc@gmail.com,url: https://www.linkedin.com,executive summary: Candidate is a well rounded,well experienced person",
    },
            
            
    {
              "role": "user",
              "content":  f"Provide the executive summary of the resume covering name,contact no,email ID,profile website link,experience,skills and qualifications in 500 words. Please don't put any initiation and ending '**' and put all data in single line of text" + pdf_text,               
            }
          ],
        max_tokens=125
    )
    return response.choices[0].message.content

# Example usage
# -


# # FUNCTION TO CAPTURE THE PII DATA OF NAME,CONTACT NO,EMAIL ID,PROFILE WEBSITE URL
# # FUNCTION TO MAP THE JOB DESCRIPTION AGAINST THE RESUMES FOR TAKING OUT RELEVANCE AND RANKING SCORE

# +

#from config import OPENAI_API_KEY
#from openai import OpenAI

# Initialize OpenAI API
##openai.api_key = OPENAI_API_KEY
openai.api_key = 'OPENAI API'

def PII_data(exec_summary):
    
    response_string = exec_summary
    
    
    data = {}
    df = []
    name_pattern = re.compile(r'Name:\s([A-Z\s]+)')
    name_pattern1 = re.compile(r'([A-Z]+\s[A-Z]+)')
    
    contact_pattern = re.compile(r'Contact No:\s(\+\d{1,3}-\d{10})')
    contact_pattern1 = re.compile(r'Contact No:\s(\d{10})')
    contact_pattern2 = re.compile(r'Contact No:\s(\d{0}-\d{10})')
    contact_pattern3 = re.compile(r'Contact No:\s(\d{1,3}-\d{10})')
    contact_pattern4 = re.compile(r'Contact No:\s(\d{1,3}\s\d{10})')
    contact_pattern5 = re.compile(r'Contact No:\s(\d{1,3}\s\s\d{10})')
    
    contact_pattern6 = re.compile(r'(\+\d{1,3}-\d{10})')
    contact_pattern7 = re.compile(r'(\d{10})')
    contact_pattern8 = re.compile(r'(\d{0}-\d{10})')
    contact_pattern9 = re.compile(r'(\d{1,3}-\d{10})')
    contact_pattern10 = re.compile(r's(\d{1,3}\s\d{10})')
    contact_pattern11 = re.compile(r'(\d{1,3}\s\s\d{10})')
    
    
    email_pattern = re.compile(r'Email ID:\s([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})')
    email_pattern1 = re.compile(r'([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,})')
    
    #url_pattern = re.compile(r'Profile Website Link:\s(www\.[^\s]+)')
    url_pattern = re.compile(r'(https?://[^\s]+)|(www\.[^\s]+)')
                             
    name_match = name_pattern.search(response_string)
    name_match1 = name_pattern1.search(response_string)
    
    contact_match = contact_pattern.search(response_string)
    contact_match1 = contact_pattern1.search(response_string)
    contact_match2 = contact_pattern2.search(response_string)
    contact_match3 = contact_pattern3.search(response_string)
    contact_match4 = contact_pattern4.search(response_string)
    contact_match5 = contact_pattern5.search(response_string)
    contact_match6 = contact_pattern6.search(response_string)
    contact_match7 = contact_pattern7.search(response_string)
    contact_match8 = contact_pattern8.search(response_string)
    contact_match9 = contact_pattern9.search(response_string)
    contact_match10 = contact_pattern10.search(response_string)
    contact_match11 = contact_pattern11.search(response_string)
    
    email_match = email_pattern.search(response_string)
    email_match1 = email_pattern1.search(response_string)
    
    #url_match = url_pattern.search(response_string)
    
    extracted_urls = []
    urls = re.findall(url_pattern, response_string)
    for url in urls:
        # URLs are returned as tuples, get the first non-empty string
        full_url = url[0] if url[0] else url[1]
        extracted_urls.append(full_url)

    # Join all URLs with a semicolon
    joined_urls = "; ".join(extracted_urls)
    joined_urls = joined_urls.rstrip(',')
    

    name = name_match.group(1) if name_match else name_match1.group(1) if name_match1 else None
    contact = (contact_match.group(1) if contact_match 
               else contact_match1.group(1) if contact_match1 
               else contact_match2.group(1) if contact_match2 
               else contact_match3.group(1) if contact_match3 
               else contact_match4.group(1) if contact_match4 
               else contact_match5.group(1) if contact_match5 
               else contact_match6.group(1) if contact_match6
               else contact_match7.group(1) if contact_match7 
               else contact_match8.group(1) if contact_match8 
               else contact_match9.group(1) if contact_match9 
               else contact_match10.group(1) if contact_match10 
               else contact_match11.group(1) if contact_match11
               else None)
    
    contact_number = f"'{contact}"
    email = email_match.group(1) if email_match else email_match1.group(1) if email_match1 else None
    #url = url_match.group(1) if url_match else None

    
    
    
    data = ({'Name': name, 'contact_no': contact_number, 'email_ID': email,'profile_url' : joined_urls,'evaluation' : ''})
    ##df = pd.DataFrame(data)
    ##list = data.values.tolist()
    ##return df
    list_values = list(data.values())
    return list_values
    

def rank_candidates(job_description, exec_summary):        
    candidates = []
    response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
        {
              "role": "system",
              "content":  "You are hiring manager for the open position and you need to rank the candidate with score on suitability of job based on resume mapping with job description",
            },
        
        {
              "role": "user",
              "content":  "Job description" +job_description,
        },
                
        {
              "role": "user",
              "content":  "Resume" +exec_summary,
        }
        ],
            max_tokens=200
    )
        #evaluation = response.choices[0].text.strip()
    evaluation = response.choices[0].message.content
    candidates.append((evaluation))
    return candidates


# -

# # CAPTURING OF PATH WHERE THE RESUMES AND JD ARE SAVED AND THEN CALLING FUNCTIONS TO GET THE DESIRED RESULTS WHICH ARE THEN SAVED IN A CSV FORMAT FILE AND THEN MADE AVAILABLE FOR DOWNLOAD

# +
st.markdown(
    """
    <style>
    .small-title {
        font-size: 14px; /* Adjust this value to fit the entire heading on one line */
        white-space: nowrap; /* This prevents the text from wrapping to the next line */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use markdown to display the title with the custom class
st.markdown('<h1 class="small-title">AI driven ATS - Application Tracking System</h1>', unsafe_allow_html=True)



resume_path = st.text_area("Enter the folder path where all the applicant resumes and the JD are saved:")
st.write("Note : All the Resumes and the Job Description to be kept in the same folder and in pdf format")


if st.button("Get Resume Analysis"):
    if resume_path:
        l = []
        j = []
        for File in os.listdir(resume_path):
            if File.endswith(".pdf") and not File.startswith("JD"):
                l.append(os.path.join(resume_path, File))
            else:
                j.append(os.path.join(resume_path, File))

        executive_summary = []
        if __name__ == "__main__":
            for pdf_path in l:
                pdf_text = extract_text_from_pdf(pdf_path)
                analysis = analyze_pdf_content(pdf_text)
                executive_summary.append(analysis)

        for pdf_path_jd in j:
            JD = extract_text_from_pdf(pdf_path_jd)
            job_description = JD

        resume_analysis = pd.DataFrame(columns=['name', 'contact_no', 'email_id', 'profile_URL', 'evaluation'])

        index_to_update = 0
        for exec_summary in executive_summary:
            PII_summary = PII_data(exec_summary)
            resume_analysis.loc[len(resume_analysis)] = PII_summary
            resume_analysis['contact_no'] = resume_analysis['contact_no'].astype(str)

            ranked_candidates = rank_candidates(job_description, exec_summary)

            resume_analysis.at[len(resume_analysis) - 1, 'evaluation'] = ranked_candidates
            index_to_update += index_to_update
        os.chdir(resume_path)
        resume_analysis.to_csv('resume_analysis.csv',index = False)
        with open('resume_analysis.csv') as f:
            csv_file = f.read()
        st.write("Resumes Vs JD evaluation file with applciant details is ready for download")
        st.download_button(
                label=f"resume_analysis.csv",
                data=csv_file,
                file_name=f"resume_analysis.csv",
                mime="application/csv"
                )

        #st.write("Resume analysis complete and saved to 'resume_analysis.csv'")
    else:
        st.write("Please enter the correct folder path where all the applicant resumes and the JD are saved")

# -






