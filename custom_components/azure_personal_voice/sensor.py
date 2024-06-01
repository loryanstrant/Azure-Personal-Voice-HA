import logging
import requests
import voluptuous as vol

from homeassistant.components.tts import PLATFORM_SCHEMA, Provider
from homeassistant.const import CONF_API_KEY, CONF_REGION
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_VOICE_NAME = 'voice_name'
CONF_SPEAKER_PROFILE_ID = 'speaker_profile_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_REGION): cv.string,
    vol.Required(CONF_VOICE_NAME): cv.string,
    vol.Required(CONF_SPEAKER_PROFILE_ID): cv.string,
})

def get_engine(hass, config, discovery_info=None):
    """Set up Azure Personal Voice TTS component."""
    return AzurePersonalVoiceProvider(
        config[CONF_API_KEY],
        config[CONF_REGION],
        config[CONF_VOICE_NAME],
        config[CONF_SPEAKER_PROFILE_ID]
    )

class AzurePersonalVoiceProvider(Provider):
    """Azure Personal Voice speech API provider."""

    def __init__(self, api_key, region, voice_name, speaker_profile_id):
        """Initialize the provider."""
        self._api_key = api_key
        self._region = region
        self._voice_name = voice_name
        self._speaker_profile_id = speaker_profile_id
        self._token = None

    @property
    def name(self):
        """Return the name of the provider."""
        return "Azure Personal Voice"

    def get_tts_audio(self, message, language, options=None):
        """Load TTS from Azure."""
        token = self._get_token()
        if not token:
            _LOGGER.error("Failed to fetch the Azure token")
            return None, None

        ssml = self._build_ssml(message)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'
        }
        url = f"https://{self._region}.tts.speech.microsoft.com/cognitiveservices/v1"
        response = requests.post(url, headers=headers, data=ssml)

        if response.status_code == 200:
            return "mp3", response.content
        else:
            _LOGGER.error("Error %d on load URL %s", response.status_code, response.url)
            return None, None

    def _get_token(self):
        """Get the access token from Azure."""
        if not self._token:
            headers = {
                'Ocp-Apim-Subscription-Key': self._api_key
            }
            url = f"https://{self._region}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
            response = requests.post(url, headers=headers)
            if response.status_code == 200:
                self._token = response.text
            else:
                _LOGGER.error("Failed to fetch the token, status: %d", response.status_code)
        return self._token

    def _build_ssml(self, text):
        """Build the SSML request body."""
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='{self._voice_name}'>
                <mstts:express-as style='friendly'>
                    <prosody rate='0%' pitch='0%'>
                        <mstts:ttsembedding speakerProfileId='{self._speaker_profile_id}'>{text}</mstts:ttsembedding>
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
        return ssml
