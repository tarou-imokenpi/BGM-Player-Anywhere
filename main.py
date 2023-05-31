import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pygame import mixer
import os
import json
import ctypes
import keyboard

class MusicPlayer:
    def __init__(self):
        self.music_list = []
        self.volume_settings = []
        self.playing_index = -1
        self.shortcuts = []

        self.load_data()
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        self.window = tk.Tk()
        self.window.title("Music Player")
        self.window.geometry("1000x500")
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()
        self.restore_window_size()

        keyboard.on_press(self.handle_shortcut_press)

        self.window.mainloop()

    def create_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)

        add_button = ttk.Button(button_frame, text="音楽を追加", command=self.add_music)
        add_button.pack(side=tk.LEFT, padx=10)

        for i, music in enumerate(self.music_list):
            frame = ttk.Frame(self.window)
            frame.pack(pady=5, padx=10, fill=tk.X)

            play_button = ttk.Button(frame, text="再生", width=5, command=lambda idx=i: self.play_music(idx))
            play_button.pack(side=tk.LEFT, padx=5)

            stop_button = ttk.Button(frame, text="停止", width=5, command=self.stop_music)
            stop_button.pack(side=tk.LEFT, padx=5)

            label = ttk.Label(frame, text=os.path.basename(music))
            label.pack(side=tk.LEFT, anchor="w", padx=(0, 10))

            volume_scale = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                     command=lambda value, idx=i: self.set_music_volume(value, idx))
            volume_scale.set(self.volume_settings[i])
            volume_scale.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

            delete_button = ttk.Button(frame, text="削除", width=5, command=lambda idx=i: self.delete_music(idx))
            delete_button.pack(side=tk.LEFT, padx=5)

            shortcut_button = ttk.Button(frame, text="ショートカットキーを登録", command=lambda idx=i: self.register_shortcut(idx))
            shortcut_button.pack(side=tk.LEFT, padx=5)

            shortcut_label = ttk.Label(frame, text=self.get_shortcut_text(i))
            shortcut_label.pack(side=tk.LEFT, padx=5)

    def add_music(self):
        file_path = filedialog.askopenfilename(filetypes=[("音楽ファイル", "*.mp3;*.aac;*.wav;*.flac")])
        if file_path:
            self.music_list.append(file_path)
            self.volume_settings.append(50)
            self.shortcuts.append((len(self.music_list) - 1, ""))
            self.create_widgets()
            self.save_data()

    def play_music(self, index):
        if self.playing_index != -1:
            mixer.music.stop()

        file_path = self.music_list[index]
        mixer.music.load(file_path)
        mixer.music.set_volume(self.volume_settings[index] / 100)
        mixer.music.play()
        self.playing_index = index

    def stop_music(self):
        if self.playing_index != -1:
            mixer.music.stop()
            self.playing_index = -1

    def set_music_volume(self, value, index):
        self.volume_settings[index] = float(value)
        if self.playing_index == index:
            mixer.music.set_volume(self.volume_settings[index] / 100)

    def delete_music(self, index):
        if index == self.playing_index:
            self.stop_music()
        del self.music_list[index]
        del self.volume_settings[index]
        del self.shortcuts[index]
        self.create_widgets()
        self.save_data()

    def on_close(self):
        result = messagebox.askyesno("保存の確認", "設定を保存しますか？")
        if result:
            self.save_data()
        self.save_window_size()
        self.window.destroy()

    def save_data(self):
        settings = {
            "music_list": self.music_list,
            "volume_settings": self.volume_settings,
            "shortcuts": self.shortcuts
        }
        with open("settings.json", "w") as file:
            json.dump(settings, file)

    def load_data(self):
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r") as file:
                    settings = json.load(file)
                    self.music_list = settings.get("music_list", [])
                    self.volume_settings = settings.get("volume_settings", [50] * len(self.music_list))
                    self.shortcuts = settings.get("shortcuts", [])
            except (json.JSONDecodeError, FileNotFoundError):
                self.init_data()
                messagebox.showinfo("読み込みエラー", "設定ファイルの読み込みに失敗したため設定ファイルを再構成しました。\n正常に起動出来ます。")
        else:
            self.init_data()

    def init_data(self):
        self.music_list = []
        self.volume_settings = []
        self.shortcuts = []

    def get_shortcut_text(self, index):
        shortcut = self.shortcuts[index][1]
        if shortcut:
            return f"Shortcut: {shortcut}"
        else:
            return "未登録"

    def register_shortcut(self, index):
        shortcut_window = tk.Toplevel(self.window)
        shortcut_window.title("ショートカットキーの登録")
        shortcut_window.geometry("400x200")
        shortcut_window.resizable(False, False)

        shortcut_label = ttk.Label(shortcut_window, text="ショートカットキーを入力:")
        shortcut_label.pack(pady=10)

        shortcut_entry = ttk.Entry(shortcut_window)
        shortcut_entry.pack(pady=5)

        def save_shortcut():
            shortcut = shortcut_entry.get()
            self.shortcuts[index] = (index, shortcut)
            self.create_widgets()
            self.save_data()
            keyboard.remove_hotkey(shortcut)  # 既存のホットキーを一旦削除
            keyboard.add_hotkey(shortcut, lambda: play_shortcut_music(index), suppress=True)  # 新しいホットキーを登録
            shortcut_window.destroy()


        save_button = ttk.Button(shortcut_window, text="保存", command=save_shortcut)
        save_button.pack(pady=5)

    def handle_shortcut_press(self, event):
        for shortcut_index, shortcut_key in self.shortcuts:
            if event.name == shortcut_key:
                self.play_music(shortcut_index)

    def save_window_size(self):
        window_size = (self.window.winfo_width(), self.window.winfo_height())
        with open("window_size.json", "w") as file:
            json.dump(window_size, file)

    def restore_window_size(self):
        if os.path.exists("window_size.json"):
            try:
                with open("window_size.json", "r") as file:
                    window_size = json.load(file)
                    self.window.geometry(f"{window_size[0]}x{window_size[1]}")
            except (json.JSONDecodeError, FileNotFoundError):
                self.window.geometry("1000x500")
        else:
            self.window.geometry("1000x500")


def play_shortcut_music(index):
    player.play_music(index)


mixer.init()
player = MusicPlayer()
