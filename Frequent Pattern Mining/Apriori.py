from csv import writer
from collections import defaultdict
from itertools import combinations
import math, tracemalloc, time

# Retrieved data from file within given threshold for Apriori algorithm
def get_data_for_apriori():
    itemsets = []
    itemset = set()
    with open(dataset, 'r') as file:
        lines = [line.strip() for line in file]
        size = int(math.ceil(len(lines) * threshold))
        for i in range(size):
            record = lines[i].strip().split()
            for item in record:
                itemset.add(frozenset([item]))
            itemsets.append(set(record))
    return itemset, itemsets

def get_above_min_support(itemset, itemset_list, minimum_support, global_itemset_with_minimum_support):
    frequent_itemset = set()
    local_itemset_with_minimum_support = defaultdict(int)
    for item in itemset:
        for itemset in itemset_list:
            if item.issubset(itemset):
                global_itemset_with_minimum_support[item] += 1
                local_itemset_with_minimum_support[item] += 1
    for item, support_count in local_itemset_with_minimum_support.items():
        support = float(support_count / len(itemset_list))
        if(support >= minimum_support):
            frequent_itemset.add(item)
    return frequent_itemset

def get_union(itemset, length):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == length])

def prune_subset_of_unfrequent_itemset(candidate_set, previous_frequent_itemset, length):
    temp_candidate_itemset = candidate_set.copy()
    for item in candidate_set:
        subsets = combinations(item, length)
        for subset in subsets:
            # Removed the set if the subset is not in previous K-frequent
            if(frozenset(subset) not in previous_frequent_itemset):
                temp_candidate_itemset.remove(item)
                break
    return temp_candidate_itemset

def store_frequent_patterns(frequent_itemset):
    # Opened CSV file to append the data of frequent patterns
    with open(frequent_patterns_file, 'a', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(['Apriori Algorithm'])
        for itemset in frequent_itemset:
            for j in itemset:
                writer_object.writerow(j)
        writer_object.writerow([])


def print_pattern(frequent_itemset):
    print("Frequent Itemsets: ")
    for itemset in frequent_itemset:
        for j in itemset:
            print(j)


def apriori_algorithm():
    c1_item_set, itemsets = get_data_for_apriori()
    global_frequent_itemset = dict()
    # With minimum support count, storing global itemset
    global_itemset_with_minimum_support = defaultdict(int)
    l1_item_set = get_above_min_support(c1_item_set, itemsets, minimum_support_ratio, global_itemset_with_minimum_support)
    current_l_set = l1_item_set
    k = 2
    while(current_l_set):
        global_frequent_itemset[k-1] = current_l_set
        candidate_set = get_union(current_l_set, k)
        candidate_set = prune_subset_of_unfrequent_itemset(candidate_set, current_l_set, k - 1)
        current_l_set = get_above_min_support(
            candidate_set, itemsets, minimum_support_ratio, global_itemset_with_minimum_support)
        k += 1

    frequent_item_set = []
    for i in global_frequent_itemset:
        itemsets = []
        for itemset in global_frequent_itemset[i]:
            itemset = list(itemset)
            items = []
            for item in itemset:
                items.append(item)
            items.sort()
            itemsets.append(items)
        itemsets.sort()
        frequent_item_set.append(itemsets)
    frequent_item_set.sort()

    if pc == 1:
        print_pattern(frequent_item_set)

    if n == 1:
        store_frequent_patterns(frequent_item_set)


if __name__ == "__main__":
    dataset = 'Dataset/toy.txt'
    frequent_patterns_file = 'pattern.txt'
    performance_analysis_file = 'toy_ap.csv'
    minimum_support_ratio = 0.22
    threshold = 1
    m = rt = pc = n= 1

    # Start monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()
    # Opened CSV file to append the data of threshold, runtime, memory usage
    with open(performance_analysis_file, 'a', newline='') as file:
        writer_object = writer(file)

        apriori_algorithm()

        # End monitoring and calculate memory usage and required time
        current, peak = tracemalloc.get_traced_memory()
        memory_usage = current / 10 ** 6
        # Stop monitoring memory usage and required time
        tracemalloc.stop()
        end = time.time_ns()
        runtime = (end - start) * (10 ** 6)

        if m == 1 and rt == 1:
            writer_object.writerow([threshold, runtime, memory_usage])
        elif rt == 1:
            writer_object.writerow([threshold, "", memory_usage])
        elif m == 1:
            writer_object.writerow([threshold, runtime, ""])