import os
import re
import sys
from pathlib import Path

comfyui_path = r"E:\AI Stuff\ComfyUI"
if comfyui_path not in sys.path:
    sys.path.insert(0, comfyui_path)


import folder_paths

# DEBUG pathlib (to replace folder_path from OS)

BASE_DIR = Path.cwd()
DATAPATH = BASE_DIR.joinpath("custom_nodes", "ComfyUI-Universal-Styler", "CSV")

my_database = [str(file) for file in DATAPATH.glob("*.csv")]

# Show Text v0.3 ##########################################################################
################

class ShowText:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            },
        }

    INPUT_IS_LIST = True
    RETURN_TYPES = ("STRING",)
    FUNCTION = "notify"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (True,)

    CATEGORY = "✴️ Universal NAI Nodes"

    def notify(self, text, unique_id=None, extra_pnginfo=None):
        if unique_id is not None and extra_pnginfo is not None:
            if not isinstance(extra_pnginfo, list):
                print("Error: extra_pnginfo is not a list")
            elif (
                not isinstance(extra_pnginfo[0], dict)
                or "workflow" not in extra_pnginfo[0]
            ):
                print("Error: extra_pnginfo[0] is not a dict or missing 'workflow' key")
            else:
                workflow = extra_pnginfo[0]["workflow"]
                node = next(
                    (x for x in workflow["nodes"] if str(x["id"]) == str(unique_id[0])),
                    None,
                )
                if node:
                    node["widgets_values"] = [text]

        return {"ui": {"text": text}, "result": (text,)}

################
# Nai Styler Complex CSV Loader v0.3 ##########################################################################
################

class NaiStylerComplexCSVLoader:

    @staticmethod
    def load_naistyles_csv(naistyles_path: str):
        """Loads naistyles CSV file, ignoring the first row (header)."""
        naistyles = {"Error loading naistyles.csv, check the console": ["", ""]}
        if not os.path.exists(naistyles_path):
            print(f"""Error. No naistyles.csv found. Put your naistyles.csv in the custom_nodes/ComfyUI-Universal-Styler/CSV directory of ComfyUI. Then press "Refresh".
                  Your current root directory is: {folder_paths.base_path}
            """)
            return naistyles
        try:
            with open(naistyles_path, "r", encoding="utf-8") as f:
                naistyles = [[x.replace('"', '').replace('\n', '') for x in re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', line)] for line in f.readlines()[1:]]
                naistyles = {x[0]: [x[1], x[2]] for x in naistyles}
        except Exception as e:
            print(f"""Error loading naistyles.csv. Make sure it is in the custom_nodes/ComfyUI-Universal-Styler/CSV directory of ComfyUI. Then press "Refresh".
                    Your current root directory is: {folder_paths.base_path}
                    Error: {e}
            """)
        return naistyles

    @classmethod
    def INPUT_TYPES(cls):
        cls.naistyles_csv = cls.load_naistyles_csv(os.path.join(folder_paths.base_path, "custom_nodes", "ComfyUI-Universal-Styler", "CSV", "naistyles.csv"))
        return {
            "required": {
                "naistyles": (list(cls.naistyles_csv.keys()),),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"
    CATEGORY = "✴️ Universal NAI Nodes"

    def execute(self, naistyles):
        return (self.naistyles_csv[naistyles][0],)

################
# Nai Styler v0.1 ##########################################################################
################

class NaiStyler:
    """A custom node for styling."""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP",),
                "mute": (["On", "Off"],),
                "mix": ("INT", {
                    "default": 50,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "float_field": ("FLOAT", {
                    "default": 0.5,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "round": 0.001,
                    "display": "slider"
                }),
                "string_field": ("STRING", {
                    "multiline": True,
                    "default": "Define Object"
                }),
                "string_field2": ("STRING", {
                    "multiline": True,
                    "default": "Define Background"
                }),
            },
        }

    RETURN_TYPES = ("CONDITIONING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("Compiled prompt", "Value", "Value2", "mix")
    FUNCTION = "test"
    CATEGORY = "✴️ Universal NAI Nodes"

    def test(self, string_field, string_field2, mix, float_field, mute):
        if mute == "On":
            print(f"""Your input contains:
                string_field: {string_field}
                int_field: {mix}
                float_field: {float_field}
            """)

################
# Concatenate Fields v0.1 ##########################################################################
################

class ConcatenateFields:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text1": ("STRING", {"multiline": False, "default": "Hello"}),
                "text2": ("STRING", {"multiline": False, "default": "World"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate_text"
    CATEGORY = "✴️ Universal NAI Nodes"

    def concatenate_text(self, text1, text2):
        return (text1 + " " + text2,)

################
# Node Class and Display Name Mappings ##########################################################################
################

NODE_CLASS_MAPPINGS = {
    "ShowText": ShowText,
    "NaiStylerComplexCSVLoader": NaiStylerComplexCSVLoader,
    "NaiStyler": NaiStyler,
    "ConcatenateFields": ConcatenateFields,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ShowText": "✴️ U-NAI Get Text",
    "NaiStylerComplexCSVLoader": "✴️ U-NAI Styles Launcher",
    "NaiStyler": "✴️ U-NAI Styler - v0.2.1",
    "ConcatenateFields": "✴️ U-NAI Fields Concatenate",
}