# a -> b -> c -> d -> None
# d -> c -> b -> a -> None
def reverse_linked_list(head):
    curr = head
    previous = None
    while True:

        # b | c
        next_link = curr.next
        # a -> None | b -> a
        curr.next = previous
        # a | b
        previous = curr

        if not next_link:
            break

        # b | c
        curr = next_link

    return curr
