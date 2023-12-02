import heapq
def custom_comparator(a, b):
    # Define your custom comparison logic here
    # For example, sorting in descending order:
    return a > b
#xx
def merge(dataSet, l, m, r, comparator):
    n1 = m - l + 1
    n2 = r - m

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = dataSet[l + i]

    for j in range(n2):
        R[j] = dataSet[m + 1 + j]

    i = j = 0
    k = l

    while i < n1 and j < n2:
        if comparator(L[i], R[j]):
            dataSet[k] = L[i]
            i += 1
        else:
            dataSet[k] = R[j]
            j += 1
        k += 1

    while i < n1:
        dataSet[k] = L[i]
        i += 1
        k += 1

    while j < n2:
        dataSet[k] = R[j]
        j += 1
        k += 1

def mergeSort(dataSet, l, r, comparator):
    if l < r:
        m = l + (r - l) // 2
        mergeSort(dataSet, l, m, comparator)
        mergeSort(dataSet, m + 1, r, comparator)
        merge(dataSet, l, m, r, comparator)


def heapSort(dataSet, comparator):
    if comparator == custom_comparator:
        # For descending order sorting, invert the values
        dataSet = [-x for x in dataSet]

    heapq.heapify(dataSet)

    sortedData = []
    while dataSet:
        if comparator == custom_comparator:
            sortedData.append(-heapq.heappop(dataSet))
        else:
            sortedData.append(heapq.heappop(dataSet))

    return sortedData
