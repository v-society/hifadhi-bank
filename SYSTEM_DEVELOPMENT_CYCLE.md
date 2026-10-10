# Hifadhi Bank System Development Cycle Documentation

## 1. Project Overview

Hifadhi Bank is a banking system prototype that combines a banking backend, ATM simulation interface, and teller-style CLI workflows. The project demonstrates how a bank account can be created, authenticated with a card number and PIN, checked for balance, and used to perform deposits and withdrawals through an ATM-like experience.

The system is currently implemented as a prototype using:

- Python with FastAPI for the backend API
- JSON as the in-memory/persistent storage model
- HTML, CSS, and JavaScript for the ATM front-end
- CLI console flows for teller and banking operations

This document captures the system development cycle up to the system design stage.

## 2. Problem Statement

The project addresses the need for a simple, educational banking application that can:

- validate an ATM card number
- authenticate a user with a PIN
- show the current account balance
- process deposits and withdrawals
- produce a transaction experience similar to a real ATM interface

The system is designed as a learning-oriented demonstration of a mini digital banking platform rather than a full production-grade financial system.

## 3. Objectives of the System

The main objectives are:

1. Provide secure card and PIN-based authentication.
2. Model account creation and account lookup.
3. Support ATM-style transaction flows.
4. Keep the application simple and easy to understand.
5. Show a practical software development cycle from requirement analysis to system design.

## 4. Scope of the Project

### In Scope

- User account creation
- Account number and card number generation
- PIN hashing for secure storage
- Card validation at ATM entry
- Authentication via API endpoint
- Deposit transaction processing
- Withdrawal transaction processing
- Balance inquiry
- ATM front-end simulation
- Teller console interactions

### Out of Scope

- Real database integration (PostgreSQL/MySQL)
- Multi-user banking permissions
- Real payment gateways
- Role-based banking administration
- Audit logging for regulatory compliance
- Encryption of data at rest and in transit
- Online banking dashboard
- Advanced fraud detection and monitoring
- Transaction reversal and history reports

## 5. System Development Life Cycle (SDLC) Overview

This project follows the standard software development life cycle phases:

1. Planning and feasibility analysis
2. Requirement gathering
3. Analysis and modeling
4. System design
5. Implementation
6. Testing and validation
7. Deployment
8. Maintenance and enhancement

This documentation covers the project up to the system design stage.

## 6. Phase 1: Planning and Feasibility

### 6.1 Project Vision

The project intends to model a simplified version of a digital banking environment for learning and demonstration. It teaches how a banking system can be decomposed into front-end interaction, API services, validation logic, and data storage.

### 6.2 Feasibility Assessment

#### Technical Feasibility

The system is technically feasible because:

- Python is suitable for backend API development.
- FastAPI provides rapid API creation.
- JSON files can store a limited number of users for a prototype.
- HTML and JavaScript are enough to simulate ATM behavior.

#### Economic Feasibility

The system is economically feasible because:

- it uses open-source tools
- it requires no expensive enterprise infrastructure
- it is ideal for educational and prototype-level deployment

#### Operational Feasibility

The system is operationally feasible because:

- users can interact with a simple interface
- the flow is easy to test manually
- requirements are easy to understand and modify

## 7. Phase 2: Requirements Gathering

### 7.1 Functional Requirements

The system must support the following:

- A user should be able to create an account with name and email.
- The system should assign an account number and card number automatically.
- The system should securely hash and store the PIN.
- A user should be able to authenticate using card number and PIN.
- A user should be able to check their balance.
- A user should be able to deposit funds.
- A user should be able to withdraw funds if sufficient balance exists.
- The ATM interface should validate card input before authorization.
- The system should reject invalid amounts and invalid account access.

### 7.2 Non-Functional Requirements

- Security: PINs must not be stored in plain text.
- Reliability: transactions should only succeed under valid conditions.
- Usability: ATM screen should guide user actions clearly.
- Maintainability: code should be modular by route, user logic, and utility functions.
- Performance: the system should respond quickly for a prototype workload.

## 8. Phase 3: Analysis and Modeling

### 8.1 Actors

- Customer: creates account and interacts with ATM.
- Teller: manages account creation and account operations in CLI mode.
- Banking API: handles authentication and transaction processing.
- Storage layer: keeps account data in JSON.

### 8.2 Use Cases

1. Create account
2. Insert card
3. Enter PIN
4. View balance
5. Deposit cash
6. Withdraw cash
7. Eject card
8. Logout

### 8.3 Process Flows

#### Account Creation Flow

1. User provides name and email.
2. System generates account number and card number.
3. System stores hashed PIN.
4. System saves new user in JSON storage.
5. System returns account details to user.

#### Authentication Flow

1. User enters card number at ATM.
2. API validates the card number.
3. User enters PIN.
4. System hashes the entered PIN.
5. System matches the result against stored PIN.
6. Authentication succeeds or fails.

#### Transaction Flow

1. User confirms a deposit or withdrawal.
2. API validates amount and account.
3. System checks funds if withdrawal is requested.
4. System updates the account balance.
5. API returns success/failure and updated balance.

## 9. System Design

### 9.1 Architectural Style

The project follows a layered architecture that separates responsibilities into distinct modules:

