import random
from collections import Counter
import numpy as np

best_first_guesses = 'tares'
best_first_guesses_inf_entropy = 'raise'

def generate_and_save_word_pool(n):
    # Example of generating a word pool for n=5, can be extended to use external word lists
    word_list = [word.strip() for word in open("dictionary/words_alpha.txt").readlines() if len(word.strip()) == n]
    # save the word pool to a file
    with open("dictionary/word_pool_" + str(n) + ".txt", "w") as f:
        for word in word_list:
            f.write(word + "\n")
        f.close()
    return word_list

def get_feedback(guess_word, target_word):
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
    Plays a Wordle-like game interactively in the console.
    User has 'max_attempts' guesses to figure out the 'target_word'.
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
    new_word_pool = []
    for word in current_word_pool:
        if get_feedback(guess, word) == feedback:
            new_word_pool.append(word)
    return new_word_pool

def get_possible_feedbacks(current_word_pool, guess):
    possible_feedbacks = {}
    for word in current_word_pool:
        feedback = tuple(get_feedback(guess, word))
        if feedback not in possible_feedbacks:
            possible_feedbacks[feedback] = 1
        else:
            possible_feedbacks[feedback] += 1
    return possible_feedbacks

def calc_v_N_entropy(possible_feedbacks):
    v_N_entropy = 0
    N = sum(possible_feedbacks.values())
    for freq in possible_feedbacks.values():
        p = freq / N
        v_N_entropy -= p * np.log(p)
    return v_N_entropy

def calc_inf_entropy(possible_feedbacks):
    return - max(possible_feedbacks.values()) / sum(possible_feedbacks.values())

def get_next_guess(word_pool, current_word_pool):
    max_entropy = float("-inf")
    best_guess = None
    for i, word in enumerate(word_pool):
        #print(f"Checking word {i+1}/{len(word_pool)}")
        possible_feedbacks = get_possible_feedbacks(current_word_pool, word)
        v_N_entropy = calc_v_N_entropy(possible_feedbacks)
        # if v_N_entropy > max_entropy - 0.1:
        #     print(f"Word: {word}, Entropy: {v_N_entropy}")
        if v_N_entropy > max_entropy:
            max_entropy = v_N_entropy
            best_guess = word
            #print(f"Word: {word}, Entropy: {v_N_entropy}")
    return best_guess

def get_next_guess_with_inf_entropy(word_pool, current_word_pool):
    max_entropy = float("-inf")
    best_guess = None
    for i, word in enumerate(word_pool):
        #print(f"Checking word {i+1}/{len(word_pool)}")
        possible_feedbacks = get_possible_feedbacks(current_word_pool, word)
        inf_entropy = calc_inf_entropy(possible_feedbacks)
        # if v_N_entropy > max_entropy - 0.1:
        #     print(f"Word: {word}, Entropy: {v_N_entropy}")
        if inf_entropy > max_entropy:
            max_entropy = inf_entropy
            best_guess = word
            #print(f"Word: {word}, Entropy: {inf_entropy}")
    return best_guess

def play_wordle_with_optimization(target_word, word_pool, max_attempts=20):
    current_word_pool = word_pool.copy()
    #print(f"Welcome to Wordle! The secret word has {len(target_word)} letters. You have {max_attempts} attempts.")
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            guess = best_first_guesses
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
    current_word_pool = word_pool.copy()
    #print(f"Welcome to Wordle! The secret word has {len(target_word)} letters. You have {max_attempts} attempts.")
    for attempt in range(1, max_attempts + 1):
        if attempt == 1:
            guess = best_first_guesses_inf_entropy
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
    '''
    This function helps you play Wordle with your friends. You need to update the feedback manually. Return the best guess.
    '''
    current_word_pool = word_pool.copy()
    for attemp in range(1, max_attempts+1):
        if attemp == 1:
            guess = best_first_guesses
        else:
            if len(current_word_pool) == 1:
                print("Only one word left in the pool.")
                guess = current_word_pool[0]
            else:
                guess = get_next_guess(word_pool, current_word_pool)
        print("best guess: ", guess)
        guess = input(f"\nAttempt {attemp}/{max_attempts} - Enter your guess: ")
        # print(f"\nAttempt {attemp}/{max_attempts} - Enter your guess: {guess}")
        feedback = input("Enter the feedback: ")
        # convert feedback into a list of colors
        feedback = feedback.split(' ')
        print("Feedback: ", feedback)
        current_word_pool = update_current_word_pool(current_word_pool, guess, feedback)



