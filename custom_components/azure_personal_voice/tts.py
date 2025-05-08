import logging
import aiohttp
from homeassistant.components.tts import Provider, PLATFORM_SCHEMA
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = "api_key"
CONF_REGION = "region"
CONF_VOICE = "voice"
CONF_PROFILE_ID = "speaker_profile_id"
CONF_LANG = "language"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_REGION): cv.string,
    vol.Required(CONF_VOICE): cv.string,
    vol.Required(CONF_PROFILE_ID): cv.string,
    vol.Optional(CONF_LANG, default="en-AU"): cv.string,
})

async def async_get_engine(hass, config, discovery_info=None):
    return AzureTTSProvider(config)

class AzureTTSProvider(Provider):
    def __init__(self, config):
        self._api_key = config[CONF_API_KEY]
        self._region = config[CONF_REGION]
        self._voice = config[CONF_VOICE]
        self._profile_id = config[CONF_PROFILE_ID]
        self._language = config[CONF_LANG]
        self.name = "AzureTTS"

    @property
    def default_language(self):
        return self._language

    @property
    def supported_languages(self):
        return [self._language]

    async def async_get_tts_audio(self, message, language, options=None):
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='{self._language}'>
            <voice name='{self._voice}'>
                <mstts:ttsembedding speakerProfileId='{self._profile_id}'>
                    {message}
                </mstts:ttsembedding>
            </voice>
        </speak>
        """

        url = f"https://{self._region}.tts.speech.microsoft.com/cognitiveservices/v1"

        headers = {
            "Content-Type": "application/ssml+xml",
            "Ocp-Apim-Subscription-Key": self._api_key,
            "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
            "User-Agent": "HomeAssistant-CustomTTS"
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=ssml.encode("utf-8")) as response:
                if response.status != 200:
                    _LOGGER.error("TTS request failed: %s", await response.text())
                    return None, None
                audio = await response.read()
                return "mp3", audio
