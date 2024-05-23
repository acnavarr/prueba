import os
import json
import re
import random
import shutil
import tempfile
import configparser


'''Config'''


def get_config(section="driver", key=""):
    config = configparser.RawConfigParser()
    config.read("setup.cfg")
    return config.get(section, key)


'''Json handle'''


def update_json(json_name, field, value):
    with open("utils/json/" + json_name, 'r+') as f:
        json_data = json.load(f)
        json_data[field] = value
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()


def clean_data(json_name):
    with open("utils/json/" + json_name, 'r+') as f:
        json_data = json.load(f)
        for val in json_data:
            json_data[val] = ""
        f.seek(0)
        f.write(json.dumps(json_data))
        f.truncate()


def read_from_json(json_name, field):
    with open("utils/json/" + json_name) as f:
        json_data = json.load(f)
        data = json_data[field]
        f.close()
    return data


def log_file(name, value):
    f = open("utils/" + replace_spaces(name) + ".json", "a+")
    f.write(str(value))
    f.close()


'''String handle'''


def replace_spaces(text):
    return text.replace(" ", "_")


def format_to_search(chain):
    list_to_manage = chain.split()
    new_list_part1 = list_to_manage[3:5]
    new_list_part2 = list_to_manage[0:3]
    str_one = concatenate(new_list_part1)
    str_tow = concatenate(new_list_part2)
    str_one = str_one.strip()
    str_tow = str_tow.rstrip()
    return str_one + ", " + str_tow


def modify_chain(chain, start_point, end_point):
    original = chain
    final_chain = original[int(start_point):int(end_point)]
    return final_chain


def concatenate(element_list):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in element_list:
        str1 += ele + " "
    # return string
    return str1


'''Generators'''


def name_generator(text, gender):
    return text + " " + names.get_first_name(gender=gender) + " " + names.get_first_name(gender=gender)


def last_name_generator(text):
    return text + " " + names.get_last_name()


def number_generator(text):
    number = str(random.random())
    return text + number[0:10]


'''File'''


def file_path(file_name):
    return os.getcwd() + "./resources/" + file_name


def file_exists(name):
    home = os.path.expanduser('~')
    if 'call_log' in name:
        return os.path.isfile(home + '/Downloads/'+name)
    else:
        return False


def message(scenario):
    array_steps = text_between_qoutes(str(scenario.steps))
    formatted_steps = ""
    passed = 0
    failed = 0
    for step in array_steps:
        if step in scenario.failed_steps:
            status_step = ' `(failed)`'
            failed += 1
        else:
            status_step = ' `(passed)`'
            passed += 1
        formatted_steps += f" \n * {step} {status_step} "
    content = f"""
      **Feature**: {text_between_qoutes(str(scenario.feature))[0]}
      **Scenario**:  {str(scenario.name)}
      **Steps**: {formatted_steps}
      **Final status**: passed:{passed}, failed:{failed}
    """
    return str(content)


def test_rail_update_state(scenario):
    try:
        if len(scenario.tags) > 1:
            client = test_rail_connection()
            test_run = scenario.tags[0]
            test_case = scenario.tags[1]
            status = object_value(str(scenario.status))
            result = client.send_post(
                "add_result_for_case/{}/{}".format(test_run, test_case),
                {
                    'status_id': test_rails_status[status],
                    'comment': message(scenario)
                }
            )
            result_id = get_results(test_run, test_case)
            for step in scenario.failed_steps:
                file = replace_spaces(step)
                send_attachment(str(result_id), file)
            return result
    except Exception as e:
        print("error:", e)


test_rails_status = {
    "passed": 1,
    "blocked": 2,
    "retest": 4,
    "failed": 5,
}


def send_attachment(result_id, file_name):
    client = test_rail_connection()
    result = client.send_post("add_attachment_to_result/{}".format(result_id),
                              "screenshots/{}.png".format(replace_spaces(file_name)))


def get_results(test_run, test_case):
    client = test_rail_connection()
    result = client.send_get("get_results_for_case/{}/{}".format(test_run, test_case))
    return result[0]['id']


def text_between_qoutes(string):
    return re.findall(r'"(.*?)"', string)
    # return string.split('"')[1::2]


def text_outside_qoutes(string):
    return string.split('"')[0::2]


def keys_in_object(string):
    return re.findall(r"[.*?](.*?)>,", string)


def object_value(value):
    if not value.isalpha():
        value = value.split(".")[1]
    return value


def is_in_list(list, list_search):
    for i in list_search:
        if not i in list:
            return False
    return True


def dictionaries_iqual(dictionary1, dictionary2):
    """
    Check if two dictionaries are the same.
    """
    return all(dictionary1.get(k) == dictionary2.get(k) for k in dictionary1.keys())

def lists_dictionaries_iqual(list1, list2):
    """
  Check if two lists of dictionaries are the same.
    """
    return all(any(dictionaries_iqual(dic1, dic2) for dic2 in list2) for dic1 in list1)


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


def update_file_setup(item,subitem,new_version):
    config = configparser.ConfigParser()
    config.read('setup.cfg')
    config.set(item, subitem, new_version)
    with open('setup.cfg', 'w') as configfile:
        config.write(configfile)



