import json
from lxml import etree as ET


# LearningSuite XML files are encoded with the Moodle XML format
# https://docs.moodle.org/405/en/Moodle_XML_format

with open('questions.json', 'r') as json_file:
    questions_json = json.load(json_file)

def classify_question_type(question: dict):
    if 'choices' in question:
        return 'multichoice'
    else:
        return 'essay'

def html_format(text: str):
    result = text

    # Replace all \n characters by <br />
    result = result.replace('\n', '<br />')

    # Split text by '$$' and use list comprehension to add <span> and </span> alternatively.
    parts = result.split('$$')
    # Join the parts with alternating <span> and </span> tags.
    result = ''.join(
        rf'<span class="math-tex">\({part}\)</span>' if i % 2 == 1 else part
        for i, part in enumerate(parts)
    )
    return result

def add_text_field(xml: ET.ElementBase, field_name: str, field_value: str, **kwargs):
    kwargs['format'] = 'html'
    field = ET.SubElement(xml, field_name, **kwargs)
    field_value_formatted = html_format(field_value)
    ET.SubElement(field, 'text').text = ET.CDATA(f"<p>{field_value_formatted}</p>")
    return field


quiz: ET.ElementBase = ET.Element('quiz')
for question in questions_json['questions']:
    # Classify question according to type
    question_type = classify_question_type(question)
    question_xml = ET.SubElement(quiz, 'question', type=question_type)

    # Add relevant fields to XML object
    # Name field
    name = ET.SubElement(question_xml, 'name')
    ET.SubElement(name, 'text').text = f"{question['title']} [{question['id']}]"

    # Question Image and Text (HTML-formatted)
    question_text = ''
    if 'image_url' in question:
        question_text += f'<img src="{question['image_url']}" width="400" /><br />'
    if isinstance(question['question_text'], str):
        # Process as string
        question_text += question['question_text']
    elif isinstance(question['question_text'], dict):
        # Process as JSON. TODO: make sure chat spits these out in a more consistent format.
        question_text += question['question_text']['text']
        if 'formulas' in question['question_text']:
            question_text += '\n\nFormulae:\n'
            question_text += '\n'.join('\n'.join(list(formula.values())) for formula in question['question_text']['formulas'])
        if 'hints' in question['question_text']:
            question_text += '\n\nHints:\n'
            question_text += '\n'.join(question['question_text']['hints'])

    else:
        print(f'Unrecognized question text format for question {question['id']}. Question will not be exported to final XML document.')
        quiz.remove(question_xml)
        continue

    add_text_field(question_xml, 'questiontext', question_text)

    # General feedback - explains how to get solution
    if 'explanation' in question:
        add_text_field(question_xml, 'generalfeedback', question['explanation'])

    # Not sure what these are
    ET.SubElement(question_xml, 'penalty').text = '0.3333333'
    ET.SubElement(question_xml, 'hidden').text = '0'

    ET.SubElement(question_xml, 'defaultgrade').text = '1'
    ET.SubElement(question_xml, 'single').text = 'true'
    ET.SubElement(question_xml, 'shuffleanswers').text = 'true'
    ET.SubElement(question_xml, 'answernumbering').text = 'abc'

    # Feedback fields
    add_text_field(question_xml, 'correctfeedback', 'Correct!')
    add_text_field(question_xml, 'partiallycorrectfeedback', 'Almost there.')
    add_text_field(question_xml, 'incorrectfeedback', "That's not correct.")

    # Multiple choice questions
    if question_type == 'multichoice':
        if 'correct_answer' in question and 'choices' in question:
            if question['correct_answer'] not in question['choices']:
                print(f'Correct answer not in choices for question {question['id']}. Question will not be exported to final XML document.')
                quiz.remove(question_xml)
                continue
            for choice in question['choices']:
                answer = add_text_field(question_xml, 'answer', choice, fraction='100' if choice == question['correct_answer'] else '0')
                #add_text_field(answer, 'feedback', question['explanation'])
        else:
            print(f'Answer choices not provided for multichoice question {question['id']}. Question will not be exported to final XML document.')
            # Delete question from XML
            quiz.remove(question_xml)
            continue

    # Essay questions
    elif question_type == 'essay':
        answer = ET.SubElement(question_xml, 'answer', fraction='0')
        ET.SubElement(answer, 'text').text = ''

    # TODO: think of what to do with the solution


# Write XML to file
tree = ET.ElementTree(quiz)
with open('quiz.xml', 'wb') as xml_file:
    tree.write(xml_file, pretty_print=True, xml_declaration=True, encoding='UTF-8')

