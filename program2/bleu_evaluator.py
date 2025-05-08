from nltk.translate.bleu_score import sentence_bleu
from evaluator import get_candidate_summary, get_reference_summary

candidate_summary = get_candidate_summary()
reference_summary = get_reference_summary()

reference = [
    reference_summary.split()
]
candidate = candidate_summary.split()


score = sentence_bleu(reference, candidate, weights=(0.5, 0.5))
print(f"Bleu Score: {score:.4f}")