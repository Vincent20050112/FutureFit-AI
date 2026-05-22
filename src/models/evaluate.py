from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


def evaluate_model(y_test, y_pred, average="macro"):
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, average=average, zero_division=0))
    print("Recall:", recall_score(y_test, y_pred, average=average, zero_division=0))
    print("F1 Score:", f1_score(y_test, y_pred, average=average, zero_division=0))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))