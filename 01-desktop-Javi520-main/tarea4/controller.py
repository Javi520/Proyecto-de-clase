from listener import Listener

class Controller(Listener):

    def __init(self):
        pass

    def set_model(self, model):
        self.model = model

    def main(self):
        self.view.show_all()
        self.view.main()
