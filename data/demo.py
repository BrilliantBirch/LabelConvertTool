from itertools import combinations
from collections import Counter

def calculate_ratio(container_items):
    total_items = sum(container_items.values())
    return {k: v / total_items for k, v in container_items.items()}

def calculate_error(group_ratios, target_ratios):
    error = 0
    all_keys = set(group_ratios.keys()).union(set(target_ratios.keys()))
    for key in all_keys:
        error += abs(group_ratios.get(key, 0) - target_ratios.get(key, 0))
    return error

def merge_containers(container_list):
    merged = Counter()
    for container in container_list:
        merged.update(container)
    return dict(merged)

def divide_containers(containers, num_groups):
    all_indices = list(range(len(containers)))
    best_error = float('inf')
    best_groups = None
    
    # 模拟各数据集类别平衡
    for combination in combinations(all_indices, len(containers) // num_groups):
        group1_indices = set(combination)
        group2_indices = set(all_indices) - group1_indices
        
        group1 = [containers[i] for i in group1_indices]
        group2 = [containers[i] for i in group2_indices]
        
        if len(group2) > 0:
            group1_merged = merge_containers(group1)
            group2_merged = merge_containers(group2)
            total_merged = merge_containers(containers)
            
            group1_ratio = calculate_ratio(group1_merged)
            group2_ratio = calculate_ratio(group2_merged)
            target_ratio = calculate_ratio(total_merged)
            
            error = calculate_error(group1_ratio, target_ratio) + calculate_error(group2_ratio, target_ratio)
            
            if error < best_error:
                best_error = error
                best_groups = (group1, group2)
    
    return best_groups


containers = [
    {'item1': 10, 'item2': 20,'item3':40},
    {'item1': 20, 'item2': 10,'item3':20},
    {'item1': 30, 'item2': 30,'item3':10},
    {'item1': 10, 'item2': 10}
]

num_groups = 2  # 分成3组
groups = divide_containers(containers, num_groups)
print("Best Groups:", groups)