- Presentation layer: ATM front-end interface
- API layer: FastAPI endpoints
- Business logic layer: account authentication and transaction rules
- Data access layer: JSON file storage and user model management

This architecture is simple and suitable for an educational prototype.

### 9.2 High-Level Architecture

The overall system can be visualized as:

Customer / ATM Front-End
        |
        v
HTTP requests to FastAPI API
        |
        v
Authentication and transaction logic
        |
        v
User model and JSON data storage

### 9.3 Components

#### 9.3.1 ATM Front-End

Location: `atm machine/frontend/`

Responsibilities:

- collect card number input
- validate card existence
- prompt for PIN
- display menu options
- send requests to backend API
- show balance and transaction results

Technologies used:

- HTML for layout
- CSS for ATM styling
- JavaScript for interaction and API calls

#### 9.3.2 Banking Backend

Location: `banking system/backend/`

Responsibilities:

- expose endpoints for card validation and authentication
- check account balance
- process deposit and withdrawal requests
- validate transaction inputs
- return success/failure responses in JSON

Key files:

- `main.py`: application entry point and route definitions
- `auth.py`: card validation and user lookup logic
- `routes/user.py`: user creation, loading, and authentication
- `routes/client.py`: deposit and withdrawal operations
- `routes/teller.py`: teller-side bank balance bookkeeping

#### 9.3.3 Data Layer

Location: `banking system/backend/data/users.json`

Responsibilities:

- store accounts in JSON format
- keep user records such as:
  - user_id
  - name
  - email
  - account_number
  - card_number
  - set_pin
  - balance

### 9.4 Core Data Model

A user record is represented conceptually as:

```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "account_number": 1234,
  "card_number": 456789,
  "set_pin": "hashed_pin_value",
  "balance": 5000.0
}
```

### 9.5 Main Functional Modules

#### User Management Module

- create new user
- generate account number
- generate card number
- store hashed PIN
- load users from JSON
- authenticate user

#### Transaction Management Module

- validate amount
- verify account exists
- handle deposit logic
- handle withdrawal logic
- check balance

#### ATM Interaction Module

- card submission
- PIN entry
- menu selection
- transaction request submission
- result display

### 9.6 API Design

The backend exposes the following major endpoints:

- `GET /` — returns service status
- `POST /card-number` — validates card number
- `POST /authenticate` — authenticates card and PIN
- `POST /balance` — returns account balance
- `POST /transactions/{transaction_type}` — handles deposit or withdrawal requests

Example request body for authentication:

```json
{
  "card_number": "123456",
  "pin": "1234"
}
```

Example response:

```json
{
  "authenticated": true,
  "name": "John Doe"
}
```

### 9.7 System Interaction Flow

#### ATM Card Validation Sequence

1. User enters card number on ATM interface.
2. Front-end sends POST request to `/card-number`.
3. Backend checks if card number is valid and registered.
4. Response is returned as accepted or rejected.

#### ATM Authentication Sequence

1. User enters PIN after card is accepted.
2. Front-end sends POST to `/authenticate`.
3. Backend hashes entered PIN and matches it with stored value.
4. Backend returns authentication status and account name.

#### Balance Inquiry Sequence

1. User selects balance option.
2. Front-end sends card number and PIN to `/balance`.
3. Backend validates credentials.
4. Backend returns current balance.

#### Withdrawal or Deposit Sequence

1. User enters amount.
2. Front-end sends request to `/transactions/withdraw` or `/transactions/deposit`.
3. Backend validates the amount and account.
4. If successful, account balance is updated and returned.

### 9.8 Security Design Considerations

The current prototype includes a basic security layer:

- PIN is hashed using SHA-256 before storage.
- Authentication compares hashed values rather than raw PIN values.
- Card numbers are validated before account lookup.

Important note: this is still a prototype and not production-grade security. For a real banking system, the following would be required:

- secure password hashing with stronger cryptographic standards
- encrypted data storage and secure transport protocols
- session management and token-based authentication
- rate limiting and brute-force protection
- audit trails and transaction logging
- PCI/DSS-level safeguards

### 9.9 Design Constraints

The system currently operates under the following constraints:

- local JSON storage instead of a database
- no real banking compliance layer
- no distributed architecture
- no multi-channel support beyond ATM and CLI
- simplified transaction logic focused on learning outcomes

## 10. System Design Summary

The project is designed as a modular banking prototype with clear separation between:

- user interface
- API services
- business rules
- storage logic

This separation makes the system easy to understand, extend, and test. It provides a solid foundation for implementation, testing, and later expansion into a fuller digital banking platform.

## 11. Recommended Next Development Phases

The next logical phases after this design stage are:

1. Implementation of the approved design modules
2. Unit testing of account and transaction logic
3. Integration testing between ATM UI and backend API
4. Security hardening and validation
5. Deployment preparation and environment setup
6. Maintenance and feature enhancement

## 12. Conclusion

This document establishes the system development cycle for the Hifadhi Bank project up to the system design phase. It defines the problem, requirements, architecture, modules, workflows, and the overall system blueprint needed before coding begins in a structured manner.

The project demonstrates a practical SDLC approach for a small-scale banking system and provides a clear base for future implementation and expansion.
