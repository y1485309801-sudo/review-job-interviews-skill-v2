# Interview Analysis and Answer Rewrite

## Evidence order

Use candidate-specific facts in this order:

1. Explicit user clarification.
2. Confirmed facts in the candidate's private project profile.
3. Resume facts.
4. Clear candidate statements in the transcript.
5. Reasonable professional knowledge stated as a proposed approach, not claimed experience.

Flag rather than resolve conflicts involving dates, metrics, ownership, company names, model names, compensation, or education.

Pending, rejected, or unresolved conflicting project updates are not evidence for
a ready-to-say answer. A resume or transcript fact that would change the private
profile must pass the confirmation workflow before being used as a new personal
claim in the final optimized answer.

## Transcript reconstruction

- Split the transcript by speaker when possible.
- Merge fragmented interviewer turns into one primary question.
- Attach immediate probes to the primary question unless they test a new competency.
- Preserve important corrections by the interviewer; they often reveal the real failure point.
- Treat long interviewer explanations as role evidence and progression signals, not candidate answers.
- Ignore filler, connection checks, greetings, and transcription artifacts.
- Normalize obvious terms such as RAG, Bad Case, Prompt, Agent, JSON, SQL Server, Vibe Coding, API, ETL/ELT, and OCR only when context is unambiguous.

For every primary question capture:

- reconstructed question;
- competency and interviewer intent;
- concise summary of the actual answer;
- what worked;
- what was missing or incorrect;
- any high-risk statement;
- improved direct answer;
- supporting candidate evidence;
- confirmed project and fact IDs used by the rewrite;
- useful follow-ups.

## Project evidence selection

- When the interviewer names a project, use that project as the primary evidence.
- For general competency questions, choose the strongest confirmed project that
  matches the JD requirement and the candidate's actual ownership.
- Prefer one primary project. Add a second project only if it demonstrates a
  distinct competency the first project cannot support.
- Use the smallest sufficient set of facts. Do not turn every answer into a full
  project introduction.
- Preserve the difference between team outcomes and the candidate's own actions.
- Include boundaries, failed attempts, or missing production experience when
  they materially affect truthfulness.
- Do not force project content into questions about location, compensation,
  availability, or personal motivation unless it directly supports the answer.
- For every rewritten answer, store `project_id`, `project_name`, `fact_id`,
  readable fact text, and whether the fact was newly confirmed in this review.
- The transcript controls actual-answer diagnosis and scoring. The profile
  controls only the improved answer and future preparation.

## Answer patterns

### Ordinary fit or motivation question

1. Answer the question in the first sentence.
2. Give one or two concrete pieces of evidence.
3. Connect the evidence to the target role.

### Behavioral or project question

Use STAR, but keep Situation and Task short. Spend most time on the candidate’s own Action and measurable Result. State collaboration accurately; do not turn team work into sole ownership.

### Product or operations question

Use:

1. user/business problem;
2. current process or evidence;
3. prioritization and proposed solution;
4. metric and validation method;
5. risks and iteration.

### Technical or system-design question

Use:

1. goal, users, data, and success criteria;
2. layered architecture or workflow;
3. accuracy, security, permissions, and failure handling;
4. MVP scope and evaluation.

Do not hide missing knowledge behind “the model can do it.” Keep deterministic controls outside the model where appropriate.

### Experience-gap question

Say:

> I have not independently shipped this in a real production environment. My transferable experience is ____. My proposed approach would be ____. I would validate it by ____.

## Risk checks

Flag:

- uncertain metrics spoken as facts;
- resume/transcript contradictions;
- claims of sole ownership for team outcomes;
- using a later experience when the user says it did not yet exist;
- unsafe or technically incorrect principles;
- vague reliance on AI without data, evaluation, or controls;
- unstable resignation motivation;
- compensation or availability inconsistencies;
- answers that fail to address the corrected question;
- excessive filler, delayed conclusions, and repeated wording.

## Writing standard

- Match the user’s language.
- Use natural spoken Chinese or English.
- Prefer short paragraphs and explicit transitions.
- Avoid generic praise and inflated adjectives.
- Keep the candidate’s voice while making the logic clearer.
