# PyCSCL 0.2.0 (development version)

PyCSCL is a collection of boolean constraint encoders. You can use it
e.g. to reduce instances of
[NP-complete problems](https://en.wikipedia.org/wiki/NP-completeness) to instances
of the
[Boolean satisifability (SAT) problem](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem),
benefitting from the availability of powerful off-the-shelf SAT
solvers.

Though PyCSCL is designed not to depend on a specific SAT solver interface,
it contains a simple and easy-to-use binding for
SAT solvers implementing the 
[IPASIR](https://github.com/biotomas/ipasir) interface.

## Installing PyCSCL

### Release packages

PyCSCL releases are distributed on the [Python Package Index](https://pypi.org/project/pycscl/).
To be consistent with package naming conventions, the PyCSCL package is named `pycscl`.
To install the latest PyCSCL release package, you can simply use `pip`:

```
python3 -m pip install pycscl
```

### Custom packages

Alternatively, you can check out this repository and install PyCSCL
by creating a package yourself. Navigate to the PyCSCL directory and issue the command

```
python3 setup.py sdist 
```

This will create a package `pycscl-<Version>.tar.gz` file in the
directory `dist`. Now, you can install your custom PyCSCL package 
by running

```
python3 -m pip install <PathToPyCSCL>/dist/pycscl-<Version>.tar.gz
```

## Documentation

* PyCSCL [tutorial](Tutorial.md)
* [Examples](#examples)
* pydoc

## Encoders

##### Cardinality (at-most-k) constraint encoders
- Binomial encoding
- LTSeq encoding

Package: `cscl.cardinality_constraint_encoders`

##### Gate constraint encoders
- AND, OR, binary XOR gates
- Binary MUX gates
- Half adder and full adder gates

Package: `cscl.basic_gate_encoders`

##### Bitvector constraint encoders
- Bitvector AND, OR, XOR gates
- Ripple-carry bitvector adder and (2's complement) subtractor gates
- Parallel bitvector multiplier gate
- Unsigned bitvector divider and modulo gate
- Signed (2's complement) and unsigned bitvector comparison gates

Package: `cscl.bitvector_gate_encoders`

## Examples
- `examples.factorization`: [integer factorization](https://en.wikipedia.org/wiki/Integer_factorization) problem encoder
- `examples.sudoku`: SAT-based [Sudoku](https://en.wikipedia.org/wiki/Sudoku) solver
- `examples.smt_qfbv_solver` (under construction): simple QF_BV
  [SMT](https://en.wikipedia.org/wiki/Satisfiability_modulo_theories) solver
