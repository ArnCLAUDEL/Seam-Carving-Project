class Core:

    def __init__(self):
        self.image = None

    def setImage(self, path):
        print("File requested")
        self.image = Image(path)
