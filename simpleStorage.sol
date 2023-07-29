// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract store {
    uint256 number=12;
    // uint256 public number = 60;
    uint256 myNumber;

    struct people {
        uint256 age;
        string name;
    }
    people public individual = people({name: "kev", age: 22});

    mapping(string => uint256) public search;

    struct student {
        uint256 admisionNumber;
        string name;
    }
    student[] public newEnrollment;

    function warehouse(uint256 numberChange) public {
        number = numberChange;
    }

    function getBack() public view returns (uint256) {
        return myNumber;
    }

    function returnNumber(uint256 myMbana) public returns (uint256) {
        myNumber = myMbana;
        return myNumber;
    }

    function getPure(int256 numbers) public pure {
        numbers + numbers;
    }

    function addStudent(string memory jina, uint256 admission) public {
        newEnrollment.push(student(admission, jina));
        search[jina] = admission;
    }
}
