import time


class VirtualSolver:  # Solver interface to inherit from
    def __init__(self, input_dict, config=None):
        self.capacity = input_dict['capacity']
        self.items = input_dict['items'] 
        self.result = []  # pary waga, wartosc, indeks
        self.start_time = 0.0
        self.finish_time = 0.0
        self.configuration = config  # slownik

    def set_configuration(self, config):
        self.configuration = config

    def solve(self):
        # placeholder, funkcja powinna zwracać wynik (wartosc, upakowanie plecaka);
        # dokladne przedmioty uzyte do upakowania powinny byc w self.result
        return self.result

    def __call__(self):  # funkcja zeby moc wywolac klase jako solver - rozwiazywanie; nie nalezy jej edytowac
        self.start_time = time.process_time()
        result = self.solve()
        self.finish_time = time.process_time()
        return result

    def get_solving_time(self):
        return self.finish_time - self.start_time

    def check_answer(self, answer):
        """Function to compare with optimal answer, should return """
        dif = answer - sum([item[0] for item, i in self.result])
        return dif 
