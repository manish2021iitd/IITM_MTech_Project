from crewai import LLM, Process
from agents import scenario_agent, bdd_writer_agent, simulator_agent
from tasks import scenario_task, bdd_writer_task, simulator_task 

GEMINI_API_KEY="___________________"
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)


agents = [scenario_agent,bdd_writer_agent,simulator_agent]

tasks = [scenario_task,bdd_writer_task,simulator_task]

# Initialize the Crew object
crew = Crew(
    agents=agents,
    tasks=tasks,
    process=Process.sequential,
    full_output=True,
    verbose=True
)

# Kickoff the process
responses = crew.kickoff()
