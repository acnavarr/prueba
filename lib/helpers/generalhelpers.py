from selenium.webdriver.remote.webelement import WebElement
import os
import configparser
import shutil
import tempfile
import json


def validate_text(comparison_type, text_a, text_b):
    if comparison_type == 'contain':
        return text_a.strip() in text_b.strip()
    else:
        return text_a.strip() == text_b.strip()


def transformation_helper(name, element_type):
    return '{}{}{}'.format(name.lower(), "_", element_type.lower())


def transformation_to_element_name(table_elements):
    element_final_list = []
    for element in table_elements:
        element_name = transformation_helper(element['name'], element['type'])
        element_final_list.append(element_name)
    return element_final_list


def transform_validation(expression):
    final_expression = True
    if expression != "should":
        final_expression = False
    return final_expression


def clean_behave_list(behave_list):
    cleaned_list = []
    for row in behave_list:
        cleaned_list.append(row[0])
    return cleaned_list


def split_and_replace_string(text_element) -> list:
    new_string = []
    for x in text_element.split(" "):
        new_string.append(x.replace("\n", ""))
    return new_string


def join_words(word_list) -> str:
    new_str = ""
    for word in word_list:
        new_str += word
    return new_str


def validate_wait_results(*waits):
    validation_results = []
    for wait in waits:
        if isinstance(wait, WebElement):
            validation_results.append(True)
        else:
            validation_results.append(wait)
    return validation_results

def element_with_value(element,value)-> str:
    element=(element[0],element[1].format(value))
    return element

'''Capture images'''


def capture(context, name,name_case):
   image_name=f"{replace_spaces(name)}.png"
   # image_location = os.path.join("/tmp", image_name)
   if not os.path.exists(os.path.join("screenshots", name_case)):
       os.makedirs(os.path.join("screenshots", name_case))
   image_location = os.path.join(f"screenshots/{name_case}", image_name)
   return context.browser.save_screenshot(image_location),image_location


def replace_spaces(text):
    return text.replace(" ", "_")

def object_value(value):
    if not value.isalpha():
        value = value.split(".")[1]
    return value

def get_config(section="driver", key=""):
    config = configparser.RawConfigParser()
    config.read("setup.cfg")
    return config.get(section, key)


def compress_and_save_to_temp(folder_to_compress,name_zip):
    try:
        # Create a temporary file for the compressed archive
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file_path  = os.path.join("/tmp", name_zip)
        temp_file.close()

        # Compress the folder into the temporary file
        shutil.make_archive(temp_file_path, 'zip', folder_to_compress)

        # Return the path of the compressed file
        return temp_file_path + ".zip"
    except Exception as e:
        print("Error compressing the folder:", e)
        return None

def add_attchmen(file):
    import requests
    url = "https://api.qase.io/v1/attachment/HNR"
    files = {"file": (file, open(file, "rb"), "application/zip")}
    headers = {
        "accept": "application/json",
        "Token": "b8c4bdf35b5cede98aa8c0993a5ca21e913c187bd482e4fe2f29b5b16e54a315"
    }
    response = requests.post(url, files=files, headers=headers)
    data = json.loads(response.text)
    hash_value = str(data["result"][0]["hash"])
    return hash_value
