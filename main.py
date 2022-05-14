import time


def get_wordle_result(guess, answer):
    result = ""
    answer_list = []
    for a in answer:
        answer_list.append(a)
    for i in range(0,5):
        for j in range(0,5):
            if guess[i] == answer_list[j]:
                if i == j:
                    result += "g"
                else:
                    result += "y"
                answer_list[j] = "?"
                break
        else:
            result += "b"
    return result


class ScoreKernel:
    def __init__(self, green_yellow_black):
        self.green = green_yellow_black[0]
        self.yellow = green_yellow_black[1]
        self.black = green_yellow_black[2]
        self.score = 0

    def evaluate(self, word):
        score = 0
        for i in range(0,5):
            if word[i] == "g":
                score += self.green[i]
            if word[i] == "y":
                score += self.yellow[i]
            if word[i] == "b":
                score += self.black[i]
        self.score = score
        return score

class GuessScore:
    def __init__(self, kernel, name):
        self.kernel = kernel
        self.name = name
        self.score = 0

    def check_guess(self, guess):
        result = get_wordle_result(guess, self.name)
        self.kernel.evaluate(result)
        self.score += self.kernel.score

    def check_dict(self, d):
        for key, value in d.items():
            self.check_guess(key)

        #print(self.name, self.score)

class WordleSolver:
    def __init__(self, kernel):
        self.answers = {}
        self.valid_words = {}
        answers_file = open("wordle_answers.txt", "r")
        valid_words_file = open("allowed_words.txt", "r")

        for line in answers_file.readlines():
            self.answers[line.strip()] = GuessScore(ScoreKernel(kernel), line.strip())
        answers_file.close()
        for line in valid_words_file.readlines():
            self.valid_words[line.strip()] = line.strip()
        valid_words_file.close()

        start = time.time()
        index = 0
        for key, value in self.answers.items():
            self.answers[key].check_dict(self.answers)
            index += 1
            # if index > 25:
            #     break

        self.sorted_results = dict(sorted(self.answers.items(), key=lambda item: item[1].score))
        for key, value in self.sorted_results.items():
            print(key, value.score)
        end = time.time()
        print("Took: ", end-start)

if __name__ == '__main__':
    value_first_and_last = ([16, 4, 2, 4, 8], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]) #Emphasize green first letters
    green_yellow_equally = ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [0, 0, 0, 0, 0]) #maximize greens and yellows, equally
    maximize_blacks = ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 1]) #hard mode

    kernel = value_first_and_last
    wordle_solver = WordleSolver(kernel)
