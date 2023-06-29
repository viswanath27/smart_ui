from utils.app.const import OPENAI_API_HOST, OPENAI_API_TYPE, OPENAI_API_VERSION, OPENAI_ORGANIZATION
from types.openai import OpenAIModel, OpenAIModelID, OpenAIModels
from trpc import procedure, router
from trpc.errors import TRPCError
import requests
from typing import Optional
from zod import z

async def get_models(ctx, input):
    """
    Retrieve a list of OpenAI models.

    Args:
        ctx (dict): The TRPC context.
        input (dict): The input parameters.

    Returns:
        list: The list of OpenAI models.
    """
    key = input.get('key')

    url = f"{OPENAI_API_HOST}/v1/models"
    if OPENAI_API_TYPE == 'azure':
        url = f"{OPENAI_API_HOST}/openai/deployments?api-version={OPENAI_API_VERSION}"

    headers = {
        'Content-Type': 'application/json',
    }
    if OPENAI_API_TYPE == 'openai':
        headers['Authorization'] = f"Bearer {key or os.environ['OPENAI_API_KEY']}"
    elif OPENAI_API_TYPE == 'azure':
        headers['api-key'] = f"{key or os.environ['OPENAI_API_KEY']}"
    if OPENAI_API_TYPE == 'openai' and OPENAI_ORGANIZATION:
        headers['OpenAI-Organization'] = OPENAI_ORGANIZATION

    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        raise TRPCError(code='UNAUTHORIZED', message='Unauthorized')
    elif response.status_code != 200:
        print(f"OpenAI API returned an error {response.status_code}: {response.text}")
        raise TRPCError(code='INTERNAL_SERVER_ERROR', message='OpenAI API returned an error')

    json_data = response.json()

    models = []
    for model in json_data['data']:
        model_name = model['model'] if OPENAI_API_TYPE == 'azure' else model['id']
        for key, value in OpenAIModelID.items():
            if value == model_name:
                model_info = OpenAIModels[value]
                model_obj = OpenAIModel(
                    id=model['id'],
                    name=model_info['name'],
                    maxLength=model_info['maxLength'],
                    tokenLimit=model_info['tokenLimit'],
                )
                models.append(model_obj)
                break

    return models

models = router({
    'list': procedure.input(z.object({
        'key': z.string().optional()
    })).query(get_models),
})
