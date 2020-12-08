# Fortress Live Security Audit Engine

Fortress Live Security Audit runs a real-time security audit on deployed smart contracts of DeFi app when a threat pattern gets detected by Fortress Threat Detection and Response Engine. Security Audit consists of checking vulnerabilities of smart contracts and logic errors related to past security incidents of DeFi apps. The engine is built on [Slither](https://github.com/crytic/slither). Requires [Solc-select](https://github.com/crytic/solc-select/) to quickly switch between Solidity compiler versions.

## How to install

Fortress requires Python 3.6+ and [solc](https://github.com/ethereum/solidity/), the Solidity compiler.

### Prequisites

- [Python virtual environment](https://docs.conda.io/en/latest/miniconda.html)
- [Solidity Compiler](https://docs.soliditylang.org/en/v0.7.4/installing-solidity.html)
- [Solc Select](https://github.com/crytic/solc-select/)

### Install

```bash
git clone https://github.com/crytic/fortress.git && cd fortress
python3 setup.py install (make sure Solc Select is installed)
```

## Manually run security audit to a contract hosted on Etherscan

fortress 0x7F37f78cBD74481E593F9C737776F7113d76B315

## Live run security audit  to a contract of DeFi app

Fortress Threat Detection and Response mechanism runs the engine live. Read README on Threat Detection and Response Engine(https://github.com/fortressfoundation/fortress-tdr-engine) repo for details.

## Detectors

Num | Detector | What it Detects | Impact | Confidence
--- | --- | --- | --- | ---
1 | `name-reused` | Contract's name reused  | High | High
2 | `rtlo` | Right-To-Left-Override control character is used  | High | High
3 | `shadowing-state` | State variables shadowing  | High | High
4 | `suicidal` | Functions allowing anyone to destruct the contract  | High | High
5 | `uninitialized-state` | Uninitialized state variables | High | High
6 | `uninitialized-storage` | Uninitialized storage variables | High | High
7 | `arbitrary-send` | Functions that send ether to arbitrary destinations  | High | Medium
8 | `controlled-delegatecall` | Controlled delegatecall destination  | High | Medium
9 | `reentrancy-eth` | Reentrancy vulnerabilities (theft of ethers)  | High | Medium
10 | `erc20-interface` | Incorrect ERC20 interfaces  | Medium | High
11 | `erc721-interface` | Incorrect ERC721 interfaces   | Medium | High
12 | `incorrect-equality` | Dangerous strict equalities  | Medium | High
13 | `locked-ether` | Contracts that lock ether  | Medium | High
14 | `shadowing-abstract` | State variables shadowing from abstract contracts  | Medium | High
15 | `tautology` | Tautology or contradiction  | Medium | High
16 | `boolean-cst` | Misuse of Boolean constant | Medium | Medium
17 | `constant-function-asm` | Constant functions using assembly code | Medium | Medium
18 | `constant-function-state` | Constant functions changing the state | Medium | Medium
19 | `divide-before-multiply` | Imprecise arithmetic operations order   | Medium | Medium
20 | `reentrancy-no-eth` | Reentrancy vulnerabilities (no theft of ethers) | Medium | Medium
21 | `tx-origin` | Dangerous usage of `tx.origin` | Medium | Medium
22 | `unchecked-lowlevel` | Unchecked low-level calls | Medium | Medium
23 | `unchecked-send` | Unchecked send | Medium | Medium
24 | `uninitialized-local` | Uninitialized local variables  | Medium | Medium
25 | `unused-return` | Unused return values | Medium | Medium
26 | `shadowing-builtin` | Built-in symbol shadowing   | Low | High
27 | `shadowing-local` | Local variables shadowing  | Low | High
28 | `void-cst` | Constructor called not implemented  | Low | High
29 | `calls-loop` | Multiple calls in a loop | Low | Medium
30 | `reentrancy-benign` | Benign reentrancy vulnerabilities | Low | Medium
31 | `reentrancy-events` | Reentrancy vulnerabilities leading to out-of-order Events  | Low | Medium
32 | `timestamp` | Dangerous usage of `block.timestamp`  | Low | Medium
33 | `assembly` | Assembly usage  | Informational | High
34 | `boolean-equal` | Comparison to boolean constant  | Informational | High
35 | `deprecated-standards` | Deprecated Solidity Standards  | Informational | High
36 | `erc20-indexed` | Un-indexed ERC20 event parameters  | Informational | High
37 | `low-level-calls` | Low level calls low-level-calls | Informational | High
38 | `naming-convention` | Conformance to Solidity naming conventions  | Informational | High
39 | `pragma` | If different pragma directives are used  | Informational | High
40 | `solc-version` | Incorrect Solidity version | Informational | High
41 | `unused-state` | Unused state variables | Informational | High
42 | `reentrancy-unlimited-gas` | Reentrancy vulnerabilities through send and transfer  | Informational | Medium
43 | `too-many-digits` | Conformance to numeric notation best practices  | Informational | Medium
44 | `constable-states` | State variables that could be declared constant | Optimization | High
45 | `external-function` | Public function that could be declared as external | Optimization | High
40 | `solc-version` | Incorrect Solidity version | Informational | High
41 | `unused-state` | Unused state variables | Informational | High
42 | `reentrancy-unlimited-gas` | Reentrancy vulnerabilities through send and transfer  | Informational | Medium
43 | `too-many-digits` | Conformance to numeric notation best practices  | Informational | Medium
44 | `constable-states` | State variables that could be declared constant | Optimization | High
45 | `external-function` | Public function that could be declared as external | Optimization | High


NOTE: This is Pre-Alpha Release. Development for stable alpha release is being done and this may work unstable at the moment.

