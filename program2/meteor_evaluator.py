from nltk.translate.meteor_score import meteor_score 
from evaluator import get_candidate_summary, get_reference_summary

candidate_summary = get_candidate_summary()
reference_summary = get_reference_summary()

# Define candidate and reference sentences 
candidate = candidate_summary.split() 
reference = reference_summary.split()

# Calculate METEOR score 
score = meteor_score([reference], candidate) 

# Print the result 
print(f"METEOR Score: {score:.4f}")