from logic import *

def main() -> None:
    """
    Function launches GUI
    """
    application = QApplication([])
    window = Logic()
    window.show()
    application.exec()


if __name__ == '__main__':
    main()