class DynamicSolver:

    def __init__(self, input_dict): #konstruktor
        self.item_list = input_dict["items"]
        self.volume = input_dict["volume"]

    def nwd (self, a, b):

        while b > 0:
            c = a % b
            a = b
            b = c

        return a

    def solve(self):
        current_nwd = self.item_list[0][1]
        for p, w in self.item_list:
            current_nwd = self.nwd(current_nwd, w)

        backpack = [-1] * (self.volume/current_nwd+1)
        backpack[0] = 0
        for p, w in self.item_list:
            pass# ... algorytm plecakowy uzupelniania plecaka
        return backpack[self.volume]







        #return