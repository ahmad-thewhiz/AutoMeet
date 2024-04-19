import os
from dotenv import load_dotenv
from typing import List
from openai import OpenAI

load_dotenv()

client = OpenAI()

def get_openai_response(messages: List, model: str = "gpt-3.5-turbo-0125"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages)
        output = response.choices[0].message.content
    except Exception as e:
        output = f"Error in model_module/openai_main: {e}"

    return output

def get_openai_json_response(messages: List, model: str = "gpt-3.5-turbo-0125"):
    try:
        response = client.chat.completions.create(
            model=model,
            response_format={ "type": "json_object" },
            messages=messages)
        output = response.choices[0].message.content
    except Exception as e:
        output = f"Error in model_module/openai_main: {e}"

    return output

def generate_report(previous_tasks: str, current_status: str, next_tasks: str, model: str = "gpt-3.5-turbo-0125"):
    try:
        system_prompt = """ 
        "You are a professional AI writer tasked with generating a checklist for the technical team lead of a company to track the current progress of employees. You will receive information about previous tasks, current status, and next tasks for each employee. Your objective is to create a checklist containing the names of all employees along with their current status. This should include whether they are still working on their previous task and have not been assigned a new one, as well as a summary of the message conveying their current status. If they have completed their previous task, the checklist should indicate the new task assigned to them. It's important to maintain professionalism throughout, and the report should be detailed and easily understandable, providing insights into the progress of each employee."


        Format of the Report:

        Title:

        Employee Name:
        Status:
        Previous Task:
        Next Task:
        """

        user_prompt = f"""
        Here are the details:

        Previous Tasks:
        {previous_tasks}

        Current Status:
        {current_status}

        Next Tasks:
        {next_tasks}
        """

        messages=[
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_prompt}"},
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages)
        
        output = response.choices[0].message.content

    except Exception as e:
        output = f"Error while generating report: {e}"

    return output