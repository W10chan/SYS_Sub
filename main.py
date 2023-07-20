import tkinter as tk
import csv
from gtts import gTTS
import os
import subprocess

def open_second_file():
    subprocess.Popen(["python","quiz1_wayaku.py"])

def open_third_file():
    subprocess.Popen(["python","add_word.py"])

def open_forth_file():
    subprocess.Popen(["python","quiz2_pronunciation.py"])

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


def save_dictionary_to_csv():
    with open("dictionary.csv", mode="w", newline="", encoding="utf-8_sig") as file:
        writer = csv.writer(file)
        for word, meaning in dictionary.items():
            writer.writerow([word, meaning])

def search_word():
    word = entry_search.get()
    if word in dictionary:
        meaning = dictionary[word]
        label_result.config(text=meaning)
    else:
        label_result.config(text="単語が見つかりません")

# Tkinterウィンドウの作成
window = tk.Tk()
window.title("Andy 検索モード")

# 辞書データの読み込み
dictionary = load_dictionary_from_csv()

# 検索フレーム
frame_search = tk.Frame(window)
frame_search.pack(pady=10)

label_search = tk.Label(frame_search, text="検索する単語:")
label_search.pack(side="left")
entry_search = tk.Entry(frame_search)
entry_search.pack(side="left")

button_search = tk.Button(frame_search, text="検索", command=search_word)
button_search.pack(side="left")

label_result = tk.Label(window, text="")
label_result.pack(pady=10)

# 発音ボタン
button_speak = tk.Button(window, text="発音", command=lambda: text_to_speech(entry_search.get()))
button_speak.pack(pady = 5)

#追加プログラムの起動
button_add_word = tk.Button(window, text="追加モード", command=open_third_file)
button_add_word.pack(pady=5)

#和訳クイズプログラム起動
button_quiz1 = tk.Button(window, text="和訳クイズ", command=open_second_file)
button_quiz1.pack(pady=5)

#発音クイズプログラムの起動
button_quiz2 = tk.Button(window, text="英訳クイズ", command=open_forth_file)
button_quiz2.pack(pady=5)

window.mainloop()

