"""
main.py
The main file with tkinter for the loot generation
"""

import tkinter as tk
from tkinter import ttk, messagebox

from loot_model import Character
from loot_service import LootService
from storage_loot import save_loot_history
from storage_characters import load_characters, save_characters, modify_character

class LootApp(tk.Tk):
    """Main application window for the loot generation GUI."""
    
    def __init__(self):
        super().__init__()
        self.title("Loot Generator")
        self.geometry("800x500")
        
        self.loot_service: LootService = LootService()
        self.characters: list[Character] = load_characters()
        
        self._create_widgets()
        self._layout_widgets()
        self._populate_classes()
        self._populate_character_dropdown()
    
    def _create_widgets(self):
        """Create all the widgets for the GUI."""
        self.label_name = tk.Label(self, text="Character Name:")
        self.entry_name = tk.Entry(self)
        
        self.label_class = tk.Label(self, text="Class:")
        self.combo_class = ttk.Combobox(self, state="readonly")
        
        self.label_level = tk.Label(self, text="Level (1–20):")
        self.spin_level = tk.Spinbox(self, from_=1, to=20)
        self.spin_level.delete(0, tk.END)
        self.spin_level.insert(0, "1")
        
        self.button_generate = tk.Button(self, text="Generate Loot", command=self._generate_loot_clicked)
        self.button_save = tk.Button(self, text="Save / Update Character", command=self._save_character_clicked)
        
        self.label_existing = tk.Label(self, text="Existing Characters:")
        self.combo_existing = ttk.Combobox(self, state="readonly")
        
        self.text_loot = tk.Text(self, height=10, width=50, state="disabled")
        self.label_status = tk.Label(self, text="Ready.", anchor="w")
        
    def _layout_widgets(self):
        """Place all the widgets in the GUI using grid layout."""
        self.label_name.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.entry_name.grid(row=1, column=0, sticky="we", padx=10)
        self.label_class.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.combo_class.grid(row=3, column=0, sticky="we", padx=10)
        self.label_level.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))
        self.spin_level.grid(row=5, column=0, sticky="w", padx=10)
        self.button_generate.grid(row=6, column=0, sticky="we", padx=10, pady=(10, 5))
        self.button_save.grid(row=7, column=0, sticky="we", padx=10, pady=(0, 10))
        self.label_existing.grid(row=8, column=0, sticky="w", padx=10, pady=(10, 0))
        self.combo_existing.grid(row=9, column=0, sticky="we", padx=10, pady=(0, 10))
        
        self.text_loot.grid(row=0, column=1, rowspan=10, padx=10, pady=10, sticky="nsew")
        self.label_status.grid(row=10, column=0, columnspan=2, sticky="we", padx=10, pady=(0, 10))
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(9, weight=1)
        
    def _populate_classes(self):
        """Populate the class dropdown with available character classes."""
        classes = ["Warrior", "Rogue", "Wizard"]
        self.combo_class['values'] = classes
        if classes:
            self.combo_class.current(0)
    
    def _populate_character_dropdown(self):
        """Populate the existing character dropdown with loaded characters."""
        names = [f"{c.name} ({c.char_class} L{c.level})" for c in self.characters]
        self.combo_existing['values'] = names
        if names:
            self.combo_existing.current(0)
            self.combo_existing.bind("<<ComboboxSelected>>", self.on_character_selected)
    
    def on_character_selected(self, event=None):
        """When a saved character is selected from the dropdown, populate the fields with its data."""
        index = self.combo_existing.current()
        if index >= 0 and index < len(self.characters):
            character = self.characters[index]
            self.entry_name.delete(0, tk.END)
            self.entry_name.insert(0, character.name)
            if character.char_class in self.combo_class['values']:
                self.combo_class.current(self.combo_class['values'].index(character.char_class))
            self.spin_level.delete(0, tk.END)
            self.spin_level.insert(0, str(character.level))
            self._set_status(f"Loaded character: {character.name}")
        
    def _save_character_clicked(self):
        """Save/update the character in characters.csv."""
        name = self.entry_name.get().strip()
        if not name:
            self._set_status("Character name cannot be empty.", is_error=True)
            messagebox.showwarning("Input Error", "Character name cannot be empty.")
            return

        char_class = self.combo_class.get().strip()
        if not char_class:
            self._set_status("Character class must be selected.", is_error=True)
            messagebox.showwarning("Input Error", "Please select a character class.")
            return

        try:
            level = int(self.spin_level.get())
        except ValueError:
            self._set_status("Level must be a number between 1 and 20.", is_error=True)
            messagebox.showwarning("Input Error", "Level must be a number between 1 and 20.")
            return

        if level < 1 or level > 20:
            self._set_status("Level must be between 1 and 20.", is_error=True)
            messagebox.showwarning("Input Error", "Level must be between 1 and 20.")
            return

        character = Character(name=name, char_class=char_class, level=level)

        modify_character(self.characters, character)
        save_characters(self.characters)
        self._populate_character_dropdown()
        self._set_status("Character saved/updated.", is_error=False)
        
    def _generate_loot_clicked(self):
        """Generate loot for the selected character."""
        name: str = self.entry_name.get().strip()
        if not name:
            self._set_status("Character name cannot be empty.", is_error=True)
            messagebox.showwarning("Input Error", "Character name cannot be empty.")
            return
        char_class: str = self.combo_class.get().strip()
        if not char_class:
            self._set_status("Character class must be selected.", is_error=True)
            messagebox.showwarning("Input Error", "Please select a character class.")
            return
        try:
            level: int = int(self.spin_level.get())
        except ValueError:
            self._set_status("Level must be a number between 1 and 20.", is_error=True)
            messagebox.showwarning("Input Error", "Level must be a number between 1 and 20.")
            return

        if level < 1 or level > 20:
            self._set_status("Level must be between 1 and 20.", is_error=True)
            messagebox.showwarning("Input Error", "Level must be between 1 and 20.")
            return

        character = Character(name=name, char_class=char_class, level=level)
        
        try:
            item = self.loot_service.generate_loot_for_character(character)
        except Exception as e:
            self._set_status(f"Error generating loot: {e}", is_error=True)
            messagebox.showerror("Loot Generation Error", f"An error occurred while generating loot: {e}")
            return

        save_loot_history(character, item)
        
        modifier_list = ", ".join(item.modifiers) if item.modifiers else "None"
        
        output = (
            f"Character: {character.name}\n"
            f"Level: {character.level}\n"
            f"Base Item: {item.base_item}\n"
            f"Full Name: {item.full_name}\n"
            f"Modifiers: {modifier_list}\n\n"
            f"Properties:\n{item.power}\n"
        )
        
        self._set_output(output)
        self._set_status(f"Loot generated for {character.name} and saved to history.", is_error=False)
        
        
    def _set_output(self, text: str):
        """Display text in the output box."""
        self.text_loot.config(state="normal")
        self.text_loot.delete("1.0", tk.END)
        self.text_loot.insert(tk.END, text)
        self.text_loot.config(state="disabled")
    
    def _set_status(self, text: str, is_error: bool = False):
        """Update status label"""
        self.label_status.config(text=text)
        if is_error:
            self.label_status.config(fg="red")
        else:
            self.label_status.config(fg="black")
    
    
def main():
    app = LootApp()
    app.mainloop()

if __name__ == "__main__":
    main()