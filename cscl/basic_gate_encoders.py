from cscl.clause_consumer import ClauseConsumer, CNFVariableFactory


def encode_or_gate(clause_consumer: ClauseConsumer, variable_factory: CNFVariableFactory, input_lits, output_lit=None):
    """
    Creates an OR gate.

    :param clause_consumer: The clause consumer to which the clauses of the gate encoding shall be added.
    :param variable_factory: The CNF variable factory to be used for creating new variables.
    :param input_lits: The gate's input literals.
    :param output_lit: The gate's output literal. If output_lit is None, a positive literal with a
                       new variable will be used as the gate's output literal.
    :return: The encoded gate's output literal.
    """
    if output_lit is None:
        output_lit = variable_factory.create_variable()

    fwd_clause = input_lits[:]
    fwd_clause.append(-output_lit)
    clause_consumer.consume_clause(fwd_clause)

    for lit in input_lits:
        clause_consumer.consume_clause([-lit, output_lit])

    return output_lit


def encode_and_gate(clause_consumer: ClauseConsumer, variable_factory: CNFVariableFactory, input_lits, output_lit=None):
    """
    Creates an AND gate.

    :param clause_consumer: The clause consumer to which the clauses of the gate encoding shall be added.
    :param variable_factory: The CNF variable factory to be used for creating new variables.
    :param input_lits: The gate's input literals.
    :param output_lit: The gate's output literal. If output_lit is None, a positive literal with a
                       new variable will be used as the gate's output literal.
    :return: The encoded gate's output literal.
    """

    if output_lit is None:
        output_lit = variable_factory.create_variable()

    fwd_clause = list(map(lambda x: -x, input_lits))
    fwd_clause.append(output_lit)
    clause_consumer.consume_clause(fwd_clause)

    for lit in input_lits:
        clause_consumer.consume_clause([lit, -output_lit])

    return output_lit


def encode_binary_xor_gate(clause_consumer: ClauseConsumer, variable_factory: CNFVariableFactory,
                           input_lits, output_lit=None):
    """
    Creates a binary XOR gate.

    :param clause_consumer: The clause consumer to which the clauses of the gate encoding shall be added.
    :param variable_factory: The CNF variable factory to be used for creating new variables.
    :param input_lits: The gate's input literals, a list of two distinct literals.
    :param output_lit: The gate's output literal. If output_lit is None, a positive literal with a
                       new variable will be used as the gate's output literal.
    :return: The encoded gate's output literal.
    """

    if output_lit is None:
        output_lit = variable_factory.create_variable()
    l1, l2 = input_lits[0], input_lits[1]

    clause_consumer.consume_clause([l1, l2, -output_lit])
    clause_consumer.consume_clause([-l1, -l2, -output_lit])
    clause_consumer.consume_clause([l1, -l2, output_lit])
    clause_consumer.consume_clause([-l1, l2, output_lit])

    return output_lit


def encode_binary_mux_gate(clause_consumer: ClauseConsumer, variable_factory: CNFVariableFactory,
                           input_lits, output_lit=None):
    """
    Creates a binary MUX gate.

    The created gate has three input literals lhs, rhs, sel (in this order) and encodes the
    constraint

      output_lit <-> ((-sel AND lhs) or (sel AND rhs))

    i.e. an "if-then-else" gate.

    :param clause_consumer: The clause consumer to which the clauses of the gate encoding shall be added.
    :param variable_factory: The CNF variable factory to be used for creating new variables.
    :param input_lits: The gate's input literals, a list of three literals.
    :param output_lit: The gate's output literal. If output_lit is None, a positive literal with a
                       new variable will be used as the gate's output literal.
    :return: The encoded gate's output literal.
    """
    if output_lit is None:
        output_lit = variable_factory.create_variable()
    sel, lhs, rhs = input_lits[0], input_lits[1], input_lits[2]

    clause_consumer.consume_clause([sel, lhs, -output_lit])
    clause_consumer.consume_clause([sel, -lhs, output_lit])
    clause_consumer.consume_clause([-sel, rhs, -output_lit])
    clause_consumer.consume_clause([-sel, -rhs, output_lit])

    return output_lit


def encode_cnf_constraint_as_gate(clause_consumer: ClauseConsumer, variable_factory: CNFVariableFactory,
                                  formula, output_lit=None):
    """
    Creates a gate whose output evaluates to true iff the given CNF constraint is satisfied.
    All literals occurring in the formula are considered inputs to the created gate.

    This encoder is not only useful for prototyping gates, but also for testing optimized constraints:
    E.g. if you have a CNF constraint C and an optimized variant C' of C (with distinct inner
    "helper" variables), you can check their equivalence by creating the following miter problem:

              _____________________
    i1 ----->|                     |
    i2 ----->| Gate encoding of C  | -------\
    ... ---->|                     |        |     _____
    iN ----->|_____________________|        \--->|     |
              _____________________              | XOR |---> o     + unary clause [o]
    i1 ----->|                     |        /--->|_____|
    i2 ----->| Gate encoding of C' |        |
    ... ---->|                     | -------/
    iN ----->|_____________________|

    The CNF encoding of this circuit is unsatisfiable if and only if C and C' are equivalent.

    Use this encoder with caution: crafting a specialized gate for the given constraint
    is likely to yield a better encoding. Let Z be the sum of the lengths of the clauses contained
    in formula. Then, this function creates len(formula)+1 gates, with 2*len(formula) + Z + 1
    clauses, out of which len(formula)+Z are binary clauses.

    :param clause_consumer: The clause consumer to which the clauses of the gate encoding shall be added.
    :param variable_factory: The CNF variable factory to be used for creating new variables.
    :param formula: The constraint to be encoded as a gate, represented as a CNF formula given as a list
                    of lists of literals (i.e. in clausal form)
    :param output_lit: The gate's output literal. If output_lit is None, a positive literal with a
                       new variable will be used as the gate's output literal.
    :return: The encoded gate's output literal.
    """

    # Potential optimizations:
    #  - if the constraint is empty, return just a unary clause containing the output literal
    #  - don't create OR gates for unary clauses in formula
    #  - don't create an AND gate if clause_outs has just one element
    # Delaying their implementation until they are actually needed.
    clause_outs = list(map(lambda clause: encode_or_gate(clause_consumer, variable_factory, clause), formula))
    return encode_and_gate(clause_consumer, variable_factory, clause_outs, output_lit)
