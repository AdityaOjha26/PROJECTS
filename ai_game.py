import tkinter as tk
from tkinter import ttk, scrolledtext
import ollama
import threading
import random

class StartupSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Startup Simulator v3.0")
        self.root.geometry("800x700")
        self.root.configure(bg="#1e1e1e")

        self.cash = 150000
        self.tech = 20
        self.morale = 85
        self.round = 1

        self.scenarios = self.load_scenarios()
        random.shuffle(self.scenarios)

        self.setup_ui()
        self.next_round()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TProgressbar", thickness=20)

        header = tk.Label(self.root, text="STARTUP DASHBOARD", font=("Urbanist", 24, "bold"), bg="#1e1e1e", fg="#deff9a")
        header.pack(pady=20)

        stat_frame = tk.Frame(self.root, bg="#1e1e1e")
        stat_frame.pack(fill="x", padx=50)

        self.cash_label = tk.Label(stat_frame, text=f"Cash: ${self.cash:,}", font=("Urbanist", 14), bg="#1e1e1e", fg="white")
        self.cash_label.grid(row=0, column=0, padx=20)

        tk.Label(stat_frame, text="Tech Level", font=("Urbanist", 12), bg="#1e1e1e", fg="#daffde").grid(row=1, column=0)
        self.tech_bar = ttk.Progressbar(stat_frame, length=200, mode='determinate', value=self.tech)
        self.tech_bar.grid(row=2, column=0, padx=20, pady=5)

        tk.Label(stat_frame, text="Team Morale", font=("Urbanist", 12), bg="#1e1e1e", fg="#daffde").grid(row=1, column=1)
        self.morale_bar = ttk.Progressbar(stat_frame, length=200, mode='determinate', value=self.morale)
        self.morale_bar.grid(row=2, column=1, padx=20, pady=5)

        self.scenario_box = tk.Label(self.root, text="", font=("Urbanist", 14, "italic"), bg="#2d2d2d", fg="white", wraplength=700, pady=20, padx=20, relief="flat")
        self.scenario_box.pack(pady=30, fill="x", padx=40)

        self.btn1 = tk.Button(self.root, text="Option 1", font=("Urbanist", 12), bg="#deff9a", fg="black", height=2, command=lambda: self.handle_choice(0))
        self.btn1.pack(fill="x", padx=100, pady=5)

        self.btn2 = tk.Button(self.root, text="Option 2", font=("Urbanist", 12), bg="#deff9a", fg="black", height=2, command=lambda: self.handle_choice(1))
        self.btn2.pack(fill="x", padx=100, pady=5)

        self.terminal = scrolledtext.ScrolledText(self.root, height=10, font=("Consolas", 10), bg="#000", fg="#00ff00", insertbackground="white")
        self.terminal.pack(pady=20, padx=40, fill="both", expand=True)
        self.terminal.insert(tk.END, ">>> System Initialized. Awaiting first decision...\n")

    def next_round(self):
        if self.cash <= 0 or self.morale <= 0:
            self.end_game("BANKRUPTCY" if self.cash <= 0 else "EMPLOYEE DESERTION")
            return
        
        if self.round > 5 or not self.scenarios:
            self.end_game("SUCCESSFUL SURVIVAL")
            return

        self.current_scenario = self.scenarios.pop(0)
        self.scenario_box.config(text=f"ROUND {self.round}: {self.current_scenario['situation']}")
        self.btn1.config(text=self.current_scenario['options'][0], state="normal")
        self.btn2.config(text=self.current_scenario['options'][1], state="normal")

    def handle_choice(self, idx):
        self.btn1.config(state="disabled")
        self.btn2.config(state="disabled")

        impact = self.current_scenario['impact'][idx]
        choice_text = self.current_scenario['options'][idx]

        self.cash += impact['cash']
        self.tech += impact['tech']
        self.morale += impact['morale']

        self.update_stats_display()

        self.terminal.insert(tk.END, f"\n[Decision]: {choice_text}\n")
        self.terminal.insert(tk.END, "🤖 AI is analyzing market response...\n")
        self.terminal.see(tk.END)

        threading.Thread(target=self.get_ai_narrative, args=(choice_text,), daemon=True).start()

    def get_ai_narrative(self, choice):
        prompt = (
            f"System: You are a business simulator engine. Write a 2-sentence corporate consequence story based on: "
            f"Situation: {self.current_scenario['situation']} | Action: {choice}. Don't mention points."
        )
        try:
            response = ollama.generate(model="phi3:mini", prompt=prompt)
            story = response['response'].strip()
            self.root.after(0, self.display_story, story)
        except:
            self.root.after(0, self.display_story, "The market reacted silently to your move.")

    def display_story(self, story):
        self.terminal.insert(tk.END, f"Outcome: {story}\n")
        self.terminal.see(tk.END)
        self.round += 1
        self.root.after(1000, self.next_round)

    def update_stats_display(self):
        self.cash_label.config(text=f"Cash: ${self.cash:,}")
        self.tech_bar['value'] = self.tech
        self.morale_bar['value'] = self.morale

    def end_game(self, reason):
        self.scenario_box.config(text=f"GAME OVER: {reason}", fg="#ff5555")
        self.btn1.config(state="disabled")
        self.btn2.config(state="disabled")

    def load_scenarios(self):
        return [
            {"situation": "Server stack crashed during peak traffic.", "options": ["Hire cloud experts ($20k)", "Force dev all-nighter"], "impact": [{"cash": -20000, "tech": 10, "morale": 0}, {"cash": 0, "tech": 5, "morale": -20}]},
            {"situation": "Competitor launched a viral smear campaign.", "options": ["Counter with $30k ads", "Focus on features"], "impact": [{"cash": -30000, "tech": 0, "morale": 5}, {"cash": 0, "tech": 15, "morale": -5}]},
            {"situation": "Team is burnt out from the last sprint.", "options": ["Company retreat ($10k)", "Push for deadline"], "impact": [{"cash": -10000, "tech": 0, "morale": 20}, {"cash": 0, "tech": 10, "morale": -30}]},
            {"situation": "VC offers a grant for strict auditing.", "options": ["Pay for audit ($15k)", "Reject the grant"], "impact": [{"cash": 40000, "tech": 5, "morale": -10}, {"cash": 0, "tech": 0, "morale": 5}]},
            {"situation": "A major cyberattack targeted your database.", "options": ["Pay PR team ($25k)", "Stealth patch"], "impact": [{"cash": -25000, "tech": 5, "morale": 0}, {"cash": 0, "tech": 20, "morale": -20}]}
        ]

if __name__ == "__main__":
    root = tk.Tk()
    app = StartupSimulator(root)
    root.mainloop()
