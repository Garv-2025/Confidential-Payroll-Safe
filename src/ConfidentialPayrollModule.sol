// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Minimal interface to interact with a Gnosis Safe
interface ISafe {
    function execTransactionFromModule(
        address to,
        uint256 value,
        bytes memory data,
        uint8 operation
    ) external returns (bool success);
}

contract ConfidentialPayrollModule {
    // Declared immutable to optimize gas usage and enforce immutability
    address public immutable employer;
    address public immutable safeAccount;

    bytes32 public payrollRulesHandle;

    event PayrollRulesUpdated(address indexed employer, bytes32 encryptedHandle);
    event SalaryPaid(address indexed employee, uint256 amount, bytes32 userRequestHandle);

    modifier onlyEmployer() {
        require(msg.sender == employer, "Unauthorized: Only Employer can execute");
        _;
    }

    constructor(address _safeAccount) {
        // Zero-address validation
        require(_safeAccount != address(0), "Invalid safe account address");

        employer = msg.sender;
        safeAccount = _safeAccount;
    }

    /// @notice Stores the encrypted rules for payroll
    function setPayrollRules(bytes32 encryptedHandle) external onlyEmployer {
        payrollRulesHandle = encryptedHandle;

        emit PayrollRulesUpdated(msg.sender, encryptedHandle);
    }

    /// @notice Triggers the confidential Nox computation callback

    function withdrawEncryptedSalary(
        address employee, 
        uint256 amountOwed, 
        bytes32 userRequestHandle
    ) external {
    
        // 1. VALIDATION: Ensure there is actually a salary to pay
        require(amountOwed > 0, "No salary owed based on TEE computation");
        require(employee != address(0), "Invalid employee address");

        // 2. EXECUTION: Tell the Safe to send the money
        // operation: 0 represents a standard CALL (sending ETH/Tokens)
        bool success = ISafe(safeAccount).execTransactionFromModule(
            employee, 
            amountOwed, 
            "", // Empty data because we are just sending native ETH
            0   // Operation: Call
        );

        require(success, "Module transaction failed");

        // 3. LOGGING: Emit an event so the indexer knows the payment was processed
        emit SalaryPaid(employee, amountOwed, userRequestHandle);
    }
}