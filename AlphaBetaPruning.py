class Node:
    def __init__(self, value=None, children=None, is_maximizing=True):
        self.value = value
        self.children = children if children else []
        self.is_maximizing = is_maximizing


class AlphaBetaPruning:
    def __init__(self):
        self.pruned_values = []

    def alpha_beta(self, node, depth, alpha, beta, maximizing_player=True):
        if depth == 0 or not node.children:
            return node.value

        if maximizing_player:
            value = float('-inf')
            for child in node.children:
                child_value = self.alpha_beta(child, depth - 1, alpha, beta, False)
                value = max(value, child_value)
                alpha = max(alpha, value)
                if value >= beta:
                    self.pruned_values.append(child_value)
                    break
            return value
        else:
            value = float('inf')
            for child in node.children:
                child_value = self.alpha_beta(child, depth - 1, alpha, beta, True)
                value = min(value, child_value)
                beta = min(beta, value)
                if value <= alpha:
                    self.pruned_values.append(child_value)
                    break
            return value

    def evaluate_game_tree(self, root, depth):
        self.pruned_values = []
        optimal_value = self.alpha_beta(root, depth, float('-inf'), float('inf'), True)
        print(f"Optimal value: {optimal_value}")
        print(f"Pruned values: {self.pruned_values}")
        return optimal_value


def create_test_tree():
    leaf1 = Node(value=3)
    leaf2 = Node(value=5)
    leaf3 = Node(value=6)
    leaf4 = Node(value=9)
    leaf5 = Node(value=1)
    leaf6 = Node(value=2)
    leaf7 = Node(value=0)
    leaf8 = Node(value=8)

    min_node1 = Node(children=[leaf1, leaf2], is_maximizing=False)
    min_node2 = Node(children=[leaf3, leaf4], is_maximizing=False)
    min_node3 = Node(children=[leaf5, leaf6], is_maximizing=False)
    min_node4 = Node(children=[leaf7, leaf8], is_maximizing=False)

    max_node1 = Node(children=[min_node1, min_node2], is_maximizing=True)
    max_node2 = Node(children=[min_node3, min_node4], is_maximizing=True)

    root = Node(children=[max_node1, max_node2], is_maximizing=False)
    return root


if __name__ == "__main__":
    tree = create_test_tree()
    ab_pruning = AlphaBetaPruning()
    result = ab_pruning.evaluate_game_tree(tree, depth=3)