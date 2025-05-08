# Azure-Personal-Voice-HA
Azure Personal Voice in Home Assistant

[![Add to HACS](https://img.shields.io/badge/HACS-Add%20Integration-blue.svg?style=for-the-badge&logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=loryanstrant&repository=Azure-Personal-Voice-HA&category=integration)


## Example action:
```
action: tts.azure_personal_voice_say
data:
  cache: false
  entity_id: media_player.living_room
  message: I hardnessed the power of the cloud, for this, critical task!!!
```
