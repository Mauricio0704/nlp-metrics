from collections import Counter

def get_ngrams(sequence, n):
    return [tuple(sequence[i:i+n]) for i in range(len(sequence)-n+1)]

def detect_ngrams(text1, text2):
    words1, words2 = text1.split(), text2.split()
    characters1, characters2 = list(text1.replace(" ", "")), list(text2.replace(" ", ""))
    
    word_ngrams1 = {f"{n}-word ngrams": Counter(get_ngrams(words1, n)) for n in range(1, 4)}
    word_ngrams2 = {f"{n}-word ngrams": Counter(get_ngrams(words2, n)) for n in range(1, 4)}
    
    char_ngrams1 = {f"{n}-char ngrams": Counter(get_ngrams(characters1, n)) for n in range(1, 4)}
    char_ngrams2 = {f"{n}-char ngrams": Counter(get_ngrams(characters2, n)) for n in range(1, 4)}
    
    return {
        "Text 1": {**word_ngrams1, **char_ngrams1},
        "Text 2": {**word_ngrams2, **char_ngrams2}
    }

# Ejemplo de uso y pruebas adicionales
if __name__ == "__main__":
    text1 = "Hola mundo, esto es una prueba de n-gramas."
    text2 = "Hola universo, esto también es una prueba de n-gramas."
    
    ngrams = detect_ngrams(text1, text2)
    
    for text, categories in ngrams.items():
        print(text)
        for category, counts in categories.items():
            print(category)
            for ngram, count in counts.items():
                print(f"  {ngram}: {count}")
