import requests

def get_session_id():
    """Gets a session ID from Google Bard."""
    url = "https://bard.google.com/v1/session"
    headers = {
    "Authorization": "Bearer xxxxxxxxxx",
    }
    data = {}

    response = requests.post(url, headers=headers, data=data)
    print(response.text)
 #Eif response.status_code == 200:
 #E  return response.json()["session_id"]
 #Eelse:
 #E  return None
get_session_id()
#session_id = 
#print(session_id)

def get_bard_response(message):
  """Gets a response from Google Bard."""
  session_id = "YOUR_SESSION_ID"
  key_file = "YOUR_KEY_FILE"

  url = "https://bard.google.com/v1/generate"
  headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Session-ID": session_id,
  }
  data = {
    "message": message,
  }

  response = requests.post(url, headers=headers, data=data)
  if response.status_code == 200:
    return response.json()["text"]
  else:
    return None

if __name__ == '__main__':
    message = "What is the weather like today in Uppsala, Sweden?"
    response = get_bard_response(message)

    if response is not None:
        print(response)
    else:
        print("Error getting response from Google Bard.")
