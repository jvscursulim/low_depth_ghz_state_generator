from qiskit.circuit import ClassicalRegister, QuantumCircuit, QuantumRegister


def create_ghz_state_quantum_circuit(
    num_qubits: int, add_measurements: bool = False
) -> QuantumCircuit:
    """Create the quantum circuit with low depth that
    prepares a GHZ state with the number of qubits gave
    as input.

    Args:
        num_qubits (int): The number of qubits in the circuit.
        add_measurements (bool, optional): A boolean flag that tells with
        we want to add measurements in the quantum circuit. Defaults to False.

    Raises:
        ValueError: If num_qubits is less than 2.

    Returns:
        QuantumCircuit: The quantum circuit of the GHZ state with the number
        of qubits desired.
    """

    if num_qubits < 2:
        raise ValueError(
            "It's not possible to create a GHZ state with less than 2 qubits!"
        )
    else:
        qubits_numbers = [*range(num_qubits)]
        if num_qubits % 2 == 1:
            qubits_numbers.remove(1)

        qubits_tuples_list = []
        half = int(len(qubits_numbers) / 2)
        i = 0
        while len(qubits_tuples_list) < int(len(qubits_numbers)) - 2:
            if i == 0:
                qubits_tuples_list.append(
                    (qubits_numbers[:half][i], qubits_numbers[:half][-1 - i])
                )
                qubits_tuples_list.append(
                    (qubits_numbers[half:][-1 - i], qubits_numbers[half:][i])
                )
                upper1 = qubits_numbers[:half][i]
                upper2 = qubits_numbers[half:][-1 - i]
                bottom1 = qubits_numbers[:half][-1 - i]
                bottom2 = qubits_numbers[half:][i]
            else:
                if i % 2 == 0:
                    qubits_tuples_list.append((upper1, qubits_numbers[:half][-1 - i]))
                    qubits_tuples_list.append((upper2, qubits_numbers[half:][i]))
                    bottom1 = qubits_numbers[:half][-1 - i]
                    bottom2 = qubits_numbers[half:][i]
                else:
                    qubits_tuples_list.append((bottom1, qubits_numbers[:half][-1 - i]))
                    qubits_tuples_list.append((bottom2, qubits_numbers[half:][i]))
                    bottom1 = qubits_numbers[:half][-1 - i]
                    bottom2 = qubits_numbers[half:][i]
            i += 1

        qubits = QuantumRegister(size=num_qubits, name="qubits")
        if add_measurements:
            bits = ClassicalRegister(size=num_qubits, name="bits")
            qc = QuantumCircuit(qubits, bits)
        else:
            qc = QuantumCircuit(qubits)

        qc.h(qubit=qubits[0])
        qc.cx(control_qubit=qubits[0], target_qubit=qubits[-1])
        if len(qubits_numbers) > 2:
            for qubits_tuple in qubits_tuples_list:
                qc.cx(
                    control_qubit=qubits[qubits_tuple[0]],
                    target_qubit=qubits[qubits_tuple[1]],
                )
        if num_qubits % 2 == 1:
            qc.cx(control_qubit=qubits[0], target_qubit=qubits[1])
        if add_measurements:
            qc.barrier()
            qc.measure(qubit=qubits, cbit=bits)

        return qc
