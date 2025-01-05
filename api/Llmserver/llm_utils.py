from .models import LLMServers
import openai
from .vllm import Vllm


def get_server_url():
    server = LLMServers.objects.first()
    return (server.name,server.server_url)

def get_chat_response(messages):
    model_name , server_url = get_server_url()
    vllm = Vllm(
        model_name=model_name,
        server_url=server_url
    )
    vllm_response = vllm.get_chat_response(messages)
    return vllm_response

def get_system_prompt(charecter_details):
    system_prompt = ""
    return system_prompt