from tts_module.tts_main import get_audio
from model_module.openai_main import get_openai_response, get_openai_json_response, generate_report
from whisperx_module.whisperx_main import get_transcription
from model_module.ollama_main import get_response
from whisperx_module.whisper import get_whisper_transcription
import os
import json
from datetime import datetime
from email_module import send_email

def load_json_file_from_path(dir_path, file_name):

    file_path = os.path.join(dir_path, file_name)
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            return None
    else:
        print("File not found.")
        return None
def append_to_messages(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages
def extract_user_messages(messages):
    user_messages = [message for message in messages if message["role"] == "user"]
    return user_messages

def save_to_json(data, file_path):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        print(f"Error while saving data to JSON file: {e}")
        return False
def load_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error while loading data from JSON file: {e}")
        return None
def create_text_file(file_path, content=""):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        return True
    except Exception as e:
        print(f"Error while creating text file: {e}")
        return False
def get_today_date_and_day():
    today = datetime.now()
    today_date = today.strftime("%Y-%m-%d")
    day_name = today.strftime("%A")
    return today_date, day_name
def get_audio_names(directory):
    """
    Get the names of all audio files (without the .wav extension) in the specified directory.

    Parameters:
        directory (str): The directory path.

    Returns:
        list: A list containing the names of all audio files (without the .wav extension) in the directory.
    """
    audio_files = [file.replace(".wav", "") for file in os.listdir(directory) if file.endswith(".wav")]
    return audio_files
def main(data_dir: str):
    input_data = load_json_file_from_path(data_dir, 'input_file.json')
    attendees_response = load_json_file_from_path(data_dir, 'attendees_response.json')
    output_data_dir = "data/output.json"


    current_status = []
    previous_tasks = input_data["previous_tasks"]
    next_tasks = input_data["next_tasks"]
    num_attendees = input_data["num_attendees"]
    attendees_names = input_data["attendees"]

    # sys_prompt = """
    # You are an AI assistant programmed to organize and lead meetings with the employees of a company. Your task is to conduct the meeting. You will be provided with the agenda and list of attendees for the meeting.

    # Firstly, you need to print the agenda of the meeting. Then, you will call the first person from the list of attendees to share their progress. As each attendee shares their progress, you will generate a json_object output with two fields: "summary", which contains the summarized response of only the latest attendee, and "next_call", which contains the message for the next attendee from the list of attendees to be called.
    # """

    sys_prompt = """
    As an AI assistant tasked with orchestrating and facilitating company meetings, your primary objective is to efficiently manage the proceedings. You will receive the meeting agenda and a roster of attendees.

    Your initial task is to display the agenda for the meeting. Subsequently, you will commence by inviting the first attendee on the list to provide their progress update. After each attendee's update, you are required to generate a JSON object with two key fields:

    1. "summary": This field encapsulates the latest attendee's progress summary. It includes any newly allocated tasks based on the provided next_tasks. If the attendee has completed the previous task, assign them a new task; otherwise, prompt them to continue their current task. Ensure all task-related information is succinctly summarized here.

    2. "next_call": This field specifies the message intended for the subsequent attendee to be called from the list. 

    Your role is to streamline the meeting process, ensuring clarity and efficiency in communication while managing task allocation seamlessly.
    """

    details = f"""
    Please refer to the agenda provided below and the list of attendees. Your task is to start by printing the agenda and then call the first attendee to share their response.

    Agenda: {input_data["agenda"]}

    Attendees: {input_data["attendees"]}

    Please maintain professionalism as you are a professional AI assistant. The output format must be strictly maintained in json_object format with two fields "summary" which is the summary of the most recent status by the user and "next_call" which is the message for the attendess
    """

    messages=[
    {"role": "system", "content": f"{sys_prompt}"},
    {"role": "user", "content": f"{details}"},
    ]

    output = get_openai_response(messages=messages)

    messages = append_to_messages(messages, 'assistant', output)

    save_to_json(messages, output_data_dir)                               

    for attendee in attendees_names:
        names = get_audio_names(f'{data_dir}/input_audio_files')
        while attendee not in names:
            print(f"{attendee} kindly share your response!\n\n")
            names = get_audio_names(f'{data_dir}/input_audio_files')
        transcription = get_whisper_transcription(f"{data_dir}/input_audio_files/{attendee}.wav")
        messages = load_from_json(f'{data_dir}/output.json')
        messages = append_to_messages(messages, 'user', transcription)
        output = get_openai_response(messages=messages)
        messages = append_to_messages(messages, 'assistant', output)
        save_to_json(messages, output_data_dir)

    today_date, day_name = get_today_date_and_day()
    Date = f"\n\nDate: {today_date} ({day_name})\n\n"

    current_status = extract_user_messages(messages)
    
    report_path = f"{data_dir}/report.txt"
    report = generate_report(previous_tasks=previous_tasks, current_status=current_status, next_tasks=next_tasks)
    report += Date
    create_text_file(file_path=report_path, content=report)

    send_email()

