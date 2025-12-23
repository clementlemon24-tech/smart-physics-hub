from models import Lesson, Quiz, Schedule
import random
from datetime import datetime, timedelta
import os
from openai import OpenAI

# Sample content templates for physics units (fundamental, derived, and derivatives)
physics_topics = [
    ('Fundamental Units: Length (Meter)', 'Meter is the unit of length. Symbol: m. Fundamental unit. Example: length of a table. Derivatives: kilometer (km) = 1000 m, centimeter (cm) = 0.01 m.'),
    ('Fundamental Units: Mass (Kilogram)', 'Kilogram is the unit of mass. Symbol: kg. Fundamental unit. Example: weight of a book. Derivatives: gram (g) = 0.001 kg, tonne = 1000 kg.'),
    ('Fundamental Units: Time (Second)', 'Second is the unit of time. Symbol: s. Fundamental unit. Example: time for heartbeat. Derivatives: minute = 60 s, hour = 3600 s.'),
    ('Derived Units: Force (Newton)', 'Newton is derived from kg*m/s². Symbol: N. Force = mass * acceleration. Example: gravity force. Derivatives: kilonewton (kN) = 1000 N.'),
    ('Derived Units: Energy (Joule)', 'Joule is N*m or kg*m²/s². Symbol: J. Energy = force * distance. Example: kinetic energy. Derivatives: kilojoule (kJ) = 1000 J, calorie ≈ 4.184 J.'),
    ('Derived Units: Electric Current (Ampere)', 'Ampere is fundamental for current. Symbol: A. But derived for charge: Coulomb (C) = A*s. Example: current in wire. Derivatives: milliampere (mA) = 0.001 A.')
]

def auto_create_lesson(subject, topic_tuple):
    topic, _ = topic_tuple  # Ignore the sample content
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Generate a detailed, educational lesson on the physics topic: {topic}.
    The lesson should be suitable for high school or introductory college level.
    Include:
    - Definition and explanation
    - Key concepts and formulas
    - Real-world examples
    - Common applications
    - Any important historical context if applicable
    Make it engaging and easy to understand, around 300-500 words.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or gpt-4 if available
            messages=[
                {"role": "system", "content": "You are a knowledgeable physics teacher creating educational content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        generated_content = response.choices[0].message.content.strip()
        calculations = ai_generate_calculations(topic)
        full_content = generated_content + "\n\nCalculations:\n" + calculations
        return Lesson(subject, topic, full_content)
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        # Fallback to original content if available
        _, fallback_content = topic_tuple
        return Lesson(subject, topic, fallback_content)
    except Exception as e:
        print(f"Unexpected error: {e}")
        _, fallback_content = topic_tuple
        return Lesson(subject, topic, fallback_content)

def ai_generate_calculations(topic):
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found in environment variables. Please set OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Generate step-by-step physics calculations and numerical examples for the topic: {topic}.
    Include:
    - Step-by-step derivation of key formulas
    - Numerical examples with calculations
    - Units and conversions if applicable
    Make it educational and clear, around 200-300 words.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a physics expert providing calculation examples."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        generated_calculations = response.choices[0].message.content.strip()
        return generated_calculations
    except Exception as e:
        print(f"Error generating calculations: {e}")
        return "Calculations could not be generated."

def auto_create_quiz(subject, topic_tuple):
    topic, _ = topic_tuple
    # Simple quiz generation for physics calculations
    questions = [
        {'question': f'Calculate the {topic} for given values.', 'options': ['Formula 1', 'Formula 2', 'Formula 3'], 'answer': 'Formula 1'},
        {'question': 'Derive the equation for this scenario.', 'options': ['Step 1', 'Step 2', 'Step 3'], 'answer': 'Step 1'}
    ]
    return Quiz(subject, topic, questions)

def auto_create_schedule(subject, topics, start_date):
    lessons = [auto_create_lesson(subject, topic) for topic in topics]
    quizzes = [auto_create_quiz(subject, topic) for topic in topics]
    dates = {}
    current_date = start_date
    for i, lesson in enumerate(lessons):
        dates[str(current_date)] = f'Lesson: {lesson.topic}'
        current_date += timedelta(days=1)
        if i < len(quizzes):
            dates[str(current_date)] = f'Quiz: {quizzes[i].topic}'
            current_date += timedelta(days=1)
    return Schedule(subject, lessons, quizzes, dates)