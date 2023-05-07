# IntegrationDemo

A WWise Integration demo (sample project) changed so we could extract sounds from Eternal Crusade. 

The idea behind this is that knowing the ID of so-called "event" (wwise audio event, eg "play sound of a weapon fired") we can load the soundbank (.bnk file) 
and trigger the event in it, recording it until it ends.

IDs of all events in sound bank can be acquired according to the [.bnk specification](https://wiki.xentax.com/index.php/Wwise_SoundBank_(*.bnk)). EC used, as many games, the
standard function AK::SoundEngine::GetIDFromString for getting the id from a string like "Play_Fire" (the readable event name, that can be mentioned in game files like blueprints).

Finally, to record the "events" sound files, the following WWise functions proved useful:

`unsigned long event_id = AK::SoundEngine::GetIDFromString(event_name)`

`AK::SoundEngine::LoadBank(soundbank_name, AK_DEFAULT_POOL_ID, bankID)`

`AkPlayingID m_iPlayingID = AK::SoundEngine::PostEvent(
        event_id,
        GAME_OBJECT_MUSIC,
        AK_EnableGetSourcePlayPosition | AK_MusicSyncBeat | AK_MusicSyncBar | AK_MusicSyncEntry |
        AK_MusicSyncExit |
        AK_EndOfEvent,
        &DemoMusicCallbacks::MusicCallback,
        this
    );
`

`AK::SoundEngine::StartOutputCapture(output_filename);`

`
AK::SoundEngine::StopOutputCapture();
AK::SoundEngine::StopAll();
AK::SoundEngine::CancelEventCallback(m_iPlayingID);
`

For the recording of sounds we changed the DemoMusicCallbacks class, because its usage of callbacks allows to stop capture of sound file exactly when the event ends. 
Since some events give similar, but random sounds, they are recorded several times. Since some events are infinite, capture time is limited to 10 seconds, such events are recorded only 1 time.

Bad news is that I didn't manage to get functions like ClearAllEvents and ClearAllSoundbanks working, so to have only 1 soundbank loaded at a time (to avoid capturing same events into several files with different bank prefixes) I restart this program for every soundbank, it automatically skips them if there are existing recorded .wav files.

## Setup

To compile this, will need WWise 2016.1 SDK, DirectX 9 SDK
