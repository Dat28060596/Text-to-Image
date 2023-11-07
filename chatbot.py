import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser as wb
import openai

with open('api.txt') as file:
  openai.api_key = file.read()
def get_repsonse(prompt: str):
  response: dict = openai.Completion.create(
    model='gpt-3.5-turbo',
    prompt=prompt,
    temperature=0.9,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[' Human:', 'AI:']
  )
  choices: dict = response.get('choices')[0]
  text: str = choices.get('text')
  return text
def history(message :str, pl: list[str]):
  pl.append(message)
def create_prompt(message:str, pl: list[str]):
  p_message: str = f'\nHuman: {message}'
  history(p_message, pl)
  prompt: str= ''.join(pl)
  return prompt
def get_bot_response(message, pl):
  prompt: str = create_prompt(message, pl)
  bot_response: str = get_repsonse(prompt)
  if bot_response:
    history(bot_response, pl)
    pos: int = bot_response.find('\nAi: ')
    bot_response = bot_response[pos + 5:]
  else:
    bot_response = 'Something went wrong...'
  return bot_response

AI = pyttsx3.init()
voices = AI.getProperty('voices')
AI.setProperty('voice', voices[1].id)

def speak(audio):
    print('AI: ' + audio)
    AI.say(audio)
    AI.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%p")
    speak("It is")
    speak(Time)
def welcome():

    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good Morning Sir!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Sir!")
    elif hour >= 18 and hour < 24:
        speak("Good Evening sir")
    speak("How can I help you,boss")
def command():
    c = sr.Recognizer()
    with sr.Microphone() as source:
        c.pause_threshold = 2
        audio = c.listen(source)
    try:
        query = c.recognize_google(audio, language='en-US')
        print("you: " + query)
    except sr.UnknownValueError:
        print('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Your order is: '))
    return query
prompt_list: list[str] = ['You are a potato and will answer as a potato']

welcome()

while True:
    query = command().lower()
    if "google" in query:
      speak("What should I search,boss")
      search = command().lower()
      url = f"https://google.com/search?q={search}"
      wb.get().open(url)
      speak(f'Here is your {search} on google')

    elif "youtube" in query:
      speak("What should I search,boss")
      search = command().lower()
      url = f"https://youtube.com/search?q={search}"
      wb.get().open(url)
      speak(f'Here is your {search} on youtube')
    elif "quit" in query:
      speak("Ai is off. Goodbye boss")
      quit()
    elif 'time' in query:
      time()
    else:
      response: str = get_bot_response(query, prompt_list)
      speak(f'bot: {response}')


