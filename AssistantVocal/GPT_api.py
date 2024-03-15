from openai import OpenAI


class GPT_API():
    """
    """
    def __init__(self,
                 api_key,
                 model_name="gpt-3.5-turbo",
                 temperature=0.7,
                 max_tokens=256,
                 top_p=1,
                 frequency_penalty=0,
                 presence_penalty=0
                 ):
        self.api_key = api_key

        self.model_name = model_name
        self.temperature=temperature
        self.max_tokens=max_tokens
        self.top_p=top_p
        self.frequency_penalty=frequency_penalty
        self.presence_penalty=presence_penalty

        self.client = OpenAI(api_key=api_key)


    def continue_text_from(self, messages):
        response = self.client.chat.completions.create(
          model=self.model_name,
          messages=messages,
          temperature=self.temperature,
          max_tokens=self.max_tokens,
          top_p=self.top_p,
          frequency_penalty=self.frequency_penalty,
          presence_penalty=self.presence_penalty,
        )
        response = response.choices[0].message.content
        return response


black = lambda text: '\033[0;30m' + text + '\033[0m'
red = lambda text: '\033[0;31m' + text + '\033[0m'
green = lambda text: '\033[0;32m' + text + '\033[0m'
yellow = lambda text: '\033[0;33m' + text + '\033[0m'
blue = lambda text: '\033[0;34m' + text + '\033[0m'
magenta = lambda text: '\033[0;35m' + text + '\033[0m'
cyan = lambda text: '\033[0;36m' + text + '\033[0m'
white = lambda text: '\033[0;37m' + text + '\033[0m'


class ChatBot(object):
    """
    A simple ChatBot
    """
    def __init__(
            self,
            api,
            preprompt="",
            x1="user",
            x2="assistant",
            x1_color=red,
            x2_color=green
        ):
        self.api = api
        self.preprompt = preprompt
        self.x1 = x1
        self.x2 = x2
        self.x1_color = x1_color
        self.x2_color = x2_color
        self.messages = [{"role": "system", "content": preprompt}]
    
    def chat(self, prompt):
        self.messages.append({"role": self.x1, "content": prompt})
        response = self.api.continue_text_from(self.messages)
        self.messages.append({"role": self.x2, "content": response})
        return response


    def get_chat_history(self):
        s = ""
        for message in self.messages[1:]:
            role = message["role"]
            content = message["content"]
            if role == self.x1:
                color = self.x1_color
            else:
                color = self.x2_color
            s += f"{color(role)} : {content}\n"
        return s
