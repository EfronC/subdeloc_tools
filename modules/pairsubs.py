import pysubs2
import json
import re

MARGIN = 1000

def load_ass(file_path):
    try:
        subs = pysubs2.load(file_path)
        return subs
    except Exception as e:
        print(f"Error loading file '{file_path}': {e}")
        return None

def intersect(t1, t2):
    if (t1[0] == t2[1] or t1[1] == t2[0]) and (t1[0] != t2[1] or t1[1] != t2[0]):
        return False
    if t1[0] > t2[1] or t2[0] > t1[1]:
        return False
    return True

def generate_item(interval):
    return {
        "interval": interval,
        "nls": [],
        "lines": {"left":[], "right":[]}
    }

def sanitize_string(string):
    # Match substrings enclosed in {}
    pattern = r"\{([^{}]*)\}"

    # Replace all occurrences of the pattern using the replace function
    result = re.sub(pattern, "", string)
    result = re.sub(r"\\.", "", result)
    return result

def find_intersections(set_a, set_b):
    intersections = []
    used_a = set()  # Track used intervals from set_a
    used_b = set()  # Track used intervals from set_b

    def check_interval_conditions(interval, other_interval):
        # Check for full containment
        fully_contained = (
            (interval['start'] >= other_interval['start'] and interval['end'] <= other_interval['end']) or
            (other_interval['start'] >= interval['start'] and other_interval['end'] <= interval['end'])
        )

        # Check if both start and end times are within the ±2 seconds margin
        within_margin = (
            abs(interval['start'] - other_interval['start']) <= MARGIN or 
            abs(interval['end'] - other_interval['end']) <= MARGIN
        )

        return fully_contained, within_margin

    def find_matches(interval, other_set):
        matches = []
        for idx, other_interval in enumerate(other_set):
            
            fully_contained, within_margin = check_interval_conditions(interval, other_interval)

            if fully_contained or within_margin:
                matches.append(other_interval)

        return matches

    def process_interval(interval, other_set, key_1='original'):
        matches = find_matches(interval, other_set)

        key_2 = 'alternative' if key_1 == 'original' else 'original'

        if matches:
            group_start = min([interval['start']] + [b['start'] for b in matches])
            group_end = max([interval['end']] + [b['end'] for b in matches])

            return {
                'start': group_start,
                'end': group_end,
                key_1: [interval],
                key_2: matches
            }, len(matches)

    # Pointers for iterating through set A and set B
    i, j = 0, 0
    
    while i < len(set_a) and j < len(set_b):
        # Get the current intervals from both sets
        interval_a = set_a[i]
        interval_b = set_b[j]

        # Check interval conditions | TODO
        fully_contained, within_margin = check_interval_conditions(interval_a, interval_b)

        if fully_contained or within_margin:
            sza = interval_a["end"] - interval_a["start"]
            szb = interval_b["end"] - interval_b["start"]

            if sza >= szb:
                matches, carry = process_interval(interval_a, set_b[j:], 'original')
                j += carry
                i += 1
            else:
                matches, carry = process_interval(interval_b, set_a[i:], 'alternative')
                i += carry
                j += 1
            if matches:
                intersections.append(matches)
        else:
            if interval_a["start"] <= interval_b["start"]:
                i += 1
            else:
                j += 1

    return intersections

def group_lines_by_time(sub1, sub2):
    intervals = []
    sub_pivot = sub2
    current = 0
    set_a = []
    set_b = []

    for nl,line in enumerate(sub1):
        if line.type == "Dialogue":
            set_a.append({"start": line.start, "end": line.end, "text":sanitize_string(line.text), "nl": nl})
    for nl,line in enumerate(sub2):
        if line.type == "Dialogue":
            set_b.append({"start": line.start, "end": line.end, "text":sanitize_string(line.text), "nl": nl})

    return find_intersections(set_a, set_b)

def pair_files(s1: str, s2: str):
    sub1 = load_ass(s1)
    sub2 = load_ass(s2)

    res = group_lines_by_time(sub1, sub2)

    return res