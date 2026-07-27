// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {ConfidentialPayrollModule} from "../src/ConfidentialPayrollModule.sol";

contract ConfidentialPayrollModuleTest is Test {
    ConfidentialPayrollModule public payrollModule;
    address public employer = address(0x1);
    address public safeAccount = address(0x2);

    function setUp() public {
        vm.prank(employer);
        payrollModule = new ConfidentialPayrollModule(safeAccount);
    }

    function test_EmployerCanSetRules() public {
        vm.prank(employer);
        payrollModule.setPayrollRules(bytes32("rules_hash"));
        assertEq(payrollModule.payrollRulesHandle(), bytes32("rules_hash"));
    }

    function test_HackerCannotSetRules() public {
        address hacker = address(0x3);
        vm.prank(hacker);
        vm.expectRevert("Unauthorized: Only Employer can execute");
        payrollModule.setPayrollRules(bytes32("hacked_rules"));
    }

    function testFuzz_HackerCannotSetRules(address randomAddress) public {
        // Exclude legitimate actors and zero address
        vm.assume(randomAddress != employer && randomAddress != address(0));

        vm.prank(randomAddress);
        vm.expectRevert("Unauthorized: Only Employer can execute");

        payrollModule.setPayrollRules(bytes32("hacked_rules"));
    }
}
