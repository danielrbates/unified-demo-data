import requests
import json
from pprint import pprint
# Disable SSL Certificate warning
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Global variables
client_id = "" # Update with your AMP Client ID
api_key = ""   # Update with your AMP API Key
list_guids = []

# Function definitions
def get(url):
    try:
        response = requests.get(url, verify=False)
        # Consider any status other than 2xx an error
        if not response.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(response)
        try:
            return response.json()
        except:
            return "Error: Non JSON response {}".format(response.text)
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        return "Error: {}".format(e)

def delete(url):
    try:
        response = requests.delete(url, verify=False)
        # Consider any status other than 2xx an error
        if not response.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(response)
        try:
            return response.json()
        except:
            return "Error: Non-JSON response {}".format(response.text)
    except requests.exceptions.RequestException as e:
        # A serious problem happened, like an SSLError or InvalidURL
        return "Error: {}".format(e)

def get_file_list_GUIDs(file_list_type):
    file_lists_url = "https://{}:{}@api.amp.cisco.com/v1/file_lists/{}".format(client_id,api_key,file_list_type)
    file_lists = get(file_lists_url)
    #parse through returned lists for their GUIDs and store in a list
    for item in file_lists["data"]:
        list_guids.append(item["guid"])
    print("Here are the GUIDs for the file lists:")
    print(list_guids)

def delete_files_in_file_list(file_list_guid):
    # Initialize list that will contain all SHA256s for the file_list
    sha256_list = []
    # GET the files in the list
    files_in_list_url = "https://{}:{}@api.amp.cisco.com/v1/file_lists/{}/files".format(client_id,api_key,file_list_guid)
    files_in_list = get(files_in_list_url)
    # Parse through returned data for SHA256s and store in sha256_list
    for item in files_in_list["data"]["items"]:
        sha256_list.append(item["sha256"])
    # DELETE the files
    sha256 = "initialized in def delete_files_in_file_list()" # Initialize this variable first
    for item in sha256_list:
        print("I'm going to delete this file: {}".format(item))
        #print("My client ID is {} and my api key is {}".format(client_id,api_key))
        sha256 = item
        #print("the file SHA256 is {}".format(sha256))
        delete_files_url = "https://{}:{}@api.amp.cisco.com/v1/file_lists/{}/files/{}".format(client_id,api_key,file_list_guid,sha256) 
        #print("I'm going to use this URL:{}".format(delete_files_url))
        delete(delete_files_url)
        print("Deleted!")
        sha256 = "re-initialized at the end of the for loop" # Re-initialize this variable

def clear_SCDs():
    get_file_list_GUIDs("simple_custom_detections")
    for item in list_guids:
        print("I'm working with SCD GUID {}".format(item))
        delete_files_in_file_list(item)

def clear_ABLs():
    get_file_list_GUIDs("application_blocking")
    for item in list_guids:
        print("I'm working with App Block List GUID {}".format(item))
        delete_files_in_file_list(item)

# Main function
if __name__ == "__main__":
    clear_SCDs()
    clear_ABLs()