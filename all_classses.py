# %%
import requests
import json
import re 
from datetime import datetime,timedelta
import ollama

# %% [markdown]
# ### todo list-
# * existing
# * new 
# * colaborartors
# * create tast 
# * assign task

# %%
class ToDoListTools:
    def __init__(self,api_token):
        # ! checking authentication
        self.api_token=api_token
        self.base_url="https://api.todoist.com/rest/v2"
        self.headers={
            "Authorization":f"Bearer {self.api_token}",
            "Content-Type":"application/json"
        }
    # ! checking projects - get projects
    def get_projects(self):
        response=requests.get(f"{self.base_url}/projects",headers=self.headers)
        if response.status_code==200:
            return response.json()
        else:
            return {"error":f"Failed to get Projects: {response.status_code}"}
        return None

    # ! fetching Project
    def get_project(self,project_name):
        projects=self.get_projects()
        if "error" in projects:
            return projects
        for project in projects:
            if project['name'].lower()==project_name.lower():
                return project
        return None

    # ! create Project
    def create_project(self,project_name ,color="berry_red"):
        existing_project=self.get_project(project_name)
        if existing_project:
            return existing_project
        
        data={
            "name": project_name,
            
            "color":color
        }

        # * posting 
        response=requests.post(
            f"{self.base_url}/projects",headers=self.headers,data=json.dumps(data)
        )

        if response.status_code==200:
            return response.json()
        else:
            return {"error":f"Failed to Create a Project {response.status_code}"}

    # ! colaborators
    def get_collaborators(self,project_id):
        response=requests.get(f"{self.base_url}/projects/{project_id}/collaborators",headers=self.headers)
        if response.status_code==200:
            return response.json()
        else:
            return {"error":f"Failed to get collaborators {response.status_code}"}

    # ! create tasks
    def create_task(self,content,project_id,due_String=None,priority=3,assignee_id=None):
        data ={
            "content":content,
            "project_id": project_id,
            "priority":priority
        }
        if due_String:
            data["due_string"]=due_String
        if assignee_id:
            data["assignee_id"]=assignee_id

        response=requests.post(f"{self.base_url}/tasks",headers=self.headers,data=json.dumps(data))
        if response.status_code==200:
            return response.json()
        else:
            return {"error": f"Failed to create a task: {response.status_code}"}

    # create and assign task

    def create_and_assign_task(self,content,project_name,assignee_name = None,due_string=None,priority=3,assignee_id=None):
        project =self.get_project(project_name)
        if not project or project==None:
            project=self.create_project(project_name)
            if "error" in project:
                return project
        project_id=project['id']
        if assignee_name:
            collaborators=self.get_collaborators(project_id)
            if "error" not in collaborators:
                for colab in collaborators:
                    if colab['name'].lower()==assignee_name.lower():
                        assignee_id=colab['id']
                        break
            
        # ~ Creating Task
        return self.create_task(content=content,project_id=project_id,due_String=due_string,priority=priority,assignee_id=assignee_id)
    
    





# %%

# 1 Transcript extractor class
class TranscriptExtractor:
    def __init__(self, source_type="google_meet"):
        self.source_type=source_type

    def get_transcript(self,meeting_id):
        if self.source_type=="google_meet":
            return self._get_google_meet_transcript(meeting_id)
        if self.source_type=="whatsapp":
            return self._get_whatsapp_transcript(meeting_id)
        if self.source_type=="telegram":
            return self._get_telegram_transcript(meeting_id)
        else:
            return {"error":f"Unsupported source type : {self.source_type}"}
    def _get_google_meet_transcript(self,meeting_id):
        return {
            "meeting_id":meeting_id,
            "transcript" :"This is a sample transcript",
            "participants":["arnav","abhay"]
        }
    def _get_whatsapp_transcript(self, meeting_id):
        return {
            "meeting_id":meeting_id,
            "transcript" :"This is a sample transcript",
            "participants":["arnav","abhay"]
        }
    
    def _get_telegram_transcript(self, meeting_id):
    	return {
            "meeting_id":meeting_id,
            "transcript" :"This is a sample transcript",
            "participants":["arnav","abhay"]
        }


