import random
from collections import Counter
import numpy as np
from multiprocessing import Pool

# Best first guess words
BEST_FIRST_GUESS = 'tares'
BEST_FIRST_GUESS_INF_ENTROPY = 'raise'


def generate_and_save_word_pool(n):
    """
    Generate a word pool of words with length n from the dictionary file and save it.
    """
    # Example of generating a word pool for n=5, can be extended to use external word lists
    word_list = [word.strip() for word in open("dictionary/words_alpha.txt").readlines() if len(word.strip()) == n]
    # save the word pool to a file
    with open("dictionary/word_pool_" + str(n) + ".txt", "w") as f:
        for word in word_list:
            f.write(word + "\n")
        f.close()
    return word_list


def get_feedback(guess_word, target_word):
    """
    Return feedback comparing guess_word against target_word.
    "green" indicates correct letter and position,
    "yellow" indicates correct letter in wrong position,
    and "gray" indicates an incorrect letter.
    """
    feedback = ["gray"] * len(guess_word)
    freq = Counter(target_word)
    for i, letter in enumerate(guess_word):
        if letter == target_word[i]:
            feedback[i] = "green"
            freq[letter] -= 1
    for i, letter in enumerate(guess_word):
        if feedback[i] == "gray" and freq[letter] > 0:
            feedback[i] = "yellow"
            freq[letter] -= 1
    return feedback


def play_wordle(target_word, word_pool, max_attempts=6):
    """
    Play an interactive Wordle game in the console.
    The player has 'max_attempts' to guess the 'target_word'.
    """
    word_length = len(target_word)
    print(f"Welcome to Wordle! The secret word has {word_length} letters. You have {max_attempts} attempts.")

    for attempt in range(1, max_attempts + 1):
        # 1. Get user input
        guess = input(f"\nAttempt {attempt}/{max_attempts} - Enter your guess: ").strip().lower()
        # check if guess is valid
        if guess not in word_pool:
            print("Your guess is not a valid word. Try again.")
            continue

        # 2. Basic validation checks
        if len(guess) != word_length:
            print(f"Your guess must be {word_length} letters long. Try again.")
            continue

        # 3. Generate feedback
        feedback = get_feedback(guess, target_word)

        # 4. Print the feedback
        print("Feedback: ", feedback)

        # 5. Check if the user has guessed the word
        if guess == target_word:
            print("Congratulations! You guessed the word correctly!")
            return

    # If user didn't guess correctly after max_attempts
    print(f"\nSorry, you've run out of attempts. The correct word was '{target_word}'. Better luck next time!")

def update_current_word_pool(current_word_pool, guess, feedback):
    """
    Update and return the word pool filtering out words that would not yield the given feedback.
    """
    new_word_pool = []
    for word in current_word_pool:
        if get_feedback(guess, word) == feedback:
            new_word_pool.append(word)
    return new_word_pool


def get_possible_feedbacks(current_word_pool, guess):
    """
    Return a dictionary mapping each feedback pattern (as a tuple) to its frequency.
    """
    possible_feedbacks = {}
    for word in current_word_pool:
        feedback = tuple(get_feedback(guess, word))
        if feedback not in possible_feedbacks:
            possible_feedbacks[feedback] = 1
        else:
            possible_feedbacks[feedback] += 1
    return possible_feedbacks

def calc_v_N_entropy(possible_feedbacks):
    """
    Calculate the Shannon entropy of the feedback distribution.
    """
    total = sum(possible_feedbacks.values())
    entropy = 0
    for freq in possible_feedbacks.values():
        p = freq / total
        entropy -= p * np.log(p)
    return entropy


def calc_inf_entropy(possible_feedbacks):
    """
    Calculate the inf_entropy metric based on the maximum frequency of a feedback pattern.
    """
    total = sum(possible_feedbacks.values())
    return -max(possible_feedbacks.values()) / total


def get_next_guess(word_pool, current_word_pool):
    """
    Return the next guess from word_pool using the maximum entropy strategy.
    """
    max_entropy = float("-inf")
    best_guess = None
    for i, word in enumerate(word_pool):
        possible_feedbacks = get_possible_feedbacks(current_word_pool, word)
        v_N_entropy = calc_v_N_entropy(possible_feedbacks)
        if v_N_entropy > max_entropy:
            max_entropy = v_N_entropy
            best_guess = word
    return best_guess


