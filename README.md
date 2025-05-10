# Azure Personal Voice in Home Assistant

![Logo which is a fusion of the Azure and Home Assistant logos, along with a speaker and megaphone.](https://github.com/loryanstrant/Azure-Personal-Voice-HA/blob/main/Azure-Personal-Voice-HA-logo-small.jpeg)

This integration allows you to use the [Personal Voice service](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview) in Azure Speech Studio with your Home Assistant instance.
<br><br>

**Why did I create this when there are services like ElevenLabs?**
<br>
Because I didn't want to upload my voice into a third-party service where I don't have full control of the data.<br>
Now, you can argue that there's enough video content of me online that my voice could be simulated from sampling those, but let me have my principles ok?
<br><br>

You can find a [write-up of the solution along with a demo here](https://www.loryanstrant.com/2025/05/10/integrating-azure-personal-voice-with-home-assistant/).
<br><br>


## Installation
The following assumes you already have:
- An Azure subscription
- Access to Personal Voice
- Created a speaker profile

If that's the case, let's continue!
<br><br>

### HACS installation

The first step is to add this repository into your Home Assistant via HACS, which you can do via the handy button below.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=loryanstrant&repository=Azure-Personal-Voice-HA&category=integration)

After the respository has been added and the custom component installed you will need to restart your Home Assistant instance.
<br><br>

### Configuration
Add the following lines to your configuration.yaml file:
```
tts:
  - platform: azure_personal_voice
    api_key: 
    region: 
    voice: 
    speaker_profile_id: 
    language: 
```
<br>
All of the lines are required.
This table explains each of the lines and what inputs should be provided.
<br>


| Configuration Item  | Description |
| ------------- | ------------- |
| api_key  | The value of the Speech resource key (aka "Ocp-Apim-Subscription-Key")  |
| region  | The Azure region where your Speech resource is deployed |
| voice  | The Azure region where your Speech resource is deployed   |
| speaker_profile_id  | The ID you [obtained in this step](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-create-voice)   |
| language  | The local language you'd like to use, using one of the [options listed here](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts#personal-voice)  |
<br>

#### Full example:
```
tts:
  - platform: azure_personal_voice
    api_key: a2323049847d79650aca3e7e0e476
    region: southeastasia
    voice: PhoenixLatestNeural
    speaker_profile_id: 12345678-ab12-1234-ab12-1abc2ef34568
    language: en-AU
```

<br>
Once you've updated the configuration.yaml file, restart Home Assistant again.
<br><br>


## Usage
Now that it's configured, you can test it out with an action and pipe the output to one of your media players.

### Example action:
(replace the entity_id with that of your speaker of choice)
```
action: tts.azure_personal_voice_say
data:
  cache: false
  entity_id: media_player.living_room
  message: I harnessed the power of the cloud, for this, critical task!!!
```

You can use the same structure in a script or automation, whatever tickles your fancy!


