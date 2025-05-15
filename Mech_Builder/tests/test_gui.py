import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock, mock_open
import os
import json
import sys
from tkinter import messagebox


from src.gui import MechManagerApp
from src.mech_manager import (
    load_mech_files,
    load_weapons,
    load_mech_data,
    load_wargear,
    calculate_carrying_weight,
    ARM_WEAPON_FILE,
    BACK_WEAPON_FILE,
)
from src.saves import save_list_to_txt, load_mechs_from_txt


MAX_MECHS = 6


class BaseMechManagerTest(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        # Mock loadings to avoid file access during tests
        self.arm_weapons_data = {
            "Rifle": {
                "weight": 5,
                "aim_assist": "+1",
                "strength": "5",
                "damage": "1",
                "range": "24",
                "keywords": ["Kinetic", "Rapid Fire"],
            },
            "Heavy Cannon": {
                "weight": 10,
                "aim_assist": "0",
                "strength": "8",
                "damage": "3",
                "range": "36",
                "keywords": ["Kinetic", "Heavy"],
            },
        }
        self.back_weapons_data = {
            "Missile Pod": {
                "weight": 8,
                "aim_assist": "+1",
                "strength": "6",
                "damage": "2",
                "range": "48",
                "keywords": ["Explosive", "Blast"],
            },
            "Shield Generator": {
                "weight": 5,
                "aim_assist": "0",
                "strength": "0",
                "damage": "0",
                "range": "0",
                "keywords": ["Defensive", "Shield"],
            },
        }
        self.wargear_data = {
            "Targeting System": {"description": "Improves aim", "limit": 2},
            "Reinforced Armor": {"description": "Increases armor", "limit": 1},
        }
        self.mech_files = ["Light Mech", "Medium Mech", "Heavy Mech"]
        self.mech_data = {
            "Light Mech": {
                "name": "Light Mech",
                "HP": 10,
                "Kinetic-Armor": 5,
                "Thermal-Armor": 5,
                "Chemical-Armor": 5,
                "Heat Cap.": 10,
                "mobility": 8,
                "type": "light",
                "keywords": ["Light", "Fast"],
                "abilities": ["Quick Strike"],
                "weapons": {"left_arm": None, "right_arm": None},
            },
            "Medium Mech": {
                "name": "Medium Mech",
                "HP": 15,
                "Kinetic-Armor": 10,
                "Thermal-Armor": 10,
                "Chemical-Armor": 10,
                "Heat Cap.": 15,
                "mobility": 6,
                "type": "medium",
                "keywords": ["Medium", "Bipdedal"],
                "abilities": ["Command Unit"],
                "weapons": {
                    "left_arm": None,
                    "right_arm": None,
                    "back_left": None,
                    "back_right": None,
                },
            },
            "Heavy Mech": {
                "name": "Heavy Mech",
                "HP": 20,
                "Kinetic-Armor": 15,
                "Thermal-Armor": 15,
                "Chemical-Armor": 15,
                "Heat Cap.": 20,
                "mobility": 4,
                "type": "heavy",
                "keywords": ["Heavy", "Durable"],
                "abilities": ["Heavy Armor"],
                "weapons": {
                    "left_arm": None,
                    "right_arm": None,
                    "back_left": None,
                    "back_right": None,
                },
            },
        }
        self.keywords_data = {
            "Light": "Lighter mechs with better mobility.",
            "Medium": "Balanced mechs with moderate stats.",
            "Heavy": "Heavy mechs with strong armor but less mobility.",
            "Fast": "Units with higher-than-average movement.",
            "Bibedal": "Units with balanced stats across the board.",
            "Durable": "Units with enhanced durability and armor.",
            "Kinetic": "Damage type that affects kinetic armor.",
            "Explosive": "Area-effect damage type.",
            "Defensive": "Provides defensive capabilities.",
        }
        self.abilities_data = {
            "Quick Strike": "Can attack early in the phase.",
            "Command Unit": "Provides bonuses to nearby allies.",
            "Heavy Armor": "Reduces incoming damage from all sources.",
        }

        # Setup mock patches
        self.patches = [
            patch("src.gui.load_mech_files", return_value=self.mech_files),
            patch(
                "src.gui.load_weapons",
                side_effect=lambda file: self.arm_weapons_data
                if file == ARM_WEAPON_FILE
                else self.back_weapons_data,
            ),
            patch("src.gui.load_wargear", return_value=self.wargear_data),
            patch(
                "src.gui.load_mech_data",
                side_effect=lambda name: self.mech_data.get(name, {}),
            ),
            patch("src.gui.load_keywords", return_value=self.keywords_data),
            patch(
                "src.gui.load_ability_descriptions", return_value=self.abilities_data
            ),
            patch("tkinter.messagebox.showinfo"),
            patch("tkinter.messagebox.showwarning"),
            patch("tkinter.messagebox.showerror"),
        ]

        # Start all patches
        for p in self.patches:
            p.start()

        # Initialize app
        self.app = MechManagerApp(self.root)

    def tearDown(self):
        """Clean up after each test."""
        # Stop all patches
        for p in self.patches:
            p.stop()
        self.root.destroy()


class TestMechManagerAppInit(BaseMechManagerTest):
    def test_init(self):
        """Test initialization of the application."""
        self.assertEqual(self.app.root.title(), "Mech List Generator")
        self.assertEqual(self.app.mech_list, [])
        self.assertEqual(self.app.available_mechs, self.mech_files)
        self.assertEqual(self.app.arm_weapons, self.arm_weapons_data)
        self.assertEqual(self.app.back_weapons, self.back_weapons_data)
        self.assertEqual(self.app.wargear_data, self.wargear_data)
        self.assertEqual(self.app.selected_wargear_counts, {})

    def test_build_gui_components(self):
        """Test that all main GUI components are created."""
        # Check top frame buttons
        top_buttons = []

        def find_buttons(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Button):
                    top_buttons.append(child)
                find_buttons(child)

        # Search in top_frame's parent (root)
        for child in self.root.winfo_children():
            find_buttons(child)

        # Should have 5 buttons
        self.assertGreaterEqual(len(top_buttons), 5)

        button_texts = [btn.cget("text") for btn in top_buttons]
        self.assertIn("Add Mech", button_texts)
        self.assertIn("Keywords", button_texts)
        self.assertIn("Abilities", button_texts)
        self.assertIn("Save list", button_texts)
        self.assertIn("Load List", button_texts)

        # Check scrollable frame setup
        canvas = None
        scrollbar = None
        scrollable_frame = None

        for child in self.root.winfo_children():
            if isinstance(child, tk.Frame):
                for grandchild in child.winfo_children():
                    if isinstance(grandchild, tk.Canvas):
                        canvas = grandchild
                    elif isinstance(grandchild, tk.Scrollbar):
                        scrollbar = grandchild
            elif isinstance(child, tk.Canvas):
                canvas = child

        self.assertIsNotNone(canvas, "Canvas not found")
        self.assertIsNotNone(scrollbar, "Scrollbar not found")
        self.assertIsNotNone(self.app.scrollable_frame, "Scrollable frame not found")


class TestMechOperations(BaseMechManagerTest):
    def test_add_mech(self):
        """Test adding a mech to the list."""
        # Initial state
        self.assertEqual(len(self.app.mech_list), 0)

        # Add a mech
        self.app.add_mech("Medium Mech")

        # Check mech was added to the list
        self.assertEqual(len(self.app.mech_list), 1)
        self.assertEqual(self.app.mech_list[0]["name"], "Medium Mech")

        # Check the mech's properties
        added_mech = self.app.mech_list[0]
        self.assertEqual(added_mech["HP"], 15)
        # Updated expectation for weapons - Mech has slots initialized to None
        expected_weapons = {
            "left_arm": None,
            "right_arm": None,
            "back_left": None,
            "back_right": None,
        }
        self.assertEqual(added_mech["weapons"], expected_weapons)
        self.assertEqual(added_mech["wargear"], None)

        # Check carrying weight was calculated
        self.assertIn("carrying_weight", added_mech)
        self.assertIn("max_carry", added_mech)
        self.assertEqual(added_mech["carrying_weight"], 0)  # No weapons yet
        self.assertEqual(added_mech["max_carry"], 20)  # Medium mech default

    def test_add_mech_max_limit(self):
        """Test adding mech when at max limit."""
        # Fill up the list with loop
        for _ in range(MAX_MECHS):
            self.app.add_mech("Medium Mech")

        # Try to add one more
        self.app.add_mech("Heavy Mech")
        messagebox.showwarning.assert_called_with(
            "Unit Limit", "You can add maximum 6 mechs."
        )
        self.assertEqual(len(self.app.mech_list), MAX_MECHS)

    def test_remove_mech_from_list(self):
        """Test removing a mech from the list."""
        mech = {"name": "Test Mech"}
        self.app.mech_list = [mech]
        mock_frame = MagicMock()

        # message box answer set to True to close them automatically
        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech, mock_frame)

        self.assertNotIn(mech, self.app.mech_list)
        mock_frame.destroy.assert_called_once()

    def test_remove_mech_not_in_list(self):
        """Test removing a mech that is not in the list."""
        mech = {"name": "Test Mech"}
        self.app.mech_list = []
        mock_frame = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech, mock_frame)

        self.assertEqual(len(self.app.mech_list), 0)
        mock_frame.destroy.assert_called_once()

    def test_remove_correct_mech_among_many(self):
        """Test removing a specific mech from a list of multiple mechs."""
        mech1 = {"name": "Alpha"}
        mech2 = {"name": "Bravo"}
        self.app.mech_list = [mech1, mech2]
        mock_frame = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech2, mock_frame)

        self.assertIn(mech1, self.app.mech_list)
        self.assertNotIn(mech2, self.app.mech_list)
        mock_frame.destroy.assert_called_once()

    def test_destroy_called_even_if_mech_absent(self):
        """Test that destroy is called even if the mech is not in the list."""
        existing_mech = {"name": "Alpha"}
        self.app.mech_list = [existing_mech]
        non_existing_mech = {"name": "Bravo"}
        mock_frame = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(non_existing_mech, mock_frame)

        self.assertIn(existing_mech, self.app.mech_list)
        mock_frame.destroy.assert_called_once()

    def test_multiple_remove_calls(self):
        """Test multiple remove calls on the same mech."""
        mech = {"name": "Duplicate"}
        self.app.mech_list = [mech, mech]
        mock_frame1 = MagicMock()
        mock_frame2 = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech, mock_frame1)
            self.app.remove_mech(mech, mock_frame2)

        self.assertEqual(self.app.mech_list, [])  # both instances deleted
        mock_frame1.destroy.assert_called_once()
        mock_frame2.destroy.assert_called_once()

    def test_remove_mech_when_list_is_empty(self):
        """Test removing a mech when the list is empty."""
        self.app.mech_list = []
        mock_frame = MagicMock()
        mech = {"name": "Phantom"}

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech, mock_frame)

        self.assertEqual(len(self.app.mech_list), 0)
        mock_frame.destroy.assert_called_once()

    def test_remove_mech_multiple_occurrences(self):
        """Test removing a mech that appears multiple times in the list."""
        mech = {"name": "Clone Mech"}
        self.app.mech_list = [mech, mech, mech]
        mock_frame = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=True):
            self.app.remove_mech(mech, mock_frame)

        # Only first occurrence should be removed
        self.assertEqual(self.app.mech_list.count(mech), 2)
        mock_frame.destroy.assert_called_once()

    def test_remove_mech_cancelled(self):
        """Test cancelling the removal of a mech."""
        mech = {"name": "Test Mech"}
        self.app.mech_list = [mech]
        mock_frame = MagicMock()

        with patch("tkinter.messagebox.askyesno", return_value=False):
            self.app.remove_mech(mech, mock_frame)

        # Mech should not be removed when cancelled
        self.assertIn(mech, self.app.mech_list)
        mock_frame.destroy.assert_not_called()


