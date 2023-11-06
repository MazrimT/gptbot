import openai
import sqlite3
from pathlib import Path

class gptBot(object):
    
    def __init__(self, api_key, system_prompt="a helpful discord bot"):

        self.system_prompt = system_prompt
        self.api_key = api_key
        
        
    def get_response(self, prompt, user, system_prompt=None):
        
        openai.api_key = self.api_key
        system = system_prompt if system_prompt else self.system_prompt


        response = openai.ChatCompletion.create(
            #model="gpt-4",
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": system},
                {"role": "system", "content": f"My username is {user}"},
                {"role": "user", "content": prompt}
            ],
            #max_tokens=150,
            user=user,
            temperature=0,
            #top_p=1,
            #frequency_penalty=0,
            #presence_penalty=0
        )

        answer = {
            "reply": response['choices'][0]['message']['content'],
            "finish_reason": response['choices'][0]['finish_reason'],
            "tokens": response["usage"]["total_tokens"],
            "model": response["model"]
        }

        return answer
    



if __name__ == '__main__':


    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    chatbot = gptBot(api_key=api_key)
    anwser = chatbot.get_response(prompt='who are you?', system_prompt='you are an ai from the year 3000', user='mazrim')
    print(anwser['reply'])