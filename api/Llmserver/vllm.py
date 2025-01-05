# vllm = Vllm(
#     model_name="ModelsLab/Llama-3.1-8b-Uncensored-Dare",
#     server_url="https://oaao5u53ka47i5-8000.proxy.runpod.net/v1"
# )


# response = vllm.get_chat_response(
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is your name?"},
#     ],
#     temperature = 0.0,
#     max_tokens =  16,
# )

# print(response)

import requests
import json

class Vllm:
    def __init__(self,
                 model_name, 
                 server_url,
                 **kwargs
                 ):
        self.model_name = model_name
        self.server_url = server_url
    
    def get_chat_response(self, messages,**kwargs):
        response = requests.post(
            f"{self.server_url}/chat/completions",
            headers={
                "Content-Type": "application/json",
            },
            json={
                "model": self.model_name,
                "messages": messages,
                **kwargs
            }
        )

        return response.json()["choices"][0]["message"]["content"]






