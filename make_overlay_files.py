import librosa
import soundfile as sf
import numpy as np

trained_participants = ['Shiven', 'Poorvi', 'Sriteja', 'Radhikesh', 'Prakul']
untrained_participants = ['Arjun', 'Mahika', 'Mihika', 'Vanshita', 'Pranav']
song_files_original = ['audio_tracks/A.wav', 'audio_tracks/B.mp3', 'audio_tracks/C.mp3']
samplerate = 44100
# template_file_participant = f"timestamp_files/{trained_participants[0]}_timestamps_{song_ids[0]}.txt"

"""TRAINED PARTICIPANTS"""
print("Generating audio files with metronome ticks for trained participants...")
# Iterate over all files in the timestamp_files directory
for participant in trained_participants:
    for song_file in song_files_original:
        song_id = song_file.split('/')[-1].split('.')[0]

        # Read the tapping times from the file
        tapping_times = None
        with open(f"timestamp_files/timestamps_{participant}_{song_id}.txt", "r") as file:
            tapping_times = file.read()

        time_points = []
        for line in tapping_times.split('\n'):
            if line.strip():
                time_points.append(float(line.split()[0]))

        # Remove entries less than 45
        time_points = [x for x in time_points if x > 30]
        
        # Load the original audio file using librosa
        audio, sr = librosa.load(song_file, sr=samplerate, mono=True)

        # Extend the audio to 80 seconds with silence
        target_duration = 80  # in seconds
        target_samples = int(target_duration * samplerate)
        new_audio = np.zeros(target_samples)
        new_audio[:len(audio)] = audio

        # Generate metronome ticks directly using librosa
        metronome_tick = librosa.clicks(times=np.array(time_points), sr=samplerate, length=target_samples, click_freq=450, click_duration=0.15)

        # Add metronome ticks to the extended audio
        new_audio_with_metronome = new_audio + metronome_tick

        # Save the new audio file as 24-bit PCM WAV with metronome
        save_path_wav = f"duet_audio_tracks/trained/{participant}_timestamps_{song_id}_with_metronome.wav"
        sf.write(save_path_wav, new_audio_with_metronome, samplerate, subtype='PCM_24')

print("Finished generating audio files for trained participants!")

"""UNTRAINED PARTICIPANTS"""
print("Generating audio files with metronome ticks for untrained participants...")

# Iterate over all files in the timestamp_files directory
for participant in untrained_participants:
    for song_file in song_files_original:
        song_id = song_file.split('/')[-1].split('.')[0]

        # Read the tapping times from the file
        tapping_times = None
        with open(f"timestamp_files/timestamps_{participant}_{song_id}.txt", "r") as file:
            tapping_times = file.read()

        time_points = []
        for line in tapping_times.split('\n'):
            if line.strip():
                time_points.append(float(line.split()[0]))

        # Remove entries less than 45
        time_points = [x for x in time_points if x > 30]
        
        # Load the original audio file using librosa
        audio, sr = librosa.load(song_file, sr=samplerate, mono=True)

        # Extend the audio to 80 seconds with silence
        target_duration = 80  # in seconds
        target_samples = int(target_duration * samplerate)
        new_audio = np.zeros(target_samples)
        new_audio[:len(audio)] = audio

        # Generate metronome ticks directly using librosa
        metronome_tick = librosa.clicks(times=np.array(time_points), sr=samplerate, length=target_samples, click_freq=450, click_duration=0.15)

        # Add metronome ticks to the extended audio
        new_audio_with_metronome = new_audio + metronome_tick

        # Save the new audio file as 24-bit PCM WAV with metronome
        save_path_wav = f"duet_audio_tracks/untrained/{participant}_timestamps_{song_id}_with_metronome.wav"
        sf.write(save_path_wav, new_audio_with_metronome, samplerate, subtype='PCM_24')

print("Finished generating audio files for untrained participants!")