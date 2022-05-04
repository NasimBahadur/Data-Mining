import sys, tracemalloc, time
import matplotlib.pyplot as plt
from collections import defaultdict
from itertools import combinations
from csv import writer,reader


# Storing all frequent patterns with minimum support
def store_frequent_patterns(algorithm,frequent_itemset):
    # Opened CSV file to append the data of frequent patterns
    with open(frequent_patterns_file, 'a', newline='') as file:
        writer_object = writer(file)
        name = 'Dataset:' + dataSet +', Algorithm:' + algoName + ', Minimum Support Threshold:' + str(minimum_support_threshold)
        writer_object.writerow([name])
        for itemset in frequent_itemset:
            for j in itemset:
                writer_object.writerow(j)
        writer_object.writerow([])


# Printing all frequent patterns with minimum support
def print_pattern(algorithm,frequent_itemset):
    name = 'Dataset:' + dataSet +', Algorithm:' + algoName + ', Minimum Support Threshold:' + str(minimum_support_threshold)
    print(name)
    print("Frequent Itemsets: ")
    for itemset in frequent_itemset:
        for j in itemset:
            print(j)


#######################      Apriori Algorithm     #######################


# Retrieving data from file within given threshold for Apriori algorithm
def get_data_for_apriori():
    itemsets = []
    itemset = set()
    with open(dataSet, 'r') as file:
        lines = [line.strip() for line in file]
        size = len(lines)
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
        if (support >= minimum_support):
            frequent_itemset.add(item)
    return frequent_itemset


def get_union(itemset, length):
    return set([i.union(j) for i in itemset for j in itemset if len(i.union(j)) == length])


def prune_subset_of_unfrequent_itemset(candidate_set, previous_frequent_itemset, length):
    temp_candidate_itemset = candidate_set.copy()
    for item in candidate_set:
        subsets = combinations(item, length)
        for subset in subsets:
            # Removing the set if the subset is not in previous K-frequent
            if (frozenset(subset) not in previous_frequent_itemset):
                temp_candidate_itemset.remove(item)
                break
    return temp_candidate_itemset


def apriori_algorithm():
    # Starting monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()

    c1_item_set, itemsets = get_data_for_apriori()
    global_frequent_itemset = dict()
    # With minimum support count, storing global itemset
    global_itemset_with_minimum_support = defaultdict(int)
    l1_item_set = get_above_min_support(c1_item_set, itemsets, minimum_support_threshold,
                                        global_itemset_with_minimum_support)
    current_l_set = l1_item_set
    k = 2
    while (current_l_set):
        global_frequent_itemset[k - 1] = current_l_set
        candidate_set = get_union(current_l_set, k)
        candidate_set = prune_subset_of_unfrequent_itemset(candidate_set, current_l_set, k - 1)
        current_l_set = get_above_min_support(
            candidate_set, itemsets, minimum_support_threshold, global_itemset_with_minimum_support)
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
        print_pattern('Apriori',frequent_item_set)

    if n == 1:
        store_frequent_patterns('Apriori',frequent_item_set)

    # Opening CSV file to append the data of threshold, runtime, memory usage
    with open(performance_analysis_file, 'a', newline='') as file:
        writer_object = writer(file)
        # End monitoring and calculate memory usage and required time
        current, peak = tracemalloc.get_traced_memory()
        memory_usage = current / 10 ** 6
        # Stop monitoring memory usage and required time
        tracemalloc.stop()
        end = time.time_ns()
        runtime = (end - start) * (10 ** 6)
        if m == 1 and rt == 1:
            writer_object.writerow([minimum_support_threshold, runtime, memory_usage])
        elif rt == 1:
            writer_object.writerow([minimum_support_threshold, "", memory_usage])
        elif m == 1:
            writer_object.writerow([minimum_support_threshold, runtime, ""])


#######################      FP-growth Algorithm     #######################


