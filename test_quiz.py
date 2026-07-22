from models.quiz import Quiz, QuizQuestion

quiz = Quiz(
    questions=[
        QuizQuestion(
            question="What color is an apple?",
            answer="Red"
        ),
        QuizQuestion(
            question="Where do apples grow?",
            answer="On trees"
        )
    ]
)

print(quiz)