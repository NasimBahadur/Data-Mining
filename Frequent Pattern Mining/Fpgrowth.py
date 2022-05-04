from collections import defaultdict
from csv import writer
import math, sys, tracemalloc, time, os

# Retrieved data from file within given threshold for FP-growth algorithm
def get_data_for_fpgrowth():
    item_sets = []
    item_frequency = []
    with open(dataset, 'r') as file:
        lines = [line.strip() for line in file]
        size = int(math.ceil(len(lines) * threshold))
        for i in range(size):
            row = lines[i].strip().split()
            rowdata = []
            for j in row:
                rowdata.append(j)
            item_sets.append(sorted(rowdata))
            item_frequency.append(1)
    return item_sets, item_frequency


def print_pattern(frequent_itemset):
    print("Frequent Itemsets: ")
    for itemset in frequent_itemset:
        for j in itemset:
            print(j)


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
    # Built header table and counted frequency
    for id, items in enumerate(item_sets):
        for item in items:
            header_table[item] += frequency[id]

    # Deleted the items below minimum support
    header_table = dict((item, support) for item, support in header_table.items() if support >= minimum_support)

    if (len(header_table) == 0):
        return None, None
    for item in header_table:
        header_table[item] = [header_table[item], None]

    # Initialized head node with Null
    FP_Tree = item_node('Null', 1, None)
    # For each cleaned and sorted itemSet update FP-tree
    for id, items in enumerate(item_sets):
        items = [item for item in items if item in header_table]
        items.sort(key=lambda item: header_table[item][0], reverse=True)
        # Updated the tree with given item and traversed from root to leaf
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
        # Incremented the count, if the item already exists
        tree_node.child_node[item].frequency_count(frequency)
    else:
        # Built new branch
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
            # Stored the prefix path and it's corresponding count
            conditional_patterns.append(prefix_path[1:])
            frequency.append(tree_node.count_frequency)
        tree_node = tree_node.next_node
    return conditional_patterns, frequency


def mine_fp_tree(header_table, minimum_support, prefix, frequent_items):
    # Created a list of sorted items with frequency
    sorted_items = [item[0] for item in sorted(list(header_table.items()), key=lambda p: p[1][0])]
    # Started with the item of the lowest frequency
    for item in sorted_items:
        # By the concatenation of suffix pattern with frequent patterns which is generated from conditional FP-tree achieves frequent pattern growth
        new_frequent_set = prefix.copy()
        new_frequent_set.add(item)
        frequent_items.append(new_frequent_set)
        # Found all the prefix path and constructed conditional pattern base
        conditional_pattern_base, frequency = find_prefix_path(item, header_table)
        # Constructed conditonal FP-Tree with conditional pattern base
        conditional_tree, new_header_table = create_tree(conditional_pattern_base, frequency, minimum_support)
        if new_header_table != None:
            # Continue mining process recursively on the tree
            mine_fp_tree(new_header_table, minimum_support, new_frequent_set, frequent_items)


def store_frequent_patterns(frequent_itemset):
    # Opened CSV file to append the data of frequent patterns
    with open(frequent_patterns_file, 'a', newline='') as file:
        writer_object = writer(file)
        writer_object.writerow(['FP-growth Algorithm'])
        for itemset in frequent_itemset:
            for j in itemset:
                writer_object.writerow(j)
        writer_object.writerow([])


def fpgrowth_algorithm():
    itemsets, frequency = get_data_for_fpgrowth()
    minimum_support = len(itemsets) * minimum_support_ratio
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
            print_pattern(frequent_item_set)

        if n==1:
            store_frequent_patterns(frequent_item_set)


if __name__ == "__main__":
    dataset = 'Dataset/toy.txt'
    frequent_patterns_file = 'pattern.txt'
    performance_analysis_file = 'toy_fp.csv'
    minimum_support_ratio = 0.22
    threshold= 1
    m = rt = pc = n= 1

    # Start monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()
    # Opened CSV file to append the data of threshold, runtime, memory usage
    with open(performance_analysis_file, 'a', newline='') as file:
        writer_object = writer(file)

        fpgrowth_algorithm()

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