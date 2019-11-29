from csv import reader
from math import log2
from scipy.stats import chi2

class Leaf:
    def __init__(self, label, examples, labels):
        self.label = label
        self.examples = examples
        self.labels = labels

class Subtree:
    def __init__(self, split_att, info_gain, examples, labels):
        self.split_att = split_att
        self.info_gain = info_gain
        self.examples = examples
        self.labels = labels
        self.edges = {}
    
    def add_edge(self, value, result):
        self.edges[value] = result
    
    def get_result(self, value):
        return self.edges[value]

class DecisionTree:
    def __init__(self):
        self.split_att = None
        self.edges = []

    def _entropy(self, values):
        # Compute the probability of each value
        prob = {}
        for value in set(values):
            prob[value] = sum([1 for v in values if v == value]) / len(values)
        
        # Compute the entropy value
        entropy = - sum([prob[v] * log2(prob[v]) for v in set(values)])
        return entropy

    def _mode(self, labels):
        mode = None
        mode_count = 0

        # Select the value with the highest count
        for value in set(labels):
            count = sum([1 for l in labels if l == value])
            if count > mode_count:
                mode = value
                mode_count = count
        
        return mode

    def _best_attribute(self, examples, attributes, labels):
        best_att = None
        best_gain = 0

        # Compute the baseline entropy of the node
        base_entropy = self._entropy(labels)

        # Evaluate splitting on each attribute
        for att in attributes:
            # Compute entropy for each value of the split attribute
            split_entropy = 0
            for value in set([e[att] for e in examples]):
                branch_labels = [labels[i] for i in range(len(labels)) if examples[i][att] == value]
                split_entropy = split_entropy + (self._entropy(branch_labels)) * len(branch_labels) / len(labels)
            
            # Evaluate information gain
            gain = split_entropy - base_entropy
            if gain < best_gain:
                best_att = att
                best_gain = gain

        return best_att, best_gain

    def _fit_int(self, examples, attributes, labels, default, level):
        # Check if examples is empty
        if len(examples) == 0:
            return Leaf(default, examples, labels)

        # Check if all elements have the same classification
        elif all([y == labels[0] for y in labels]):
            return Leaf(labels[0], examples, labels)
        
        # Check if attributes is empty
        elif len(attributes) == 0:
            return Leaf(self._mode(labels), examples, labels)
        
        # Select the split attribute
        split_att, info_gain = self._best_attribute(examples, attributes, labels)

        # Create the subtree
        subtree = Subtree(split_att, info_gain, examples, labels)
        
        # Create edges for each value
        for value in set([e[split_att] for e in examples]):
            split_examples = [e for e in examples if e[split_att] == value]
            split_attributes = [a for a in attributes if a != split_att]
            split_labels = [labels[i] for i in range(len(labels)) if examples[i][split_att] == value]
            
            subtree.add_edge(value, self._fit_int(split_examples, split_attributes, split_labels, self._mode(labels), level + 1))
        
        return subtree

    def fit(self, examples, labels):
        # Fit the tree
        self.root = self._fit_int(examples, examples[0].keys(), labels, self._mode(labels), 0)

    def predict(self, examples):
        labels = []

        # Check that the tree has already been fitted
        if self.root == None:
            print("Decision tree has not been fitted yet!")
            return

        for e in examples:
            # Start from the root
            current = self.root

            # Traverse the tree until a leaf node is found
            while type(current) != Leaf:
                current = current.get_result(e[current.split_att])
            
            # Append the label to the list
            labels.append(current.label)
        
        return labels
    
    def test(self, examples, labels):
        # Check that the tree has already been fitted
        if self.root == None:
            print("Decision tree has not been fitted yet!")
            return
        
        # Compute the overall accuracy
        predicted_labels = self.predict(examples)
        return sum([1 for i in range(len(labels)) if labels[i] == predicted_labels[i]]) / len(labels)
    
    def _prune_int(self, node, alpha):
        # Process any subtree of the current node
        for value in node.edges:
            if type(node.edges[value]) == Subtree:
                node.edges[value] = self._prune_int(node.edges[value], alpha)

        # Test a node for pruning if it has only Leaf edges
        if all([type(node.edges[v]) == Leaf for v in node.edges]):
            # Count positive and negative elements in the node
            p = sum([1 for l in node.labels if l == "Yes"])
            n = sum([1 for l in node.labels if l == "No"])
            data_chi2 = 0

            # Count positive and negative elements in the leaves and update the chi-squared
            for value in node.edges:
                pk = sum([1 for l in node.edges[value].labels if l == "Yes"])
                nk = sum([1 for l in node.edges[value].labels if l == "No"])
                pk_hat = p * (pk + nk) / (p + n)
                nk_hat = n * (pk + nk) / (p + n)
                data_chi2 = data_chi2 + ((pk - pk_hat) ** 2) / pk_hat + ((nk - nk_hat) ** 2) / nk_hat
            
            # Check chi-squared and prune the tree
            if data_chi2 >= chi2(len(node.edges) - 1).ppf(1 - alpha):
                return Leaf(self._mode(node.labels), node.examples, node.labels)
            else:
                return node
        
        return node
    
    def prune(self, alpha):
        # Check that the tree has already been fitted
        if self.root == None:
            print("Decision tree has not been fitted yet!")
            return
        
        # Prune the tree
        self.root = self._prune_int(self.root, alpha)

    def _print_int(self, node, level):
        if type(node) == Leaf:
            print("    " * level + f"Label: {node.label}")
            return
        
        print("    " * level + f"Split on: {node.split_att}")
        for value in node.edges:
            print("    " * level + f"Value: {value}")
            self._print_int(node.edges[value], level + 1)
    
    def print(self):
        self._print_int(self.root, 0)

def parse_restaurants(filename):
    examples = []
    labels = []

    with open(filename, "r", newline="") as f:
        # Create the CSV parser
        parser = reader(f)

        # Read the class names
        class_names = next(parser)

        for line in parser:
            # Read properties of the next example
            e = {}
            for i in range(len(line) - 1):
                e[class_names[i]] = line[i]
            
            # Insert the next example and the relative label
            examples.append(e)
            labels.append(line[-1])
    
    return examples, labels

# Parse the input file
examples, labels = parse_restaurants("restaurant.csv")

# Learn the decision tree
tree = DecisionTree()
tree.fit(examples, labels)

# Print the obtained tree
print("Decision tree before pruning:")
tree.print()

# Test the classification
accuracy = tree.test(examples, labels)
print(f"Decision tree accuracy: {accuracy:.2%}")

print()

# Prune the tree
tree.prune(0.05)

# Print the pruned tree
print("Decision tree after pruning:")
tree.print()

# Test the classification
accuracy = tree.test(examples, labels)
print(f"Decision tree accuracy: {accuracy:.2%}")