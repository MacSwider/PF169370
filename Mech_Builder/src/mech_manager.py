import os
import json

DATA_DIR = os.path.join(os.getcwd(), "data")
MECH_DATA_FOLDER = os.path.join(DATA_DIR, "mech_data")
ARM_WEAPON_FILE = os.path.join(DATA_DIR, "weapons.json")
BACK_WEAPON_FILE = os.path.join(DATA_DIR, "back_weapons.json")
KEYWORD_FILE = os.path.join(DATA_DIR, "keywords.json")
ABILITY_FILE = os.path.join(DATA_DIR, "abilities.json")
WARGEAR_FILE = os.path.join(DATA_DIR, "wargear.json")


def load_mech_files():
    # Return list of files with mechs

    files = [f for f in os.listdir(MECH_DATA_FOLDER) if f.endswith(".json")]
    return [os.path.splitext(f)[0] for f in files]


def load_mech_data(mech_name):
    # Load mechs data from JSON.
    # Convert mech name to lowercase and remove -Class suffix
    # Faster than renaming every json file
    file_name = mech_name.lower().replace("-class", "")
    path = os.path.join(MECH_DATA_FOLDER, file_name + ".json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if "armor" not in data:
            kinetic = data.get("Kinetic-Armor", 0)
            thermal = data.get("Thermal-Armor", 0)
            chemical = data.get("Chemical-Armor", 0)
            data["armor"] = (
                f"Kinetic: {kinetic}, Thermal: {thermal}, Chemical: {chemical}"
            )

        return data
    except Exception as e:
        print(f"Loading Error {path}: {e}")
        return {}


def load_weapons(filename):
    # Load weapons data from json

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Loading Error {filename}: {e}")
        return {}


def load_keywords():
    # Load keywords dictionary from JSON

    if not os.path.exists(KEYWORD_FILE) or os.path.getsize(KEYWORD_FILE) == 0:
        return {}
    try:
        with open(KEYWORD_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Loading Error {KEYWORD_FILE}: {e}")
        return {}


def load_ability_descriptions(filename=ABILITY_FILE):
    # Load abilities and its discription from JSON

    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Loading Error {filename}: {e}")
        return {}


def describe_weapon(weapon_name, weapons):
    # Return weapon description with its statistic as text
    if not weapon_name or weapon_name not in weapons:
        return "No Data"

    w = weapons.get(weapon_name, {})
    try:
        aim = w.get("aim_assist")
        strength = w.get("strength")
        damage = w.get("damage")
        range_ = w.get("range")
        keywords = w.get("keywords", [])

        # Handling values
        aim = (
            str(round(float(aim)))
            if isinstance(aim, (int, float))
            else str(aim)
            if aim
            else "None"
        )
        strength = str(eval(str(strength))) if strength else "None"
        damage = str(damage) if damage else "None"
        range_ = str(range_) if range_ else "None"

        damage_type = keywords[0] if keywords else "None"
        keyword_tags = ", ".join(keywords[1:]) if len(keywords) > 1 else "None"

        return (
            f"Damage Type: {damage_type}\n"
            f"Aim Assist: {aim}\n"
            f"Strength: {strength}\n"
            f"Damage: {damage}\n"
            f"Range: {range_}\n"
            f"Keywords: {keyword_tags}"
        )

    except Exception as e:
        return f"Weapon description error: {str(e)}"


def load_wargear(filename=WARGEAR_FILE):
    # load list of wargear
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Could not read: {filename}: {e}")
        return {}


def calculate_carrying_weight(mech, arm_weapons, back_weapons):
    # Calculate weapons weight and max_weight of mech
    type_limits = {"light": 15, "medium": 20, "heavy": 25}

    # Default type
    mech_type = mech.get("type", "medium").lower()

    # Overwrite if there is keyword that describe weight
    keywords = [k.lower() for k in mech.get("keywords", [])]
    for keyword in keywords:
        if keyword in type_limits:
            mech_type = keyword
            break

    max_carry = type_limits.get(mech_type, 20)
    total_weight = 0

    for slot, weapon_name in mech.get("weapons", {}).items():
        if not weapon_name:
            continue
        weapon_data = arm_weapons.get(weapon_name) or back_weapons.get(weapon_name)
        if weapon_data:
            weight = weapon_data.get("weight", 0)
            total_weight += weight

    mech["carrying_weight"] = total_weight
    mech["max_carry"] = max_carry
