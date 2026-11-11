import pyautogui
import pygetwindow as gw
import win32process
import win32api
import win32con
import time
import pyaudio
import wave
import os

print('listing devices...')
print('please select your output device, over which spotify plays the music. Devices may be listed multiple times. Just select one of them.')
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(str(p.get_device_info_by_index(i)['index'])+': '+str(p.get_device_info_by_index(i)['name'][:100]))
print('')
deviceindex = int(input('Device number:'))

def getSpotifySong():
    windows = pyautogui.getAllWindows()

    for window in windows:
        if (" - " in window.title):
            try:
                hwnd = gw.getWindowsWithTitle(window.title)
                hwnd = int(str(hwnd)[18:len(str(hwnd))-2])
                pid = win32process.GetWindowThreadProcessId(hwnd)
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid[1])
                proc_name = win32process.GetModuleFileNameEx(handle, 0)
                if ("Spotify.exe" in proc_name):
                    return str(window.title)
            except:
                pass
    return str('-')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

print("Just start the playlist and the programm will start recording")
name="None"
oldname=""
newname=""
while True:
    if not os.path.isdir("SpotifyWavs"):
        os.makedirs("SpotifyWavs")
    name = str(getSpotifySong())
    if not (name=="-"):
        if not (name==oldname):
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,channels=CHANNELS,rate=RATE,input=True,input_device_index = deviceindex,frames_per_buffer=CHUNK)
            frames = []
            newname = str(getSpotifySong())
            print("Now recording: "+name)
            while name==newname:
                data = stream.read(CHUNK)
                frames.append(data)
                newname = str(getSpotifySong())
            stream.stop_stream()
            stream.close()
            p.terminate()

            filename=name.replace("\\","")
            filename=filename.replace("/","")
            filename=filename.replace(":","")
            filename=filename.replace("*","")
            filename=filename.replace("?","")
            filename=filename.replace('"',"")
            filename=filename.replace("<","")
            filename=filename.replace(">","")
            filename=filename.replace("|","")
            filename=filename.replace("^","")
            wf = wave.open("SpotifyWavs\\"+filename+'.wav', 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

    oldname = name
    time.sleep(0.01)