from agent_translate.llm_translate import llm_translate

async def agent_translate(message):

    var1 = '' #global_status['var1']
    var2 = '' #global_status['var2']

    answer = await llm_translate(message)

    global_status_update = {'agent_translate': answer}
        
    return global_status_update