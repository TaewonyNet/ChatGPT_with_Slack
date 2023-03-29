import openai

# 발급받은 OpenAI API Key 기입
YOUR_API_KEY = '<your-openai-api-key>'


def ChatGPT(prompt, API_KEY=YOUR_API_KEY, model='gpt-3.5-turbo'):
    # api key 세팅
    openai.api_key = API_KEY

    # ChatGPT API 호출
    # https://platform.openai.com/docs/models/gpt-4
    completion = openai.ChatCompletion.create(
        model=model #'gpt-3.5-turbo' #'text-davinci-003'  # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
        , messages=[{'role':'user', 'content':prompt}]
        , temperature=0.5
        , max_tokens=1024
        , top_p=1
        , frequency_penalty=0
        , presence_penalty=0)

    return completion['choices'][0]['message']['content']


def main():
    # 지문 입력 란
    prompt = input("Insert a prompt: ")
    # print(ChatGPT(prompt).strip())


if __name__ == '__main__':
    main()
