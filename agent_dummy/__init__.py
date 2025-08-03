from agent_dummy.llm_dummy import llm_dummy

async def agent_dummy(message):

    var1 = '' #global_status['var1']
    var2 = '' #global_status['var2']

    answer = await llm_dummy(message)

    global_status_update = {'agent_dummy': answer}
        
    return global_status_update