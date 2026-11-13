 
# Unification Algorithm in First Order Logic

# Check whether a term is a variable
def is_variable(x):
    return isinstance(x, str) and x.islower()


# Apply substitutions to an expression
def substitute(term, subst):

    if is_variable(term):
        if term in subst:
            return substitute(subst[term], subst)
        return term

    if isinstance(term, tuple):
        return tuple(substitute(x, subst) for x in term)

    return term


# Check whether a variable occurs inside a term
def occurs(variable, term, subst):

    term = substitute(term, subst)

    if variable == term:
        return True

    if isinstance(term, tuple):
        return any(occurs(variable, x, subst) for x in term)

    return False


# Main unification function
def unify(x, y, subst=None):

    if subst is None:
        subst = {}

    # Apply existing substitutions
    x = substitute(x, subst)
    y = substitute(y, subst)

    # Both expressions are identical
    if x == y:
        return subst

    # First expression is a variable
    if is_variable(x):

        if occurs(x, y, subst):
            return None

        subst[x] = y
        return subst

    # Second expression is a variable
    if is_variable(y):

        if occurs(y, x, subst):
            return None

        subst[y] = x
        return subst

    # Both expressions must have the same structure
    if isinstance(x, tuple) and isinstance(y, tuple):

        # Function or predicate symbols must match
        if x[0] != y[0]:
            return None

        # Number of arguments must match
        if len(x) != len(y):
            return None

        # Unify arguments recursively
        for a, b in zip(x[1:], y[1:]):

            subst = unify(a, b, subst)

            if subst is None:
                return None

        return subst

    # Different constants
    return None


# Display results
def test_unification(exp1, exp2):

    print("\nExpression 1:", exp1)
    print("Expression 2:", exp2)

    result = unify(exp1, exp2)

    if result is None:
        print("Unification Failed")

    else:
        print("Unification Successful")
        print("Substitution:", result)

        print("Unified Expression 1:",
              substitute(exp1, result))

        print("Unified Expression 2:",
              substitute(exp2, result))


# Example 1
test_unification(
    ("Eats", "x", "Apple"),
    ("Eats", "Riya", "y")
)

# Example 2
test_unification(
    ("P", "x", "y"),
    ("Q", "a", "b")
)

# Example 3
test_unification(
    ("P", "John", "x"),
    ("P", "Mary", "y")
)

# Example 4
test_unification(
    ("P", ("f", "x"), "y"),
    ("P", ("f", "John"), "Apple")
)

# Example 5
test_unification(
    ("P", "x", "x"),
    ("P", "a", "a")
)

# Example 6: Occurs check
test_unification(
    ("P", "x"),
    ("P", ("f", "x"))
)
