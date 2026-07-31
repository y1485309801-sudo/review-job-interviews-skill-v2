---
name: review-job-interviews
description: Review job interviews from a candidate resume, job description, interview transcript or recording transcription, and a private confirmed project profile. Use when Codex needs to extract interview questions, diagnose answers, maintain candidate-approved internship or personal-project facts, rewrite truthful project-grounded ready-to-say responses, score interview performance and role fit, compare multiple interviews, prepare likely follow-ups, or generate a polished Chinese or English DOCX interview review with a project-profile change receipt.
---

# Review Job Interviews

Turn a resume, job description, interview transcript, and private confirmed
project profile into a fact-grounded review whose main artifact is the extracted
question plus an improved answer the candidate can say directly.

## Select the mode

- Use **full review** when the user asks to make, produce, or fully review the interview. Default to a polished DOCX.
- Use **quick score** when the user asks only for a score. Reply inline, do not
  create a document, and do not mutate the project profile unless explicitly
  requested.
- Use **answer rewrite** when the user wants only questions and improved answers. Reply inline unless a file is requested.
- Use **comparison** when the user asks whether interview performance improved or declined. Compare interview execution separately from role fit.

Do not inflate scope. If the user says “only score,” give only the score and a concise conclusion.

## Read the inputs

1. Read the full resume, job description, and transcript.
2. Use the PDF and Documents skills when source formats require them.
3. Identify the candidate and locate their private project profile. If none
   exists, follow the first-use bootstrap in
   [references/project-memory-schema.md](references/project-memory-schema.md).
4. Treat the supplied resume as the version used in the interview. Only apply a
   historical cutoff when the user explicitly says an experience did not yet
   exist or asks to compare historical interviews.
5. Do not browse for company or role information unless the user asks, the JD is
   missing, or current external facts are necessary.

## Build the evidence base

Extract candidate facts before evaluating:

- employers, dates, roles, projects, responsibilities, tools, metrics, education, and stated preferences;
- which facts come from the resume, transcript, or user message;
- confirmed facts already present in the private project profile;
- uncertain numbers, ASR errors, contradictions, and claims that may overstate individual ownership.

Never invent a project, metric, responsibility, tool, or outcome. When a technical answer goes beyond demonstrated experience, label it as a proposed approach: “I have not independently shipped this in a real environment; my design approach would be…”

## Maintain the private project profile

Read
[references/project-memory-schema.md](references/project-memory-schema.md)
before any full review or profile-aware answer rewrite.

1. Compare the current inputs with the confirmed profile.
2. Create an update proposal containing every new, enriched, reinforced, or
   conflicting project fact.
3. Show all proposed changes to the user, including source and affected question
   IDs. Allow batch confirmation, edits, and rejection.
4. Do not add pending content to the formal profile or ready-to-say answers.
5. After the user decides, run the update script in apply mode:

```bash
"$PYTHON_BIN" "$SKILL_DIR/scripts/update_project_memory.py" \
  --mode apply \
  --profile "$PRIVATE_PROFILE" \
  --updates "$DECIDED_UPDATES" \
  --receipt "$PROFILE_RECEIPT"
```

Run it in `preview` mode before confirmation. Keep the profile, proposal, and
receipt outside the Skill directory and any public repository.

If substantive updates remain pending, pause before producing the final DOCX.
The user may explicitly choose to proceed with only the already confirmed facts.

## Analyze the interview

Read [references/analysis-and-rewrite.md](references/analysis-and-rewrite.md) before extracting questions or rewriting answers.

1. Identify interviewer and candidate turns.
2. Reconstruct each primary question and its follow-up chain.
3. Summarize the candidate’s actual answer without copying transcript noise.
4. Diagnose strengths, omissions, factual risks, technical errors, motivation inconsistencies, and communication issues.
5. Map each question to the JD competency it tests.
6. Separate answer quality from role fit and interviewer signals.

Correct only obvious ASR errors from context. Do not silently “correct” names, metrics, model names, employers, or dates when uncertain.

Diagnose and score what the candidate actually said using the transcript only.
Do not let a stronger project profile retroactively improve the description or
score of the live answer.

## Score

Read [references/scoring-rubric.md](references/scoring-rubric.md) for any scoring or comparison task.

- Produce an **interview execution score** for answer quality and transferable interviewing ability.
- Produce a **role fit score** for experience-to-JD alignment.
- Produce a **progression signal score** only when there is enough interviewer behavior to assess it.
- Do not backsolve a high score from a known pass result or a low score from a known rejection.
- For comparisons, compare execution scores; explain role-fit differences separately.

## Rewrite answers

- Lead with the conclusion.
- Use evidence from the resume and transcript.
- Prefer “conclusion - evidence - role link” for ordinary questions.
- Prefer STAR for behavioral questions.
- Prefer “goal - layered approach - risk controls - MVP” for system-design questions.
- Keep ordinary answers to roughly 60-90 seconds and complex questions to 2-3 minutes.
- Use natural spoken language, not essay prose.
- Preserve honest uncertainty and experience boundaries.
- Use only confirmed profile facts in personal claims.
- Prefer one primary role-relevant project per answer; add a second only when it
  proves a different necessary competency.
- Do not force project evidence into logistics, compensation, availability, or
  motivation answers when it is not relevant.
- Record the project name and fact IDs used by every profile-grounded rewrite.
- After an approved profile update, rewrite only questions listed in the
  receipt's `affected_question_ids`.
- Add likely follow-ups only when they materially improve preparation.

## Produce a full review

Read [references/report-schema.md](references/report-schema.md), then create a
task-local JSON report matching that schema. Include the applied project-profile
receipt and the project evidence used by each rewritten answer.

Run:

```bash
"$PYTHON_BIN" "$SKILL_DIR/scripts/build_review_docx.py" \
  --input "$REPORT_JSON" \
  --output "$FINAL_DOCX"
```

Use the bundled workspace Python returned by the workspace dependency loader. Do not use system Python.

The builder reproduces the retained reference report’s design language: centered cover, navy/blue hierarchy, pale callouts, transcript-derived Q sections, fixed-width tables, strategy section, and quick-reference card. It must not contain any previous company’s or candidate’s data.

After building, use the Documents skill to render the DOCX to PNGs and inspect every page. Fix missing CJK glyphs, clipping, broken tables, awkward page breaks, or inconsistent headers before delivery. On macOS, if the bundled renderer cannot see Chinese system fonts, provide a task-local Fontconfig file that scans `/System/Library/Fonts`, `/System/Library/Fonts/Supplemental`, and `/Library/Fonts` with a writable cache, then rerender.

Return only the final DOCX unless the user asks for additional formats.

## Output quality gates

- Every optimized personal claim is supported by the supplied evidence.
- Every profile-grounded answer identifies the confirmed project facts it uses.
- No pending or rejected update appears in a ready-to-say answer.
- The report includes a complete project-profile update receipt.
- Questions reflect the transcript rather than generic interview lists.
- Direct answers are ready to say aloud.
- Technical corrections are accurate and distinguish experience from proposal.
- Scores follow the role-adjusted rubric.
- Known interview outcomes do not distort scoring.
- No private data from previous candidates appears.
- Real private profiles never enter the public Skill repository.
- A full DOCX passes structural and visual QA.
