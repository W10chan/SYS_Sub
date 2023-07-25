import tkinter as tk
import csv
from random import sample
import azure.cognitiveservices.speech as speechsdk

class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.master.geometry("400x500")
        self.master.title("Andy 英訳テスト")

        self.canvas = tk.Canvas(self.master, bg="white", width=50, height=50)
        self.canvas.place(x=30, y=185)
        self.Load_dictionary_from_csv()
        self.SelectQuestions()
        self.SetVar()
        self.widget()

        self.correct_answers = 0
        self.total_questions = 0
        self.answered_words = []

        self.master.bind("<Return>", self.Judge)

    def SetVar(self):
        self.judgeNum = -1
        self.num = self.questions[0]

    def Load_dictionary_from_csv(self):
        f = open("dictionary.csv", "r", encoding="utf-8-sig")
        self.wordlist = list(csv.reader(f))
        f.close()

    def SelectQuestions(self):
        self.questions = sample(range(len(self.wordlist)), 3)

    def widget(self):
        entry_font = ("Arial", 25)
        label_font = ("Arial", 25)
        self.text1 = tk.Entry(self.master, width=15, font=entry_font)
        self.text1.place(x=50, y=30)
        self.text1.insert(0, self.wordlist[self.num][1])

        self.text2 = tk.Entry(self.master, width=15, font=entry_font)
        self.text2.place(x=50, y=90)
        self.text2.focus_set()

        self.speech_config = speechsdk.SpeechConfig(subscription="YOUR_API_KEY", region="YOUR_API_KEY")
        self.speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config)

        self.speech_recognizer.recognized.connect(self.process_speech)

        self.start_button = tk.Button(self.master, text="音声入力開始", command=self.start_speech)
        self.start_button.pack()
        self.start_button.place(x=275, y=90)

        self.BtnJudge = tk.Button(self.master, text="Check", command=self.Judge, width=10)
        self.BtnJudge.place(x=110, y=148)

        self.BtnNext = tk.Button(self.master, text="次の単語", command=self.Next, width=10)
        self.BtnNext.place(x=215, y=148)

    def process_speech(self, event):
        if event.result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = event.result.text
            recognized_text = event.result.text.lower()  # テキストを小文字に変換
            recognized_text = recognized_text.replace(".", "")  # ピリオドを削除
            recognized_text = recognized_text.replace("\n", "")  # 改行文字を削除
            recognized_text = recognized_text.replace("?", "")  # ?を削除
            self.text2.delete(0, tk.END)
            self.text2.insert(tk.END, recognized_text)  # 新しいテキストを挿入
            #self.text2.insert(tk.END, recognized_text + "\n")

    def start_speech(self):
        self.speech_recognizer.start_continuous_recognition()

    def Judge(self, event=None):
        self.total_questions += 1
        if self.text2.get() == self.wordlist[self.num][0]:
            self.correct_answers += 1
            self.marupro()
        else:
            self.batsupro()
        self.answered_words.append((self.wordlist[self.num][0], self.wordlist[self.num][1]))

    def marupro(self):
        self.canvas.delete("batsu1")
        self.canvas.delete("batsu2")
        self.judgeNum = 1
        self.canvas.create_oval(10, 10, 43, 43, outline="red", width=5, tag="maru")

    def batsupro(self):
        self.canvas.create_line(10, 10, 43, 43, fill="black", width=5, tag="batsu1")
        self.canvas.create_line(10, 43, 43, 10, fill="black", width=5, tag="batsu2")
        self.text2.delete(0, tk.END)

    def Next(self):
        self.speech_recognizer.stop_continuous_recognition()
        if self.judgeNum == 1:
            self.canvas.delete("maru")
        if len(self.questions) > 1:
            self.questions.pop(0)
            self.num = self.questions[0]
            self.text1.delete(0, tk.END)
            self.text2.delete(0, tk.END)
            self.text1.insert(0, self.wordlist[self.num][1])
            self.judgeNum = -1
        else:
            self.ShowResults()

    def ShowResults(self):
        accuracy = self.correct_answers / self.total_questions * 100

        result_text = f"正答率: {accuracy:.2f}%\n\n出題された単語と答え:\n"
        for word, answer in self.answered_words:
            result_text += f"{word}: {answer}\n"

        result_label = tk.Label(self.master, text=result_text, font=("Arial", 12), justify="left")
        result_label.place(x=30, y=200)

def main():
    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()
