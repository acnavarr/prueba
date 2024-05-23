import os
import pdb

import requests
from dotenv import load_dotenv
from lib.helpers.generalhelpers import get_config

load_dotenv()


class QaseService:
    __HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Token": "20b0e723ce99769498b6bb8557e2ad1a0efcbc66e6e54eb955072ff19dfd4bba"
    }
    __BASE_END_POINT = "https://api.qase.io/v1/"
    __PROJECT_CODE = get_config("qase","QASE_PROJECT_CODE")
    def __init__(self):
        pass

    @classmethod
    def get_test_plan_name(cls, test_plan_id: int):
        """
        Searches for an existing TEST PLAN on Qase

        Parameters:
            test_plan_id: Integer corresponding to the ID of an existing TEST PLAN on Qase.

        Returns:
            The name of the existing TEST PLAN.
        """

        url = f"{cls.__BASE_END_POINT}plan/{cls.__PROJECT_CODE}/{test_plan_id}"

        response = requests.get(url=url, headers=cls.__HEADERS)

        if response.status_code == 200:
            return response.json().get("result").get("title")
        else:
            raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def create_test_run(cls, plan_id: int, title: str):
        """
        Creates a TEST RUN containing the TEST CASES of an existing TEST PLAN on Qase

        Parameters:
            plan_id: Integer corresponding to the ID of an existing TEST PLAN on Qase.
            title: Name to be assigned to the new TEST RUN on Qase.

        Returns:
            The ID of the new TEST RUN
        """
        url = f"{cls.__BASE_END_POINT}run/{cls.__PROJECT_CODE}"
        environment_id = 1 if os.getenv("ENVIRONMENT") == "Dev" else 4

        payload = {
            "title": title,
            "plan_id": plan_id,
            "environment_id": environment_id,
            "is_autotest": True

        }

        response = requests.post(url=url, headers=cls.__HEADERS, json=payload)
        if response.status_code == 200:
            return response.json().get("result").get("id")
        else:
            raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def create_result(cls, test_case_id: int, test_case_status: str, test_run_id: int, time_spent: int, scenario_name: str,scenario, hash_value: str):
        """
        Creates a RUN RESULT for a SINGLE TEST CASE  inside a TEST RUN on Qase

        Parameters:
            test_case_id: Integer corresponding an existing test case on Qase.
            test_case_status: String which describes the final result of the test.
            test_run_id: Integer corresponding to a TEST RUN in progress.
            time_spent: Integer specifying the duration in milliseconds of the test execution.

        Returns:
            The HASH of the CASE RESULT
        """

        url = f"{cls.__BASE_END_POINT}result/{cls.__PROJECT_CODE}/{test_run_id}"
        param={}

        if scenario._row is not None:
            param= {scenario._row.headings[0]: scenario._row[0]}
        payload = {
            "case_id": test_case_id,
            "status": test_case_status,
            "time_ms": time_spent * 1000,
            "comment": scenario_name,
            "param": param,
            "attachments":[hash_value]
        }
        response = requests.post(url=url, headers=cls.__HEADERS, json=payload)

        if response.status_code == 200:
            return response.json().get("result").get("hash")
        else:
            raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def complete_test_run(cls, test_run_id: int):
        """
        Marks a TEST RESULT as completed on Qase

        Parameters:
            test_run_id: Integer corresponding to an existing TEST RUN on Qase

        Returns:
            Nothing
        """

        url = f"{cls.__BASE_END_POINT}run/{cls.__PROJECT_CODE}/{test_run_id}/complete"

        response = requests.post(url=url, headers=cls.__HEADERS)

        if response.status_code == 200:
            print("")
            print("TEST RUN COMPLETED")
            print("")
        else:
            raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def check_test_case_is_automated(cls, test_case_id: int):
        """
        Checks if a TEST CASE its already marked as automated.

        Parameters:
            test_case_id: Integer corresponding to a TEST CASE ID of an existing project.
        Returns:
            Automation status
        """

        url = f"{cls.__BASE_END_POINT}case/{cls.__PROJECT_CODE}/{test_case_id}"

        response = requests.get(url=url, headers=cls.__HEADERS)

        if response.status_code == 200:
            return response.json().get("result").get("automation") == 2
        else:
            raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def update_test_case(cls, test_case_id: int,title_case: str):
        """
        Updates the Automation Status of a TEST CASE inside a PROJECT in Qase

        Parameters:
            test_case_id: Integer corresponding to a TEST CASE ID of an existing project.
        Returns:
            Nothing
        """

        url = f"{cls.__BASE_END_POINT}case/{cls.__PROJECT_CODE}/{test_case_id}"

        payload = {
            "automation": 2,
            "title":title_case
        }

        if cls.check_test_case_is_automated(test_case_id):
            pass
        else:
            response = requests.patch(url=url, json=payload, headers=cls.__HEADERS)
            if response.status_code == 200:
                print("")
                print(f"Test case {test_case_id} marked as automated")
                print("")
            else:
                raise QaseAPIError(response.status_code, response.text)

    @classmethod
    def get_current_milestone(cls):
        """
        Gets the last created milestone from Qase.

        Parameters:

        Returns:
            Nothing
        """

        url = f"{cls.__BASE_END_POINT}milestone/{cls.__PROJECT_CODE}"

        response = requests.get(url=url, headers=cls.__HEADERS)

        if response.status_code == 200:
            total_milestones = response.json().get("result").get("total")
            url = f"{url}?limit={2}&offset={total_milestones - 2}"
            response = requests.get(url=url, headers=cls.__HEADERS)
            current_milestone = \
                (list(filter(lambda x: x.get("status") == "active", response.json().get("result").get("entities"))))[-1]
            return current_milestone.get("id")
        else:
            raise QaseAPIError(response.status_code, response.text)


class QaseAPIError(Exception):

    def __init__(self, status_code, response_content):
        self.status_code = status_code
        self.response_content = response_content
        self.message = f"Qase API returned = \x7BCode: {self.status_code}, Content: {self.response_content}\x7D"
        super().__init__(self.message)
