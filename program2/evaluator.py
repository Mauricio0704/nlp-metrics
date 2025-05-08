from pypdf import PdfReader
import json
import collections
import pprint

def create_char_ngrams(text, n):
    ngrams = collections.Counter()

    for ngram in (tuple(text[i:i + n]) for i in range(len(text) - n + 1)):
        ngrams[ngram] += 1
    return ngrams

def create_word_ngrams(text, n):
    words = text.split()

    ngrams = collections.Counter()
    ngrams_list = (tuple(words[i:i + n]) for i in range(len(words) - n + 1))

    for ngram in ngrams_list:
        ngrams[ngram] += 1

    return ngrams


def get_overlapping_ngrams(reference_ngrams, candidate_ngrams):
    overlapping_number_of_ngrams = 0

    for ngram in reference_ngrams:
        overlapping_number_of_ngrams += min(reference_ngrams[ngram], candidate_ngrams[ngram])

    return overlapping_number_of_ngrams


def get_rougeN_score(reference_ngrams, candidate_ngrams):
    overlapping_number_of_ngrams = get_overlapping_ngrams(reference_ngrams, candidate_ngrams)

    number_of_ngrams_in_the_reference = sum(reference_ngrams.values())
    number_of_ngrams_in_the_candidate = sum(candidate_ngrams.values())

    recall = overlapping_number_of_ngrams / max(number_of_ngrams_in_the_reference, 1)
    precision = overlapping_number_of_ngrams / max(number_of_ngrams_in_the_candidate, 1)

    if precision + recall == 0:
        rouge_score = 0
    else:
        rouge_score = (2 * precision * recall) / (precision + recall)

    return rouge_score
   

def get_candidate_summary():
    data = ""

    with open("equipo1/conversation_A01225357.json", encoding="utf-8") as file:
        data = json.load(file)

    user_data = ' '.join([data[i]["message"] for i in range(len(data)) if data[i]["role"] == "assistant"])

    return user_data


def get_reference_summary():
    reader = PdfReader("equipo1/Equipo1-ProyectoE1.pdf")

    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def get_lcs_table(ref, can):
    """Create 2-d LCS score table."""
    rows = len(ref)
    cols = len(can)
    lcs_table = [[0] * (cols + 1) for _ in range(rows + 1)]
    for i in range(1, rows + 1):
        for j in range(1, cols + 1):
            if ref[i - 1] == can[j - 1]:
                lcs_table[i][j] = lcs_table[i - 1][j - 1] + 1
            else:
                lcs_table[i][j] = max(lcs_table[i - 1][j], lcs_table[i][j - 1])
                
    return lcs_table


def get_rougeL_score(reference, candidate):
    if not reference or not candidate:
        return 0

    reference = reference.split()
    candidate = candidate.split()

    lcs_table = get_lcs_table(reference, candidate)
    lcs_length = lcs_table[-1][-1]

    precision = lcs_length / len(candidate)
    recall = lcs_length / len(reference)
    fmeasure = (2 * precision * recall) / (precision + recall)

    return fmeasure


candidate_summary = get_candidate_summary()
reference_summary = get_reference_summary()


def get_number_of_words(text):
    words = text.split()
    return len(words)

if __name__ == "__main__":
    results = {}

    results['Candidate summary words'] = get_number_of_words(candidate_summary)
    results['Candidate summary chars'] = len(candidate_summary)
    results['Reference summary chars'] = len(reference_summary)
    results['Reference summary words'] = get_number_of_words(reference_summary)

    for n in range(1, 5):
        # print(f"Evaluating {n}-grams")
        reference_ngrams = create_char_ngrams(reference_summary, n)
        candidate_ngrams = create_char_ngrams(candidate_summary, n)

        if n == 1:
            rougeL_score = get_rougeL_score(reference_summary, candidate_summary)
            results['Rouge-L'] = rougeL_score

        # print(f"Candidate n-grams: {sum(candidate_ngrams.values())}")
        # print(f"Reference n-grams: {sum(reference_ngrams.values())}")

        overlapping_ngrams = get_overlapping_ngrams(reference_ngrams, candidate_ngrams)
        # print(f"Overlapping n-grams: {overlapping_ngrams}")

        rouge_score = get_rougeN_score(reference_ngrams, candidate_ngrams)
        # print(f"Rouge-{n} score: {rouge_score}")
        results[f'Char {n}-grams'] = {
           'Overlapping n-grams': overlapping_ngrams,
           'Rouge score': rouge_score
           }
        # print("-------------------------------")

    for n in range(1, 4):
        # print(f"Evaluating {n}-grams")
        reference_word_ngrams = create_word_ngrams(reference_summary, n)
        candidate_word_ngrams = create_word_ngrams(candidate_summary, n)

        # print(f"Candidate word n-grams: {sum(candidate_word_ngrams.values())}")
        # print(f"Reference word n-grams: {sum(reference_word_ngrams.values())}")

        overlapping_ngrams = get_overlapping_ngrams(reference_word_ngrams, candidate_word_ngrams)
        # print(f"Overlapping word n-grams: {overlapping_ngrams}")
        # print("-------------------------------")
        rouge_score = get_rougeN_score(reference_word_ngrams, candidate_word_ngrams)

        results[f'Word {n}-grams'] = {
           'Overlapping n-grams': overlapping_ngrams,
           'Rouge score': rouge_score
           }
        
    pprint.pprint(results)