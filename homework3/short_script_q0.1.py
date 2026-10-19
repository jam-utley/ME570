# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 16:13:03 2026

@author: Owner
"""

groceries=[(2,'Bananas'),(3,'Cantelope'),(1,'Apples')]

priority_queue = Priority_Queue.__init__()
for items in groceries:
    priority_queue = Priority_Queue.push()

while priority_queue.is_empty()==False:
    ascending_value = priority_queue.pop()
    print(f"Priority Queue: {ascending_value}")

