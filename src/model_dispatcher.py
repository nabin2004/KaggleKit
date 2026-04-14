from sklearn import ensemble, linear_model, tree

models = {
    "decision_tree_gini": tree.DecisionTreeClassifier(criterion="gini"),
    "decision_tree_entropy": tree.DecisionTreeClassifier(criterion="entropy"),
    "rf": ensemble.RandomForestClassifier(),
    "log_reg": linear_model.LogisticRegression(),
    "line_reg": linear_model.LinearRegression(),
}
