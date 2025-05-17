from crewai import Task

scenario_task = Task(
    description=f"""Interpret the following high-level ADAS requirement: {requirement}.

                    Think through this step-by-step:
                    - First, identify what ADAS function is being tested (e.g., AEB, ACC, Lane Assist)
                    - Break down the requirement into:
                        - Environment conditions (weather, time, road type)
                        - Ego vehicle configuration (type, speed, lane, heading)
                        - Other actors and their behavior
                        - Trigger event (e.g., pedestrian suddenly crossing)
                        - Expected ADAS outcome (e.g., emergency braking, no collision)
                    - Then, systematically vary one or more elements to create distinct scenarios:
                        - Vary weather, lighting, or road geometry
                        - Vary actor types and positions
                        - Change trigger timings and distances
                    - Represent each variation clearly in a structured JSON dictionary.

                    Output format:
                    {{
                        "Scenario 01": {{
                            "environment": {{...}},
                            "ego_vehicle": {{...}},
                            "actors": [{{...}}],
                            "expected_outcome": "..."
                        }},
                        ...
                    }}""",
    expected_output="A JSON dictionary with uniquely labeled scenario variants based on the requirement.",
    output_file="/content/scenario.json",
    agent=scenario_agent
)

bdd_writer_task = Task(
    description="""Read the structured scenario JSON from `/content/scenario.json`.

                  Think through the following steps:
                  1. For each scenario:
                      - Parse the JSON and extract relevant details.
                      - Determine feature title and unique scenario name.
                  2. Create a `.feature` file using the Gherkin Given-When-Then syntax.
                      - Use `Given` for initial conditions like weather and ego vehicle state.
                      - Use `And` to describe other actors and their configuration.
                      - Use `When` to describe the trigger event.
                      - Use `Then` to define expected ADAS behavior.
                  3. Repeat for all scenarios and append them clearly in the same file.

                  Ensure syntax correctness and readability for downstream automation tools.""",
    expected_output="A single `.feature` file containing one or more well-structured ADAS test cases.",
    output_file="/content/bdd_generated_files.feature",
    agent=bdd_writer_agent
)

simulator_task = Task(
    description="""Generate a Python simulation script based on BDD `.feature` file `/content/bdd_generated_files.feature`.

                    Think step-by-step:
                    1. Parse the `.feature` file and extract:
                        - Scenario name and description
                        - Environment conditions (weather, time, road type)
                        - Ego vehicle configuration
                        - Actor types, locations, and trigger behavior
                    2. Translate these into Python using CARLA’s API:
                        - Connect to CARLA (`carla.Client(...)`)
                        - Get blueprint library, spawn vehicles/actors
                        - Attach camera sensor and set up logging
                        - Run simulation in `world.tick()` loop
                        - Implement trigger logic (e.g., event at t=5s)
                    3. Add logging and proper cleanup:
                        - Print key steps
                        - Save sensor data
                        - Destroy actors and sensors on exit

                    Your output must be a clean, executable script named `run_simulation.py` that runs on a local CARLA server.""",
    expected_output="A fully functional Python script using CARLA Python API implementing the BDD scenario logic.",
    output_file="/content/simulationpy/run_simulation.py",
    agent=simulator_agent
)

