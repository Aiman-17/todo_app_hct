#!/usr/bin/env python3
"""Test rule-based classifier directly"""

import sys
sys.path.insert(0, 'backend')

from src.agents.rule_based_classifier import RuleBasedClassifier

classifier = RuleBasedClassifier()

# Test cases
test_cases = [
    "shw my tsks",
    "Buy milk",
    "I need to remember to pay bills",
    "Whats pending",
]

for test in test_cases:
    result = classifier.classify(test)
    print(f"\nInput: '{test}'")
    print(f"Intent: {result['intent']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Entities: {result['entities']}")
