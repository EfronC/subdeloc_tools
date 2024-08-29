from modules import extract_subs
from modules import pairsubs
from modules import honorific_fixer
import json
import re

honorifics = {
	"honorifics": {
		"san": {
			"kanjis": ["さん"],
			"alternatives": ["Mr.", "Ms.", "Miss", "Mister"],
		},
		"sama": {
			"kanjis": ["さま", "様"],
			"alternatives": ["Lady", "Lord", "Sir", "Ma'am"],
		},
		"kun": {
			"kanjis": ["くん", "君"],
			"alternatives": [],
		},
		"chan": {
			"kanjis": ["ちゃん"],
			"alternatives": [],
		},
		"tan": {
			"kanjis": ["たん"],
			"alternatives": [],
		},
		"senpai": {
			"kanjis": ["先輩", "せんぱい"],
			"alternatives": [],
		},
		"sensei": {
			"kanjis": ["先生", "せんせい"],
			"alternatives": ["Teacher", "Master", "Doctor", "Professor"],
		},
		"dono": {
			"kanjis": ["殿"],
			"alternatives": ["Sir"],
		},
		"nee": {
			"kanjis": ["姉"],
			"alternatives": ["Big sis", "Sis"],
		},
	    "onee": {
	    	"kanjis": ["お姉"],
	    	"alternatives": ["Big sis", "Sis"],
	    },
	    "neechan": {
	    	"kanjis": ["姉ちゃん"],
	    	"alternatives": ["Big sis", "Sis"],
	    },
	    "oneechan": {
	    	"kanjis": ["お姉ちゃん"],
	    	"alternatives": ["Big sis", "Sis"],
	    },
	    "neesan": {
	    	"kanjis": ["姉さん"],
	    	"alternatives": ["Big sis", "Sis"],
	    },
	    "oneesan": {
	    	"kanjis": ["お姉さん"],
	    	"alternatives": ["Big sis", "Sis"],
	    },
	    "nii": {
	    	"kanjis": ["兄"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "onii": {
	    	"kanjis": ["お兄"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "niichan": {
	    	"kanjis": ["兄ちゃん"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "oniichan": {
	    	"kanjis": ["お兄ちゃん"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "niisan": {
	    	"kanjis": ["兄さん"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "oniisan": {
	    	"kanjis": ["お兄さん"],
	    	"alternatives": ["Big bro", "Bro"],
	    },
	    "otosan": {
	    	"kanjis": ["お父さん"],
	    	"alternatives": [],
	    },
	    "ojisan": {
	    	"kanjis": ["叔父さん","小父さん","伯父さん"],
	    	"alternatives": ["Uncle"],
	    },
	    "ojiisan": {
	    	"kanjis": ["お祖父さん","御爺さん","お爺さん","御祖父さん"],
	    	"alternatives": ["Grandfather", "Grandpa"],
	    },
	    "okaasan": {
	    	"kanjis": ["お母さん"],
	    	"alternatives": [],
	    },
	    "obasan": {
	    	"kanjis": ["伯母さん","小母さん","叔母さん"],
	    	"alternatives": ["Aunt"],
	    },
	    "obaasan": {
	    	"kanjis": ["お祖母さん","御祖母さん","御婆さん","お婆さん"],
	    	"alternatives": ["Grandmother", "Grandma"],
	    },
	    "baachan": {
	    	"kanjis": ["祖母ちゃん"],
	    	"alternatives": ["Grandmother", "Grandma"],
	    },
	    "baasan": {
	    	"kanjis": ["祖母さん"],
	    	"alternatives": ["Grandmother", "Grandma"],
	    },
	    "jiichan": {
	    	"kanjis": ["祖父ちゃん"],
	    	"alternatives": ["Grandfather", "Grandpa"],
	    },
	    "jiisan": {
	    	"kanjis": ["祖父さん"],
	    	"alternatives": ["Grandfather", "Grandpa"],
	    },
	}
}

names = {}

def print_to_file(data, filename="result.json"):
    """Writes the data to a JSON file."""
    with open(filename, "w", encoding="utf8") as output:
        json.dump(data, output, ensure_ascii=False, indent=2)

def main():
    s1 = "./eng.ass"
    s2 = "./jap.ass"

    # Assuming pairsubs.pair_files is defined elsewhere and returns a list of subtitles
    res = pairsubs.pair_files(s1, s2)
    s = search_honorifics(res)
    honorific_fixer.fix_original(s1, s)


def prepare_honor_array():
    """Prepares an array of all kanjis from the honorifics."""
    return [kanji for h in honorifics["honorifics"].values() for kanji in h["kanjis"]]

def search_honorifics(subs):
    """Searches for honorifics in the subtitles and processes them."""
    honor = prepare_honor_array()

    for sub in subs:
        for alternative in sub["alternative"]:
            for h in honor:
                if h in alternative["text"]:
                    check_sub(sub, h, alternative["text"])
                    break  # Exit loop after first match to avoid redundant checks

    #print_to_file(subs)
    return subs

def find_key_by_string(dictionary, target_string, search_array):
    """
    Finds the key in a dictionary whose value (an array of strings) contains the target string.
    
    Args:
        dictionary (dict): The dictionary to search.
        target_string (str): The string to search for.
        search_array (str): The key in the nested dictionary to search for the string.

    Returns:
        str or None: The key that contains the target string in its array, or None if not found.
    """
    for key, nested_dict in dictionary.get("honorifics", {}).items():
        if target_string in nested_dict.get(search_array, []):
            return key
    return None

def check_sub(sub, honor, original_text):
    """Checks and replaces honorifics in the subtitles."""
    honorific = find_key_by_string(honorifics, honor, "kanjis")

    if not honorific:
        return False

    for name, name_value in names.items():
        if name_value in original_text:
            for orig in sub["original"]:
                if name in orig["text"]:
                    # Perform replacements for name and honorifics
                    orig["text"] = re.sub(name, f"{name}-{honorific}", orig["text"], flags=re.I)
                    
                    for alternative in honorifics["honorifics"][honorific]["alternatives"]:
                        orig["text"] = re.sub(alternative, "", orig["text"], flags=re.I)

                    orig["text"] = orig["text"].strip()
    return True

if __name__ == '__main__':
    main()