# Private Project Memory

Use a private candidate project profile as the evidence layer for full reviews and
answer-rewrite tasks. The profile is candidate-specific data, not Skill content.
Never save a real profile, update proposal, or receipt inside the Skill directory
or a public repository.

## Storage boundary

- Ask the user for a preferred private directory when practical.
- Otherwise use a task-local private path such as
  `interview-memory/<candidate-id>/candidate-profile.json`.
- Keep update proposals and receipts beside that profile.
- Public Skill repositories may contain only schemas, scripts, and fictional
  examples used for testing.
- Never print the absolute private profile path in a public-facing report. Use a
  note such as `Private local profile` instead.

## Candidate profile

Use UTF-8 JSON:

```json
{
  "schema_version": "1.0",
  "candidate": {
    "candidate_id": "stable-private-id",
    "name": "Candidate name"
  },
  "projects": [
    {
      "project_id": "stable-project-id",
      "project_type": "internship",
      "name": "Project name",
      "organization": "Organization",
      "period": "YYYY-MM to YYYY-MM",
      "role": "Candidate role",
      "facts": [
        {
          "fact_id": "stable-fact-id",
          "field": "actions",
          "value": "Candidate-specific confirmed fact",
          "status": "confirmed",
          "sources": [
            {
              "source_type": "user",
              "source_label": "User confirmation",
              "interview_id": "optional-interview-id",
              "date": "YYYY-MM-DD"
            }
          ],
          "previous_values": []
        }
      ]
    }
  ],
  "change_history": []
}
```

Recommended `project_type` values:

- `internship`
- `personal`
- `academic`
- `competition`
- `research`
- `work`
- `other`

Recommended fact `field` values:

- `background`
- `target_users`
- `responsibilities`
- `actions`
- `tech_stack`
- `deliverables`
- `results`
- `metrics`
- `challenges`
- `decisions`
- `learnings`
- `collaboration`
- `boundaries`

## Update proposal

Create one proposal after reading the current resume, JD, transcript, user
clarifications, and existing profile. Every detected addition, enrichment,
reinforcement, or conflict must appear in `updates`.

```json
{
  "schema_version": "1.0",
  "candidate_id": "stable-private-id",
  "interview": {
    "interview_id": "stable-interview-id",
    "company": "Target company",
    "role": "Target role",
    "date": "YYYY-MM-DD"
  },
  "updates": [
    {
      "update_id": "U001",
      "change_type": "enrich",
      "operation": "add_fact",
      "project_id": "project-id",
      "fact_id": "new-fact-id",
      "field": "actions",
      "value": "Proposed fact",
      "source": {
        "source_type": "transcript",
        "source_label": "Interview answer to Q03",
        "interview_id": "stable-interview-id",
        "date": "YYYY-MM-DD"
      },
      "decision": "pending",
      "edited_value": "",
      "target_fact_id": "",
      "conflicts_with_fact_ids": [],
      "affected_question_ids": ["Q03", "Q07"]
    }
  ]
}
```

Allowed `change_type` values:

- `new`: a new project or fact not present in the profile;
- `enrich`: additional detail about an existing project;
- `reinforce`: another source supports an existing fact;
- `conflict`: the proposed value conflicts with a confirmed fact.

Allowed `operation` values:

- `add_project`: create project metadata. Put the project object in `project`.
- `add_fact`: append a new confirmed fact to an existing project.
- `reinforce_fact`: append a source to `target_fact_id` without changing its value.
- `replace_fact`: replace `target_fact_id`; preserve its old value in
  `previous_values`.

Allowed `decision` values:

- `pending`
- `confirmed`
- `edited`
- `rejected`

For `edited`, provide `edited_value` for fact operations or `edited_project` for
`add_project`. A conflict is not resolved by the word `confirmed` alone. It must
be rejected, or converted to a deliberate `replace_fact` operation with a valid
`target_fact_id`.

## Required confirmation display

Before profile mutation, show every proposal in a compact numbered list or table:

- update ID;
- project;
- change type and field;
- proposed value;
- source;
- conflict note, if any;
- affected interview questions;
- current decision.

Tell the user they may respond in one batch, for example:

> Confirm U001 and U003; edit U002 to “…”; reject U004.

Do not summarize away low-confidence or conflicting proposals. They are exactly
the items the user needs to inspect.

## Merge and rewrite rules

1. Run `scripts/update_project_memory.py` in `preview` mode first.
2. Show the preview to the user and collect batch decisions.
3. Update the proposal JSON with those decisions.
4. Run the script in `apply` mode.
5. Only `confirmed` and valid `edited` items enter the formal profile.
6. `pending` and `rejected` items never enter the profile or ready-to-say answers.
7. Rebuild only answers listed in applied updates' `affected_question_ids`.
8. For each rebuilt answer, record the project name, fact IDs, facts used, and
   whether each fact was newly confirmed in this review.
9. Include the apply receipt in the final Word report.

The diagnosis of the candidate's actual interview performance must still use
only the transcript. The project profile may improve the rewritten answer, but it
must never retroactively improve the score or description of what the candidate
actually said.

## First-use bootstrap

If no profile exists:

1. Draft project metadata and facts from the resume and transcript.
2. Mark every proposed item `pending`.
3. Show the complete proposal to the user.
4. Create the formal profile only after confirmation.
5. Generate the final ready-to-say answers after the first confirmed merge.

## Quick-score exception

Quick-score mode may read a confirmed profile when already available, but it
does not create or mutate a profile unless the user explicitly requests that
work. Keep the answer concise.