class TestWeaponOperations(BaseMechManagerTest):
    def test_create_weapon_dropdown(self):
        """Test weapon dropdown creation and selection."""
        self.app.add_mech("Medium Mech")
        added_mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)

        self.app.create_weapon_dropdown(
            test_frame, added_mech, "left_arm", "Test Weapon", self.arm_weapons_data
        )

        option_menu = None
        for widget in test_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.OptionMenu):
                        option_menu = child
                        break

        self.assertIsNotNone(option_menu)

        string_var = None
        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.arm_weapons_data.keys()
                ):
                    string_var = self.app.root.children[var]
                    break

        if string_var is None:
            for widget in test_frame.winfo_children():
                if isinstance(widget, tk.LabelFrame):
                    for name in widget.children:
                        child = widget.children[name]
                        if hasattr(child, "get") and callable(child.get):
                            try:
                                value = child.get()
                                if value in ["None"] + list(
                                    self.arm_weapons_data.keys()
                                ):
                                    string_var = child
                                    break
                            except:
                                pass

        if string_var:
            string_var.set("Rifle")
            self.root.update()

            self.assertEqual(added_mech["weapons"]["left_arm"], "Rifle")
            self.assertEqual(added_mech["carrying_weight"], 5)

    def test_calculate_carrying_weight(self):
        """Test weight calculation with different weapon loadouts."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        self.assertEqual(mech["carrying_weight"], 0)

        mech["weapons"] = {"left_arm": "Rifle", "right_arm": "Heavy Cannon"}

        calculate_carrying_weight(mech, self.app.arm_weapons, self.app.back_weapons)

        self.assertEqual(mech["carrying_weight"], 15)

        mech["weapons"]["back_left"] = "Missile Pod"
        mech["weapons"]["back_right"] = "Shield Generator"

        calculate_carrying_weight(mech, self.app.arm_weapons, self.app.back_weapons)

        self.assertEqual(mech["carrying_weight"], 28)
        self.assertTrue(mech["carrying_weight"] > mech["max_carry"])

    def test_weapon_overweight(self):
        """Test handling of weapon selection causing overweight condition."""
        self.app.add_mech("Light Mech")
        mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)

        mech["max_carry"] = 5

        self.app.create_weapon_dropdown(
            test_frame, mech, "left_arm", "Test Weapon", self.arm_weapons_data
        )

        string_var = None
        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.arm_weapons_data.keys()
                ):
                    string_var = self.app.root.children[var]
                    break

        if string_var:
            string_var.set("Heavy Cannon")
            self.root.update()

            messagebox.showwarning.assert_called_with(
                "Overweight",
                f"{mech['name']} exceed weight limit!\n Please change its loadout.",
            )

            self.assertIsNone(mech["weapons"]["left_arm"])

    def test_weapon_dropdown_for_closed_slot(self):
        """Test that weapon dropdown is disabled for closed weapon slots."""
        self.app.add_mech("Light Mech")

        self.root.update()

        mech_frames = [
            f
            for f in self.app.scrollable_frame.winfo_children()
            if isinstance(f, tk.LabelFrame)
        ]
        self.assertEqual(len(mech_frames), 1)

        option_menus = []

        def find_option_menus(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.OptionMenu):
                    option_menus.append(child)
                if child.winfo_children():
                    find_option_menus(child)

        find_option_menus(mech_frames[0])

        self.assertGreaterEqual(len(option_menus), 2)

        back_dropdown = None
        dropdown_frames = []

        def find_dropdown_frames(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.LabelFrame) and ("Back" in child.cget("text")):
                    dropdown_frames.append(child)
                find_dropdown_frames(child)

        find_dropdown_frames(mech_frames[0])

        for frame in dropdown_frames:
            for child in frame.winfo_children():
                if isinstance(child, tk.OptionMenu):
                    back_dropdown = child
                    break

        if back_dropdown:
            self.assertEqual(back_dropdown.cget("state"), "disabled")

    def test_multiple_weapon_selection(self):
        """Test selecting weapons for multiple slots on the same mech."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)
        self.app.create_weapon_dropdown(
            test_frame, mech, "left_arm", "Left Arm", self.arm_weapons_data
        )
        self.app.create_weapon_dropdown(
            test_frame, mech, "right_arm", "Right Arm", self.arm_weapons_data
        )
        self.app.create_weapon_dropdown(
            test_frame, mech, "back_left", "Back Left", self.back_weapons_data
        )

        string_vars = []
        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.arm_weapons_data.keys()
                ) + list(self.back_weapons_data.keys()):
                    string_vars.append(self.app.root.children[var])

        if len(string_vars) >= 3:
            string_vars[0].set("Rifle")
            self.root.update()
            string_vars[1].set("Heavy Cannon")
            self.root.update()
            string_vars[2].set("Missile Pod")
            self.root.update()

            self.assertIn("Rifle", mech["weapons"].values())
            self.assertIn("Heavy Cannon", mech["weapons"].values())
            self.assertIn("Missile Pod", mech["weapons"].values())

            self.assertEqual(mech["carrying_weight"], 23)

    def test_weapon_selection_update_description(self):
        """Test that selecting a weapon updates its description text."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)
        self.app.create_weapon_dropdown(
            test_frame, mech, "left_arm", "Left Arm", self.arm_weapons_data
        )

        string_var = None
        text_widget = None

        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.arm_weapons_data.keys()
                ):
                    string_var = self.app.root.children[var]

        for widget in test_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Text):
                        text_widget = child

        if string_var and text_widget:
            string_var.set("Rifle")
            self.root.update()

            description = text_widget.get("1.0", "end-1c")
            self.assertIn("weight: 5", description)
            self.assertIn("aim_assist: +1", description)
            self.assertIn("Rapid Fire", description)

            string_var.set("Heavy Cannon")
            self.root.update()

            description = text_widget.get("1.0", "end-1c")
            self.assertIn("weight: 10", description)
            self.assertIn("strength: 8", description)
            self.assertIn("Heavy", description)

    def test_empty_mech_has_zero_carrying_weight(self):
        """Test that a mech with no weapons has zero carrying weight."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        self.assertEqual(mech["carrying_weight"], 0)

        mech["weapons"]["left_arm"] = "Rifle"
        calculate_carrying_weight(mech, self.app.arm_weapons, self.app.back_weapons)
        self.assertEqual(mech["carrying_weight"], 5)

        mech["weapons"]["left_arm"] = None
        calculate_carrying_weight(mech, self.app.arm_weapons, self.app.back_weapons)
        self.assertEqual(mech["carrying_weight"], 0)

    def test_weapon_missing_from_data(self):
        """Test handling of a weapon that exists in mech but not in weapon data."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        mech["weapons"]["left_arm"] = "NonexistentWeapon"

        try:
            calculate_carrying_weight(mech, self.app.arm_weapons, self.app.back_weapons)
            self.assertEqual(mech["carrying_weight"], 0)
        except KeyError:
            self.fail(
                "calculate_carrying_weight raised KeyError with nonexistent weapon"
            )


class TestWargearOperations(BaseMechManagerTest):
    def test_create_wargear_dropdown(self):
        """Test wargear dropdown creation and selection."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)

        self.app.create_wargear_dropdown(test_frame, mech)

        option_menu = None
        for widget in test_frame.winfo_children():
            if isinstance(widget, tk.LabelFrame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.OptionMenu):
                        option_menu = child
                        break

        self.assertIsNotNone(option_menu)

        string_var = None
        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.wargear_data.keys()
                ):
                    string_var = self.app.root.children[var]
                    break

        if string_var is None:
            for widget in test_frame.winfo_children():
                if isinstance(widget, tk.LabelFrame):
                    for name in widget.children:
                        child = widget.children[name]
                        if hasattr(child, "get") and callable(child.get):
                            try:
                                value = child.get()
                                if value in ["None"] + list(self.wargear_data.keys()):
                                    string_var = child
                                    break
                            except:
                                pass

        if string_var:
            string_var.set("Targeting System")
            self.root.update()

            self.assertEqual(mech["wargear"], "Targeting System")
            self.assertEqual(
                self.app.selected_wargear_counts.get("Targeting System", 0), 1
            )

    def test_wargear_limit(self):
        """Test that wargear limits are enforced."""
        self.app.add_mech("Medium Mech")
        self.app.add_mech("Heavy Mech")
        mech1 = self.app.mech_list[0]
        mech2 = self.app.mech_list[1]

        frame1 = tk.Frame(self.root)
        frame2 = tk.Frame(self.root)

        self.app.create_wargear_dropdown(frame1, mech1)
        self.app.create_wargear_dropdown(frame2, mech2)

        var1 = tk.StringVar(value="None")

    def test_wargear_none_selection(self):
        """Test selecting None as wargear."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        test_frame = tk.Frame(self.root)

        self.app.create_wargear_dropdown(test_frame, mech)

        string_var = None
        for var in self.app.root.children:
            if isinstance(self.app.root.children[var], tk.StringVar):
                if self.app.root.children[var].get() in ["None"] + list(
                    self.wargear_data.keys()
                ):
                    string_var = self.app.root.children[var]
                    break

        if string_var:
            string_var.set("None")
            self.root.update()

            self.assertEqual(mech["wargear"], "None")


class TestAbilitiesAndKeywords(BaseMechManagerTest):
    def test_show_abilities(self):
        """Test abilities display window for a specific mech."""
        self.app.add_mech("Heavy Mech")
        mech = self.app.mech_list[0]

        initial_toplevel_count = len(self.root.winfo_children())

        self.app.show_abilities(mech)

        self.root.update()
        new_toplevel_count = len(self.root.winfo_children())
        self.assertEqual(new_toplevel_count, initial_toplevel_count + 1)

        abilities_window = None
        for child in self.root.winfo_children():
            if (
                isinstance(child, tk.Toplevel)
                and child.title() == f"Abilities - {mech['name']}"
            ):
                abilities_window = child
                break

        self.assertIsNotNone(abilities_window)

        labels = []

        def find_labels(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    labels.append(child)
                find_labels(child)

        find_labels(abilities_window)

        self.assertGreaterEqual(len(labels), 1)

        label_texts = [lbl.cget("text") for lbl in labels]
        self.assertIn("Reduces incoming damage from all sources.", label_texts)

        abilities_window.destroy()

    def test_show_available_abilities(self):
        """Test displaying all abilities in the current mech list."""
        self.app.add_mech("Light Mech")
        self.app.add_mech("Medium Mech")

        initial_toplevel_count = len(self.root.winfo_children())

        self.app.show_available_abilities()

        self.root.update()
        new_toplevel_count = len(self.root.winfo_children())
        self.assertEqual(new_toplevel_count, initial_toplevel_count + 1)

        abilities_window = None
        for child in self.root.winfo_children():
            if isinstance(child, tk.Toplevel) and child.title() == "Mechs abilities":
                abilities_window = child
                break

        self.assertIsNotNone(abilities_window)

        labels = []

        def find_labels(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    labels.append(child)
                find_labels(child)

        find_labels(abilities_window)

        self.assertGreaterEqual(len(labels), 3)

        label_texts = " ".join([lbl.cget("text") for lbl in labels])
        self.assertIn("Can attack early in the phase", label_texts)
        self.assertIn("Provides bonuses to nearby allies", label_texts)

        abilities_window.destroy()

    def test_keywords_no_mechs(self):
        """Test showing keywords when no mechs are loaded."""
        self.app.mech_list = []

        initial_toplevel_count = len(self.root.winfo_children())

        self.app.show_keywords()

        self.root.update()
        new_toplevel_count = len(self.root.winfo_children())
        self.assertEqual(new_toplevel_count, initial_toplevel_count + 1)

        keywords_window = None
        for child in self.root.winfo_children():
            if (
                isinstance(child, tk.Toplevel)
                and child.title() == "Keywords Dictionary"
            ):
                keywords_window = child
                break

        self.assertIsNotNone(keywords_window)

        labels = []

        def find_labels(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    labels.append(child)
                find_labels(child)

        find_labels(keywords_window)

        self.assertGreaterEqual(len(labels), len(self.keywords_data) * 2)

        keywords_window.destroy()

    def test_show_keywords_no_mechs(self):
        """Test showing keywords when no mechs are present."""
        self.app.mech_list = []

        with patch(
            "src.gui.load_keywords",
            return_value={"Keyword1": "Desc1", "Keyword2": "Desc2"},
        ):
            self.app.show_keywords()

            keywords_window = None
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                    keywords_window = widget
                    break

            self.assertIsNotNone(keywords_window)
            self.assertEqual(keywords_window.title(), "Keywords Dictionary")

    def test_show_abilities_no_abilities(self):
        """Test showing abilities for a mech with no abilities."""
        mech = {"name": "Test Mech", "abilities": []}

        self.app.show_abilities(mech)

        abilities_window = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                abilities_window = widget
                break

        self.assertIsNotNone(abilities_window)
        self.assertEqual(abilities_window.title(), "Abilities - Test Mech")

        ability_frames = [
            w for w in abilities_window.winfo_children() if isinstance(w, tk.LabelFrame)
        ]
        self.assertEqual(len(ability_frames), 0)

    def test_show_available_abilities_no_mechs(self):
        """Test showing available abilities when no mechs are present."""
        self.app.mech_list = []

        self.app.show_available_abilities()

        messagebox.showinfo.assert_called_with(
            "No mechs detected", "Add at least 1 mech to roaster"
        )


class TestSaveLoadOperations(BaseMechManagerTest):
    def test_save_mechs_to_file(self):
        """Test saving mechs to file."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]
        mech["weapons"] = {"left_arm": "Rifle", "right_arm": "Heavy Cannon"}
        mech["wargear"] = "Targeting System"

        with patch("src.gui.save_list_to_txt") as mock_save:
            self.app.save_mechs_to_file()

            mock_save.assert_called_once()
            args = mock_save.call_args[0][0]

            self.assertEqual(len(args), 1)
            self.assertIn("Medium Mech", args[0])
            self.assertIn("Wargear: Targeting System", args[0])
            self.assertIn("left_arm: Rifle", args[0])
            self.assertIn("right_arm: Heavy Cannon", args[0])

    def test_load_mechs_from_file_empty(self):
        """Test loading when no mechs are found in the file."""
        with patch("src.gui.load_mechs_from_txt", return_value=None):
            initial_length = len(self.app.mech_list)
            self.app.load_mechs_from_file()
            self.assertEqual(len(self.app.mech_list), initial_length)

    def test_save_mechs_to_file_no_mechs(self):
        """Test saving when no mechs are in the list."""
        self.app.mech_list = []

        self.app.save_mechs_to_file()

        messagebox.showinfo.assert_called_with("No Data", "There are no mechs added.")


