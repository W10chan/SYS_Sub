import tkinter as tk
import csv
from gtts import gTTS
import os
import subprocess

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    tts.save('output.mp3')
    os.system('afplay output.mp3')

def load_dictionary_from_csv():
    try:
        with open("dictionary.csv", newline="", encoding="utf-8_sig") as file:
            reader = csv.reader(file)
            dictionary = {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        dictionary = {}

    return dictionary

def save_dictionary_to_csv(dictionary):
    with open("dictionary.csv", mode="w", newline="", encoding="utf-8_sig") as file:
        writer = csv.writer(file)
        for word, meaning in dictionary.items():
            writer.writerow([word, meaning])

def add_word():
    word = entry_add_word.get()
    meaning = entry_add_meaning.get()
    if word and meaning:
        if word not in dictionary:
            dictionary[word] = meaning
            label_add_status.config(text="単語が追加されました")
            save_dictionary_to_csv(dictionary)
        else:
            label_add_status.config(text="単語が既に存在します")
    else:
        label_add_status.config(text="単語と意味を入力してください")

# Tkinterウィンドウの作成
window = tk.Tk()
window.title("Andy 追加モード")

# 辞書データの読み込み
dictionary = load_dictionary_from_csv()

# 追加フレーム
frame_add = tk.Frame(window)
frame_add.pack(pady=10)

label_add_word = tk.Label(frame_add, text="追加する単語:")
label_add_word.pack(side="left")

entry_add_word = tk.Entry(frame_add)
entry_add_word.pack(side="left")

label_add_meaning = tk.Label(frame_add, text="意味:")
label_add_meaning.pack(side="left")

entry_add_meaning = tk.Entry(frame_add)
entry_add_meaning.pack(side="left")

button_add = tk.Button(window, text="追加", command=add_word)
button_add.pack(pady=10)

label_add_status = tk.Label(window, text="")
label_add_status.pack()

# 発音ボタン
button_speak = tk.Button(window, text="発音", command=lambda: text_to_speech(entry_add_word.get()))
button_speak.pack()


window.mainloop()