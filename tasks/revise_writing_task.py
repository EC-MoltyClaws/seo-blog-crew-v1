from crewai.tasks.conditional_task import ConditionalTask
from crewai.tasks.task_output import TaskOutput


def _evaluation_failed(output: TaskOutput) -> bool:
    # Run the revision task only when the evaluator returned FAIL
    return "FAIL" in output.raw.upper()


def build_revise_writing_task(agent, context_tasks):
    return ConditionalTask(
        description=(
            "The evaluator has scored the blog post draft and the manager has determined "
            "that revision is required before HTML conversion can begin.\n\n"
            "Review the evaluation notes in context to understand exactly what failed. "
            "Rewrite or improve every section that caused a score deduction. "
            "Keep all sections that were not flagged unchanged. "
            "The title must remain exactly as provided in the topic brief — do not change it. "
            "Produce the full revised draft — not just the changed sections."
        ),
        expected_output=(
            "A complete revised blog post draft with all required sections, "
            "addressing every issue flagged in the evaluation notes."
        ),
        condition=_evaluation_failed,
        agent=agent,
        context=context_tasks,
    )
