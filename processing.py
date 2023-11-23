import pandas as pd
import fitz  
import PyPDF2
from PIL import Image
import pytesseract
import unicodedata
import pdfrw 
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal



# Example usage


excel_file = 'Lockton.xlsx'
df = pd.read_excel(excel_file)
pdf_path = r'C:\Users\raeme\Onedrive\Documents\Career\1Club\projpt1\lockapp.pdf'
#pdf_document = fitz.open(pdf_path)

organized_df = pd.DataFrame(columns=['Section','Question','Answer','Response','Text_type'])

Section = None
Question = None
question_onemany = None
Response = None

answers = []
Text_type = None
par = [0,0]
i=0
no = [29, 33, 37]
form_data = {}
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from pdfminer.pdfpage import PDFPage

# def identify_form_fields(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         parser = PDFParser(file)
#         document = PDFDocument(parser)
#         for page_number, page in enumerate(PDFPage.create_pages(document), start=1):
#             annotations = resolve1(page.annots)
#             if annotations is not None:
#                 for annot in annotations:
#                     subtype = str(resolve1(annot).get('Subtype'))
#                     # Check if the annotation is a text box
#                     if subtype == "/'Widget'" and resolve1(annot).get('FT') == "/'Tx'":
#                         rect = resolve1(annot).get('Rect', [])
#                         field_name = str(resolve1(annot).get('T'))
#                         field_value = str(resolve1(annot).get('V'))
#                         print(f"Page {page_number}: Text Box - Field: {field_name}, Rect: {rect}, Value: {field_value}")

#                     # Check if the annotation is a radio button
#                     elif subtype == "/'Widget'" and resolve1(annot).get('FT') == "/'Btn'":
#                         rect = resolve1(annot).get('Rect', [])
#                         field_name = str(resolve1(annot).get('T'))
#                         field_value = str(resolve1(annot).get('V'))

#                         print(f"Page {page_number}: Radio Button - Field: {field_name}, Rect: {rect}, Value: {field_value}")

#                     # Check if the annotation is a checkbox
#                     elif subtype == "/'Widget'" and resolve1(annot).get('FT') == "/'Ch'": #b'/Btn' and '/V' not in annot
#                         rect = resolve1(annot).get('Rect', [])
#                         field_name = str(resolve1(annot).get('T'))

#                         print(f"Page {page_number}: Checkbox - Field: {field_name}, Rect: {rect}")

# pdf_path = "C:/Users/raeme/Onedrive/Documents/Career/lockapp.pdf"
# identify_form_fields(pdf_path)

#NEW 
# def print_all_annotations(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         parser = PDFParser(file)
#         document = PDFDocument(parser)

#         for page_number, page in enumerate(PDFPage.create_pages(document), start=1):
#             annotations = resolve1(page.annots)

#             if annotations is not None:
#                 for annot in annotations:
#                     annot_type = str(resolve1(annot).get('Subtype', b''))
#                     rect = resolve1(annot).get('Rect', [])
#                     field_name = str(resolve1(annot).get('T', b''))
#                     field_value = str(resolve1(annot).get('V', b''))
#                     form_data[field_name] = field_value 
        
#     return form_data


# pdf_path = "C:/Users/raeme/Onedrive/Documents/Career/lockapp.pdf"
# filled_form_data = print_all_annotations(pdf_path)
# if filled_form_data:
#     for field_name, field_value in filled_form_data.items():
#         print(field_name, field_value)
#         answers.append([field_value]) #appends field values to an arrway#


# ATTEMPT FOR RADIO BOXES
# def extract_radio_boxes(pdf_path):
#     with open(pdf_path, 'rb') as file:
#         reader = PyPDF2.PdfReader(file)
#         num_pages = len(reader.pages)

#         for page_number in range(num_pages):
#             page = reader.pages[page_number]
#             image = page.extract_text  # Extract the text as an image
#             text = pytesseract.image_to_string(Image.frombytes('RGB', image.size, image.tobytes()))


