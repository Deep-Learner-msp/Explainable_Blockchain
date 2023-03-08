pragma solidity ^0.8.0;

contract Voting {
    // an array of candidates, where each candidate has an ID and a name
    struct Candidate {
        uint256 id;
        string name;
        uint256 voteCount;
    }
    
    // an array of voters, where each voter has an address and a boolean indicating if they have voted
    struct Voter {
        address voterAddress;
        bool hasVoted;
    }

    // the person who deploys the contract is the owner
    address public owner;
    
    // an array of candidates
    Candidate[] public candidates;
    
    // a mapping of voter addresses to voters
    mapping(address => Voter) public voters;

    // an event that is emitted when a vote is cast
    event VoteCast(address indexed voter, uint256 candidateId);

    constructor() {
        owner = msg.sender;
    }

    // function to add a new candidate to the candidates array
    function addCandidate(string memory name) public {
        require(msg.sender == owner, "Only the owner can add candidates.");
        candidates.push(Candidate(candidates.length, name, 0));
    }

    // function to cast a vote for a candidate
    function castVote(uint256 candidateId) public {
        // check that the voter has not already voted
        require(!voters[msg.sender].hasVoted, "You have already voted.");
        
        // check that the candidate ID is valid
        require(candidateId < candidates.length, "Invalid candidate ID.");

        // record the vote and mark the voter as having voted
        candidates[candidateId].voteCount++;
        voters[msg.sender].hasVoted = true;

        // emit a VoteCast event
        emit VoteCast(msg.sender, candidateId);
    }

    // function to get the total number of votes for a candidate
    function getVoteCount(uint256 candidateId) public view returns (uint256) {
        require(candidateId < candidates.length, "Invalid candidate ID.");
        return candidates[candidateId].voteCount;
    }
}
