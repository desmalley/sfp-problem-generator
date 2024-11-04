import json

def unroll_json(json_chunk, prefix=""):
    """
    Unrolls a nested dictionary into a formatted string representation.

    Args:
        json_chunk (dict): The dictionary to be unrolled.
        prefix (str): A prefix to add to each key (for nested contexts).

    Returns:
        str: A formatted string representation of the dictionary.
    """
    unrolled_text = ""
    
    for key, value in json_chunk.items():
        # Capitalize the key and append the prefix if provided
        formatted_key = f"{prefix}{key.capitalize()}: "

        if isinstance(value, dict):
            # Recursively call unroll_context for nested dictionaries
            nested_prefix = prefix + key.capitalize() + " - "
            unrolled_text += unroll_context(value, nested_prefix)
        else:
            # Add the key-value pair to the unrolled text
            unrolled_text += f"{formatted_key}{value}\n"

    return unrolled_text

    # Example usage
    """context = {
        "general": {
            "abstract": "Displays created with lasers are limited in size and too expensive, making them impractical for educational and commercial applications.",
            "problem": "Current laser-based display systems are too costly and small for broader use.",
            "solution": "Replace lasers with incoherent light sources like microLEDs and sunlight.",
            "innovation": "First use of incoherent light for particle trapping, reducing costs.",
            "target": "Students and educators for affordable, scalable display technology."
        },
        "specific": {
            "phase_1": {
                "goal": "Develop a prototype of the incoherent light display.",
                "tasks": ["Test microLEDs", "Explore sunlight for display applications"]
            }
        }
    }

    # Unrolling the 'general' part of the context
    unrolled_text = unroll_context(context["general"])
    print(unrolled_text)

    # Unrolling the full context dictionary
    full_unrolled_text = unroll_context(context)
    print(full_unrolled_text)
    """


# Generate markdown for problem statement
def generate_markdown_problem(problem):

    markdown = f"""
### Problem {problem['id']}
**{problem['title']}**

*Insight*: {problem['insight']}

**Question**:
{problem['question_text']}

<img src="{problem["image_url"]}" alt="Alt Text" width="200" height="133">

---
"""
    return markdown

# Generate markdown for solution
def generate_markdown_solution(problem):
    solution = problem["solution"]
    markdown = f"""
### Solution for Problem {problem['id']}
<img src="{problem["solution_url"]}" alt="Alt Text" width="200" height="133">

**Answer**: {solution['final_answer']}

**Steps**:
"""
    for i, step in enumerate(solution['steps'], start=1):
        markdown += f"\n{i}. {step}"

    markdown += "\n\n---\n"
    return markdown





# Generate and print the markdown content

with open('input.json', 'r') as file:
    problem_data = json.load(file)

problem_markdown = generate_markdown_problem(problem_data)
solution_markdown = generate_markdown_solution(problem_data)

print("Problem Markdown:\n")
print(problem_markdown)
print("Solution Markdown:\n")
print(solution_markdown)

