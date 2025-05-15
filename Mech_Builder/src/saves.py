import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List, Dict


def save_list_to_txt(
    data_list: List[str],
    title: str = "Save as...",
    default_filename: str = "mechs_list.txt",
) -> None:
    """
    Save a list of strings to a text file.

    Args:
        data_list: List of strings to save
        title: Dialog window title
        default_filename: Default filename for save dialog
    """
    root = tk.Tk()
    root.withdraw()  # Hide tkinter window

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Pliki tekstowe", "*.txt")],
        title=title,
        initialfile=default_filename,
    )

    if not file_path:
        return  # User canceled save

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for item in data_list:
                f.write(f"{item}\n")
        messagebox.showinfo("List saved", f"List saved at:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Cound't save list:\n{e}")


def load_mechs_from_txt() -> List[Dict[str, str]]:
    """
    Load mech data from a text file.

    Returns:
        List of dictionaries containing mech data with keys:
        - name: str
        - wargear: str
        - weapons: Dict[str, str]
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        filetypes=[("Pliki tekstowe", "*.txt")], title="Load mech data"
    )

    if not file_path:
        return []

    mechs = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                name = parts[0].strip()
                wargear = "None"
                weapons = {}

                for part in parts[1:]:
                    if "Wargear:" in part:
                        wargear = part.split("Wargear:")[1].strip()
                    elif "Weapons:" in part:
                        weapon_str = part.split("Weapons:")[1].strip()
                        for item in weapon_str.split(","):
                            if ":" in item:
                                slot, weapon = item.strip().split(":", 1)
                                weapons[slot.strip()] = weapon.strip()

                mechs.append({"name": name, "wargear": wargear, "weapons": weapons})

        return mechs
    except Exception as e:
        messagebox.showerror("Loading Error", f"Error with:\n{e}")
        return []
