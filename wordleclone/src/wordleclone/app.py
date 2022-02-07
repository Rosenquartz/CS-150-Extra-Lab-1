import toga
import random
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER, RIGHT

class GuessRow():
    def __init__(self):
        self.box = toga.Box(
            style=Pack(direction=ROW,alignment='center',flex=1, padding=(2,0))
        )
        self.buttons = [0]*5
        for i in range(5):
            self.buttons[i] = toga.Button(
                '', 
                style=Pack(width=50,height=50,color="white",padding=(0,2),font_size=15)
            )
            self.box.add(self.buttons[i])
    def update(self, answerString, inputString):
        wrong = [0,1,2,3,4]
        right = []
        for i in range(5):
            if answerString[i] == inputString[i]:
                wrong.remove(i)
                right.append(i)
            self.buttons[i].label = inputString[i]
        for i in range(5):
            if i in right:
                self.buttons[i].style.background_color = "#48a03a"
            elif inputString[i] in [answerString[j] for j in wrong]:
                wrong.remove(answerString.index(inputString[i]))
                self.buttons[i].style.background_color = "#b1892d"
            else:
                self.buttons[i].style.background_color = "#808080"
    def reset(self):
        for i in range(5):
            self.buttons[i].label = ''
            self.buttons[i].style.background_color = "white"

class Alphabet():
    def __init__(self):
        self.box = toga.Box(
                style=Pack(direction=ROW, alignment=CENTER, padding=(5,0))
            )
        self.letters=[0]*26
        for i in range(26):
            self.letters[i] = toga.Label(
                    chr(65+i),
                    style=Pack(text_align=CENTER,color="white",font_size=8)
                )
            self.box.add(self.letters[i])
    def blankout(self, inputString):
        for i in inputString:
            self.letters[ord(i)-65].style.font_size=5
            self.letters[ord(i)-65].style.color='orange'
    def reset(self):
        for i in range(26):
            self.letters[i].enabled = True
            self.letters[i].style.font_size=8
            self.letters[i].style.color='white'

class WordleClone(toga.App):
    def startup(self):
        answertxt = open(str(self.paths.app) + "\\resources\\answers.txt")
        self.answers = []
        for x in answertxt:
            self.answers.append(x.strip('\n').upper())
        
        guessestxt = open(str(self.paths.app) + "\\resources\\guesses.txt")
        self.guessWords = []
        for x in guessestxt:
            self.guessWords.append(x.strip('\n').upper()) 

        self.answer = self.answers[random.randrange(len(self.answers))]
        #print(self.answer)
        self.currentRow = 0

        main_box = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER, background_color="#262626"))

        input_label = toga.Label(
            'Guess: ',
            style=Pack(padding=(5, 5),color="white")
        )
        self.guess_input = toga.TextInput(style=Pack(flex=1, padding=(5,0)))
        input_box = toga.Box(style=Pack(direction=ROW))
        input_box.add(input_label)
        input_box.add(self.guess_input)

        guessButton = toga.Button(
            'GUESS!',
            style=Pack(padding=(5,0),background_color='#5e5e5e',color="white"),
            on_press=self.guess
        )

        self.alphabet = Alphabet()

        main_box.add(input_box)
        main_box.add(guessButton)
        main_box.add(self.alphabet.box)

        guessesBox = toga.Box(
            style=Pack(direction=COLUMN, alignment=CENTER)
        )
        self.rows=[0]*6
        for i in range(6):
            self.rows[i]=GuessRow()
            guessesBox.add(self.rows[i].box)
        main_box.add(guessesBox)
        restartButton = toga.Button(
            'RESTART!',
            style=Pack(padding=(5,0),background_color='#5e5e5e',color="white"),
            on_press=self.reset
        )
        main_box.add(restartButton)

        self.main_window = toga.MainWindow(title=self.formal_name, size=(400,465))
        self.main_window.content = main_box
        self.main_window.show()

    def guess(self, widget):
        inputGuess = self.guess_input.value.upper()
        self.guess_input.value = ''
        if len(inputGuess) != 5:
            self.main_window.info_dialog('Invalid input!', 'Guess should have exactly five letters.')
        elif inputGuess not in self.guessWords:
            self.main_window.info_dialog('GAME OVER', 'Guess is not a valid word.')
        else:
            self.rows[self.currentRow].update(self.answer, inputGuess)
            self.alphabet.blankout(inputGuess)
            self.currentRow += 1
        if inputGuess==self.answer:
            if self.currentRow == 0: dialogue="A GENIUS!"
            elif self.currentRow <= 3: dialogue="IMPRESSIVE!"
            elif self.currentRow <=5: dialogue="GREAT!"
            else: dialogue="okay"
            self.main_window.info_dialog('You won!', f"You're {dialogue}")
            self.resettwo()
        elif self.currentRow == 6:
            self.main_window.info_dialog('GAME OVER', f'Game over! Correct answer was {self.answer}!')
            self.resettwo()

    def reset(self, widget):
        for i in range(6):
            self.rows[i].reset()
        self.alphabet.reset()
        self.answer = self.answers[random.randrange(len(self.answers))]
        self.currentRow = 0

    def resettwo(self):
        for i in range(6):
            self.rows[i].reset()
        self.alphabet.reset()
        self.answer = self.answers[random.randrange(len(self.answers))]
        self.currentRow = 0


def main():
    return WordleClone()