from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent_dummy import *
from agent_translate import *

app = FastAPI()

# Custom exception for empty parameters
class EmptyParameterError(HTTPException):
    def __init__(self, parameter_name: str):
        super().__init__(status_code=400, detail=f"The parameter '{parameter_name}' cannot be empty.")


class Item(BaseModel):
    topic: str


# Function to validate the parameters
def validate_item(item: Item):
    if not item.topic:
        raise EmptyParameterError("topic")
    
@app.get("/")
async def ping():
   return True

@app.post("/topic")
async def query_bot(
    item: Item,
):
    # Validate input before processing
    validate_item(item)

    topic = item.topic
    
    sentence = await agent_dummy(topic)

    answer = await agent_translate(sentence['agent_dummy'])

    # API Outputs
    return {
        "answer": answer,
    }
