from crewai import Task


def build_evaluate_writing_task():
    return Task(
        description=(
            "Score the blog post draft produced by the writer in this crew against the three "
            "matrices below. Each matrix is marked out of 20. A total of 48/60 or above is a PASS.\n\n"

            "--- MATRIX 1: SEO Friendly (out of 20) ---\n"
            "Award points based on how many of these are present and correct:\n"
            "  - At least 2 APA in-text citations in the body (4 pts)\n"
            "  - References section with full APA 7th edition entries and source URLs (3 pts)\n"
            "  - FAQ contains exactly 5 questions (3 topic-related, 2 product-related) (4 pts)\n"
            "  - Meta description is between 150 and 160 characters (3 pts)\n"
            "  - URL handle is lowercase letters and hyphens only (2 pts)\n"
            "  - Tags is a non-empty comma-separated keyword string (2 pts)\n"
            "  - First product mention links to the UTM URL (2 pts)\n\n"

            "--- MATRIX 2: Clear Answer Paragraph (out of 20) ---\n"
            "Identify the main question the post is trying to answer (from the title or brief). "
            "Check whether the key insights section directly and completely answers the "
            "central question. Score on:\n"
            "  - It directly and completely answers the main question (15 pts)\n"
            "  - It reads as a standalone answer with no assumed context (5 pts)\n\n"

            "--- MATRIX 3: Original Insight (out of 20) ---\n"
            "Does the post contain at least one observation, angle, or recommendation that goes "
            "beyond summarising what other articles say? Score on:\n"
            "  - At least one specific, non-generic insight tied to the topic (8 pts)\n"
            "  - The insight is supported by evidence or clear reasoning (7 pts)\n"
            "  - The insight would not appear in a generic search result on this topic (5 pts)\n\n"

            "Return your evaluation in exactly this format:\n"
            "MATRIX 1 — SEO Friendly: [score]/20\n"
            "MATRIX 2 — Clear Answer Paragraph: [score]/20\n"
            "MATRIX 3 — Original Insight: [score]/20\n"
            "TOTAL: [sum]/60\n"
            "RESULT: PASS or FAIL\n"
            "NOTES: [brief explanation for each score, and specific fixes required if FAIL]"
        ),
        expected_output=(
            "Three matrix scores (each out of 20), a total out of 60, a PASS or FAIL result, "
            "and brief notes explaining each score with specific fixes listed if the result is FAIL."
        ),
    )
