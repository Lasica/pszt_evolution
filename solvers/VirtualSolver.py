import time


class VirtualSolver:  # Solver interface to inherit from
    def __init__(self, input_dict, config=None):
        self.capacity = input_dict['capacity']
        self.items = input_dict['items'] 
        self.result = None  # pary waga, wartosc, indeks
        self.start_time = 0.0
        self.finish_time = 0.0
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

    def check_answer(self, answer):
        """Function to compare with optimal answer, should return """
        dif = answer - sum([p for w, p, i in self.result])
        return dif