#             # Check for a keyword that might indicate a radio button
#             if "radio" in text.lower():
#                 print(f"Radio button found on page {page_number + 1}")

# ATTEMPT FOR RADIO BOXES

# extract_radio_boxes(pdf_path)

# def contains_checkbox_symbol(text):
#     # Check for Unicode checkbox symbol
#     return any(char == '☑' for char in text)

# def contains_radio_button_symbol(text):
#     # Check for Unicode radio button symbol
#     return any(char == '■' for char in text)

# def identify_unicode_symbols(pdf_path):
#     doc = fitz.open(pdf_path)

#     for page_number in range(doc.page_count):
#         page = doc[page_number]
#         text = page.get_text()

#         if contains_checkbox_symbol(text):
#             print(f"Checkbox found on page {page_number + 1}")
        
#         if contains_radio_button_symbol(text):
#             print(f"Radio button found on page {page_number + 1}")

#     doc.close()

# identify_unicode_symbols(pdf_path)

#Response
from PyPDF2 import PdfReader


# Initialize a PDF reader object
reader = PdfReader(pdf_path)

# Function to extract form field data
# def extract_form_data(reader):
#     form_data = {}
#     for page in reader.pages:
#         for field in page.get_form_text_fields().items():
#             form_data[field[0]] = field[1]
#         for field in page.get_form_checkboxes().items():
#             form_data[field[0]] = field[1]
#         for field in page.get_form_radios().items():
#             form_data[field[0]] = field[1]
#     return form_data


def extract_pdf_form_data(pdf_path):
    form_data = {}
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            if '/Annots' in page:
                annotations = page['/Annots']
                for annotation_ref in annotations:
                    annotation = annotation_ref.get_object()
                    if annotation.get('/Subtype', '').lower() == '/widget':
                        #checks for any textboxes or checkboxes headers
                        field_name = annotation.get('/T', '')
                        field_value = annotation.get('/V', '')                      
                        if 'Radio' in field_name:
                            if field_value == '/Off':
                                field_value ='Yes'
                        elif field_value == '/Off':
                            field_value = 'No'
                        elif field_value == '/Yes':
                            field_value ='Yes'
                        form_data[field_name] = field_value 
        
    return form_data    


filled_form_data = extract_pdf_form_data(pdf_path)
if filled_form_data:
    for field_name, field_value in filled_form_data.items():
        print(field_name, field_value)
        answers.append([field_value]) #appends field values to an arrway#




#ORGANISED EXCEL FILE
for index, row in df.iterrows():
    #Section
    if row['text_type'] != 'extra_text':
        if row['text_type'] == 'section_heading': 
            Section = row['display_name']  
            section_name = row['display_name'] 
        else: 
            Section = section_name 
        
        #Question
        if row['answer_one_many'] == 'one' or row['answer_one_many']=='many': #checks if question has multiple option
            par[0] = row['version_detail_id']
            #stores this 'parent' record for future ref
            par[1] = row['display_name'] 
        if row['parent_id'] == par[0]: # checks if this current record has a parent
            Question = par[1] #takes the parent display name (question for answer)
        else:
            Question = row['display_name']
        #Answer
        Answer = row['display_name']  
        
        #Response
        #first condition is for questions with freetext answers, 
        # second conition or (row['text_type'] == 'answer_text')is for questions unincluded in prev condition
        #  as their answers has with checkboxes as they are typically 
        # answer type null
        
        if row['version_detail_id'] not in no and row['answer_type'] == 'freetext' or row['text_type'] == 'answer_text':
            try:
                Response = answers[i] #add to the response
                i += 1
            except IndexError:
                Response = ''
        else:
            Response = ''
        #Text Type
        Text_type = row['text_type']

        organized_df = organized_df._append({'Section': Section,'Question': Question, 'Answer':Answer, 'Response': Response, 'Text_type': Text_type}, ignore_index=True)

       
# pdf_document.close()

output_excel_path = 'output_lockton.xlsx'
# Write the organized DataFrame to a new Excel file
organized_df.to_excel(output_excel_path, index=False)

# Display the organized DataFrame
print(organized_df)