def get_next_guess_with_inf_entropy(word_pool, current_word_pool):
    """
    Return the next guess from word_pool using the inf_entropy strategy.
    """
    max_entropy = float("-inf")
    best_guess = None
    for i, word in enumerate(word_pool):
        possible_feedbacks = get_possible_feedbacks(current_word_pool, word)
        inf_entropy = calc_inf_entropy(possible_feedbacks)
        if inf_entropy > max_entropy:
            max_entropy = inf_entropy
            best_guess = word
    return best_guess


def play_wordle_with_optimization(target_word, word_pool, max_attempts=20):
    """
    Simulate an optimized Wordle game using the maximum entropy strategy.
    Returns the number of attempts taken to guess the target word.
    """
    current_word_pool = word_pool.copy()
    #print(f"Welcome to Wordle! The secret word has {len(target_word)} letters. You have {max_attempts} attempts.")
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            guess = BEST_FIRST_GUESS
        else:
            if len(current_word_pool) == 1:
                guess = current_word_pool[0]
            else:
                guess = get_next_guess(word_pool, current_word_pool)
        #print(f"\nAttempt {attempt}/{max_attempts} - Enter your guess: {guess}")
        feedback = get_feedback(guess, target_word)
        #print("Feedback: ", feedback)
        if guess == target_word:
            #print("Congratulations! You guessed the word correctly!")
            return attempt
        current_word_pool = update_current_word_pool(current_word_pool, guess, feedback)
    #print(f"\nSorry, you've run out of attempts. The correct word was '{target_word}'. Better luck next time!")


def play_wordle_with_optimization_inf_entropy(target_word, word_pool, max_attempts=20):
    """
    Simulate an optimized Wordle game using the inf_entropy strategy.
    Returns the number of attempts taken to guess the target word.
    """
    current_word_pool = word_pool.copy()
    #print(f"Welcome to Wordle! The secret word has {len(target_word)} letters. You have {max_attempts} attempts.")
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            guess = BEST_FIRST_GUESS_INF_ENTROPY
        else:
            if len(current_word_pool) == 1:
                guess = current_word_pool[0]
            else:
                guess = get_next_guess_with_inf_entropy(word_pool, current_word_pool)
        #print(f"\nAttempt {attempt}/{max_attempts} - Enter your guess: {guess}")
        feedback = get_feedback(guess, target_word)
        #print("Feedback: ", feedback)
        if guess == target_word:
            #print("Congratulations! You guessed the word correctly!")
            return attempt
        current_word_pool = update_current_word_pool(current_word_pool, guess, feedback)
    #print(f"\nSorry, you've run out of attempts. The correct word was '{target_word}'. Better luck next time!")


def wordle_couch(word_pool, max_attempts=6):
    """
    Play Wordle with manual feedback entry while providing best guess suggestions.
    """
    current_word_pool = word_pool.copy()
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            suggested_guess = BEST_FIRST_GUESS
        else:
            if len(current_word_pool) == 1:
                print("Only one word left in the pool.")
                suggested_guess = current_word_pool[0]
            else:
                suggested_guess = get_next_guess(word_pool, current_word_pool)
        print("Best guess:", suggested_guess)
        guess = input(f"\nAttempt {attempt}/{max_attempts} - Enter your guess: ").strip().lower()
        feedback = input("Enter the feedback (colors separated by space): ").split()
        print("Feedback:", feedback)
        current_word_pool = update_current_word_pool(current_word_pool, guess, feedback)


def worker_function(args):
    """
    Worker function to be executed in parallel.
    Returns a tuple (word, steps_taken) using the maximum entropy strategy.
    """
    word, word_pool = args
    steps_taken = play_wordle_with_optimization(word, word_pool, max_attempts=20)
    return word, steps_taken


def worker_function_inf_entropy(args):
    """
    Worker function to be executed in parallel.
    Returns a tuple (word, steps_taken) using the inf_entropy strategy.
    """
    word, word_pool = args
    steps_taken = play_wordle_with_optimization_inf_entropy(word, word_pool, max_attempts=20)
    return word, steps_taken


if __name__ == "__main__":
    n = 5
    word_pool = generate_and_save_word_pool(n)
    target_word = random.choice(word_pool)

    # Calculate statistics using the inf_entropy strategy
    args_list = [(word, word_pool) for word in word_pool]
    with Pool(16) as p:
        results = p.map(worker_function_inf_entropy, args_list)

    steps = dict(results)
    filename = f"steps_{n}_inf_entropy.txt"
    with open(filename, "w") as f:
        for word, step in steps.items():
            f.write(f"{word} {step}\n")
    print(f"Finished! Results saved to '{filename}'.")