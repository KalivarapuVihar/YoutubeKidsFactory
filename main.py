from services.lesson_generator import LessonGenerator
from services.openai_service import OpenAIService


def main():

    service = OpenAIService()

    generator = LessonGenerator(service)

    lesson = generator.generate(
        topic="Butterflies"
    )

    print()

    print("Lesson Generated Successfully!")

    print()

    print(lesson.topic)

    print()

    print(lesson.introduction)


if __name__ == "__main__":
    main()