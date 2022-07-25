def split(li, nb_batches):
    len_li = len(li)
    batch_size_base = len_li // nb_batches
    remainder = len_li % nb_batches
    batch_sizes = [batch_size_base for _ in range(nb_batches)]
    for i in range(remainder):
        batch_sizes[i] += 1
    assert sum(batch_sizes) == len_li
    batch_indexes = [sum(batch_sizes[:i]) for i in range(len(batch_sizes) + 1)]
    batches = []
    for i in range(len(batch_indexes) - 1):
        batch = li[batch_indexes[i]:batch_indexes[i + 1]]
        batches.append(batch)
    return batches
