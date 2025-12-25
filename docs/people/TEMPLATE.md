# New Person Submission Template

**Before submitting:** Open a GitHub Issue first to discuss the addition. All new people require community review.

---

## Required Information

### 1. Basic Profile

| Field | Required | Example |
|-------|----------|---------|
| Full Name | Yes | David Grusch |
| Title/Role | Yes | Former Intelligence Officer |
| Known For | Yes | Congressional UAP testimony |
| Active Since | Yes | 2023 |
| Primary Platform | Yes | Congressional testimony, Podcasts |
| Photo | Yes | 300x300px minimum, public domain or licensed |

### 2. Scoring (each 0.0 - 1.0)

| Criterion | Score | Rationale (required) |
|-----------|-------|----------------------|
| Evidence | 0.X | Why this score? What sources do they cite? |
| Consistency | 0.X | Do their positions change? Contradictions? |
| Transparency | 0.X | Do they cite sources? Correct errors? |
| Sensationalism | 0.X | Measured or dramatic presentation? |
| Ethics | 0.X | Conflicts of interest? Monetization? |

**Scoring guide:** 0.0 = No issues, 0.5 = Some concerns, 1.0 = Major problems

### 3. Minimum 2 Documented Quotes

Each quote must include:

- **Exact verbatim text** (no paraphrasing)
- **Date** (Month Day, Year)
- **Source** (specific show, article, hearing, etc.)
- **Context** (circumstances, what prompted the statement)
- **Fact check status**: TRUE / FALSE / UNVERIFIED with explanation

### 4. Sources

- At least 2 verifiable sources
- Archive links preferred (archive.org, etc.)
- No paywalled-only sources

---

## Markdown Template

Copy everything below this line for your submission:

{% raw %}
```markdown
<div class="person-header">
    <img src="../../assets/images/people/FILENAME.svg" alt="NAME" class="person-image">
    <div class="person-info">
        <div class="person-name">FULL NAME</div>
        <div class="person-title">TITLE/ROLE</div>
        {{ score_breakdown(evidence=0.5, consistency=0.5, transparency=0.5, sensationalism=0.5, monetization=0.5, evidence_note="WHY", consistency_note="WHY", transparency_note="WHY", sensationalism_note="WHY", monetization_note="WHY") }}
        <div class="info-grid">
            <span class="info-item"><span class="info-label">Known For:</span> <span class="info-value">WHAT</span></span>
            <span class="info-item"><span class="info-label">Active:</span> <span class="info-value">YEAR</span></span>
            <span class="info-item"><span class="info-label">Platform:</span> <span class="info-value">WHERE</span></span>
        </div>
    </div>
</div>

---

## Tracked Quotes

<div class="quote-box">
    <div class="quote-date">Month Day, Year</div>
    <div class="quote-source">Source Name</div>
    <div class="quote-text">
        "Exact verbatim quote here"
    </div>
    <div class="quote-context">
        <span class="quote-context-label">Context:</span> Circumstances of the statement
    </div>
    <div class="fact-check unverified">
        <span class="fact-check-label">UNVERIFIED</span> — Explanation
    </div>
</div>

---

## Updates

- **Date**: Any corrections or updates

## Sources

- [Source 1](URL) — Description
- [Source 2](URL) — Description

---

<small>**Last Updated:** {{ last_updated() }}</small>
```
{% endraw %}

---

## Submission Checklist

- [ ] Opened GitHub Issue for discussion first
- [ ] All required fields completed
- [ ] 5 scores with rationales
- [ ] Minimum 2 quotes with full attribution
- [ ] At least 2 verifiable sources
- [ ] Photo provided (or placeholder acceptable)
- [ ] Reviewed by at least one other contributor
