import unittest
from unittest.mock import patch, mock_open
import os
import sys


from src.mech_manager import (
    load_mech_files,
    load_mech_data,
    load_weapons,
    load_keywords,
    load_ability_descriptions,
    describe_weapon,
    load_wargear,
    calculate_carrying_weight,
    DATA_DIR,
)


class TestLoadMechFiles(unittest.TestCase):
    """Tests for the load_mech_files function."""

    @patch("os.listdir")
    def test_load_mech_files(self, mock_listdir):
        mock_listdir.return_value = ["mech1.json", "mech2.json", "README.txt"]
        result = load_mech_files()
        self.assertEqual(result, ["mech1", "mech2"])

    @patch("os.listdir")
    def test_load_mech_files_empty(self, mock_listdir):
        mock_listdir.return_value = []
        result = load_mech_files()
        self.assertEqual(result, [])

    @patch("os.listdir")
    def test_load_mech_files_no_json(self, mock_listdir):
        mock_listdir.return_value = ["test_file.txt", "image.png"]
        result = load_mech_files()
        self.assertEqual(result, [])


class TestLoadMechData(unittest.TestCase):
    """Tests for the load_mech_data function."""

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            '{"name": "Test Mech", "HP": 10, "Kinetic-Armor": 5, '
            '"Thermal-Armor": 3, "Chemical-Armor": 2}'
        ),
    )
    def test_load_mech_data_success(self, mock_file):
        result = load_mech_data("test_mech")
        expected = {
            "name": "Test Mech",
            "HP": 10,
            "Kinetic-Armor": 5,
            "Thermal-Armor": 3,
            "Chemical-Armor": 2,
            "armor": "Kinetic: 5, Thermal: 3, Chemical: 2",
        }
        self.assertEqual(result, expected)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_mech_data_file_not_found(self, mock_file):
        result = load_mech_data("nonexistent_mech")
        self.assertEqual(result, {})

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"name": "Test Mech", "armor": "Custom Armor", "HP": 10}',
    )
    def test_load_mech_data_with_armor(self, mock_file):
        result = load_mech_data("test_mech")
        self.assertEqual(result["armor"], "Custom Armor")

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_mech_data_invalid_json(self, mock_file):
        result = load_mech_data("invalid_mech")
        self.assertEqual(result, {})

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"name": "Test Mech", "HP": 10}',
    )
    def test_load_mech_data_no_armor_values(self, mock_file):
        result = load_mech_data("test_mech")
        self.assertEqual(result["armor"], "Kinetic: 0, Thermal: 0, Chemical: 0")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"name": "Mech-über", "HP": 10, "armor": "Custom Armor"}',
    )
    def test_load_mech_data_unicode(self, mock_file):
        result = load_mech_data("unicode_mech")
        self.assertEqual(result["name"], "Mech-über")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"name": "Test Mech", "HP": 10, "Kinetic-Armor": 5}',
    )
    def test_load_mech_data_partial_armor(self, mock_file):
        result = load_mech_data("test_mech")
        self.assertEqual(result["armor"], "Kinetic: 5, Thermal: 0, Chemical: 0")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            '{"name": "Test Mech", "HP": 10, "SugarArmor": 5, '
            '"PlotArmor": 3, "ChemicalArmor": 2}'
        ),
    )
    def test_load_mech_data_nonstandard_armor_names(self, mock_file):
        result = load_mech_data("test_mech")
        # Should still default to 0 since it doesn't recognize these fields
        self.assertEqual(result["armor"], "Kinetic: 0, Thermal: 0, Chemical: 0")


