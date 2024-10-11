from .greetings import greetings_responses
from .topics import topics_responses

def get_response(topic, message):
    if topic in topics_responses:
        if message.lower() in topics_responses[topic]:
            return topics_responses[topic][message.lower()]
    
    if message.lower() in greetings_responses:
        return greetings_responses[message.lower()]
    
    if message.lower() == "change topic":
        return "TOPIC_CHANGE"
    elif message.lower() in ["goodbye", "bye", "exit"]:
        return "END_CHAT"
    
    return f"I'm not sure how to respond to that in the context of {topic}. Can you try rephrasing or ask something else?"

def get_topics():
    return list(topics_responses.keys())