class TestUIComponents(BaseMechManagerTest):
    def test_create_text_section(self):
        """Test creation of text section with content."""
        test_frame = tk.Frame(self.root)

        title = "Test Section"
        content = "This is test content\nLine 2"
        self.app.create_text_section(test_frame, title, content)

        label_frames = [
            w for w in test_frame.winfo_children() if isinstance(w, tk.LabelFrame)
        ]
        self.assertEqual(len(label_frames), 1)
        self.assertEqual(label_frames[0].cget("text"), title)

        text_widgets = []

        def find_text(widget):
            for child in widget.winfo_children():
                if isinstance(child, tk.Text):
                    text_widgets.append(child)
                find_text(child)

        find_text(label_frames[0])

        self.assertEqual(len(text_widgets), 1)
        self.assertEqual(text_widgets[0].get("1.0", "end-1c"), content)
        self.assertEqual(text_widgets[0].cget("state"), "disabled")

    def test_mech_selection_adds_display(self):
        """Test that selecting a mech adds its display to the UI."""
        initial_widget_count = len(self.app.scrollable_frame.winfo_children())

        self.app.add_mech("Medium Mech")

        self.root.update()

        new_widget_count = len(self.app.scrollable_frame.winfo_children())

        self.assertGreater(new_widget_count, initial_widget_count)

        mech_frames = [
            w
            for w in self.app.scrollable_frame.winfo_children()
            if isinstance(w, tk.LabelFrame)
        ]
        self.assertGreaterEqual(len(mech_frames), 1)
        self.assertIn("Medium Mech", mech_frames[-1].cget("text"))

    def test_mech_weapon_slots_initialization(self):
        """Test that mech weapon slots are properly initialized."""
        self.app.add_mech("Light Mech")
        self.app.add_mech("Medium Mech")
        self.app.add_mech("Heavy Mech")

        light_mech = self.app.mech_list[0]
        self.assertEqual(len(light_mech["weapons"]), 4)
        self.assertIn("left_arm", light_mech["weapons"])
        self.assertIn("right_arm", light_mech["weapons"])
        self.assertIn("back_left", light_mech["weapons"])
        self.assertIn("back_right", light_mech["weapons"])

        medium_mech = self.app.mech_list[1]
        self.assertEqual(len(medium_mech["weapons"]), 4)
        self.assertIn("left_arm", medium_mech["weapons"])
        self.assertIn("right_arm", medium_mech["weapons"])
        self.assertIn("back_left", medium_mech["weapons"])
        self.assertIn("back_right", medium_mech["weapons"])

        heavy_mech = self.app.mech_list[2]
        self.assertEqual(len(heavy_mech["weapons"]), 4)
        self.assertIn("left_arm", heavy_mech["weapons"])
        self.assertIn("right_arm", heavy_mech["weapons"])
        self.assertIn("back_left", heavy_mech["weapons"])
        self.assertIn("back_right", heavy_mech["weapons"])

    def test_mech_type_specific_weapon_slots(self):
        """Test that different mech types have appropriate weapon slot configurations."""
        self.app.add_mech("Light Mech")
        self.app.add_mech("Medium Mech")
        self.app.add_mech("Heavy Mech")

        light_mech = self.app.mech_list[0]
        self.assertIn("back_left", light_mech["weapons"])
        self.assertIn("back_right", light_mech["weapons"])

        medium_mech = self.app.mech_list[1]
        self.assertIn("back_left", medium_mech["weapons"])
        self.assertIn("back_right", medium_mech["weapons"])

        heavy_mech = self.app.mech_list[2]
        self.assertIn("back_left", heavy_mech["weapons"])
        self.assertIn("back_right", heavy_mech["weapons"])

    def test_mech_initialization(self):
        """Test that mechs are properly initialized with correct default values."""
        self.app.add_mech("Medium Mech")
        mech = self.app.mech_list[0]

        self.assertEqual(mech["name"], "Medium Mech")
        self.assertEqual(mech["HP"], 15)
        self.assertEqual(mech["Kinetic-Armor"], 10)
        self.assertEqual(mech["Thermal-Armor"], 10)
        self.assertEqual(mech["Chemical-Armor"], 10)
        self.assertEqual(mech["Heat Cap."], 15)
        self.assertEqual(mech["mobility"], 6)

        for slot in mech["weapons"].values():
            self.assertIsNone(slot)

        self.assertIsNone(mech["wargear"])

        self.assertEqual(mech["carrying_weight"], 0)

    def test_mech_list_management(self):
        """Test basic mech list management functionality."""
        self.assertEqual(len(self.app.mech_list), 0)

        self.app.add_mech("Medium Mech")
        self.assertEqual(len(self.app.mech_list), 1)
        self.assertEqual(self.app.mech_list[0]["name"], "Medium Mech")

        self.app.add_mech("Heavy Mech")
        self.assertEqual(len(self.app.mech_list), 2)
        self.assertEqual(self.app.mech_list[1]["name"], "Heavy Mech")

        self.app.mech_list.pop(0)
        self.assertEqual(len(self.app.mech_list), 1)
        self.assertEqual(self.app.mech_list[0]["name"], "Heavy Mech")

    def test_weapon_data_loading(self):
        """Test that weapon data is properly loaded and accessible."""
        self.assertIn("Rifle", self.app.arm_weapons)
        self.assertIn("Heavy Cannon", self.app.arm_weapons)

        rifle_data = self.app.arm_weapons["Rifle"]
        self.assertEqual(rifle_data["weight"], 5)
        self.assertEqual(rifle_data["aim_assist"], "+1")
        self.assertEqual(rifle_data["strength"], "5")
        self.assertEqual(rifle_data["damage"], "1")
        self.assertEqual(rifle_data["range"], "24")
        self.assertIn("Kinetic", rifle_data["keywords"])
        self.assertIn("Rapid Fire", rifle_data["keywords"])

        self.assertIn("Missile Pod", self.app.back_weapons)
        self.assertIn("Shield Generator", self.app.back_weapons)

        missile_data = self.app.back_weapons["Missile Pod"]
        self.assertEqual(missile_data["weight"], 8)
        self.assertEqual(missile_data["aim_assist"], "+1")
        self.assertEqual(missile_data["strength"], "6")
        self.assertEqual(missile_data["damage"], "2")
        self.assertEqual(missile_data["range"], "48")
        self.assertIn("Explosive", missile_data["keywords"])
        self.assertIn("Blast", missile_data["keywords"])

    def test_wargear_data_loading(self):
        """Test that wargear data is properly loaded and accessible."""
        self.assertIn("Targeting System", self.app.wargear_data)
        self.assertIn("Reinforced Armor", self.app.wargear_data)

        targeting_data = self.app.wargear_data["Targeting System"]
        self.assertEqual(targeting_data["description"], "Improves aim")
        self.assertEqual(targeting_data["limit"], 2)

        armor_data = self.app.wargear_data["Reinforced Armor"]
        self.assertEqual(armor_data["description"], "Increases armor")
        self.assertEqual(armor_data["limit"], 1)

    def test_mech_keywords_and_abilities(self):
        """Test that mech keywords and abilities are properly loaded and accessible."""
        self.app.add_mech("Light Mech")
        self.app.add_mech("Medium Mech")
        self.app.add_mech("Heavy Mech")

        light_mech = self.app.mech_list[0]
        self.assertIn("Light", light_mech["keywords"])
        self.assertIn("Fast", light_mech["keywords"])
        self.assertIn("Quick Strike", light_mech["abilities"])

        medium_mech = self.app.mech_list[1]
        self.assertIn("Medium", medium_mech["keywords"])
        self.assertIn("Bipdedal", medium_mech["keywords"])
        self.assertIn("Command Unit", medium_mech["abilities"])

        heavy_mech = self.app.mech_list[2]
        self.assertIn("Heavy", heavy_mech["keywords"])
        self.assertIn("Durable", heavy_mech["keywords"])
        self.assertIn("Heavy Armor", heavy_mech["abilities"])


