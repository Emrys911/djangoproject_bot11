import openai

api_key = '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'


def get_neiro_memes():
    openai.api_key = api_key
    openai.Image.create(
        prompt='dog and cat memes',
        n=10,
        size='512x512',
        response_format='url'
    )
