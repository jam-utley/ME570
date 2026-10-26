import me570_pq
groceries=[(2,'Bananas'),(3,'Cantelope'),(1,'Apples')]

print(f"\nOriginal list order: {groceries}\n")

#Initialize the class
priority_queue = me570_pq.PriorityQueue()

for item in groceries:
    priority_queue.key = item[1]
    priority_queue.cost = item[0]
    #push cost and key to the queue
    priority_queue.push(priority_queue.cost,priority_queue.key)

while priority_queue.is_empty()!=True:
    ascending_value = priority_queue.pop()
    print(f"Priority Queue: {ascending_value}")