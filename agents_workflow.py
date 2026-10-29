"""Optional CrewAI workflow. Requires `pip install -r requirements-ai.txt`,
OPENAI_API_KEY and an OpenAI-compatible CrewAI LLM configuration.

This online mode cannot be verified without the user's keys and usage credits.
"""

def run_crew(company, question, evidence):
    from crewai import Agent, Task, Crew, Process

    excerpts = '\n\n'.join(
        f'[{i}] {r["source"]}: {r["text"][:900]}'
        for i, r in enumerate(evidence, 1)
    )
    researcher = Agent(
        role='Document Evidence Analyst',
        goal='Extract defensible facts from supplied source excerpts, using citations.',
        backstory='A cautious research analyst who never fabricates company facts.',
        verbose=False, allow_delegation=False
    )
    strategist = Agent(
        role='Market Intelligence Advisor',
        goal='Assess possible risks, opportunities, and unknowns with explicit uncertainty.',
        backstory='A strategy analyst who distinguishes evidence, inference, and gaps.',
        verbose=False, allow_delegation=False
    )
    editor = Agent(
        role='Executive Report Editor',
        goal='Create a concise report with evidence citations and next steps.',
        backstory='An editor who identifies unverified claims rather than inventing them.',
        verbose=False, allow_delegation=False
    )
    t1 = Task(
        description=f'Company: {company}. Question: {question}. Only use the following retrieved evidence, cite the numbered sources exactly, and list missing data:\n{excerpts}',
        expected_output='List of source-grounded findings with [1], [2] citations and data gaps.',
        agent=researcher
    )
    t2 = Task(
        description='Use the evidence analyst output to propose tentative risks and opportunities. Label each claim as observed, inferred, or unknown.',
        expected_output='Risks/opportunities with explicit evidence and uncertainty.',
        agent=strategist, context=[t1]
    )
    t3 = Task(
        description='Write a Markdown executive brief with question, evidence, qualified risks, opportunities, limitations, and recommendations. Cite the source numbers.',
        expected_output='Markdown report; distinguish confirmed facts and interpretations.',
        agent=editor, context=[t1, t2]
    )
    return str(Crew(agents=[researcher, strategist, editor],
                    tasks=[t1, t2, t3], process=Process.sequential, verbose=False).kickoff())
