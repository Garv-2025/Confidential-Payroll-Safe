// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import { Nox } from "@iexec-nox/nox-protocol-contracts/contracts/sdk/Nox.sol";
import { Enum } from "@safe-global/safe-contracts/contracts/common/Enum.sol";

interface ISafe {
    function execTransactionFromModule(
        address to,
        uint256 value,
        bytes memory data,
        Enum.Operation operation
    ) external returns (bool success);
}

contract ConfidentialPayrollModule {
    address public safeAccount;

    // We store the encrypted handle pointing to the total payroll split rules
    bytes32 public payrollRulesHandle;

    constructor(address _safeAccount) {
        safeAccount = _safeAccount;
    }

    /// @notice Stores the encrypted rules for payroll
    function setPayrollRules(bytes32 encryptedHandle) external {
        // Nox will manage the ACL (Access Control List) for this encrypted handle
        payrollRulesHandle = encryptedHandle;
    }

    /// @notice Triggers the confidential Nox computation
    function withdrawEncryptedSalary(bytes32 userRequestHandle) external {
        // 1. Nox SDK validates the handle proofs.
        // 2. An off-chain TEE computes if msg.sender is owed money.
        // 3. A callback triggers ISafe(safeAccount).execTransactionFromModule(...)
        
        // Advanced smart contract concepts and security modifiers will be built here.
    }
}