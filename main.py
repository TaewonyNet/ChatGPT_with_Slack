import re
from slack import RTMClient
from chatgpt import ChatGPT
from logger import logger

# 발급받은 슬랙 bot user token 기
bot_token = "<your-slack-bot-token>"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
starterbot_id = ''

# 지속적으로 슬랙 메세지 트래킹
@RTMClient.run_on(event="message")
def chatgptbot(**payload):
    data = payload["data"]
    web_client = payload["web_client"]
    bot_id = data.get("bot_id", "")
    subtype = data.get("subtype", "")
    origin_text = data.get("text", "")
    tag_code = origin_text.split(" ")[0]

    # 메세지 정보 파악
    # print(data)
    logger.info(data)
    
    # Bot이 입력한 채팅이 아닐 경우 ChatGPT 동작
    if bot_id == "" and subtype == "" and ">" in tag_code:
        user_id, message = parse_direct_mention(origin_text)
        global starterbot_id
        # print(user_id, message, starterbot_id, user_id == starterbot_id)
        if user_id == starterbot_id:
            channel_id = data["channel"]
            # 해당 메세지 입력 시간을 파악하여 답글을 달 수 있도록 지정
            message_ts = data["ts"]

            #받아온 텍스트를 ChatGPT에 전달하고 ChatGPT의 답변 저장
            # model = 'code-davinci-002' if 'python' in message.lower() or '파이썬' in message.lower() else 'gpt-3.5-turbo' 
            model = 'gpt-3.5-turbo' 
            response = ChatGPT(message, model=model)

            logger.info(response)
            # 슬랙에 메세지 전달
            web_client.chat_postMessage(channel=channel_id, text=response, thread_ts=message_ts)

@RTMClient.run_on(event="open")
def opened(**payload):
    data = payload["data"]
    global starterbot_id
    starterbot_id = data.get("self", {}).get('id')
    print(f"Starter Bot ID : {starterbot_id}")

def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


if __name__ == "__main__":
    try:
        # RTM 클라이언트 호출 및 시작
        rtm_client = RTMClient(token=bot_token)
        print("Starter Bot connected and running!")
        rtm_client.start()
    except Exception as err:
        print(err)
