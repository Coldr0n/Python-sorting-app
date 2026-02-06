__all__ = [
    "bubbleSort",
    "cocktailSort",
    "selectionSort",
    "insertionSort",
    "shellSort",
    "quickSort",
    "mergeSort",
    "heapSort",
    "cycleSort",
    "countingSort",
    "radixSort",
    "timSort",
    "combSort",
    "gnomeSort",
    "pigeonholeSort",
]
"""
All the algorithms are form online, they are a bit modified to be generators
"""


def verif(arr):
    indices = []
    for i in range(len(arr)):
        indices.append(i)
        yield arr, indices


def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, (j, j + 1)
                swapped = True

        if not swapped:
            break

    yield from verif(arr)


def selectionSort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
                yield arr, (i, min_idx)

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, (i, min_idx)

    yield from verif(arr)


def insertionSort(arr):
    n = len(arr)
    for i in range(1, n):
        value = arr[i]
        j = i - 1
        while j >= 0 and value < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, (j + 1, j)
        arr[j + 1] = value
        yield arr, (j + 1, i)

    yield from verif(arr)


def shellSort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        j = gap
        while j < n:
            i = j - gap

            while i >= 0:
                if arr[i + gap] > arr[i]:
                    break
                else:
                    arr[i + gap], arr[i] = arr[i], arr[i + gap]
                    yield arr, (i + gap, i)
                i -= gap
            j += 1

        gap = gap // 2

    yield from verif(arr)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, (i, j)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quickSort(arr, low=None, high=None):
    if low is None:
        low = 0
    if high is None:
        high = len(arr) - 1

    if low < high:
        # pi is the partition return index of pivot
        pi = yield from partition(arr, low, high)

        # Recursion calls for smaller elements
        # and greater or equals elements
        yield from quickSort(arr, low, pi - 1)
        yield from quickSort(arr, pi + 1, high)

    if low == 0 and high == len(arr) - 1:
        yield from verif(arr)


def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    L = [0] * n1
    R = [0] * n2

    for i in range(n1):
        L[i] = arr[left + i]
    for j in range(n2):
        R[j] = arr[mid + 1 + j]

    i = 0  # Initial index of first subarr
    j = 0  # Initial index of second subarr
    k = left  # Initial index of merged subarr

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            yield arr, (k, i)
            i += 1
        else:
            arr[k] = R[j]
            yield arr, (k, j)
            j += 1
        k += 1

    while i < n1:
        arr[k] = L[i]
        yield arr, (k, i)
        i += 1
        k += 1

    while j < n2:
        arr[k] = R[j]
        yield arr, (k, j)
        j += 1
        k += 1


def mergeSort(arr, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(arr) - 1

    if left < right:
        mid = (left + right) // 2

        yield from mergeSort(arr, left, mid)
        yield from mergeSort(arr, mid + 1, right)
        yield from merge(arr, left, mid, right)

    if left == 0 and right == len(arr) - 1:
        yield from verif(arr)


def heapify(arr, n, i):
    largest = i

    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr, (i, largest)
        yield from heapify(arr, n, largest)


def heapSort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr, (0, i)
        yield from heapify(arr, i, 0)

    yield from verif(arr)


def cycleSort(arr):
    writes = 0

    for cycleStart in range(0, len(arr) - 1):
        item = arr[cycleStart]

        pos = cycleStart
        for i in range(cycleStart + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        if pos == cycleStart:
            continue

        while item == arr[pos]:
            pos += 1

        arr[pos], item = item, arr[pos]
        yield arr, (pos, cycleStart)
        writes += 1

        while pos != cycleStart:
            pos = cycleStart
            for i in range(cycleStart + 1, len(arr)):
                if arr[i] < item:
                    pos += 1

            while item == arr[pos]:
                pos += 1

            arr[pos], item = item, arr[pos]
            yield arr, (pos, cycleStart)
            writes += 1

    yield from verif(arr)


def countingSort(arr):
    M = max(arr)
    count_arr = [0] * (M + 1)

    for num in arr:
        count_arr[num] += 1

    for i in range(1, M + 1):
        count_arr[i] += count_arr[i - 1]

    output_arr = arr.copy()

    for i in range(len(arr) - 1, -1, -1):
        output_arr[count_arr[arr[i]] - 1] = arr[i]
        yield output_arr, (count_arr[arr[i]] - 1, i)
        count_arr[arr[i]] -= 1

    yield from verif(output_arr)


def exp_countingSort(arr, exp1):
    n = len(arr)
    output = arr.copy()

    count = [0] * (10)

    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        yield output, (count[index % 10] - 1, i)
        count[index % 10] -= 1
        i -= 1

    return output


def radixSort(arr):
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        arr = yield from exp_countingSort(arr, exp)
        exp *= 10

    yield from verif(arr)


def calcMinRun(n):
    MIN_MERGE = 32
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


def lr_insertionSort(arr, left, right):
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            yield arr, (j, j - 1)
            j -= 1


def timSort(arr):
    n = len(arr)
    minRun = calcMinRun(n)

    for start in range(0, n, minRun):
        end = min(start + minRun - 1, n - 1)
        yield from lr_insertionSort(arr, start, end)

    size = minRun
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            if mid < right:
                yield from merge(arr, left, mid, right)

        size = 2 * size

    yield from verif(arr)


def getNextGap(gap):
    gap = (gap * 10) // 13
    if gap < 1:
        return 1
    return gap


def combSort(arr):
    n = len(arr)
    gap = n

    swapped = True

    while gap != 1 or swapped == 1:
        gap = getNextGap(gap)

        swapped = False

        for i in range(0, n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                yield arr, (i, i + gap)
                swapped = True

    yield from verif(arr)


def cocktailSort(arr):
    n = len(arr)

    swapped = True
    start = 0
    end = n - 1

    while swapped == True:
        swapped = False

        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                yield arr, (i, i + 1)
                swapped = True

        if swapped == False:
            break
        swapped = False
        end = end - 1

        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                yield arr, (i, i + 1)
                swapped = True

        start = start + 1

    yield from verif(arr)


def gnomeSort(arr):
    n = len(arr)
    i = 0
    while i < n:
        if i == 0:
            i = i + 1
        if arr[i] >= arr[i - 1]:
            i = i + 1
        else:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            yield arr, (i, i - 1)
            i = i - 1

    yield from verif(arr)


def pigeonholeSort(arr):
    my_min = min(arr)
    my_max = max(arr)
    size = my_max - my_min + 1

    holes = [0] * size

    for x in arr:
        assert type(x) is int, "integers only please"
        holes[x - my_min] += 1

    i = 0
    for count in range(size):
        while holes[count] > 0:
            holes[count] -= 1
            arr[i] = count + my_min
            yield arr, (i, count + my_min)
            i += 1

    yield from verif(arr)
