import numpy as np
import random
from collections import Counter
import matplotlib.pyplot as plt
from numba import jit, prange


def construct_table(choices):
    weights = np.array([p for p in choices.values()])
    mean = np.mean(weights)
    print("mean = %f" % mean)

    # Should be careful in case one of the weights equals the mean
    # Divide by mean to normalise probability
    shorts = {key: value for key, value in choices.items() if value < mean}
    talls = {key: value for key, value in choices.items() if value > mean}

    # Should not really be using dictionaries if we want the code to be fast...

    table = []

    while len(talls) > 0:
        # Take a tall out
        tall_index = next(iter(talls))
        tall_height = talls[tall_index]
        talls.pop(tall_index)

        # Take a short out (or do nothing if there are none left)
        short_index = -1
        short_height = 0
        if len(shorts) > 0:
            short_index = next(iter(shorts))
            short_height = shorts[short_index]
            shorts.pop(short_index)

        # Add the pair to the table
        table.append((short_index, short_height,
                      tall_index, mean - short_height))

        # Put the remainder into shorts or talls
        if short_index != -1:
            remainder = tall_height + short_height - mean

            # The len(shorts) == 0 check is really important
            # Because of some roundoff error, the final tall could sometimes
            #  get placed inside shorts instead of talls
            if remainder > mean or len(shorts) == 0:
                talls[tall_index] = remainder
            else:
                # Use the tall index, because the tall one is the remainder
                shorts[tall_index] = remainder


    return table


def sample_table(table):
    i = random.randint(0, len(table) - 1)
    tup = table[i]

    choice_A = tup[0]
    choice_B = tup[2]
    choice_A_weight = tup[1]
    choice_B_weight = tup[3]
    if random.random() < choice_A_weight / (choice_A_weight + choice_B_weight):
        return choice_A
    else:
        return choice_B


choices = {
    'Meeting with supervisor': 10,
    'Laundry': 0.5,
    'Mark problem sheets': 5,
    'Solve problem sheet': 8,
    'Research': 1,
}
total_weight = np.sum(np.array([p for p in choices.values()]))
avg_weight = np.mean(np.array([p for p in choices.values()]))

table = construct_table(choices)
print("Table: " + str(table) + "\n")


# Courtesy of GPT4
def plot_table(data):
    # List of colors
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta']

    # Dictionary to map labels to colors
    label_colors = {}

    # Assign colors to labels dynamically
    for tuple in data:
        for label in (tuple[0], tuple[2]):  # Check both labels in the tuple
            if label not in label_colors:
                label_colors[label] = colors[len(label_colors) % len(colors)]

    # Create the stacked bar chart
    for i, (a_label, a_height, b_label, b_height) in enumerate(data, start=1):
        plt.bar(i, a_height/avg_weight, color=label_colors[a_label], label=a_label if a_label not in plt.gca().get_legend_handles_labels()[1] else "")
        plt.bar(i, b_height/avg_weight, bottom=a_height/avg_weight, color=label_colors[b_label], label=b_label if b_label not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.title('Sunday problem')

    # Create legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Removes duplicates
    plt.legend(by_label.values(), by_label.keys())

    # Set the x-axis ticks to match the number of bars
    plt.xticks(range(1, len(data) + 1))

    # Set the y-axis limit to make the total height visible as 1
    plt.ylim(0, 1)

    plt.show()

plot_table(table)

num_samples = 100000
samples = [sample_table(table) for i in range(num_samples)]




counts = Counter(samples)
sorted_counts = {key: value / num_samples for key, value in sorted(counts.items())}

print("\n\n")
for key, value in sorted_counts.items():
    print("%s: %.7f (prob = %.7f)" % (key, value, choices[key]/total_weight))



#  Bar chart
sorted_keys = sorted(counts.keys())
plt.figure(figsize=(10, 6))
plt.bar(sorted_keys, [counts[key]/num_samples for key in sorted_keys],
        color='skyblue', edgecolor='black')
plt.xticks(rotation=45)
plt.ylabel("Frequency")
plt.title("Sunday problem")
plt.tight_layout()
plt.show()
