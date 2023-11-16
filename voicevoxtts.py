import os
import asyncio
from io import BytesIO
from voicevox import Client
import customtkinter as ctk
import pygame
import sounddevice

speaker_id = 6

async def generate_wav_file(text, speaker_id, filepath, pitch=1.0, volume=1.0, speed=1.0, intonation=1.0):
    async with Client() as client:
        audio_query = await client.create_audio_query(text, speaker=speaker_id)
        audio_query.pitch_scale = pitch
        audio_query.volume_scale = volume
        audio_query.speed_scale = speed
        audio_query.intonation_scale = intonation
        with open(filepath, "wb") as f:
            f.write(await audio_query.synthesis(speaker=speaker_id))


devs = sounddevice.query_devices()
device_names = [dev['name'] for dev in devs]
print(device_names)



    


    
def play_and_route_audio(audio, device):
    mixer = pygame.mixer
    mixer.init(devicename=device)
    mixer.music.load(audio)
    mixer.music.play()
    while mixer.music.get_busy():
        continue
    mixer.quit()

def device_selection(device):
    global selected_device
    selected_device = device

async def generate_and_play_audio(text, speaker_id, pitch=1.0, volume=1.0, speed=1.0, intonation=1.0):
    output_file_name = "output.wav"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(current_dir, output_file_name)

    await generate_wav_file(text, speaker_id, output_file_path, pitch, volume, speed, intonation)

    with open(output_file_path, "rb") as f:
        audio = BytesIO(f.read())

    play_and_route_audio(audio, selected_device)


def speaker_selection_callback(selected_speaker):

    speaker_mapping = {"Speaker 1": 1, "Speaker 2": 2, "Speaker 3": 3, "Speaker 4": 4, "Speaker 5": 5, "Speaker 6": 6, "Speaker 7": 7, "Speaker 8": 8}
    

    if selected_speaker in speaker_mapping:
        global speaker_id
        speaker_id = speaker_mapping[selected_speaker]
        print(f"Selected Speaker: {selected_speaker}, speaker_id: {speaker_id}")
    else:
        print(f"Unknown Speaker: {selected_speaker}")





        

app = ctk.CTk()
app.title("Voicevox Audio Generator")
app.geometry("600x480")  
app.minsize(600, 480)  
app.maxsize(600, 480) 

def set_appearance_mode(mode):
    ctk.set_appearance_mode(mode)


    

content_frame = ctk.CTkFrame(app)
content_frame.pack(fill='both', expand=True)


theme_frame = ctk.CTkFrame(content_frame)
theme_frame.grid(row=0, column=0, sticky='nw')

dark_mode_button = ctk.CTkButton(theme_frame, text="Dark Mode", command=lambda: set_appearance_mode("dark"))
dark_mode_button.grid(row=0, column=0, padx=1, pady=15)

light_mode_button = ctk.CTkButton(theme_frame, text="Light Mode", command=lambda: set_appearance_mode("light"))
light_mode_button.grid(row=1, column=0, padx=1, pady=15)

speaker_options = ["Speaker 1", "Speaker 2", "Speaker 3", "Speaker 4", "Speaker 5", "Speaker 6", "Speaker 7", "Speaker 8"]
speaker_select_button = ctk.CTkOptionMenu(master=theme_frame, values=speaker_options, command=speaker_selection_callback)
speaker_select_button.grid(row=2, column=0, padx=1, pady=15)


device_select_button = ctk.CTkOptionMenu(master=theme_frame, values=device_names, command=device_selection)
device_select_button.grid(row=3, column=0, padx=1, pady=15)






input_frame = ctk.CTkFrame(content_frame)
input_frame.grid(row=0, column=1, sticky='ne')

text_label = ctk.CTkLabel(input_frame, text="Enter text:")
text_label.grid(row=0, column=0, padx=0, pady=0)

text_entry = ctk.CTkTextbox(input_frame, width=150, height=4, wrap='none')
text_entry.grid(row=1, column=0, padx=0, pady=0)

def pitch_slider_event(value):
    pitch_label.configure(text=f"Pitch: {value / 10:.1f}")  

pitch_slider = ctk.CTkSlider(input_frame, from_=-1, to=1, number_of_steps=101, command=pitch_slider_event, width=400)
pitch_slider.grid(row=2, column=0, padx=0, pady=0)
pitch_slider.set(100)  

pitch_label = ctk.CTkLabel(input_frame, text="Pitch: 0.0")
pitch_label.grid(row=3, column=0, padx=0, pady=0)

def volume_slider_event(value):
    volume_label.configure(text=f"Volume: {value / 10:.1f}")  

volume_slider = ctk.CTkSlider(input_frame, from_=0, to=20, number_of_steps=101, command=volume_slider_event, width=400)
volume_slider.grid(row=4, column=0, padx=0, pady=0)
volume_slider.set(10)  

volume_label = ctk.CTkLabel(input_frame, text="Volume: 1.0")
volume_label.grid(row=5, column=0, padx=0, pady=0)


def speed_slider_event(value):
    speed_label.configure(text=f"Speed: {value / 10:.1f}")

speed_slider = ctk.CTkSlider(input_frame, from_=0, to=20, number_of_steps=201, command=speed_slider_event, width=400)
speed_slider.grid(row=6, column=0, padx=0, pady=0)
speed_slider.set(100)  

speed_label = ctk.CTkLabel(input_frame, text="Speed: 1.0")
speed_label.grid(row=7, column=0, padx=0, pady=0)

def intonation_slider_event(value):
    intonation_label.configure(text=f"Intonation: {value / 10:.1f}")

intonation_slider = ctk.CTkSlider(input_frame, from_=0, to=20, number_of_steps=201, command=intonation_slider_event, width=400)
intonation_slider.grid(row=8, column=0, padx=0, pady=0)
intonation_slider.set(100)  

intonation_label = ctk.CTkLabel(input_frame, text="Intonation: 1.0")
intonation_label.grid(row=9, column=0, padx=0, pady=0)

def generate_and_play_audio_callback():
    asyncio.run(generate_and_play_audio(
        text_entry.get(1.0, "end"),
        speaker_id,
        pitch_slider.get() / 10,
        volume_slider.get() / 10,
        speed_slider.get() / 10,
        intonation_slider.get() / 10
    ))

generate_button = ctk.CTkButton(input_frame, text="Generate and Play", command=generate_and_play_audio_callback)
generate_button.grid(row=10, column=0, padx=5, pady=5)

app.mainloop()
