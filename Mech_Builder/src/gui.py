import tkinter as tk
from tkinter import messagebox
from src.mech_manager import (
    load_mech_files,
    load_weapons,
    load_mech_data,
    load_wargear,
    calculate_carrying_weight,
    load_keywords,
    load_ability_descriptions,
    ARM_WEAPON_FILE,
    BACK_WEAPON_FILE,
)
from src.saves import save_list_to_txt, load_mechs_from_txt


MAX_MECHS = 6


class MechManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mech List Generator")
        self.root.geometry("1100x700")

        self.mech_list = []
        self.available_mechs = load_mech_files()
        self.arm_weapons = load_weapons(ARM_WEAPON_FILE)
        self.back_weapons = load_weapons(BACK_WEAPON_FILE)
        self.wargear_data = load_wargear()
        self.selected_wargear_counts = {}

        self.build_gui()

    def save_mechs_to_file(self):
        if not self.mech_list:
            messagebox.showinfo("No Data", "There are no mechs added.")
            return

        data_lines = []
        for mech in self.mech_list:
            name = mech.get("name", "Unknown")
            wargear = mech.get("wargear", "None")
            weapons = mech.get("weapons", {})
            weapon_str = ", ".join(
                f"{slot}: {weapon}" for slot, weapon in weapons.items() if weapon
            )
            data_lines.append(f"{name} | Wargear: {wargear} | Weapons: {weapon_str}")

        save_list_to_txt(
            data_lines, title="Save mech list", default_filename="mech_list.txt"
        )

    def build_gui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.add_mech_button = tk.Button(
            top_frame, text="Add Mech", command=self.show_mech_selector
        )
        self.add_mech_button.pack(side=tk.LEFT, padx=5)

        self.keyword_button = tk.Button(
            top_frame, text="Keywords", command=self.show_keywords
        )
        self.keyword_button.pack(side=tk.LEFT, padx=5)

        self.abilities_button = tk.Button(
            top_frame, text="Abilities", command=self.show_available_abilities
        )
        self.abilities_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(
            top_frame, text="Save list", command=self.save_mechs_to_file
        )
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.load_button = tk.Button(
            top_frame, text="Load List", command=self.load_mechs_from_file
        )
        self.load_button.pack(side=tk.LEFT, padx=5)

        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame)
        self.scrollbar = tk.Scrollbar(
            canvas_frame, orient="vertical", command=self.canvas.yview
        )
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def show_mech_selector(self):
        selector_frame = tk.Toplevel(self.root)
        selector_frame.title("Select Mech")

        tk.Label(selector_frame, text="Select Mech from list").pack(pady=5)

        for name in self.available_mechs:
            tk.Button(
                selector_frame,
                text=name,
                width=30,
                command=lambda n=name, win=selector_frame: self.add_mech(n, win),
            ).pack(pady=2)

    def add_mech(self, mech_name, window=None):
        if len(self.mech_list) >= MAX_MECHS:
            messagebox.showwarning("Unit Limit", "You can add maximum 6 mechs.")
            return

        mech_data = load_mech_data(mech_name)
        if not mech_data:
            messagebox.showerror("Error", "Could not read mech data")
            return

        # Weapons and wargear initiliazed
        mech_data.setdefault("weapons", {})
        mech_data["wargear"] = None

        self.mech_list.append(mech_data)
        self.display_mech(mech_data)

        mech_data.setdefault("weapons", {})
        mech_data["wargear"] = None

        calculate_carrying_weight(mech_data, self.arm_weapons, self.back_weapons)

        if window:
            window.destroy()

    def remove_mech(self, mech, frame):
        confirm = messagebox.askyesno(
            "Deleting procesure", f"Are you  want to delete {mech['name']}?"
        )
        if not confirm:
            return

        if mech in self.mech_list:
            self.mech_list.remove(mech)

        # Wargear counter update
        wargear = mech.get("wargear")
        if wargear and wargear != "None":
            self.selected_wargear_counts[wargear] = (
                self.selected_wargear_counts.get(wargear, 1) - 1
            )
            if self.selected_wargear_counts[wargear] <= 0:
                del self.selected_wargear_counts[wargear]

        # Deletes mech's frame from GUI
        frame.destroy()

    def display_mech(self, mech):
        outer = tk.LabelFrame(
            self.scrollable_frame, text=f"{mech['name']}", padx=10, pady=10
        )
        outer.pack(fill=tk.X, padx=10, pady=10)

        button_frame = tk.Frame(outer)
        button_frame.pack(fill=tk.X)

        remove_btn = tk.Button(
            button_frame,
            text="Delete",
            fg="white",
            bg="red",
            command=lambda: self.remove_mech(mech, outer),
        )
        remove_btn.pack(side=tk.LEFT, padx=5, pady=5)

        top = tk.Frame(outer)
        top.pack(fill=tk.X)

        stats = (
            f"HP: {mech.get('HP', '?')}\n"
            f"Kinetic Armor: {mech.get('Kinetic-Armor', '?')}\n"
            f"Thermal Armor: {mech.get('Thermal-Armor', '?')}\n"
            f"Chemical Armor: {mech.get('Chemical-Armor', '?')}\n"
            f"Mobility: {mech.get('mobility', '?')}\n"
            f"Heat Capacity: {mech.get('Heat Cap.', '?')}\n"
        )

        self.create_text_section(top, "Statistics", stats)

        self.create_weapon_dropdown(
            top, mech, "left_arm", "Left Arm Weapon", self.arm_weapons
        )
        self.create_weapon_dropdown(
            top, mech, "right_arm", "Right Arm Weapon", self.arm_weapons
        )
        self.create_weapon_dropdown(
            top,
            mech,
            "back_left",
            "Left Back Weapon",
            self.back_weapons,
            disabled="back_left" not in mech.get("weapons", {}),
        )
        self.create_weapon_dropdown(
            top,
            mech,
            "back_right",
            "Right Back Weapon",
            self.back_weapons,
            disabled="back_right" not in mech.get("weapons", {}),
        )

        # Wargear dropdown
        self.create_wargear_dropdown(outer, mech)

        # Abilities and Keywords
        bot = tk.LabelFrame(outer, text="Keywords and Abilities")
        bot.pack(fill=tk.X, pady=5)

        keywords = ", ".join(mech.get("keywords", []))
        abilities = "\n".join(mech.get("abilities", []))

        if mech.get("abilities"):
            ability_button = tk.Button(
                outer, text="Abilities", command=lambda m=mech: self.show_abilities(m)
            )
            ability_button.pack(pady=5)

        content = f"Keywords: {keywords}\nAbilities:\n{abilities}"
        text = tk.Text(bot, height=4)
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        text.pack(fill=tk.X)

    def create_text_section(self, parent, title, content):
        frame = tk.LabelFrame(parent, text=title)
        frame.pack(side=tk.LEFT, padx=5, pady=5)

        text = tk.Text(frame, height=8, width=30)
        text.insert(tk.END, content)
        text.config(state=tk.DISABLED)
        text.pack()

    def create_weapon_dropdown(
        self, parent, mech, slot, label, weapon_dict, disabled=False
    ):
        frame = tk.LabelFrame(parent, text=label, padx=5, pady=5)
        frame.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

        var = tk.StringVar()
        current = mech["weapons"].get(slot)
        var.set(current if current else "None")

        options = list(weapon_dict.keys()) if not disabled else ["Slot Locked"]

        desc_text = tk.Text(frame, height=8, width=35, wrap=tk.WORD)
        desc_text.pack(pady=5)

        def describe_weapon(name):
            weapon = weapon_dict.get(name)
            if not weapon:
                return "no test_data"
            return "\n".join(
                f"{k}: {', '.join(v) if isinstance(v, list) else v}"
                for k, v in weapon.items()
            )

        def update_description(*args):
            selected = var.get()
            if selected in weapon_dict:
                mech["weapons"][slot] = selected
            else:
                mech["weapons"][slot] = None

            calculate_carrying_weight(mech, self.arm_weapons, self.back_weapons)

            if mech["carrying_weight"] > mech["max_carry"]:
                messagebox.showwarning(
                    "Overweight",
                    f"{mech['name']} exceed weight limit!\n Please change its loadout.",
                )
                mech["weapons"][slot] = None
                var.set("None")
                desc = "no test_data"
            else:
                desc = (
                    describe_weapon(selected)
                    if selected in weapon_dict
                    else "no test_data"
                )

            # Always update description field
            desc_text.config(state=tk.NORMAL)
            desc_text.delete("1.0", tk.END)
            desc_text.insert(tk.END, desc)
            desc_text.config(state=tk.DISABLED)

        var.trace_add("write", update_description)

        calculate_carrying_weight(mech, self.arm_weapons, self.back_weapons)
        if mech["carrying_weight"] > mech["max_carry"]:
            messagebox.showwarning("Overweight", f"{mech['name']} : load limit exceed!")

        menu = tk.OptionMenu(frame, var, options[0], *options)
        if disabled:
            menu.config(state=tk.DISABLED)
        menu.pack()

        update_description()

    def load_mechs_from_file(self):
        loaded_data = load_mechs_from_txt()
        if not loaded_data:
            return

        if len(loaded_data) > MAX_MECHS:
            messagebox.showwarning(
                "Maximal Roaster Exceed",
                f"Maximal number is {MAX_MECHS}. Only first {MAX_MECHS} loaded.",
            )
            loaded_data = loaded_data[:MAX_MECHS]

        self.mech_list = []  # Clear the list
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()  # Clear the GUI from previous mechs

        for mech in loaded_data:
            full_data = load_mech_data(mech["name"])
            if not full_data:
                continue
            full_data["weapons"] = mech.get("weapons", {})
            full_data["wargear"] = mech.get("wargear", "None")

            # Weapon and weight
            calculate_carrying_weight(full_data, self.arm_weapons, self.back_weapons)
            self.mech_list.append(full_data)
            self.display_mech(full_data)

    def create_wargear_dropdown(self, parent, mech):
        frame = tk.LabelFrame(parent, text="(Wargear)", padx=5, pady=5)
        frame.pack(fill=tk.X, padx=10, pady=5)

        wargear_var = tk.StringVar()
        wargear_var.set("None")

        options = ["None"] + list(self.wargear_data.keys())

        desc_text = tk.Text(frame, height=5, width=80)
        desc_text.pack(pady=5)

        def update_wargear(*args):
            selected = wargear_var.get()

            if selected == "None":
                mech["wargear"] = "None"
                desc_text.config(state=tk.NORMAL)
                desc_text.delete("1.0", tk.END)
                desc_text.insert(tk.END, "No wargear Selected.")
                desc_text.config(state=tk.DISABLED)
                return

            # Limit check
            count = self.selected_wargear_counts.get(selected, 0)
            limit = self.wargear_data.get(selected, {}).get("limit", None)
            if limit is not None and count >= limit:
                messagebox.showwarning(
                    "Limit exceded", f"Can't equip more than {limit} of {selected}."
                )
                wargear_var.set("None")
                return

            self.selected_wargear_counts[selected] = count + 1

            previous = mech.get("wargear")
            if previous and previous != "None":
                self.selected_wargear_counts[previous] = (
                    self.selected_wargear_counts.get(previous, 1) - 1
                )

            mech["wargear"] = selected

            desc = (
                self.wargear_data.get(selected, {}).get("description", "none test_data")
                if selected != "none"
                else "none"
            )
            limit_info = (
                f"(Limit: {self.wargear_data.get(selected, {}).get('limit', '-')})"
                if selected != "none"
                else ""
            )

            desc_text.config(state=tk.NORMAL)
            desc_text.delete("1.0", tk.END)
            desc_text.insert(tk.END, f"{desc}\n{limit_info}")
            desc_text.config(state=tk.DISABLED)

        wargear_var.trace_add("write", update_wargear)

        menu = tk.OptionMenu(frame, wargear_var, *options)
        menu.pack()

        mech["wargear"] = wargear_var.get()
        update_wargear()

    def show_keywords(self):
        keywords_dict = load_keywords()

        if self.mech_list:
            used_keywords = set()
            for mech in self.mech_list:
                used_keywords.update(mech.get("keywords", []))
                for weapon_name in mech.get("weapons", {}).values():
                    weapon_data = self.arm_weapons.get(
                        weapon_name
                    ) or self.back_weapons.get(weapon_name)
                    if weapon_data:
                        used_keywords.update(weapon_data.get("keywords", []))
        else:
            used_keywords = set(keywords_dict.keys())

        if not used_keywords:
            messagebox.showinfo("No keywords")
            return

        win = tk.Toplevel(self.root)
        win.title("Keywords" if self.mech_list else "Keywords Dictionary")

        table_frame = tk.Frame(win)
        table_frame.pack(padx=10, pady=10)

        tk.Label(
            table_frame,
            text="Keyword",
            font=("Arial", 10, "bold"),
            width=20,
            anchor="w",
        ).grid(row=0, column=0)
        tk.Label(
            table_frame,
            text="Description",
            font=("Arial", 10, "bold"),
            width=60,
            anchor="w",
        ).grid(row=0, column=1)

        for i, key in enumerate(sorted(used_keywords), start=1):
            desc = keywords_dict.get(key, "No description.")
            tk.Label(table_frame, text=key, anchor="w", width=20).grid(
                row=i, column=0, sticky="w"
            )
            tk.Label(
                table_frame,
                text=desc,
                anchor="w",
                width=60,
                wraplength=500,
                justify="left",
            ).grid(row=i, column=1, sticky="w")

    def show_abilities(self, mech):
        all_abilities = load_ability_descriptions()
        mech_abilities = mech.get("abilities", [])

        win = tk.Toplevel(self.root)
        win.title(f"Abilities - {mech['name']}")

        for ability in mech_abilities:
            desc = all_abilities.get(ability, "No description.")
            frame = tk.LabelFrame(win, text=ability, padx=10, pady=5)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=desc, wraplength=500, justify="left").pack(anchor="w")

    def show_available_abilities(self):
        if not self.mech_list:
            messagebox.showinfo("No mechs detected", "Add at least 1 mech to roaster")
            return

        all_abilities = load_ability_descriptions()
        used_abilities = set()

        for mech in self.mech_list:
            used_abilities.update(mech.get("abilities", []))

        if not used_abilities:
            messagebox.showinfo("No abilities")
            return

        win = tk.Toplevel(self.root)
        win.title("Mechs abilities")

        tk.Label(
            win, text="Mechs abilities in current squad", font=("Arial", 12, "bold")
        ).pack(pady=10)

        for ability in sorted(used_abilities):
            description = all_abilities.get(ability, "No description.")
            frame = tk.LabelFrame(win, text=ability, padx=10, pady=5)
            frame.pack(fill=tk.X, padx=10, pady=5)
            tk.Label(frame, text=description, wraplength=500, justify="left").pack(
                anchor="w"
            )
