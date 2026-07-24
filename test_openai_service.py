from services.openai_service import OpenAIService

service = OpenAIService()

reply = service.generate_text("Tell me one fun fact about dolphins for preschool children.")

print(reply)