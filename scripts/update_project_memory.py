#!/usr/bin/env python3
"""Preview or apply confirmed updates to a private candidate project profile."""

import argparse
import copy
import json
import os
import tempfile
from datetime import date
from pathlib import Path


DECISIONS = {"pending", "confirmed", "edited", "rejected"}
OPERATIONS = {"add_project", "add_fact", "reinforce_fact", "replace_fact"}


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def empty_profile(candidate_id, candidate_name=""):
    return {
        "schema_version": "1.0",
        "candidate": {"candidate_id": candidate_id, "name": candidate_name},
        "projects": [],
        "change_history": [],
    }


def validate_profile(profile, candidate_id):
    candidate = profile.get("candidate") or {}
    existing_id = str(candidate.get("candidate_id") or "")
    if existing_id and existing_id != candidate_id:
        raise ValueError(
            f"Candidate mismatch: profile has {existing_id!r}, proposal has {candidate_id!r}"
        )
    profile.setdefault("schema_version", "1.0")
    profile.setdefault("candidate", {"candidate_id": candidate_id, "name": ""})
    profile["candidate"]["candidate_id"] = candidate_id
    profile.setdefault("projects", [])
    profile.setdefault("change_history", [])
    if not isinstance(profile["projects"], list) or not isinstance(
        profile["change_history"], list
    ):
        raise ValueError("Profile projects and change_history must be arrays")


def locate_project(profile, project_id):
    for project in profile["projects"]:
        if project.get("project_id") == project_id:
            return project
    return None


def locate_fact(profile, fact_id):
    for project in profile["projects"]:
        for fact in project.get("facts") or []:
            if fact.get("fact_id") == fact_id:
                return project, fact
    return None, None


def source_from(update):
    source = copy.deepcopy(update.get("source") or {})
    return source if source else {"source_type": "unknown", "source_label": "Unspecified"}


def display_value(update):
    if update.get("operation") == "add_project":
        project = (
            update.get("edited_project")
            if update.get("decision") == "edited"
            else update.get("project")
        ) or {}
        return project.get("name") or project.get("project_id") or ""
    if update.get("decision") == "edited":
        return update.get("edited_value", "")
    return update.get("value", "")


def validate_update(update):
    update_id = str(update.get("update_id") or "")
    if not update_id:
        raise ValueError("Every update requires update_id")
    decision = update.get("decision", "pending")
    operation = update.get("operation")
    if decision not in DECISIONS:
        raise ValueError(f"{update_id}: unsupported decision {decision!r}")
    if operation not in OPERATIONS:
        raise ValueError(f"{update_id}: unsupported operation {operation!r}")
    if decision == "edited":
        if operation == "add_project":
            if not isinstance(update.get("edited_project"), dict):
                raise ValueError(f"{update_id}: edited add_project requires edited_project")
        elif not str(update.get("edited_value") or "").strip():
            raise ValueError(f"{update_id}: edited fact requires edited_value")
    if update.get("change_type") == "conflict" and decision in {"confirmed", "edited"}:
        if operation != "replace_fact" or not update.get("target_fact_id"):
            raise ValueError(
                f"{update_id}: a conflict must be rejected or resolved with "
                "replace_fact and target_fact_id"
            )


def apply_one(profile, update):
    operation = update["operation"]
    update_id = update["update_id"]
    project_id = update.get("project_id")

    if operation == "add_project":
        project_data = copy.deepcopy(
            update.get("edited_project")
            if update.get("decision") == "edited"
            else update.get("project")
        )
        if not isinstance(project_data, dict):
            raise ValueError(f"{update_id}: add_project requires project")
        project_data.setdefault("project_id", project_id)
        project_id = project_data.get("project_id")
        if not project_id:
            raise ValueError(f"{update_id}: add_project requires project_id")
        if locate_project(profile, project_id):
            raise ValueError(f"{update_id}: project {project_id!r} already exists")
        project_data.setdefault("project_type", "other")
        project_data.setdefault("name", project_id)
        project_data.setdefault("organization", "")
        project_data.setdefault("period", "")
        project_data.setdefault("role", "")
        project_data.setdefault("facts", [])
        profile["projects"].append(project_data)
        return

    if operation in {"add_fact", "reinforce_fact"}:
        project = locate_project(profile, project_id)
        if project is None:
            raise ValueError(f"{update_id}: project {project_id!r} does not exist")
        project.setdefault("facts", [])

    if operation == "add_fact":
        fact_id = update.get("fact_id")
        if not fact_id:
            raise ValueError(f"{update_id}: add_fact requires fact_id")
        _, duplicate = locate_fact(profile, fact_id)
        if duplicate is not None:
            raise ValueError(f"{update_id}: fact {fact_id!r} already exists")
        value = display_value(update)
        if not str(value).strip():
            raise ValueError(f"{update_id}: fact value cannot be empty")
        project["facts"].append(
            {
                "fact_id": fact_id,
                "field": update.get("field") or "other",
                "value": value,
                "status": "confirmed",
                "sources": [source_from(update)],
                "previous_values": [],
            }
        )
        return

    target_fact_id = update.get("target_fact_id")
    target_project, fact = locate_fact(profile, target_fact_id)
    if fact is None:
        raise ValueError(f"{update_id}: target fact {target_fact_id!r} does not exist")
    if project_id and target_project.get("project_id") != project_id:
        raise ValueError(f"{update_id}: target fact belongs to another project")

    if operation == "reinforce_fact":
        source = source_from(update)
        sources = fact.setdefault("sources", [])
        if source not in sources:
            sources.append(source)
        return

    if operation == "replace_fact":
        value = display_value(update)
        if not str(value).strip():
            raise ValueError(f"{update_id}: replacement value cannot be empty")
        old_value = fact.get("value", "")
        fact.setdefault("previous_values", []).append(
            {
                "value": old_value,
                "replaced_on": date.today().isoformat(),
                "update_id": update_id,
            }
        )
        fact["value"] = value
        fact["field"] = update.get("field") or fact.get("field") or "other"
        fact["status"] = "confirmed"
        fact.setdefault("sources", []).append(source_from(update))


