#!/usr/bin/env python3
import json
import re
import csv

A1_PATH = "Deutsch_1__Goethe_A1_Wortliste/deck.json"
A2_PATH = "Deutsch_1__Goethe_A2_Wortliste/deck.json"
B1_PATH = "Deutsch_2__Goethe_B1_Wortliste/deck.json"

def load_words_from_deck(path, word_field_index):
    with open(path, encoding="utf-8") as f:
        deck = json.load(f)
    
    words = {}
    for note in deck.get("notes", []):
        if note.get("__type__") == "Note":
            fields = note.get("fields", [])
            if len(fields) > word_field_index:
                word = fields[word_field_index].strip()
                if word:
                    guid = note.get("guid", "")
                    words[word] = (word, guid)
    return words

def normalize_word(word):
    word = word.strip()
    
    word = word.replace("|", "")
    
    word = re.sub(r"^\([^)]+\)\s*", "", word)
    word = re.sub(r"\s*\([^)]+\)$", "", word)
    
    article_match = re.match(r"^(der|die|das|den|dem|des)\s+(.+)$", word)
    if article_match:
        word = article_match.group(2)
    
    word = re.sub(r",.*$", "", word)
    word = re.sub(r"\s*\(pl\.\)$", "", word)
    
    word = word.strip()
    
    return word.lower()

def main():
    a1_words = load_words_from_deck(A1_PATH, 1)
    a2_words = load_words_from_deck(A2_PATH, 0)
    b1_words = load_words_from_deck(B1_PATH, 0)
    
    a1_normalized = {normalize_word(w): v for w, v in a1_words.items()}
    a2_normalized = {normalize_word(w): v for w, v in a2_words.items()}
    b1_normalized = {normalize_word(w): v for w, v in b1_words.items()}
    
    duplicates = []
    for norm_b1, (original_b1, guid_b1) in b1_normalized.items():
        if norm_b1 in a1_normalized:
            original_a1, guid_a1 = a1_normalized[norm_b1]
            duplicates.append((norm_b1, original_a1, guid_a1, "", "", original_b1, guid_b1, "A1"))
        elif norm_b1 in a2_normalized:
            original_a2, guid_a2 = a2_normalized[norm_b1]
            duplicates.append((norm_b1, "", "", original_a2, guid_a2, original_b1, guid_b1, "A2"))
    
    duplicates.sort(key=lambda x: x[0].lower())
    
    with open("duplicates_b1.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "a1_word", "a1_guid", "a2_word", "a2_guid", "b1_word", "b1_guid", "found_in"])
        for norm, a1_w, a1_g, a2_w, a2_g, b1_w, b1_g, found_in in duplicates:
            writer.writerow([norm, a1_w, a1_g, a2_w, a2_g, b1_w, b1_g, found_in])
    
    print(f"Wrote {len(duplicates)} duplicates to duplicates_b1.csv")

if __name__ == "__main__":
    main()
