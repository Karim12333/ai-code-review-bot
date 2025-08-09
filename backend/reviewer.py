import yaml, textwrap
from typing import Dict, Any, List
from openai import OpenAI
from config import settings
from models import ReviewResult, FileReview, Finding

client = OpenAI(api_key=settings.openai_api_key)

DEFAULT_RULES = {
    "max_findings_per_file": 5,
    "focus": ["correctness", "security", "performance", "readability"],
    "ignore_globs": ["*.lock", "*.md", "dist/**", "build/**"],
    "severity_threshold": "info"  # info | minor | major | critical
}

SEVERITY_ORDER = {"info":0, "minor":1, "major":2, "critical":3}

def parse_repo_rules(config_text: str | None) -> Dict[str, Any]:
    try:
        if not config_text:
            return DEFAULT_RULES
        y = yaml.safe_load(config_text) or {}
        return {**DEFAULT_RULES, **y}
    except Exception:
        return DEFAULT_RULES

def shorten_patch(patch: str, max_chars: int) -> str:
    if not patch:
        return ""
    if len(patch) <= max_chars:
        return patch
    head = patch[: max_chars // 2]
    tail = patch[-max_chars // 2 :]
    return f"{head}\n... [truncated] ...\n{tail}"

async def review_changed_files(owner: str, repo: str, pr_number: int, changed: List[Dict[str, Any]], repo_rules: Dict[str, Any]) -> ReviewResult:
    files_payload = []
    for f in changed:
        if f.get("status") in {"removed", "renamed"}:
            # skip removed and summarized renamed without patch
            continue
        path = f["filename"]
        patch = f.get("patch") or ""
        files_payload.append({"path": path, "patch": shorten_patch(patch, settings.max_patch_chars)})

    if not files_payload:
        return ReviewResult(summary="No actionable changes detected.", files=[])

    system = (
        "You are a senior code reviewer. Provide concise, actionable feedback.\n"
        "Return findings grouped by file as JSON only, with keys: file, findings[{severity,title,details,suggestion}]. "
        "Severity one of: info, minor, major, critical. Keep it practical; include concrete suggestions."
    )

    user_instructions = textwrap.dedent(f"""
    Project rules (YAML):
    {yaml.safe_dump(repo_rules, sort_keys=False)}

    Pull Request diff hunks:
    {yaml.safe_dump(files_payload, sort_keys=False)}
    """)

    resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":user_instructions}
        ],
        response_format={"type":"json_object"}
    )

    data = resp.choices[0].message.content
    # Defensive parse: LLM returns object like {"files":[{file,findings:...}], "summary":"..."} or similar
    import json
    try:
        payload = json.loads(data)
    except Exception:
        payload = {"files": [], "summary": "AI returned unparsable output."}

    files = []
    for f in payload.get("files", []):
        findings = []
        for g in f.get("findings", []):
            findings.append(Finding(
                severity=g.get("severity","info"),
                title=g.get("title",""),
                details=g.get("details",""),
                suggestion=g.get("suggestion")
            ))
        files.append(FileReview(file=f.get("file", "unknown"), findings=findings))

    summary = payload.get("summary") or "Automated review generated."
    # Apply severity threshold & cap per file
    minsev = SEVERITY_ORDER.get(repo_rules.get("severity_threshold","info"), 0)
    maxpf = int(repo_rules.get("max_findings_per_file", 5))
    for fr in files:
        fr.findings = [x for x in fr.findings if SEVERITY_ORDER.get(x.severity,0) >= minsev][:maxpf]

    return ReviewResult(summary=summary, files=files)

def render_markdown(result: ReviewResult, tag: str) -> str:
    lines = []
    lines.append(f"<!-- {tag} -->")
    lines.append("## 🤖 AI Code Review\n")
    lines.append(result.summary.strip())
    for fr in result.files:
        if not fr.findings:
            continue
        lines.append(f"\n### `{fr.file}`")
        for f in fr.findings:
            lines.append(f"- **{f.severity.upper()}** — **{f.title}**\n  {f.details.strip()}")
            if f.suggestion:
                lines.append(f"  \n  _Suggestion_: {f.suggestion.strip()}")
    lines.append("\n> _Re-run automatically on new commits (synchronize)_")
    return "\n".join(lines)
