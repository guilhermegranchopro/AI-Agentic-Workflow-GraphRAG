from openai_requests import chat_completion


def create_prompt(sentence):
    prompt = f"""
    You will translate the SENTENCE from english to portugiese from Portugal.

    SENTENCE: {sentence}
    """.format(topic=sentence)
        
    prompt_messages = [{"role": "system", "content": prompt}]

    return prompt_messages

async def llm_translate(sentence):

    prompt_messages = create_prompt(sentence)

    fallback = "Failed"
    answer = await chat_completion(prompt_messages, 0, fallback)
            
    return answer