def atomic_write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def build_receipt(proposal, mode):
    receipt = {
        "schema_version": "1.0",
        "candidate_id": proposal["candidate_id"],
        "interview": copy.deepcopy(proposal.get("interview") or {}),
        "mode": mode,
        "applied": mode == "apply",
        "generated_on": date.today().isoformat(),
        "counts": {
            "total": 0,
            "confirmed": 0,
            "edited": 0,
            "rejected": 0,
            "pending": 0,
            "applied": 0,
        },
        "changes": [],
        "affected_question_ids": [],
    }
    affected = set()
    for update in proposal.get("updates") or []:
        validate_update(update)
        decision = update.get("decision", "pending")
        receipt["counts"]["total"] += 1
        receipt["counts"][decision] += 1
        if mode == "apply" and decision in {"confirmed", "edited"}:
            receipt["counts"]["applied"] += 1
            status = "applied"
            affected.update(update.get("affected_question_ids") or [])
        elif decision == "rejected":
            status = "rejected"
        else:
            status = "pending" if decision == "pending" else "preview_only"
        project_data = (
            update.get("edited_project")
            if update.get("decision") == "edited"
            else update.get("project")
        ) or {}
        receipt["changes"].append(
            {
                "update_id": update["update_id"],
                "change_type": update.get("change_type", ""),
                "operation": update["operation"],
                "project_id": update.get("project_id", ""),
                "project_name": update.get("project_name")
                or project_data.get("name", ""),
                "field": update.get("field", ""),
                "value": display_value(update),
                "source": copy.deepcopy(update.get("source") or {}),
                "decision": decision,
                "status": status,
                "affected_question_ids": update.get("affected_question_ids") or [],
            }
        )
    receipt["affected_question_ids"] = sorted(affected)
    return receipt


def applied_update_keys(profile):
    keys = set()
    for history in profile.get("change_history") or []:
        interview = history.get("interview") or {}
        interview_id = str(interview.get("interview_id") or "")
        receipt = history.get("receipt") or {}
        for change in receipt.get("changes") or []:
            if change.get("status") == "applied" and change.get("update_id"):
                keys.add((interview_id, str(change["update_id"])))
    return keys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--updates", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--mode", choices=("preview", "apply"), default="preview")
    parser.add_argument("--candidate-name", default="")
    args = parser.parse_args()

    proposal = load_json(args.updates)
    candidate_id = str(proposal.get("candidate_id") or "")
    if not candidate_id:
        raise SystemExit("Update proposal requires candidate_id")
    if not isinstance(proposal.get("updates"), list):
        raise SystemExit("Update proposal updates must be an array")

    if args.profile.exists():
        profile = load_json(args.profile)
    else:
        profile = empty_profile(candidate_id, args.candidate_name)
    validate_profile(profile, candidate_id)
    receipt = build_receipt(proposal, args.mode)

    if args.mode == "apply":
        interview_id = str((proposal.get("interview") or {}).get("interview_id") or "")
        existing_keys = applied_update_keys(profile)
        duplicate_ids = [
            update["update_id"]
            for update in proposal["updates"]
            if update.get("decision", "pending") in {"confirmed", "edited"}
            and (interview_id, str(update["update_id"])) in existing_keys
        ]
        if duplicate_ids:
            joined = ", ".join(duplicate_ids)
            raise SystemExit(
                f"Refusing duplicate apply for interview {interview_id!r}: {joined}"
            )
        for update in proposal["updates"]:
            if update.get("decision", "pending") in {"confirmed", "edited"}:
                apply_one(profile, update)
        history_entry = {
            "interview": copy.deepcopy(proposal.get("interview") or {}),
            "applied_on": receipt["generated_on"],
            "receipt": copy.deepcopy(receipt),
        }
        profile["change_history"].append(history_entry)
        destination = args.output or args.profile
        atomic_write_json(destination, profile)
        receipt["profile_output"] = str(destination)

    atomic_write_json(args.receipt, receipt)
    print(args.receipt.resolve())


if __name__ == "__main__":
    main()
