from openai_requests import chat_completion


def create_prompt(topic):
    prompt = f"""
    You are a random sentence generator. Repply with just one random sentence, maximum 10 words, about the topic.

    Topic: {topic}
    """.format(topic=topic)
        
    prompt_messages = [{"role": "system", "content": prompt}]

    return prompt_messages

async def llm_dummy(topic):

    prompt_messages = create_prompt(topic)

    fallback = "Failed"
    answer = await chat_completion(prompt_messages, 0, fallback)
            
    return answer