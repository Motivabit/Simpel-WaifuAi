import os as _os
import pyttsx3 as _py
import speech_recognition as _s
from azure.ai.inference import ChatCompletionsClient as _Client
from azure.ai.inference.models import SystemMessage as _Sys, UserMessage as _Usr
from azure.core.credentials import AzureKeyCredential as _Key

_EP = "https://models.github.ai/inference"
_MODEL = "openai/gpt-4.1-mini"
_TK = _os.getenv("GITHUB_TOKEN")

if not _TK:
    raise EnvironmentError("❌ Token tidak ditemukan.")

_client = _Client(endpoint=_EP, credential=_Key(_TK))

def _f0():  # TTS Init
    e = _py.init()
    e.setProperty('rate', 150)
    v = e.getProperty('voices')
    if v:
        e.setProperty('voice', v[1].id)
    return e

def _f1(r, m):  # Listen
    with m as s:
        print("[🎤] Mendengarkan...yok bisa yok!")
        r.adjust_for_ambient_noise(s, duration=0.5)
        a = r.listen(s)
    try:
        t = r.recognize_google(a, language='id-ID')
        print(f"[🧑‍🦱 Kamu]: {t}")
        return t
    except _s.UnknownValueError:
        print("[⚠️] Tidak terdengar jelas.")
    except _s.RequestError as e:
        print(f"[🚫] Error permintaan: {e}")
    return None

def _f2(p):  # Chat
    r = _client.complete(
        messages=[_Sys("You are a helpful Indonesian-speaking assistant."), _Usr(p)],
        temperature=0.7,
        top_p=1.0,
        model=_MODEL
    )
    d = r.choices[0].message.content.strip()
    print(f"[🤖 AI]: {d}")
    return d

def _f3(e, t):  # Speak
    e.say(t)
    e.runAndWait()

def _main():
    r = _s.Recognizer()
    m = _s.Microphone()
    tts = _f0()

    print("=== 🎧 Asisten AI Suara Aktif ===")
    print("Silakan bicara. Tekan Ctrl+C untuk keluar.")
    try:
        while True:
            u = _f1(r, m)
            if not u:
                continue
            a = _f2(u)
            _f3(tts, a)
    except KeyboardInterrupt:
        print("\n👋 Keluar. Sampai jumpa!")

if __name__ == '__main__':
    _main()
