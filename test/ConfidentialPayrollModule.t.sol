// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Test.sol";
import "../src/ConfidentialPayrollModule.sol";

contract ConfidentialPayrollModuleTest is Test {
    ConfidentialPayrollModule public payrollModule;
    
    // Create dummy addresses for testing
    address employer = address(1);
    address randomHacker = address(2);
    address dummySafe = address(3);

    function setUp() public {
        // vm.prank simulates the 'employer' wallet deploying the contract
        vm.prank(employer); 
        payrollModule = new ConfidentialPayrollModule(dummySafe);
    }

    function test_EmployerCanSetRules() public {
        vm.prank(employer); // Act as the employer
        payrollModule.setPayrollRules(bytes32("secret_rules"));
        
        // Check that the rules were successfully saved
        assertEq(payrollModule.payrollRulesHandle(), bytes32("secret_rules"));
    }

    function test_HackerCannotSetRules() public {
        vm.prank(randomHacker); // Act as a random unauthorized wallet
        
        // We tell Foundry to EXPECT this next transaction to fail with our exact error message
        vm.expectRevert("Unauthorized: Only Employer can execute");
        
        // The hacker tries to overwrite the rules
        payrollModule.setPayrollRules(bytes32("hacked_rules"));
    }
}