import sys

sys.path.append("../")

import pytest

from qiskit.circuit import QuantumCircuit
from qiskit_aer import AerSimulator

from ghz_state_generator import create_ghz_state_quantum_circuit

BACKEND = AerSimulator()
SHOTS = 1024
NUM_QUBITS_LIST = [*range(2, 17)]


def test_object_type():
    qc = create_ghz_state_quantum_circuit(num_qubits=2)

    assert isinstance(qc, QuantumCircuit)


def test_error_message():
    with pytest.raises(
        ValueError,
        match="It's not possible to create a GHZ state with less than 2 qubits!",
    ):
        _ = create_ghz_state_quantum_circuit(num_qubits=1)


@pytest.mark.parametrize("num_qubits", NUM_QUBITS_LIST)
def test_ghz_state(num_qubits):
    qc = create_ghz_state_quantum_circuit(num_qubits=num_qubits, add_measurements=True)
    counts = BACKEND.run(qc, shots=SHOTS).result().get_counts()

    assert sorted(list(counts.keys()))[0] == "0" * num_qubits
    assert sorted(list(counts.keys()))[1] == "1" * num_qubits