class TestLoadWeapons(unittest.TestCase):
    """Tests for the load_weapons function."""

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"weapon1": {"damage": 5}, "weapon2": {"damage": 10}}',
    )
    def test_load_weapons_success(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_weapons("weapons.json")
        expected = {"weapon1": {"damage": 5}, "weapon2": {"damage": 10}}
        self.assertEqual(result, expected)

    @patch("os.path.exists")
    def test_load_weapons_file_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = load_weapons("nonexistent.json")
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_load_weapons_empty_file(self, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 0
        result = load_weapons("empty.json")
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_weapons_invalid_json(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_weapons("invalid.json")
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_load_weapons_io_error(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_weapons("weapons.json")
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open, read_data="{}")
    def test_load_weapons_empty_data(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 2
        result = load_weapons("weapons.json")
        self.assertEqual(result, {})


class TestLoadKeywords(unittest.TestCase):
    """Tests for the load_keywords function."""

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"keyword1": "desc1", "keyword2": "desc2"}',
    )
    def test_load_keywords_success(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_keywords()
        expected = {"keyword1": "desc1", "keyword2": "desc2"}
        self.assertEqual(result, expected)

    @patch("os.path.exists")
    def test_load_keywords_file_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = load_keywords()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_load_keywords_empty_file(self, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 0
        result = load_keywords()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"keyword1": "desc1", "keyword2": "desc2"}',
    )
    def test_load_keywords_custom_file(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        # we can load keywords from a custom file path if needed
        custom_path = os.path.join(DATA_DIR, "custom_keywords.json")
        with patch("src.mech_manager.KEYWORD_FILE", custom_path):
            result = load_keywords()
            expected = {"keyword1": "desc1", "keyword2": "desc2"}
            self.assertEqual(result, expected)


class TestLoadAbilityDescriptions(unittest.TestCase):
    """Tests for the load_ability_descriptions function."""

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"ability1": "desc1", "ability2": "desc2"}',
    )
    def test_load_ability_descriptions_success(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_ability_descriptions()
        expected = {"ability1": "desc1", "ability2": "desc2"}
        self.assertEqual(result, expected)

    @patch("os.path.exists")
    def test_load_ability_descriptions_file_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = load_ability_descriptions()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_ability_descriptions_invalid_json(
        self, mock_file, mock_size, mock_exists
    ):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_ability_descriptions()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"ability1": "desc1", "ability2": "desc2"}',
    )
    def test_load_ability_descriptions_custom_file(
        self, mock_file, mock_size, mock_exists
    ):
        mock_exists.return_value = True
        mock_size.return_value = 100
        custom_path = "/path/to/custom_abilities.json"
        result = load_ability_descriptions(custom_path)
        expected = {"ability1": "desc1", "ability2": "desc2"}
        self.assertEqual(result, expected)


