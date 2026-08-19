"""
Loads data/rules.json (rich schema) into the `rules` table.

Run from backend/:
    python scripts/seed_rules.py
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.db import SessionLocal, init_db
from database.models_v2 import Rule

RULES_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "rules.json")


def parse_avg_days(display_str: str) -> int:
    """
    'estimated_processing_time' comes in as a display string like
    '7-15 working days'. Extract a usable average for ETA math.
    Falls back to 14 if the format is unrecognized (logs a warning).
    """
    numbers = [int(n) for n in re.findall(r"\d+", display_str)]
    if len(numbers) >= 2:
        return (numbers[0] + numbers[1]) // 2
    if len(numbers) == 1:
        return numbers[0]
    print(f"WARNING: could not parse avg_days from '{display_str}', defaulting to 14")
    return 14


def seed_rules() -> None:
    init_db()
    db = SessionLocal()

    with open(RULES_PATH, "r", encoding="utf-8") as f:
        rules = json.load(f)

    added, skipped = 0, 0
    for r in rules:
        exists = db.query(Rule).filter(Rule.rule_id == r["id"]).first()
        if exists:
            skipped += 1
            continue

        db.add(
            Rule(
                rule_id=r["id"],
                certificate_type=r.get("certificate_type", r["id"]),
                name=r["name"],
                description=r["description"],
                life_event=r["life_event"],
                department=r["department"],
                office=r["office"],
                prerequisites_json=json.dumps(r.get("prerequisites", [])),
                required_documents_json=json.dumps(r["required_documents"]),
                outputs_json=json.dumps(r["outputs"]),
                enables_json=json.dumps(r.get("enables", [])),
                avg_days=parse_avg_days(r["estimated_processing_time"]),
                estimated_processing_time_display=r["estimated_processing_time"],
                common_rejection_reasons_json=json.dumps(r.get("common_rejection_reasons", [])),
                next_step=r.get("next_step"),
                citizen_guidance=r.get("citizen_guidance"),
            )
        )
        added += 1

    db.commit()
    db.close()
    print(f"Seeded rules: {added} added, {skipped} already present.")


if __name__ == "__main__":
    seed_rules()
