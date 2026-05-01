from PyQt6.QtWidgets import *
from gui import *
import os
import csv

class Logic(QMainWindow, Ui_Project2):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.label_3.setStyleSheet("color: blue;")
        self.scoresub_button.clicked.connect(self.submit)
        self.final_button.clicked.connect(self.pullgrade)
        self.score_frame.hide()
        self.input_attempts.setPlaceholderText("Enter attempts: 1-4")
        self.input_attempts.textChanged.connect(self.newscore)
        self.label_statusmessage.setText("")

        


    def submit(self) -> None:
        """
        Function is connected to the submit button 
        and is used to write student name, scores for all attempts, and average for final to the csv file "grades.csv". 
        """
        file = "grades.csv"
        scores = []
        scoresin = [self.line_score1, self.line_score2, self.line_score3, self.line_score4]

        try:
            name = self.input_name.text().strip().lower()
            if not name:
                raise ValueError
        
        except ValueError:
            self.label_statusmessage.setText("Must enter a name!")
            self.label_statusmessage.setStyleSheet("color: red;")
            return
        
        namecheck = name.strip().split()

        for val in namecheck:
            if not val.isalpha():
                self.label_statusmessage.setText("Name must be letters!")
                self.label_statusmessage.setStyleSheet("color: red;")
                return

            
        
        for item in scoresin:
            if item.isVisible():
                score = item.text().strip()

                if not score:
                    self.label_statusmessage.setText("Must fill in all attempts!")
                    self.label_statusmessage.setStyleSheet("color: red;")
                    return
                
                try:
                    value = float(score)

                    if value < 0 or value > 100:
                        self.label_statusmessage.setText("Scores must be between 0-100!")
                        self.label_statusmessage.setStyleSheet("color: red;")
                        return

                    scores.append(value)

                except ValueError:
                    self.label_statusmessage.setText("Scores must be numbers!")
                    self.label_statusmessage.setStyleSheet("color: red;")
                    return
        try:
            avg = f"{(sum(scores) / len(scores)):.2f}"

        except ZeroDivisionError:
            self.label_statusmessage.setText("Must enter number of attempts!")
            self.label_statusmessage.setStyleSheet("color: red;")
            return

        scores.append(avg)

        if not os.path.exists(file):
            open(file, 'w').close()


        with open(file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name] + scores)

        

        for item in scoresin:
            item.clear()

        self.score_frame.hide()
        self.input_name.clear()
        self.input_attempts.clear()
        self.label_statusmessage.setText("Submitted!")
        self.label_statusmessage.setStyleSheet("color: green;")
        


    def pullgrade(self) -> None:
        """
        Function is connected to the pull final grade button and uses the students name to search the
        "grade.csv" file and pull the final grade for the student name entered.
        """
        file = "grades.csv"

        try:
            name = self.input_name.text().strip().lower()
            if not name:
                raise ValueError
        
        except ValueError:
            self.label_statusmessage.setText("Must enter a name!")
            self.label_statusmessage.setStyleSheet("color: red;")
            return

        with open (file, 'r') as csvfile:
            final = ''
            content = csv.reader(csvfile, delimiter=',')

            for line in content:
                if line[0] == name:
                    final = line[-1]

            if final == '':
                self.label_statusmessage.setText("Student doesn't exist!")
                self.label_statusmessage.setStyleSheet("color: red;")
                return


        self.label_statusmessage.setText(f"Final grade for {name} is {final}%")
        self.label_statusmessage.setStyleSheet("color: green;")
        self.input_name.clear()

    def newscore(self, text) -> None:
        """
        Function is connected to NO of attempts input box "input_attempts" and is used to dynamically display 
        the number of the attempts the student took for the final.
        :param text: Contains the current data entered within the "no of attempts" input box called "input_attempts"
        """
        try:
            num = int(text)
        except ValueError:
            self.label_statusmessage.setText("Must enter a number between 1-4!")
            self.label_statusmessage.setStyleSheet("color: red;")
            self.score_frame.hide()
            return


        if num < 1 or num > 4:
            self.label_statusmessage.setText("Must enter a number between 1-4!")
            self.label_statusmessage.setStyleSheet("color: red;")
            self.score_frame.hide()
            return

        
        self.score_frame.show()

        scoresin = [self.line_score1, self.line_score2, self.line_score3, self.line_score4]
        scorelab = [self.label_score1, self.label_score2, self.label_score3, self.label_score4]

        for i in range(len(scoresin)):
            visible = i < num
            scoresin[i].setVisible(visible)
            scorelab[i].setVisible(visible)




