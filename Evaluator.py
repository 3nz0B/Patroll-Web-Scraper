from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json

def simulated_patent_search(base_patent: str, winning_patents: list, prior_art_list: list):
    winning_set = set(p.upper() for p in winning_patents)
    found_set = set(p.upper() for p in prior_art_list)
    found_matches = list(winning_set & found_set)
    success = len(found_matches) > 0
    return found_matches, success

# Load JSON file instead of Excel
with open("scraped_patents.json", "r") as f:
    scraped_data = json.load(f)

# ✅ Replace this with real known answers
ground_truth = {
    "US1234567B2": ["US7654321B1", "US9999999A1"],
    "US2468135B2": ["US1357924A1", "US9876543B2"],
    # Add more known contest-patent mappings here
}

# Initialize metrics
total = 0
success_count = 0
recall_scores = []
hit_counts = []

for item in scraped_data:
    troll_patent = item.get("troll_patent") or item.get("base_patent")
    prior_art = item.get("prior_art")

    if not troll_patent or troll_patent not in ground_truth:
        continue

    # Make sure prior_art is a list
    if isinstance(prior_art, str):
        scraped_prior_art = [p.strip().upper() for p in prior_art.split(",")]
    elif isinstance(prior_art, list):
        scraped_prior_art = [p.strip().upper() for p in prior_art]
    else:
        scraped_prior_art = []

    correct_prior_art = [p.upper() for p in ground_truth[troll_patent]]

    found, success = simulated_patent_search(troll_patent, correct_prior_art, scraped_prior_art)

    true_positives = len(found)
    recall = true_positives / len(correct_prior_art) if correct_prior_art else 0

    recall_scores.append(recall)
    hit_counts.append(true_positives)

    if success:
        success_count += 1
    total += 1

# Final metrics
accuracy = (success_count / total) * 100 if total else 0
mean_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0
average_hits = sum(hit_counts) / len(hit_counts) if hit_counts else 0

print(f"\n📊 Evaluation Metrics:")
print(f"Total Contests Evaluated: {total}")
print(f"✅ Success Rate: {accuracy:.2f}%")
print(f"📈 Average Recall: {mean_recall:.2f}")
print(f"🎯 Average Ground Truth Hits: {average_hits:.2f} per contest")