# %%
# ! Class telegram Communicator 
class TelegramCommunicator:
    def __init__(self, bot_token,chat_id):
        self.bot_token =bot_token 
        self.base_url = f"https://api.telegram.org/bot{bot_token}/"
        self.chat_id=chat_id
    
    def send_message(self,message):
        data={
            "chat_id":self.chat_id,
            "text":message,
            "parse_mode":"Markdown"
        }
        response=requests.post(
            url=f"{self.base_url}/sendMessage",
            data=data
        )
        if response.status_code==200:
            return response.json()
        else:
            return {
                "error": f"Failed to send Message : {response.status_code}"
            }
    # ask confirmaom telegram
    def ask_confirmation(self,question,options=None):
        if options is None:
            options=['Yes','No']
        keyboard=[]
        for option in options:
            keyboard.append([{'text':option,"callback_data":option}])
        data={
            "chat_id":self.chat_id,
            "text":question,
            "reply_markup":json.dumps({
                'inline_keyboard':keyboard
            })
        }
        response=requests.post(
            f"{self.base_url}/sendMessage",
            data=data
        )
        if response.status_code==200:
            return response.json()
        else:
            return {
                "Error":f"Failed to send Messages: {response.status_code}"
            }
    


# %%
from twilio.rest import Client

class WhatsAppCommunicator:
    def __init__(self, account_sid, auth_token, from_whatsapp_number, to_whatsapp_number):
        self.client = Client(account_sid, auth_token)
        self.from_whatsapp_number = f"whatsapp:{from_whatsapp_number}"
        self.to_whatsapp_number = f"whatsapp:{to_whatsapp_number}"

    def send_message(self, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_whatsapp_number,
                to=self.to_whatsapp_number
            )
            return {"status": "Message sent", "sid": message.sid}
        except Exception as e:
            return {"error": str(e)}


# %%
class TaskExtractor:
    def __init__(self,llm):
        self.llm=llm
    def extract_tasks_from_transcript(self,transcript):
        prompt=f"""
        Please analyze the following meeting transcipt and identify  
        1. Project names mentioned
        2. Tasks that needed to be completed
        3. Who should be assigned to each task (if mentioned)
        4. Due dates for tasks (if mentioned)
        Format your response as json with the following structure:
        {{
        "Projects":[{{
        "name":"Project Name",
        "tasks":[{{
        "content":"Task description","assignee":"Assignee Name or null",
        "due_string":"Due Date String or null","priority":1-4 (4 is highest)
        }}]
        }}
        ]
        }}  
        Transcript : {transcript}
        """

        response=self.llm.invoke(prompt).content
        # response = ollama.generate(
        #     model=self.llm,prompt=prompt,
        # ).response
        json_match=re.search(r'```json\n(.*?)\n```',response,re.DOTALL)
        if json_match:
            json_str=json_match.group(1)
        else:
            json_str=response
        try:
            clean_json=json_str.strip()
            return json.loads(clean_json)
        except :
            return {"error":"Failed to parse extracted tasks"}
        



# %%
class ToDoListMeetingManager:
    def __init__(self,todolist_api,telegram_bot_token=None,telegram_chat_id=None,transcript_source="google_meet",llm=None):
        self.todolist_tools=ToDoListTools(todolist_api)
        self.transcript_extractor=TranscriptExtractor(transcript_source)
        self.telegram =None
        if telegram_bot_token and telegram_chat_id:
            self.telegram=TelegramCommunicator(telegram_bot_token,telegram_chat_id)
        self.task_extractor=TaskExtractor(llm)
    
    def process_meeting(self,meeting_id):
        transcript_data=self.transcript_extractor.get_transcript(meeting_id)
        if 'error' in transcript_data:
            return transcript_data
        extracted_data=self.task_extractor.extract_tasks_from_transcript(transcript_data,["transcript"])
        if "error" in extracted_data:
            return extracted_data
        results={
            "projects_created":[],
            "tasks_created":[]


        }

        for project_data in extracted_data["projects"]:
            project_name=project_data['name']
            if self.telegram:
                confirmation=self.telegram.ask_confirmation(f"Can I create a new Project {project_name} ?")
            # ! creating Project
            project = self.todolist_tools.create_project(project_name)
            if "error" in project:
                results["error"] = project["error"]
                return results
            results["projects_created"].append(project_name)

            # ! creatin task
            for task_data in project_data["task"]:
                task=self.todolist_tools.create_and_assign_task(
                    task_data['content'],
                    project_name,
                    task_data.get("assignee"),
                    task_data.get("due_string"),
                    task_data.get("priority",3)

                )
                if "error" in task:
                    results["task_errors"]=results.get("task_error",[])+[task["error"]]
                else:
                    results["tasks_created"].append({
                        "content":task_data["content"],
                        "project":project_name,
                        "assignee": task_data.get("assignee")
                    })
                    if self.telegram and task_data.get("assignee"):
                        self.telegram.send_message(
                        f"*New Task Assigned \n\n"
                        f"Project: {project_name}\n"
                        f"Task: {task_data['content']}\n"
                        f"Assigened to : {task_data['assignee']}\n"
                        f"Due : {task_data.get('due_string','Not Specified')}"
                        )
        return results