from multiprocessing import Pool


def worker_function(args):
    """
    This function will be executed in parallel for each word.
    It returns (word, steps_taken).
    """
    # 'play_wordle_with_optimization' is assumed to be defined elsewhere in your code
    word, word_pool = args
    step_count = play_wordle_with_optimization(word, word_pool, max_attempts=20)
    return word, step_count

def worker_function_inf_entropy(args):
    """
    This function will be executed in parallel for each word.
    It returns (word, steps_taken).
    """
    # 'play_wordle_with_optimization' is assumed to be defined elsewhere in your code
    word, word_pool = args
    step_count = play_wordle_with_optimization_inf_entropy(word, word_pool, max_attempts=20)
    return word, step_count


if __name__ == "__main__":
    n = 5
    # 1. Generate the word pool (already implemented in your code)
    word_pool = generate_and_save_word_pool(n)

    # 2. Select a random target word (optional for debugging)
    target_word = random.choice(word_pool)
    # print(target_word)  # For debugging

    # (Optional) Play or test other functions here:
    # play_wordle_with_optimization(target_word, word_pool, max_attempts=20)
    # wordle_couch(word_pool, max_attempts=6)

    # # 3. Calculate the statistics of steps needed to guess each word in parallel

    # word_pool = word_pool[:]  # For testing purposes, you can reduce the number of words
    # args_list = [(word, word_pool) for word in word_pool]
    # with Pool(16) as p:
    #     # 'p.map' applies 'worker_function' to each element of 'word_pool' in parallel
    #     results = p.map(worker_function, args_list)

    # # 4. Convert results (a list of (word, steps)) into a dictionary
    # steps = dict(results)

    # # 5. Print progress
    # for i, (word, step) in enumerate(results):
    #     print(f"word: {word}, steps: {step}, {i+1}/{len(word_pool)}")

    # # 6. Save steps to a file
    # filename = f"steps_{n}.txt"
    # with open(filename, "w") as f:
    #     for word, step in steps.items():
    #         f.write(f"{word} {step}\n")

    # print(f"\nFinished! Results saved to '{filename}'.")

    # play_wordle_with_optimization_inf_entropy(target_word, word_pool, max_attempts=20)

    # 3. Calculate the statistics of steps needed to guess each word in parallel

    word_pool = word_pool[:1000]  # For testing purposes, you can reduce the number of words
    args_list = [(word, word_pool) for word in word_pool]
    with Pool(16) as p:
        # 'p.map' applies 'worker_function' to each element of 'word_pool' in parallel
        results = p.map(worker_function_inf_entropy, args_list)
        
    # 4. Convert results (a list of (word, steps)) into a dictionary
    steps = dict(results)
    
    # save steps to a file
    with open("steps_" + str(n) + "_inf_entropy.txt", "w") as f:
        for word, step in steps.items():
            f.write(word + " " + str(step) + "\n")
        f.close()
    print("Finished! Results saved to 'steps_" + str(n) + "_inf_entropy.txt'.")






# if __name__ == "__main__":
#     n = 5
#     word_pool = generate_and_save_word_pool(n)

#     # Select a random word from the word pool
#     target_word = random.choice(word_pool)
#     # print(target_word)  # For debugging purposes

#     # # Play the Wordle game optimally
#     # play_wordle_with_optimization(target_word, word_pool, max_attempts=20)

#     # # help you play Wordle with your friends
#     # wordle_couch(word_pool, max_attempts=6)

#     # Calculate the statistics of steps needed to guess the word correctly for all possible words in the word pool
#     steps = {}
#     for i, word in enumerate(word_pool):
#         steps[word] = play_wordle_with_optimization(word, word_pool, max_attempts=20)
#         print("word: ", word, "steps: ", steps[word],i+1, "/", len(word_pool))
#     # save steps to a file
#     with open("steps_" + str(n) + ".txt", "w") as f:
#         for word, step in steps.items():
#             f.write(word + " " + str(step) + "\n")
#         f.close()


