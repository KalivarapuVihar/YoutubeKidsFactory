from services.openai_service import OpenAIService
from services.lesson_generator import LessonGenerator


service = OpenAIService()

generator = LessonGenerator(service)

lesson = generator.generate("Butterflies")

print(lesson)