import os
import openai
from webex_bot.models.command import Command
from webex_bot.webex_bot import WebexBot

# API anahtarlarını ortam değişkenlerinden al
WEBEX_API_TOKEN = os.getenv("WEBEX_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI istemci nesnesi oluşturuluyor
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class GPTCommand(Command):
    
    def __init__(self):

        super().__init__()
        self.messages = [{"role": "system", "content": "Bir network mühendisi olarak, örneklerle ve basitçe açıkla"}]
    
    def execute(self, message, attachment_actions, activity):
        """
        Args:
            message (str)
            attachment_actions (dict)
            activity (dict)

        Returns:
            str:
        """
        # Kullanıcının mesajını `messages` listesine ekliyoruz
        self.messages.append({"role": "user", "content": message})

        # OpenAI ChatCompletion çağrısı (Yeni API formatında)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        # OpenAI'den gelen yanıtı al
        gpt_response = completion.choices[0].message.content

        # Asistanın cevabını da `messages` listesine ekle (sohbet bağlamı için)
        self.messages.append({"role": "assistant", "content": gpt_response})

        return gpt_response


bot = WebexBot(WEBEX_API_TOKEN, approved_domains=["morten.com.tr"])

bot.commands.clear()

bot.add_command(GPTCommand())

bot.help_command = GPTCommand()

bot.run()
