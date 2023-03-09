// SPDX-License-Identifier: MIT

// OpenZeppelin Contracts (last updated v4.8.0) (token/ERC20/ERC20.sol)


pragma solidity ^0.8.0;


import ;

import ;

import ;



    function decimals() public view virtual override returns (uint8) {

        // return 18;

        return 0;

    }


    

    function totalSupply() public view virtual override returns (uint256) {

        return _totalSupply;

    }


    

    function balanceOf(address account) public view virtual override returns (uint256) {

        return _balances[account];

    }


    

    function transfer(address to, uint256 amount) public virtual override returns (bool) {

        address owner = _msgSender();

        _transfer(owner, to, amount);

        return true;

    }


    

    function allowance(address owner, address spender) public view virtual override returns (uint256) {

        return _allowances[owner][spender];

    }


    

    function approve(address spender, uint256 amount) public virtual override returns (bool) {

        address owner = _msgSender();

        _approve(owner, spender, amount);

        return true;

    }


    

    function _afterTokenTransfer(address from, address to, uint256 amount) internal virtual {}

}