import timeit

def wrapper(func, *args, **kwargs):

    def wrapped():
        return func(*args, **kwargs)

    return wrapped

def is_compare(comparison_count):
    total_count = 0
    for _ in range(comparison_count):
        if 1 is -1:
            # should never get here
            total_count = 0
        else:
            total_count += 1
    assert total_count == comparison_count, "Error: *is* test did not run correctly."

def eq_compare(comparison_count):
    total_count = 0
    for _ in range(comparison_count):
        if 1 == -1:
            # should never get here
            total_count = 0
        else:
            total_count += 1
    assert total_count == comparison_count, "Error: *==* test did not run correctly."


class TestIsVsEq(object):
    is_wins = 0
    is_diff = []  # track difference between comparison times
    eq_wins = 0
    eq_diff = []  # track difference between comparison times

    def __init__(self, is_function, eq_function, **kwargs):
        self.is_function = is_function
        self.eq_function = eq_function
        self.times = kwargs.get("times", 100)
        self.verbose = kwargs.get("verbose", False)

    @staticmethod
    def verify_python_standards():
        assert -1 is -1, "This test won't work because this version of Python doesn't follow the unwritten rules."

    def show_stats(self):
        assert self.is_wins + self.eq_wins != 0, "No tests run!"

        is_won_competition = self.is_wins > self.eq_wins
        if is_won_competition:
            average = sum(self.is_diff) / len(self.is_diff)
        else:
            average = sum(self.eq_diff) / len(self.eq_diff)

        print("Out of {} tests, *{}* won {} times!".format(self.is_wins + self.eq_wins,
                                                           'is' if is_won_competition else 'eq',
                                                           max(self.is_wins, self.eq_wins)))
        print("\t*{}* won {} times.".format('eq' if is_won_competition else 'is',
                                          min(self.is_wins, self.eq_wins)))

        print("Average difference in time was {} seconds.".format(average))

    def run_test(self):
        print("Testing *is* comparisons {} times.".format(self.times))
        is_time = timeit.timeit(self.is_function, number=self.times)
        print("Testing *==* comparisons {} times.".format(self.times))
        eq_time = timeit.timeit(self.eq_function, number=self.times)

        is_won_round = is_time < eq_time

        if is_won_round:
            self.is_wins += 1
            self.is_diff.append(eq_time - is_time)
        else:
            self.eq_wins += 1
            self.eq_diff.append(is_time - eq_time)

        print("*{}* is the faster operator!".format('is' if is_won_round else '=='))
        print("\tis_time: {}".format(is_time))
        print("\teq_time: {}".format(eq_time))

if __name__ == '__main__':
    number_of_comparisons = 2 ** 20

    test = TestIsVsEq(is_function = wrapper(is_compare, number_of_comparisons),
                      eq_function = wrapper(eq_compare, number_of_comparisons),
                      verbose=True)

    test.verify_python_standards()

    while True:
        try:
            test.run_test()
            if test.verbose:
                test.show_stats()

        except KeyboardInterrupt:
            print("")
            test.show_stats()
            exit(0)