class TestLoadWargear(unittest.TestCase):
    """Tests for the load_wargear function."""

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data='{"gear1": {"description": "desc1"}, "gear2": {"description": "desc2"}}',
    )
    def test_load_wargear_success(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_wargear()
        expected = {
            "gear1": {"description": "desc1"},
            "gear2": {"description": "desc2"},
        }
        self.assertEqual(result, expected)

    @patch("os.path.exists")
    def test_load_wargear_file_not_exist(self, mock_exists):
        mock_exists.return_value = False
        result = load_wargear()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_load_wargear_empty_file(self, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 0
        result = load_wargear()
        self.assertEqual(result, {})

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_load_wargear_invalid_json(self, mock_file, mock_size, mock_exists):
        mock_exists.return_value = True
        mock_size.return_value = 100
        result = load_wargear()
        self.assertEqual(result, {})


class TestDescribeWeapon(unittest.TestCase):
    """Tests for the describe_weapon function."""

    def test_describe_weapon_success(self):
        weapons = {
            "test_weapon": {
                "aim_assist": 3,
                "strength": 5,
                "damage": "2d6",
                "range": '24"',
                "keywords": ["Kinetic", "Rapid Fire", "Heavy"],
            }
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertIn("Damage Type: Kinetic", result)
        self.assertIn("Aim Assist: 3", result)
        self.assertIn("Strength: 5", result)
        self.assertIn("Damage: 2d6", result)
        self.assertIn('Range: 24"', result)
        self.assertIn("Keywords: Rapid Fire, Heavy", result)

    def test_describe_weapon_none(self):
        result = describe_weapon(None, {})
        self.assertEqual(result, "No Data")

    def test_describe_weapon_not_in_weapons(self):
        result = describe_weapon("unknown_weapon", {"weapon1": {}})
        self.assertEqual(result, "No Data")

    def ftest_describe_weapon_one_keyword(self):
        weapons = {
            "test_weapon": {
                "aim_assist": 3,
                "strength": 5,
                "damage": "2d6",
                "range": '24"',
                "keywords": ["Kinetic"],
            }
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertIn("Damage type: Kinetic", result)
        self.assertIn("Keywords: None", result)

    def test_describe_weapon_missing_fields(self):
        weapons = {
            "test_weapon": {
                "keywords": ["Kinetic", "Rapid Fire"]
            }
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertIn("Damage Type: Kinetic", result)
        self.assertIn("Aim Assist: None", result)
        self.assertIn("Strength: None", result)
        self.assertIn("Keywords: Rapid Fire", result)

    def test_describe_weapon_numeric_values(self):
        weapons = {
            "test_weapon": {
                "aim_assist": 4,
                "strength": "6",  # String instead of int
                "damage": 4,
                "range": 24,
                "keywords": ["Kinetic", "Burst Fire"],
            }
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertIn("Aim Assist: 4", result)
        self.assertIn("Strength: 6", result)

    def test_describe_weapon_missing_keywords(self):
        weapons = {
            "test_weapon": {
                "aim_assist": 4,
                "strength": 6,
                "damage": "2d6",
                "range": '24"',
                # No keywords field
            }
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertIn("Damage Type: None", result)
        self.assertIn("Keywords: None", result)

    def test_describe_weapon_exception(self):
        weapons = {
            "test_weapon": None  # Will cause an exception when accessed
        }
        result = describe_weapon("test_weapon", weapons)
        self.assertTrue(result.startswith("Weapon description error:"))


class TestCalculateCarryingWeight(unittest.TestCase):
    """Tests for the calculate_carrying_weight function."""

    def test_calculate_carrying_weight_light(self):
        mech = {
            "type": "light",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 15)

    def test_calculate_carrying_weight_medium(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_heavy(self):
        mech = {
            "type": "heavy",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 25)

    def test_calculate_carrying_weight_keyword_override(self):
        mech = {
            "type": "medium",
            "keywords": ["Heavy"],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 25)

    def test_calculate_carrying_weight_keyword_light_override(self):
        mech = {
            "type": "medium",
            "keywords": ["Light"],
            "weapons": {"left_arm": "weapon1"},
        }
        arm_weapons = {"weapon1": {"weight": 5}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 5)
        self.assertEqual(mech["max_carry"], 15)

    def test_calculate_carrying_weight_no_type(self):
        mech = {
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 20)  # Default medium

    def test_calculate_carrying_weight_mixed_weapons(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "back_left": "back1"},
        }
        arm_weapons = {"weapon1": {"weight": 5}}
        back_weapons = {"back1": {"weight": 8}}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 13)
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_unknown_weapon(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "unknown", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 7)  # Unknown weapon ignored
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_no_weapons(self):
        mech = {"type": "medium", "keywords": [], "weapons": {}}
        arm_weapons = {}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 0)
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_no_weapons_field(self):
        mech = {"type": "medium", "keywords": []}  # No weapons field
        arm_weapons = {"weapon1": {"weight": 5}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 0)
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_missing_weapon_weight(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon1": {}, "weapon2": {"weight": 7}}  # weapon1 has no weight
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 7)  # Only weapon2's weight counted
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_duplicate_weapon(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "shared_weapon", "right_arm": "weapon2"},
        }
        arm_weapons = {"shared_weapon": {"weight": 5}, "weapon2": {"weight": 7}}
        back_weapons = {
            "shared_weapon": {"weight": 10}
        }  # Different weight for same name

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        # Should use arm_weapon definition (5) not back_weapon (10)
        self.assertEqual(mech["carrying_weight"], 12)
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_empty_weapon_name(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "", "right_arm": "weapon2"},
        }
        arm_weapons = {"weapon2": {"weight": 7}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 7)  # Empty weapon name ignored
        self.assertEqual(mech["max_carry"], 20)

    def test_calculate_carrying_weight_invalid_type(self):
        mech = {
            "type": "invalid_type",
            "keywords": [],
            "weapons": {"left_arm": "weapon1"},
        }
        arm_weapons = {"weapon1": {"weight": 5}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        self.assertEqual(mech["carrying_weight"], 5)
        self.assertEqual(mech["max_carry"], 20)  # Default to medium

    def test_calculate_carrying_weight_multiple_type_keywords(self):
        mech = {
            "type": "medium",
            "keywords": ["Heavy", "Light"],
            "weapons": {"left_arm": "weapon1"},
        }
        arm_weapons = {"weapon1": {"weight": 5}}
        back_weapons = {}

        calculate_carrying_weight(mech, arm_weapons, back_weapons)

        # Should take the first matching type in keywords
        self.assertEqual(mech["max_carry"], 25)  # Heavy comes first

    def test_calculate_carrying_weight_invalid_weight(self):
        mech = {
            "type": "medium",
            "keywords": [],
            "weapons": {"left_arm": "weapon1", "right_arm": "weapon2"},
        }
        arm_weapons = {
            "weapon1": {"weight": "heavy"},
            "weapon2": {"weight": 7},
        }  # Invalid weight type
        back_weapons = {}

        # Since no exception handling for this case, it should fail
        with self.assertRaises(Exception):
            calculate_carrying_weight(mech, arm_weapons, back_weapons)


if __name__ == "__main__":
    unittest.main()
