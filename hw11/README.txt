################################################################################
#                                  Homework 11                                 #
#                CS 411 - Artificial Intelligence I - Fall 2019                #
#                           Matteo Corain 650088272                            #
################################################################################

## Requirements ##

- Python3 interpreter (tested on Python 3.8.0, Windows OS)
- SciPy package (for computing chi2 values, can be installed using pip)

## How to run ##

Run script dtree.py using the Python interpreter:
    > python dtree.py [restaurant_input_file]

Options:
    - restaurant_input_file: path to the file containing the restaurant data.

## How it works ##

The decision tree is represented by means of the DecisionTree class, exposing 
to the client the following methods:

- fit(examples, labels), used for learning the tree from the given examples and 
labels;
- predict(examples), used for predicting the class label for the given examples 
after having trained the model;
- test(examples, labels), used to evaluate the accuracy of the classification 
on the given examples;
- prune(alpha), used to prune a trained tree with the given significance level;
- print(), used to print the obtained tree to the console.

Two additional classes are needed for the representation of the tree:

- Leaf: it represents a leaf node, associated with a certain class label;
- Subtree: it represents a subtree, characterized by the attribute on which the 
split has occurred, its information gain and a set of edges (associated with 
every possible value for the split attribute and in turn pointing to other leaf 
or subtree nodes).

The input file is parsed through the parse_restaurants() function, that exploits
the CSV reader class provided by the Python language to construct the examples 
dictionaries (each property corresponds to an attribute of the data point) and 
the list of labels. These are then passed to the fit() method, which calls the 
internal recursive procedure _fit_int() with the initial parameters; this takes 
the following actions:

- If the list of examples is empty, it returns a leaf node associated with the 
default value as label;
- If all examples have the same label, it returns a leaf node associated with 
that particular label;
- If no more split attributes are available, it returns a leaf node associated 
with the mode of the labels of the provided examples;
- In all other cases, it selects the best attribute through the internal method 
_best_attribute(), creates a new subtree and populates it with all the edges 
associated to each value of the selected split attribute; the node towards which
each edge points is determined by a recursive call to the method.

The _best_attribute() method selects the best attribute by computing the gain in
entropy obtained by performing a split on each available attribute with respect 
to the entropy of the node if no split is performed, returning the one resulting
in the highest gain. Entropies are computed through the _entropy() method.

The predict() method performs, for each of the given examples, a tree traversal 
starting from the root and terminating when a leaf node is found, at which point
the corresponding label is returned. This method is internally used also by the 
test() method, which additionally compares the predicted labels with the actual 
labels provided as parameter.

The prune() method implements a chi-squared pruning procedure for an already 
trained decision tree. The computation is carried out in the internal recursive 
procedure _prune_int(), which performs the following actions:

- It checks for each outgoing edge from the current node whether it is a leaf 
or a subtree, in which case it recursively calls itself on that node;
- If, after all the recursive calls have been performed, the current node has 
only leaves as children, it proceeds to compute the values of parameters p, n, 
pk, nk, pk_hat and nk_hat for each outgoing edge, consequently computing the 
chi-squared value for the node;
- Finally, it checks whether the computed value is lower than the value of the 
chi-squared distribution with a number of degrees of freedom equal to the number
of outgoing edges minus one, in which case it transforms the current node into 
a leaf node to which the class label of the majority is assigned; otherwise, the
old node is returned and no change is made.

Finally, the print() function calls the internal _print_int() function, which 
performs the following actions:

- If the current node is a leaf, it prints the class label and the number of 
examples in that node, then returns;
- If the current node is a subtree, it prints the split attribute and the info 
gain, then loops through the outgoing edges and calls itself on each of the 
connected nodes.