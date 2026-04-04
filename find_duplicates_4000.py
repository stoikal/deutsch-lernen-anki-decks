#!/usr/bin/env python3
import json
import re
import csv

A1_PATH = "Deutsch_1__Goethe_A1_Wortliste/deck.json"
A2_PATH = "Deutsch_1__Goethe_A2_Wortliste/deck.json"
B1_PATH = "Deutsch_2__Goethe_B1_Wortliste/deck.json"
WORDS_PATH = "Deutsch_2__4000_German_Words_by_Frequency/deck.json"

FIELD_INDICES = {
    "A1": 1,   # de_word
    "A2": 0,   # Wort_DE
    "B1": 2,   # base_d
    "4000": 0, # German
}

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
    
    word = re.sub(r"^\([^)]+\)\s*", "", word)
    word = re.sub(r"\s*\([^)]+\)$", "", word)
    
    article_match = re.match(r"^(der|die|das|den|dem|des)\s+(.+)$", word)
    if article_match:
        word = article_match.group(2)
    
    word = re.sub(r",.*$", "", word)
    
    word = word.strip()
    
    return word.lower()

def main():
    a1_words = load_words_from_deck(A1_PATH, FIELD_INDICES["A1"])
    a2_words = load_words_from_deck(A2_PATH, FIELD_INDICES["A2"])
    b1_words = load_words_from_deck(B1_PATH, FIELD_INDICES["B1"])
    words_4000 = load_words_from_deck(WORDS_PATH, FIELD_INDICES["4000"])
    
    a1_normalized = {normalize_word(w): v for w, v in a1_words.items()}
    a2_normalized = {normalize_word(w): v for w, v in a2_words.items()}
    b1_normalized = {normalize_word(w): v for w, v in b1_words.items()}
    words_normalized = {normalize_word(w): v for w, v in words_4000.items()}
    
    all_base_words = {**a1_normalized, **a2_normalized, **b1_normalized}
    
    duplicates = []
    for norm, (original_w, guid_w) in words_normalized.items():
        if norm in all_base_words:
            source_word, source_guid = all_base_words[norm]
            duplicates.append((norm, source_word, source_guid, original_w, guid_w))
    
    duplicates.sort(key=lambda x: x[0].lower())
    
    with open("duplicates_4000.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["word", "base_word", "base_guid", "words_4000_word", "words_4000_guid"])
        for norm, src_w, src_g, w, g in duplicates:
            writer.writerow([norm, src_w, src_g, w, g])
    
    print(f"A1 words: {len(a1_normalized)}")
    print(f"A2 words: {len(a2_normalized)}")
    print(f"B1 words: {len(b1_normalized)}")
    print(f"Total base words (A1+A2+B1): {len(all_base_words)}")
    print(f"4000 words total: {len(words_normalized)}")
    print(f"Duplicates found: {len(duplicates)}")
    print(f"Non-duplicates (unique to 4000): {len(words_normalized) - len(duplicates)}")
    print(f"Written to duplicates_4000.csv")

if __name__ == "__main__":
    main()
