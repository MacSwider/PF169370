import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add project directory to path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.saves import save_list_to_txt, load_mechs_from_txt


class TestSaveListToTxt(unittest.TestCase):
    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_success(self, mock_msgbox, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"
        data = [
            "Mech1 | Wargear: Shield | Weapons: left_arm: Laser",
            "Mech2 | Wargear: Boost | Weapons: right_arm: Rocket",
        ]

        save_list_to_txt(data)

        mock_file.assert_called_once_with("/path/to/file.txt", "w", encoding="utf-8")
        handle = mock_file()
        calls = [unittest.mock.call(f"{item}\n") for item in data]
        handle.write.assert_has_calls(calls)
        mock_msgbox.assert_called_once()

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open")
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_cancel(self, mock_msgbox, mock_file, mock_dialog):
        mock_dialog.return_value = ""  # User canceled
        data = ["Mech1", "Mech2"]

        save_list_to_txt(data)

        mock_file.assert_not_called()
        mock_msgbox.assert_not_called()

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    @patch("tkinter.messagebox.showerror")
    def test_save_list_to_txt_error(self, mock_error, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"
        data = ["Mech1", "Mech2"]

        save_list_to_txt(data)

        mock_file.assert_called_once()
        mock_error.assert_called_once()

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_custom_title(self, mock_msgbox, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"
        data = ["Mech1", "Mech2"]

        save_list_to_txt(data, title="Custom Title")

        mock_dialog.assert_called_once()
        self.assertEqual(mock_dialog.call_args[1]["title"], "Custom Title")

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_custom_filename(
        self, mock_msgbox, mock_file, mock_dialog
    ):
        mock_dialog.return_value = "/path/to/file.txt"
        data = ["Mech1", "Mech2"]

        save_list_to_txt(data, default_filename="custom.txt")

        mock_dialog.assert_called_once()
        self.assertEqual(mock_dialog.call_args[1]["initialfile"], "custom.txt")

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_empty_list(self, mock_msgbox, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"
        data = []

        save_list_to_txt(data)

        # Should still try to save an empty file
        mock_file.assert_called_once()
        mock_msgbox.assert_called_once()

    @patch("tkinter.filedialog.asksaveasfilename")
    @patch("builtins.open", new_callable=mock_open)
    @patch("tkinter.messagebox.showinfo")
    def test_save_list_to_txt_with_special_chars(
        self, mock_msgbox, mock_file, mock_dialog
    ):
        mock_dialog.return_value = "/path/to/file.txt"
        data = [
            "Mech1 | Wargear: Shield© | Uzbrojenie: left_arm: Laser™",
            "Mech2 | Wargear: Boost® | Uzbrojenie: right_arm: Rocket£",
        ]

        save_list_to_txt(data)

        mock_file.assert_called_once_with("/path/to/file.txt", "w", encoding="utf-8")
        handle = mock_file()
        calls = [unittest.mock.call(f"{item}\n") for item in data]
        handle.write.assert_has_calls(calls)


class TestLoadMechsFromTxt(unittest.TestCase):
    """Tests for loading mechs from text file"""

    @patch("tkinter.filedialog.askopenfilename")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Mech1 | Wargear: Shield | Weapons: left_arm: Laser, right_arm: Rocket\n"
        + "Mech2 | Wargear: Boost | Weapons: back_left: Missile",
    )
    def test_load_mechs_from_txt_success(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"

        result = load_mechs_from_txt()

        expected = [
            {
                "name": "Mech1",
                "wargear": "Shield",
                "weapons": {"left_arm": "Laser", "right_arm": "Rocket"},
            },
            {"name": "Mech2", "wargear": "Boost", "weapons": {"back_left": "Missile"}},
        ]

        self.assertEqual(result, expected)

    @patch("tkinter.filedialog.askopenfilename")
    def test_load_mechs_from_txt_cancel(self, mock_dialog):
        mock_dialog.return_value = ""  # User canceled

        result = load_mechs_from_txt()

        self.assertEqual(result, [])

    @patch("tkinter.filedialog.askopenfilename")
    @patch("builtins.open", new_callable=mock_open, read_data="Mech1\nMech2")
    def test_load_mechs_from_txt_simple_format(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"

        result = load_mechs_from_txt()

        expected = [
            {"name": "Mech1", "wargear": "None", "weapons": {}},
            {"name": "Mech2", "wargear": "None", "weapons": {}},
        ]

        self.assertEqual(result, expected)

    @patch("tkinter.filedialog.askopenfilename")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_mechs_from_txt_empty_file(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/empty.txt"

        result = load_mechs_from_txt()

        self.assertEqual(result, [])

    @patch("tkinter.filedialog.askopenfilename")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Mech1 | Wargear: Shield | Weapons: left_arm Laser",
    )  # missing „:”
    def test_load_mechs_from_txt_invalid_weapon_format(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"

        result = load_mechs_from_txt()

        expected = [{"name": "Mech1", "wargear": "Shield", "weapons": {}}]

        self.assertEqual(result, expected)

    @patch("tkinter.filedialog.askopenfilename")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_mechs_from_txt_empty_file(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/empty.txt"

        result = load_mechs_from_txt()

        self.assertEqual(result, [])

    @patch("tkinter.filedialog.askopenfilename")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="This is not a valid mech line",
    )
    def test_load_mechs_from_txt_invalid_line_format(self, mock_file, mock_dialog):
        mock_dialog.return_value = "/path/to/file.txt"

        result = load_mechs_from_txt()

        expected = [
            {"name": "This is not a valid mech line", "wargear": "None", "weapons": {}}
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
