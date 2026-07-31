# Full Review JSON Schema

Create UTF-8 JSON with the following shape. Optional arrays may be empty. Omit unsupported claims rather than inventing content.

```json
{
  "meta": {
    "language": "zh",
    "candidate": "Candidate name",
    "company": "Company",
    "role": "Role",
    "role_meta": "Location | function",
    "date": "YYYY-MM-DD",
    "source_note": "Based on resume, JD, and transcript",
    "usage_note": "How to use this report"
  },
  "summary": {
    "verdict": "One-sentence conclusion",
    "score_line": "Execution 6.8/10 | Role fit 7.5/10 | Progression signal 6.5/10",
    "strengths": ["..."],
    "gaps": ["..."],
    "match_rows": [
      {
        "requirement": "...",
        "evidence": "...",
        "fit": "Strong",
        "strategy": "..."
      }
    ],
    "fact_boundary": "Optional experience boundary or conflict note"
  },
  "questions": [
    {
      "question_id": "Q03",
      "question": "Reconstructed question",
      "intent": "What it tests",
      "diagnosis": "What happened in the actual answer",
      "risk": "Optional high-risk statement",
      "answer": "Ready-to-say answer",
      "evidence": "Resume/transcript basis",
      "project_evidence": [
        {
          "project_id": "stable-project-id",
          "project_name": "Confirmed project name",
          "facts_used": [
            {
              "fact_id": "stable-fact-id",
              "fact": "Readable confirmed fact used in this answer",
              "newly_confirmed": true
            }
          ]
        }
      ],
      "rewrite_note": "Rewritten after confirming U001 and U003",
      "followups": [
        {"question": "...", "answer": "..."}
      ]
    }
  ],
  "likely_questions": [
    {
      "question_id": "L01",
      "question": "Likely next-round question",
      "intent": "...",
      "diagnosis": "Why this remains untested or weak",
      "answer": "...",
      "evidence": "...",
      "project_evidence": [],
      "rewrite_note": "",
      "followups": []
    }
  ],
  "strategy": {
    "answer_structures": [
      {"title": "...", "body": "..."}
    ],
    "risky_phrases": [
      {"avoid": "...", "replace": "..."}
    ],
    "speaking_tips": ["..."]
  },
  "quick_card": {
    "positioning": "...",
    "core_evidence": ["..."],
    "keyword_groups": [
      {"title": "...", "items": ["..."]}
    ],
    "boundaries": "...",
    "reverse_questions": ["..."],
    "practice": ["..."]
  },
  "profile_update_receipt": {
    "candidate_id": "stable-private-id",
    "profile_path_note": "Private local profile",
    "interview": {
      "interview_id": "stable-interview-id",
      "company": "Target company",
      "role": "Target role",
      "date": "YYYY-MM-DD"
    },
    "counts": {
      "total": 4,
      "confirmed": 1,
      "edited": 1,
      "rejected": 1,
      "pending": 1,
      "applied": 2
    },
    "changes": [
      {
        "update_id": "U001",
        "change_type": "enrich",
        "operation": "add_fact",
        "project_id": "stable-project-id",
        "project_name": "Confirmed project name",
        "field": "actions",
        "value": "Confirmed fact",
        "source": {
          "source_type": "transcript",
          "source_label": "Interview answer to Q03"
        },
        "decision": "confirmed",
        "status": "applied",
        "affected_question_ids": ["Q03"]
      }
    ],
    "affected_question_ids": ["Q03", "Q07"]
  }
}
```

## Content rules

- Put transcript-derived questions in `questions`.
- Give each question a stable `question_id`. Use the same IDs in update
  proposals, rewrite notes, and `affected_question_ids`.
- Put only high-probability, JD-derived preparation in `likely_questions`.
- Keep answers in spoken form.
- Use `risk` only for material factual, technical, safety, motivation, or integrity risks.
- Diagnose the actual answer from the transcript only. Project memory may improve
  `answer`, but it must not change `diagnosis` or the score.
- Put only confirmed project facts in `project_evidence`.
- Set `newly_confirmed` to true only when the applied receipt from this review
  introduced, edited, or deliberately reinforced that fact.
- Use `rewrite_note` to name the update IDs that caused an answer to be rebuilt.
- Include every update decision in `profile_update_receipt.changes`, including
  rejected and explicitly unresolved items. Never expose the absolute private
  profile path; use `profile_path_note`.
- A final report should normally have zero pending substantive changes. If the
  user explicitly proceeds with pending items, show them in the receipt and keep
  them out of optimized answers.
- Keep table cells concise; move paragraph-length material into questions or callouts.
- Preserve candidate privacy and never reuse another report’s personal content.
