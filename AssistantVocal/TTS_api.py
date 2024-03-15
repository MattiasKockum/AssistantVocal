import google.cloud.texttospeech as tts
from google.oauth2 import service_account

import datetime


class TTS_API():
    """
    """
    def __init__(self, credentials_path):
        self.cred = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )


    def text_to_wav(self, voice_name: str, text: str, folder="./"):
        language_code = "-".join(voice_name.split("-")[:2])
        text_input = tts.SynthesisInput(text=text)
        voice_params = tts.VoiceSelectionParams(
            language_code=language_code, name=voice_name
        )
        audio_config = tts.AudioConfig(
                audio_encoding=tts.AudioEncoding.LINEAR16
        )
        client = tts.TextToSpeechClient(credentials=self.cred)

        response = client.synthesize_speech(
            input=text_input,
            voice=voice_params,
            audio_config=audio_config,
        )

        date_iso = datetime.datetime.now().isoformat()
        filename = f"{folder}/{voice_name}_{date_iso}.wav"

        with open(filename, "wb") as out:
            out.write(response.audio_content)
            print(f'Generated speech saved to "{filename}"')

        return filename

