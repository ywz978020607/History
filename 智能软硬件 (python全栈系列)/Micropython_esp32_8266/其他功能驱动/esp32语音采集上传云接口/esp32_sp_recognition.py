#esp32端代码
import machine
import utime
import array

#采样率8k，采16000个点即录音2s
pcmArray = array.array("H", [0 for x in range(16001)])
pcmCount = 0

micTimer1_1 = machine.Timer(1)

mic0Pin = machine.Pin(35, machine.Pin.IN)
mic0 = machine.ADC(mic0Pin)
#衰减一下以支持0~3.3V的mic数据
mic0.atten(machine.ADC.ATTN_11DB)

def micRead(timer):
    global mic0
    global pcmArray
    global micTimer1_1
    global pcmCount
    pcmArray[pcmCount] = mic0.read()
    #采样16000个, 0-15999
    if pcmCount>15998:
        micTimer1_1.deinit()
    else:
        pcmCount += 1

def micSample():
    global mic0
    global pcmArray
    global micTimer1_1
    global pcmCount

    startTime = utime.ticks_us()
    #采样频率设置为8k
    micTimer1_1.init(mode=machine.Timer.PERIODIC, callback=micRead, freq=8000)
    while pcmCount<15999:
        pass
    micTimer1_1.deinit()

    endTime = utime.ticks_us()
    duraTime = endTime-startTime
    #rate，计算实际采样频率
    rate = 16000/(duraTime/1000/1000)
    pcmArray[16000] = 8000
    s = open("speech_data.wav", "wb")
    s.write(pcmArray)
    s.close()
    print(rate)
micSample()

#PC端代码
import numpy
import array
import wave
import struct
import _thread

def wavSetOut(outAddress, pcmArray, pcmRate):
    waveF = wave.open(outAddress, "wb")
    #设置声道数
    waveF.setnchannels(1)
    #设置多少bit记录，一般为16bit=2Byte
    waveF.setsampwidth(2)
    #设置采样率
    waveF.setframerate(pcmRate)

    for val in pcmArray:
        #float转为int
        val = round(float(val))
        dataStruct = struct.pack('<h', val)
        waveF.writeframesraw(dataStruct)
    waveF.writeframes(b"")
    waveF.close()

def Get_wav(speech_data_file, outPath):
    #读出esp32采样得到的数据
    s = open(speech_data_file, "rb")
    recvAll = s.read()
    s.close()
    recvArray = numpy.frombuffer(recvAll[0:32002], "uint16")
    rate = recvArray[16000]

    pcmData12Bit = recvArray[0:16000]
    #用float32去保存
    pcmDataU12bit_f = pcmData12Bit.astype(numpy.float32)
    #把12bit的采样数据拉伸到16bit
    pcmDataU16bit_f = pcmDataU12bit_f*16
    #转为-32768-32767(正规PCM数据)
    pcmData16bit_f = pcmDataU16bit_f - 32768
    wavSetOut(outPath, pcmData16bit_f, rate)

#语音识别代码，这里直接使用speech_recognition库带的语音识别函数，注意使用这个函数需要全局模式翻墙，可以改用科大讯飞的语音识别接口
import speech_recognition
def speechToText(wav_Path):
    sr = speech_recognition.Recognizer()
    with speech_recognition.AudioFile(wav_Path) as source:
        #降噪
        sr.adjust_for_ambient_noise(source, duration=0.2)
        audio = sr.record(source)
    text = sr.recognize_google(audio, language="zh-CN", show_all=True)
    print(text)

Get_wav("speech_data.wav", "speech.wav")
speechToText("speech.wav")