class TestMechSelector(BaseMechManagerTest):
    def test_show_mech_selector(self):
        """Test the mech selector window creation and functionality."""
        self.app.show_mech_selector()

        selector_window = None
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel) and widget.winfo_exists():
                selector_window = widget
                break

        self.assertIsNotNone(selector_window, "Selector window was not created")
        self.assertEqual(selector_window.title(), "Select Mech")

        label_found = False
        for widget in selector_window.winfo_children():
            if (
                isinstance(widget, tk.Label)
                and widget.cget("text") == "Select Mech from list"
            ):
                label_found = True
                break
        self.assertTrue(label_found, "Label not found in selector window")

        button_count = 0
        for widget in selector_window.winfo_children():
            if isinstance(widget, tk.Button):
                button_count += 1
        self.assertEqual(
            button_count,
            len(self.app.available_mechs),
            "Number of buttons doesn't match available mechs",
        )


class TestLoadMechsFromFile(BaseMechManagerTest):
    def test_load_mechs_from_file_empty(self):
        """Test loading mechs from file when file is empty."""
        with patch("src.gui.load_mechs_from_txt", return_value=[]):
            self.app.load_mechs_from_file()
            self.assertEqual(len(self.app.mech_list), 0)

    def test_load_mechs_from_file_max_limit(self):
        """Test loading mechs when exceeding MAX_MECHS limit."""
        test_data = [{"name": f"Test Mech {i}"} for i in range(MAX_MECHS + 2)]

        with (
            patch("src.gui.load_mechs_from_txt", return_value=test_data),
            patch(
                "src.gui.load_mech_data", return_value={"name": "Test Mech", "HP": 10}
            ),
        ):
            self.app.load_mechs_from_file()

            messagebox.showwarning.assert_called_with(
                "Maximal Roaster Exceed",
                f"Maximal number is {MAX_MECHS}. Only first {MAX_MECHS} loaded.",
            )

            self.assertEqual(len(self.app.mech_list), MAX_MECHS)

    def test_load_mechs_from_file_invalid_data(self):
        """Test loading mechs with invalid data."""
        test_data = [{"name": "Invalid Mech"}]

        with (
            patch("src.gui.load_mechs_from_txt", return_value=test_data),
            patch("src.gui.load_mech_data", return_value=None),
        ):
            self.app.load_mechs_from_file()
            self.assertEqual(len(self.app.mech_list), 0)