# Retrieving data from file within given threshold for FP-growth algorithm
def get_data_for_fpgrowth():
    item_sets = []
    item_frequency = []
    with open(dataSet, 'r') as file:
        lines = [line.strip() for line in file]
        size = len(lines)
        for i in range(size):
            row = lines[i].strip().split()
            rowdata = []
            for j in row:
                rowdata.append(j)
            item_sets.append(sorted(rowdata))
            item_frequency.append(1)
    return item_sets, item_frequency


class item_node:
    def __init__(self, item, frequency, parent):
        self.item_name = item
        self.count_frequency = frequency
        self.next_node = None
        self.parent_node = parent
        self.child_node = {}

    def frequency_count(self, frequency):
        self.count_frequency += frequency


def create_tree(item_sets, frequency, minimum_support):
    header_table = defaultdict(int)
    # Crating header table and counting frequency
    for id, items in enumerate(item_sets):
        for item in items:
            header_table[item] += frequency[id]

    # Deleting the items below minimum support
    header_table = dict((item, support) for item, support in header_table.items() if support >= minimum_support)

    if (len(header_table) == 0):
        return None, None
    for item in header_table:
        header_table[item] = [header_table[item], None]

    # Initializing head node with Null
    FP_Tree = item_node('Null', 1, None)
    # For each cleaned and sorted itemSet updating FP-tree
    for id, items in enumerate(item_sets):
        items = [item for item in items if item in header_table]
        items.sort(key=lambda item: header_table[item][0], reverse=True)
        # Updating the tree with given item and traversing from root to leaf
        current_node = FP_Tree
        for item in items:
            current_node = update_fp_tree(item, current_node, header_table, frequency[id])
    return FP_Tree, header_table


def update_header_table(item, target_node, header_table):
    if (header_table[item][1] == None):
        header_table[item][1] = target_node
    else:
        current_node = header_table[item][1]
        while current_node.next_node != None:
            current_node = current_node.next_node
        current_node.next_node = target_node


def update_fp_tree(item, tree_node, header_table, frequency):
    if item in tree_node.child_node:
        # Incrementing the count, if the item already exists
        tree_node.child_node[item].frequency_count(frequency)
    else:
        # Building new branch
        new_item_node = item_node(item, frequency, tree_node)
        tree_node.child_node[item] = new_item_node
        # Linking between the branch and header table
        update_header_table(item, new_item_node, header_table)
    return tree_node.child_node[item]


def ascend_fp_tree(node, prefix_path):
    if node.parent_node != None:
        prefix_path.append(node.item_name)
        ascend_fp_tree(node.parent_node, prefix_path)


def find_prefix_path(base_pattern, header_table):
    tree_node = header_table[base_pattern][1]
    conditional_patterns = []
    frequency = []
    while tree_node != None:
        prefix_path = []
        ascend_fp_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            # Storing the prefix path and it's corresponding count
            conditional_patterns.append(prefix_path[1:])
            frequency.append(tree_node.count_frequency)
        tree_node = tree_node.next_node
    return conditional_patterns, frequency


def mine_fp_tree(header_table, minimum_support, prefix, frequent_items):
    # Creating a list of sorted items with frequency
    sorted_items = [item[0] for item in sorted(list(header_table.items()), key=lambda p: p[1][0])]
    # Starting with the item of the lowest frequency
    for item in sorted_items:
        # By the concatenation of suffix pattern with frequent patterns which is generated from conditional FP-tree achieves frequent pattern growth
        new_frequent_set = prefix.copy()
        new_frequent_set.add(item)
        frequent_items.append(new_frequent_set)
        # Finding all the prefix path and constructed conditional pattern base
        conditional_pattern_base, frequency = find_prefix_path(item, header_table)
        # Constructing conditonal FP-Tree with conditional pattern base
        conditional_tree, new_header_table = create_tree(conditional_pattern_base, frequency, minimum_support)
        if new_header_table != None:
            # Continue mining process recursively on the tree
            mine_fp_tree(new_header_table, minimum_support, new_frequent_set, frequent_items)


