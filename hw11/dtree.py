import csv
import math

class Leaf:
    def __init__(self, label):
        self.label = label

class Subtree:
    def __init__(self, split_att):
        self.split_att = split_att
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
        entropy = - sum([prob[v] * math.log2(prob[v]) for v in set(values)])
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
            branch_entropies = []
            for value in set([e[att] for e in examples]):
                branch_entropies.append(self._entropy([labels[i] for i in range(len(labels)) if examples[i][att] == value]))
            
            # Compute overall split entropy
            split_entropy = sum(branch_entropies) / len(branch_entropies)

            # Evaluate information gain
            gain = split_entropy - base_entropy
            if gain < best_gain:
                best_att = att
                best_gain = gain

        return best_att

    def _dtree_learn(self, examples, attributes, labels, default, level):
        # Check if examples is empty
        if len(examples) == 0:
            print("  " * level + f"Label: {default}")
            return Leaf(default)

        # Check if all elements have the same classification
        elif all([y == labels[0] for y in labels]):
            print("  " * level + f"Label: {labels[0]}")
            return Leaf(labels[0])
        
        # Check if attributes is empty
        elif len(attributes) == 0:
            print("  " * level + f"Label: {self._mode(labels)}")
            return Leaf(self._mode(labels))
        
        # Select the split attribute
        split_att = self._best_attribute(examples, attributes, labels)
        print("  " * level + f"Splitting on {split_att}:")

        # Create the subtree
        subtree = Subtree(split_att)
        
        # Create edges for each value
        for value in set([e[split_att] for e in examples]):
            split_examples = [e for e in examples if e[split_att] == value]
            split_attributes = [a for a in attributes if a != split_att]
            split_labels = [labels[i] for i in range(len(labels)) if examples[i][split_att] == value]
            
            print("  " * level + f"Value {value}:")
            subtree.add_edge(value, self._dtree_learn(split_examples, split_attributes, split_labels, self._mode(labels), level + 1))
        
        return subtree

    def fit(self, examples, labels):
        self.root = self._dtree_learn(examples, examples[0].keys(), labels, self._mode(labels), 0)

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

def parse_restaurants(filename):
    examples = []
    labels = []

    with open(filename, "r", newline="") as f:
        # Create the CSV parser
        parser = csv.reader(f)

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

# Test the classification
accuracy = tree.test(examples, labels)
print(f"Decision tree accuracy: {accuracy:.2%}")