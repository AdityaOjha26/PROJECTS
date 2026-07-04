import os
import sys
import threading
import tkinter as tk
from tkinter import ttk
from deep_translator import GoogleTranslator

class AILanguageTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("System Core: AI Neural Translation Matrix")
        self.root.geometry("750x480")
        self.root.configure(bg="#1e1e2e")
        
        # Supported language matrix mapping (Display Name -> ISO Language Code)
        self.language_map = {
            "Hindi": "hi",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Gujarati": "gu",
            "Japanese": "ja",
            "Russian": "ru",
            "Arabic": "ar"
        }

        # --- High-End Dark UI Layout ---
        # Header Branding Panel
        header_frame = tk.Frame(self.root, bg="#313244", height=55)
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 5))
        
        lbl_title = tk.Label(header_frame, text="🤖 REAL-TIME AI TRANSLATION ENGINE", font=("Arial", 11, "bold"), fg="#a6e3a1", bg="#313244")
        lbl_title.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.lbl_status = tk.Label(header_frame, text="Engine Idle", font=("Arial", 9, "italic"), fg="#bac2de", bg="#313244")
        self.lbl_status.pack(side=tk.RIGHT, padx=15, pady=15)

        # ⚙️ Configuration & Language Selection Bar
        config_frame = tk.Frame(self.root, bg="#1e1e2e")
        config_frame.pack(fill=tk.X, padx=15, pady=5)
        
        tk.Label(config_frame, text="Source: English (Auto)", font=("Arial", 10, "bold"), fg="#bac2de", bg="#1e1e2e").pack(side=tk.LEFT, padx=10)
        
        # Target Language Dropdown Menu (Combobox)
        tk.Label(config_frame, text="➡️ Target Language:", font=("Arial", 10), fg="#bac2de", bg="#1e1e2e").pack(side=tk.LEFT, padx=(20, 5))
        self.combo_target = ttk.Combobox(config_frame, values=list(self.language_map.keys()), state="readonly", width=15)
        self.combo_target.pack(side=tk.LEFT, padx=5)
        self.combo_target.set("Hindi") # Default selection

        # 📊 Symmetrical Dual-Panel Workspace (IO Text Blocks)
        workspace_frame = tk.Frame(self.root, bg="#1e1e2e")
        workspace_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        workspace_frame.columnconfigure(0, weight=1)
        workspace_frame.columnconfigure(1, weight=1)

        # Left Panel: Input English Text
        left_frame = tk.Frame(workspace_frame, bg="#1e1e2e")
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")
        tk.Label(left_frame, text="📝 ENTER ENGLISH TEXT:", font=("Arial", 9, "bold"), fg="#a6adc8", bg="#1e1e2e").pack(anchor="w", pady=2)
        self.txt_source = tk.Text(left_frame, bg="#11111b", fg="#cdd6f4", insertbackground="white", font=("Arial", 11), bd=0, wrap=tk.WORD)
        self.txt_source.pack(fill=tk.BOTH, expand=True)
        self.txt_source.insert("1.0", "Type something here and click translate...")

        # Right Panel: Output Translated Text
        right_frame = tk.Frame(workspace_frame, bg="#1e1e2e")
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")
        tk.Label(right_frame, text="🔮 AI NEURAL TRANSLATION:", font=("Arial", 9, "bold"), fg="#a6adc8", bg="#1e1e2e").pack(anchor="w", pady=2)
        self.txt_target = tk.Text(right_frame, bg="#181825", fg="#f9e2af", font=("Arial", 11, "bold"), bd=0, wrap=tk.WORD)
        self.txt_target.pack(fill=tk.BOTH, expand=True)
        self.txt_target.config(state=tk.DISABLED)

        # 🚀 Transmit Action Button
        self.btn_translate = tk.Button(self.root, text="Execute Neural Translation ⚡", bg="#89b4fa", fg="#11111b", font=("Arial", 10, "bold"), bd=0, cursor="hand2", command=self._trigger_translation_thread)
        self.btn_translate.pack(fill=tk.X, padx=25, pady=15, ipady=8)

    def _trigger_translation_thread(self):
        """Asynchronously triggers the translator worker thread to prevent UI lockup."""
        source_text = self.txt_source.get("1.0", tk.END).strip()
        target_lang_name = self.combo_target.get()
        target_lang_code = self.language_map[target_lang_name]

        if not source_text or source_text == "Type something here and click translate...":
            messagebox.showwarning("Empty Input", "Please type some English text to translate first!")
            return

        # Update UI components into a loading configuration state
        self.lbl_status.config(text="🧠 AI Processing Vectors...", fg="#fab387")
        self.btn_translate.config(state=tk.DISABLED, bg="#45475a")

        # Spin off background execution pipeline thread
        threading.Thread(target=self._translation_worker, args=(source_text, target_lang_code), daemon=True).start()

    def _translation_worker(self, text, lang_code):
        """Communicates with the translation engine mapping layer on an isolated thread."""
        try:
            # Initialize the translator module mapping targeting English as source
            translated_string = GoogleTranslator(source='auto', target=lang_code).translate(text)
            
            # Safely re-inject computed metrics back onto the main display window fields
            self.root.after(0, self._update_ui_success, translated_string)
        except Exception as e:
            self.root.after(0, self._update_ui_failure, str(e))

    def _update_ui_success(self, translated_text):
        """Renders the translated characters smoothly inside the target text matrix box."""
        self.txt_target.config(state=tk.NORMAL)
        self.txt_target.delete("1.0", tk.END)
        self.txt_target.insert("1.0", translated_text)
        self.txt_target.config(state=tk.DISABLED)
        
        self.lbl_status.config(text="🟢 Translation Complete", fg="#a6e3a1")
        self.btn_translate.config(state=tk.NORMAL, bg="#89b4fa")

    def _update_ui_failure(self, error_msg):
        """Gracefully alerts the terminal if a network timeout occurs."""
        self.lbl_status.config(text="❌ Pipeline Error", fg="#f38ba8")
        self.btn_translate.config(state=tk.NORMAL, bg="#89b4fa")
        messagebox.onerror("Engine Failure", f"Translation layer error: {error_msg}")

if __name__ == "__main__":
    root = tk.Tk()
    
    # Custom styling parameters to enforce modern layout bounds on internal dropdown widgets
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground="#313244", background="#1e1e2e", foreground="#cdd6f4")
    
    app = AILanguageTranslator(root)
    root.mainloop()