def fpgrowth_algorithm():
    # Start monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()

    itemsets, frequency = get_data_for_fpgrowth()
    minimum_support = len(itemsets) * minimum_support_threshold
    fp_tree, header_table = create_tree(itemsets, frequency, minimum_support)
    if(fp_tree == None):
        print('No frequent itemset exist')
    else:
        frequent_items = []
        mine_fp_tree(header_table, minimum_support, set(), frequent_items)

        maxlength = 0
        for itemset in frequent_items:
            if maxlength < len(itemset):
                maxlength = len(itemset)

        frequent_item_set = []
        for item_set in range(1, maxlength + 1):
            items = []
            for item in frequent_items:
                if len(item) == item_set:
                    items.append(sorted(item))
            items.sort()
            frequent_item_set.append(items)
        frequent_item_set.sort()

        if pc==1:
            print_pattern('FP-growth',frequent_item_set)

        if n==1:
            store_frequent_patterns('FP-growth',frequent_item_set)

    # Opening CSV file to append the data of threshold, runtime, memory usage
    with open(performance_analysis_file, 'a', newline='') as file:
        writer_object = writer(file)
        # End monitoring and calculate memory usage and required time
        current, peak = tracemalloc.get_traced_memory()
        memory_usage = current / 10 ** 6
        # Stop monitoring memory usage and required time
        tracemalloc.stop()
        end = time.time_ns()
        runtime = (end - start) * (10 ** 6)
        if m == 1 and rt == 1:
            writer_object.writerow([minimum_support_threshold, runtime, memory_usage])
        elif rt == 1:
            writer_object.writerow([minimum_support_threshold, "", memory_usage])
        elif m == 1:
            writer_object.writerow([minimum_support_threshold, runtime, ""])


# Press the left green triangle button in the gutter to run the script.
if __name__ == '__main__':
    # name = input("Enter your name:")
    arguments = len(sys.argv)       # n: total arguments
    algoName = ""
    dataSet = ""
    performance_analysis_file = ""
    frequent_patterns_file = ""
    minimum_support_threshold = ""
    m = rt = pc = n = 0

    if arguments > 1:
        for i in range(1, arguments):
            param = sys.argv[i]  # name = sys.argv[1];parsing the command line arguments and setting the parameters
            if param == "-a":
                algoName = sys.argv[i + 1]
                if (algoName != "AP") and (algoName != "FP"):
                    print(
                        "You have entered wrong input. Please enter algoname 'AP' for append pattern or 'FP' for flip pattern.")
                    # AlgoName = "AP"
            if param == "-d":
                dataSetet = 'Dataset/'+sys.argv[i + 1]
            if param == "-t":
                minimum_support_threshold = float(sys.argv[i + 1])
            if param == "-o":
                performance_analysis_file = sys.argv[i + 1]
            if param == "-pf":
                frequent_patterns_file = sys.argv[i + 1]
            if param == "-n":
                n = 1
            if param == "-rt":
                rt = 1
            if param == "-m":
                m = 1
            if param == "-pc":
                pc = 1

    # Generate file name if not given in argument
    if algoName == "":
        algoName = "AP"
    if dataSet == "":
        dataSet = 'Dataset/toy.txt'
    if performance_analysis_file == "":
        performance_analysis_file = dataSet[:len(dataSet) - 4] + "_" + algoName + ".csv"
    if frequent_patterns_file == "":
        frequent_patterns_file = dataSet[:len(dataSet) - 4] + "_" + algoName + ".txt"
    if minimum_support_threshold == "":
        minimum_support_threshold = float(0.75)
    if m == 0:
        m = 1
    if rt == 0:
        rt = 1
    if pc == 0:
        pc = 1
    if n == 0:
        n = 1

    # call the functions as given in the command
    if algoName == "FP":
        fpgrowth_algorithm()
    elif algoName == "AP":
        apriori_algorithm()