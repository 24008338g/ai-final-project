from fireworks import Fireworks
import traceback

client = Fireworks()

try:
    response = client.chat.completions.create(
        model='fireworks/flux-kontext-pro',
        messages=[{
            'role': 'user',
            'content': 'Generate a JSON object with key "image_base64" containing a base64-encoded PNG of a dark gothic hallway lit by candles.'
        }],
        max_tokens=400,
        temperature=0.7
    )
    print('response type:', type(response))
    print('response repr:', response)
    print('choices count:', len(response.choices))
    if response.choices:
        choice = response.choices[0]
        print('choice text:', getattr(choice, 'text', None))
        if hasattr(choice, 'message'):
            print('choice message:', choice.message)
except Exception as e:
    traceback.print_exc()
