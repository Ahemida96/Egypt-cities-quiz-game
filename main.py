import turtle
import pandas as pd

FONT = ('Courier', 15, 'normal')
FONT_2 = ('Courier', 10, 'normal')
MINUTES = 5
# Create the timer object
timer = turtle.Turtle()
timer.hideturtle()
timer.color("black")
timer.penup()
timer.goto(-280, 250)
timer_flag = False

map_path = "egypt-map.gif"
screen = turtle.Screen()
screen.title("Egypt Cities Game")
screen.tracer(0)
turtle.bgpic(map_path)
turtle.pu()
turtle.hideturtle()


def countdown(minutes=MINUTES, seconds=0):
    global timer_flag
    if minutes >= 0 and seconds >= 0:
        time_string = f"Time left: {minutes:02d}:{seconds:02d}"
        timer.clear()
        timer.write(time_string, align="center", font=("Courier", 10, "bold"))
        if seconds > 0:
            seconds -= 1
        else:
            minutes -= 1
            seconds = 59
        if not timer_flag:
            turtle.ontimer(lambda: countdown(minutes, seconds), 1000)
    else:
        timer.clear()
        timer.write("Time's up, last chance!", align="center", font=("Courier", 10, "bold"))
        timer_flag = True


governorate_data = pd.read_csv("egypt-governorates.csv")
cities_names_ar = governorate_data["governorate_name_ar"].tolist()
cities_names_en = governorate_data["governorate_name_en"].tolist()
guessed_governorate = []
user_tries = 0


def game_end(cities_name):
    remained_governorates = [gov for gov in cities_name if gov not in guessed_governorate]
    states_to_learn = pd.DataFrame(remained_governorates)
    states_to_learn.to_csv("governorates_to_learn.csv")
    turtle.goto(-290, -50)
    accuracy = 0
    if user_tries != 0:
        accuracy = round((len(guessed_governorate) * 100) / user_tries)
    if len(guessed_governorate) == 27:
        turtle.write(f"You got all guesses right! GOOD JOB\nGuess accuracy: {accuracy}%",
                     align="left", font=FONT)
    else:
        turtle.write(f"You get {len(guessed_governorate)} right guesses\nGuess accuracy: {accuracy}%\nLeft:",
                     align="left", font=FONT)
        for cities in remained_governorates:
            turtle.sety(turtle.ycor()-18)
            if turtle.ycor() < -290:
                turtle.setposition(-100, -50)
            turtle.write(f"{cities}", align="left", font=FONT)


def game(cities_name, column, title):
    global timer_flag
    global user_tries
    countdown()
    while len(guessed_governorate) < len(cities_name) and not timer_flag:
        screen.update()
        try:
            user_answer = screen.textinput(title=f"{len(guessed_governorate)}/{len(cities_name)} Correct Guesses",
                                           prompt=title).title()
        except Exception:
            user_answer = None
        if user_answer == "exit" or user_answer is None:
            timer_flag = True
            game_end(cities_name)
            break

        if user_answer in cities_name and user_answer not in guessed_governorate:
            guessed_governorate.append(user_answer)
            target_governorate = governorate_data[governorate_data[column] == user_answer]
            turtle.goto(int(target_governorate.x), int(target_governorate.y))
            turtle.write(user_answer, font=FONT_2)
        user_tries += 1

    else:
        timer_flag = True
        game_end(cities_name)


try:
    game_mode = int(screen.textinput("Choose the game language", "1-English\n2-العربية"))
except Exception:
    game_mode = 0
if game_mode == 1:
    game(cities_name=cities_names_en, column="governorate_name_en", title="What is the governorate name?")
elif game_mode == 2:
    game(cities_name=cities_names_ar, column="governorate_name_ar", title="ما هي إسم المحافظة؟")
else:
    pass
turtle.mainloop()



