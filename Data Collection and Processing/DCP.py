'''
Group Members:
1) Nasim Bahadur (Id: 2018-1-60-073)
2) Md Shakirul Islam (Id: 2018-1-60-064)
'''
import math, sys, tracemalloc, time
from csv import writer

def AppendPattern(DataSet, Thold, OutputFileName, m, rt):
    print("Here goes the append pattern algorithm", "with ", DataSet, "and", Thold)

    # Start monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()

    # Read data from file
    with open(DataSet, 'r') as file:
        lines = [line.strip() for line in file]

    # Write appended data into file
    with open(OutputFileName, 'a', newline='') as file:
        writer_object = writer(file)
        size = int(math.ceil(len(lines) * Thold))
        for i in range(size):
            rowdata = lines[i].strip()
            rows = []
            row = ''
            length = len(rowdata)
            flag = None
            for j in range(length):
                if (rowdata[j] == " " and (j > 0 and j < length - 1)):
                    if rowdata[j + 1] == " ":
                        continue
                    elif (flag == 1 and (rowdata[j + 1] >= '0' and rowdata[j + 1] <= '9')):
                        continue
                    elif (flag == 0 and (rowdata[j + 1] < '0' and rowdata[j + 1] > '9')):
                        continue
                    elif (flag == 0 and (rowdata[j + 1] >= '0' and rowdata[j + 1] <= '9')):
                        row += rowdata[j]
                    elif (flag == 1 and (rowdata[j + 1] < '0' and rowdata[j + 1] > '9')):
                        row += rowdata[j]
                else:
                    if (rowdata[j] >= '0' and rowdata[j] <= '9'):
                        flag = 1
                        row += rowdata[j]
                    else:
                        flag = 0
                        row += rowdata[j]
                # print(row)
            rows.append(row)
            print(rows)
            # Store/write appended pattern data into file
            # writer_object.writerow(rows)

        # End monitoring and calculate memory usage and required time
        current, peak = tracemalloc.get_traced_memory()
        MemoryUsage = current / 10 ** 6
        # print(f"Current memory usage is {MemoryUsage} MB and Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()
        end = time.time_ns()
        Runtime = (end - start) * (10 ** 6)
        # print(f"Runtime of {AlgoName} Algorithm: {Runtime} ms")
        #writer_object.writerow(['Partition(Thold)', 'Time Required(ms)', 'Memory Usage(MB)'])
        if m == 1 and rt == 1:
            writer_object.writerow([Thold, Runtime, MemoryUsage])
        elif rt == 1:
            writer_object.writerow([Thold, "", MemoryUsage])
        elif m == 1:
            writer_object.writerow([Thold, Runtime, ""])


def FlipPattern(DataSet, Thold, OutputFileName, m, rt):
    print("Here goes the flip pattern algorithm", "with ", DataSet, "and", Thold)

    # Start monitoring memory usage and required time
    tracemalloc.start()
    start = time.time_ns()

    # Read data from file
    with open(DataSet, 'r') as file:
        lines = [line.strip() for line in file]

    # Write flipped data into file
    with open(OutputFileName, 'a', newline='') as file:
        writer_object = writer(file)
        size = int(math.ceil(len(lines) * Thold))
        for i in range(size):
            rowdata = lines[i].strip().split()
            rows = []
            for j in range(len(rowdata)):
                reverse = str(rowdata[j])
                length = len(reverse)
                row = reverse[length::-1]
                # print(row)
                rows.append(row)
            print(rows)
            # Store/write flipped pattern data into file
            # writer_object.writerow(rows)

        # End monitoring and calculate memory usage and required time
        current, peak = tracemalloc.get_traced_memory()
        MemoryUsage = current / 10 ** 6
        # print(f"Current memory usage is {MemoryUsage} MB and Peak memory usage was {peak / 10 ** 6} MB")
        tracemalloc.stop()
        end = time.time_ns()
        Runtime = (end - start) * (10 ** 6)
        # print(f"Runtime of {AlgoName} Algorithm: {Runtime} ms")
        # writer_object.writerow(['Partition(Thold)', 'Time Required(ms)', 'Memory Usage(MB)'])
        if m==1 and rt==1:
            writer_object.writerow([Thold, Runtime, MemoryUsage])
        elif rt==1:
            writer_object.writerow([Thold, "", MemoryUsage])
        elif m==1:
            writer_object.writerow([Thold, Runtime, ""])


# Press the left green triangle button in the gutter to run the script.
if __name__ == '__main__':
    # name = input("Enter your name:")
    n = len(sys.argv) # n: total arguments
    AlgoName = "AP"
    DataSet = "toy.txt"
    Thold = 0.5
    Runtime = MemoryUsage = 0.0
    m = rt = 0
    OutputFileName = ""

    try:
        if n > 1:
            for i in range(1, n):
                param = sys.argv[i]  # name = sys.argv[1];parsing the command line arguments and setting the parameters
                if param == "-a":
                    AlgoName = sys.argv[i + 1]
                    if (AlgoName != "AP") and (AlgoName != "FP"):
                        print("You have entered wrong input. Please enter algoname 'AP' for append pattern or 'FP' for flip pattern.")
                        # AlgoName = "AP"
                if param == "-d":
                    DataSet = sys.argv[i + 1]
                if param == "-p":
                    Thold = float(sys.argv[i + 1])
                if param == "-o":
                    OutputFileName = sys.argv[i + 1]
                if param == "-m":
                    m = 1
                if param == "-rt":
                    rt = 1

        # Generate file name if not given in argument
        if OutputFileName == "":
            OutputFileName = DataSet[:len(DataSet) - 4] + "_" + AlgoName + "_" + str(Thold) + ".csv"

        # call the functions as given in the command
        if AlgoName == "AP":
            AppendPattern(DataSet, Thold, OutputFileName, m, rt)
        elif AlgoName == "FP":
            FlipPattern(DataSet, Thold, OutputFileName, m, rt)

    except:
        print("Something went wrong, try again.")
