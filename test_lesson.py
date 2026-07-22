from models.activity import Activity
from models.lesson import Lesson
from models.metadata import Metadata
from models.quiz import Quiz, QuizQuestion
from models.song import Song

activity = Activity(
    title="Find Something Red",
    instructions="Look around your room and find a red object."
)

quiz = Quiz(
    questions=[
        QuizQuestion(
            question="What color is an apple?",
            answer="Red"
        ),
        QuizQuestion(
            question="Where do apples grow?",
            answer="On trees"
        ),
        QuizQuestion(
            question="What is the taste of an apple?",
            answer="Sweet or tart"
        )
    ]
)

song = Song(
    title="Apple Song",
    lyrics="Apple Apple Red and Bright",
    mood="Happy",
    duration_seconds=45
)

metadata = Metadata(
    title="Learn Apples for Kids",
    description="A fun educational lesson about apples.",
    tags=[
        "apple",
        "kids",
        "learning"
    ]
)

lesson = Lesson(
    topic="Apple",
    introduction="Today we will learn about apples.",
    examples=[
        "Apple is red.",
        "Apple grows on trees."
    ],
    activity=activity,
    quiz=quiz,
    song=song,
    metadata=metadata,

    difficulty="Beginner",
    estimated_duration_minutes=60,
    language="English"
)

# print("\nLesson Topic:")
# print(lesson.topic)

# print("\nSong Title:")
# print(lesson.song.title)

# print("\nActivity:")
# print(lesson.activity.title)

# print("\nFirst Quiz Question:")
# print(lesson.quiz.questions[0].question)

# print("\nFirst Quiz Answer:")
# print(lesson.quiz.questions[0].answer)

# print("\nVideo Title:")
# print(lesson.metadata.title)

# print("\nTags:")
# print(lesson.metadata.tags)

# lesson_dict = lesson.model_dump()

# print("\nDictionary:")
# #print(lesson_dict)

# print("\nJSON:")

# print(
#     lesson.model_dump_json(
#         indent=4
#     )
# ) 



print(lesson.quiz.questions[2].answer)
print(len(lesson.quiz.questions))
print(lesson.metadata.tags[-1])
