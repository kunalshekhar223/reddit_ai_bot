import os
import praw
import openai
import datetime as datetime

# Authentication credentials
client_id = 'zI2Uznsrqc77p62Pik85tw'
client_secret = 'e48XaFRHDV3kMP0FMJRz96MrpRGY3Q'
user_agent = 'testing_bot'
username = 'chandler_not_nice'
password = 'Kunal@3143'
openai_api_key = ''

# Create a Reddit API instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password
)

openai.api_key = openai_api_key
# Example usage: Retrieve and print the title of the top posts in a subreddit
subreddit_name = 'progr'

# Get the subreddit instance
subreddit = reddit.subreddit(subreddit_name)

trigger_phrase = "!bot"
  
# check every comment in the subreddit
comment = subreddit.stream.comments(skip_existing=True)

def logger(user_response, ai_response,comment_score):
    try:
        log_file = 'chat_logs.txt'
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f'{timestamp} - User: {user_response}\n{timestamp} - AI: {ai_response}\n - Comment score: {comment_score} ---------------\n'
        
        with open(log_file, 'a',encoding="utf-8") as file:
            file.write(log_entry)
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def chatbot(input):
    messages = [{"role": "system", "content": "You are a offensive assistant and also sarcastic."},
                {"role": "system", "content": "Add a emoji to represent the tone of the response"},]
    try:
        if input:
                messages.append({"role": "user", "content": input})
                chat = openai.ChatCompletion.create(
                                                    model="gpt-3.5-turbo", 
                                                    messages=messages,
                                                    max_tokens=100,
                                                    temperature=0.8,
                                                    n=1,
                                                    stop=None,
                                                    frequency_penalty=0.6,
                                                    presence_penalty=0.2
                                                    )
                reply = chat.choices[0].message.content
                # print(reply)
                print("----")
                messages.append({"role": "assistant", "content": reply})
                return reply
    except Exception as e:
        error = f"An error occurred: {str(e)}"
        return error

for top_level_comment in comment:
    # check the trigger_phrase in each comment
    if trigger_phrase in top_level_comment.body:
        # extract the word from the comment
        word = top_level_comment.body.replace(trigger_phrase,"")
        print("----")
        print(word)
        # initialize the reply text
        reply_text = chatbot(word)
        # comment the similar words
        top_level_comment.reply(reply_text)
        logger(word,reply_text,top_level_comment.score)
        print(top_level_comment.score)

