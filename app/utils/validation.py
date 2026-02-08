def is_multi_mark(fill_ratios, threshold):
    marked = [f for f in fill_ratios if f > threshold]
    return len(marked) > 1
