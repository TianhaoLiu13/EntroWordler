import numpy as np
import matplotlib.pyplot as plt

# read steps_5.txt, every line is a word + ' ' + its steps required. Read it as a dictionary

def read_steps(file_name):
    steps_dict = {}
    with open(file_name, 'r') as f:
        for line in f:
            word, steps = line.split()
            # print(word)
            steps_dict[word] = int(steps)
    return steps_dict

# get the statistics of the steps required for the words in steps_5.txt

def get_statistics(steps_dict):
    steps_array = np.array(list(steps_dict.values()))
    print('Mean:', np.mean(steps_array))
    print('Median:', np.median(steps_array))
    print('Standard deviation:', np.std(steps_array))
    print('Max:', np.max(steps_array))
    print('Min:', np.min(steps_array))
    print('25th percentile:', np.percentile(steps_array, 25))
    print('75th percentile:', np.percentile(steps_array, 75))

# visualize the distribution of the steps required for the words in steps_5.txt

def visualize_distribution(steps_dict):
    steps_array = np.array(list(steps_dict.values()))
    # Count occurrences of each unique step
    unique_steps, counts = np.unique(steps_array, return_counts=True)

    # Compute probability for each step value
    probabilities = counts / counts.sum()

    # Plot the probability mass function (PMF)
    plt.bar(unique_steps, probabilities, width=0.6, align='center')
    plt.xlabel("Steps")
    plt.ylabel("Probability")
    plt.title("Probability Distribution of Steps")
    plt.xticks(unique_steps)  # Ensure all steps are displayed

    # label each bar with its count
    for i, count in enumerate(counts):
        plt.text(unique_steps[i], probabilities[i], count, ha='center', va='bottom')
    plt.show()
if __name__ == '__main__':
    steps = read_steps('steps_5.txt')
    get_statistics(steps)
    visualize_distribution(steps)

    # print out all words with 7 steps required
    for word, steps in steps.items():
        if steps == 7:
            print(word)