# Rules - Thresholds & Monitoring

This file contains operational rules and thresholds to monitor continuously.

## Token Thresholds - Boot Files

To avoid saturating the context window at boot, initialization files must respect these thresholds:

- **identity.md**: max 3,000 tokens (~12k chars)
- **personal.md**: max 5,000 tokens (~20k chars)
- **rules.md**: max 2,000 tokens (~8k chars)
- **TOTAL boot files**: max 10,000 tokens (~40k chars)

### Continuous Monitoring

When loading boot files, verify:
1. Individual file size vs thresholds
2. Total combined size
3. Report if thresholds exceeded and propose optimizations

### Overflow Management

If a file exceeds threshold:
- **identity.md**: move detailed rules to rules.md, keep only essentials
- **personal.md**: move project details to projects/name.md, keep only one-liners
- **rules.md**: evaluate if some rules belong in other specific files

## Project Structure

### Projects WITH Repository

For projects with a GitHub repo, keep ONLY a one-liner in **personal.md**:
```markdown
### project-name
**Repo:** https://github.com/user/project-name
**Local:** /local/path/if/exists/
Brief description (max 1 line)
```

**IMPORTANT**: Keep BOTH (repo + local path), even if local path is deleted. This way if you delete the local directory, you still know what we're talking about from the repo.

### Projects WITHOUT Repository

For projects without a GitHub repo, create detailed file in **projects/project-name.md** with:
- Full description
- Tech stack
- Status
- Features
- Notes

In **personal.md** just a one-liner pointing to the file:
```markdown
### project-name
**Details:** projects/project-name.md
Brief description (max 1 line)
```

**IMPORTANT - When NOT to use projects/**:
- ❌ If project SHOULD have a repo (even if it doesn't yet) → use `log/` for temporary notes
- ❌ If it's a one-time task or event documentation → use `log/YYYY/YYYY-MM-DD-description.md`
- ✅ Only real projects without definitive repo (internal tools, experiments, docs for others' projects)

### General Rule

**ONE OR THE OTHER**: don't duplicate. Either in projects/ OR it's a repo, never both for the same level of detail.

### Notes for Projects WITH Repo

**IMPORTANT**: If a project has its own repository, notes/ideas go **directly in the repo**, NOT in brain/.

**Practical example**:
- Sketch: "add references to Divine Comedy"
- ❌ WRONG: Add in `brain/personal.md`
- ✅ CORRECT: Create `project/docs/literary-inspirations.md` in project repo

**Motivation**:
- Project context lives in its repo
- Brain contains only pointers (one-liner in personal.md)
- Maintain separation: brain = overview, repo = details

## Log Structure

- **log/**: work, business projects, clients, professional tasks
- **diary/**: personal life, emotions, family, friends, thoughts, memories
- **projects/**: specific projects without repo
- Flexible granularity: `2025.md`, `2025/2025-10.md`, `2025/2025-10-15.md`, or even `1983.md` for ancient events
