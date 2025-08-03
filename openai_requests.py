import requests
import logging
import json
import openai

from config import AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY

AZURE_OPENAI_API_VERSION = '2024-08-01-preview'
CHAT_COMPLETION_DEPLOYMENT = 'gpt-4o'

openai_client = openai.AsyncAzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_API_KEY, api_version=AZURE_OPENAI_API_VERSION)


class FailedOpenAIChatCompletionRequest(Exception):
    pass


class FailedOpenAIEmbeddingRequest(Exception):
    pass


def validate_json_format(content, json_schema):
    '''Auxiliary function used to validate LLM JSON response'''
    for key, value in content.items():
        if key not in json_schema.keys():
            return f"LLM response contains an unexpected key '{key}'"
        else:
            allowed_values = json_schema[key]
            if len(allowed_values) > 0 and value not in allowed_values:
                return f"LLM response contains a not allowed value '{value}' for field '{key}'"
    
    for key in json_schema.keys():
        if key not in content.keys():
            return f"LLM response is missing the key '{key}'"
        
    return None


async def chat_completion(messages, temperature, fallback=None, response_format='string', json_schema=None):
    '''
    Function that makes a request to the chat completion Azure OpenAI endpoint and validates that the response is in the right format.
    If the request fails or the output does have the expected format, the function will return the 

    Inputs:
        * messages: A list of messages comprising the conversation so far.
        * temperature: Model parameter (number between 0 and 2) that controls how the deterministic the output is (higher temperature -> less deterministic)
        * fallback: Value to return if the request fails. Must have the type defined in 'response_format'. If None, an exception will be raised if the request fails.
        * response_format: How the LLM should output the result. Must be either 'string' or 'json'. If 'json', the prompt should instruct the model to generate output in this format.
        * json_schema: Schema of json to be returned. Keys should be the same as intended in the response, while the values should be lists of allowed values for that field.
                       When a value is an empty list, then the field may have any value. If not defined, no schema validation is made.
    '''
    assert 0 <= temperature <= 2, f"The value '{temperature}' for input 'temperature' is not a number between 0 and 2."
    response_format = response_format.lower()
    assert response_format in ('string', 'json'), f"The value '{response_format}' for input 'response_format' must either 'string' or 'json'."
    if fallback is not None:
        if response_format == 'string':
            assert type(fallback) == str, f"The value '{fallback}' for input 'fallback' must a string, since 'response_format' is 'string'"
        else:
            assert type(fallback) == dict, f"The value '{fallback}' for input 'fallback' must a dictionary, since 'response_format' is 'json'."
            if json_schema is not None:
                validation_fallback = validate_json_format(fallback, json_schema)
                assert validation_fallback is None, f"Input 'fallback' is not valid as defined by 'json_schema': {validation_fallback.replace('LLM response', 'fallback')}" 

    error_message = None

    # Make request to OpenAI
    try:
        if response_format == 'json':
            result = await openai_client.chat.completions.create(model=CHAT_COMPLETION_DEPLOYMENT, messages=messages, temperature=temperature, response_format={"type": "json_object"})
        else:
            result = await openai_client.chat.completions.create(model=CHAT_COMPLETION_DEPLOYMENT, messages=messages, temperature=temperature)
    except openai.APIConnectionError as e:
        error_message = f"Error connecting to Azure OpenAI endpoint:\n {e.__cause__}"
    except openai.APIStatusError as e:
        try:
            error_dict = e.response.json()
            # Catch prompt filtering errors to add more information
            if error_dict['error']['innererror']['code'] == 'ResponsibleAIPolicyViolation':
                error_message = f"Request blocked by content filter at input."
                error_message += f"\n Input content filter results:\n {error_dict['error']['innererror']['content_filter_result']}"
            else:
                error_message = e.message
        except:
            error_message = e.message
    else:     
        response_choices = result.choices[0]
        # Check if model stopped generating for the right reason
        if response_choices.finish_reason == 'content_filter':
            error_message = f"Request blocked by content filter at output."
            error_message +=  f"\n Output content filter results:\n {response_choices.content_filter_results}"
        elif response_choices.finish_reason != 'stop':
            error_message = f"Model output finished for reason '{response_choices.finish_reason}' instead of 'stop'."
        else:
            content = response_choices.message.content
            if response_format == 'json':
                try:
                    content = json.loads(content)
                    assert type(content) == dict
                except:
                    error_message = f"LLM response '{content}' not in the expected format"
                else:
                    if json_schema is not None:
                        error_message = validate_json_format(content, json_schema)
                    
    if error_message is not None:
        # If fallback not defined, raise exception
        if fallback is None:
            raise FailedOpenAIChatCompletionRequest(error_message)
        # If fallback is defined, log the error and return fallback
        # The try except block is just so logging.exception can be used
        try:
            raise FailedOpenAIChatCompletionRequest(error_message)
        except FailedOpenAIChatCompletionRequest as e:
            logging.exception(e)
            logging.warning(f"Returning fallback value: '{fallback}'")
            return fallback
    else:
        return content