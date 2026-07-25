from services.openai_service import OpenAIService
from services.topic_generator import TopicGenerator

service = OpenAIService()

generator = TopicGenerator(service)

topic = generator.generate()

print(topic)