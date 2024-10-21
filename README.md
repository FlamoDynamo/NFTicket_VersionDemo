# NFTicket - Smart Contract for Event Management with NFT Integration

## Overview
NFTicket is a smart contract built on the Algorand blockchain that integrates NFT (Non-Fungible Token) management for events. This contract allows users to create, store, and manage events by associating each event with a unique NFT ID and setting an end timestamp for each event. The contract also supports stopping events once their designated time has passed.

## Features

### 1. **Contract Creation**
   - **Functionality:** When the contract is deployed, it initializes the `event_count` to `0`, which keeps track of the total number of events created through the contract.
   - **Purpose:** Ensures that the contract starts with a clean state and has the ability to track event creation.
   - **Log Output:** 
     - `"Creating contract, initializing event_count to 0"`

### 2. **Create Event**
   - **Functionality:** The contract allows the creator to create a new event by specifying the event's NFT ID and the end timestamp. Each event is assigned a unique ID based on the current `event_count`.
   - **Steps:**
     - Checks that the current number of events does not exceed the maximum allowed events (`MAX_EVENTS`).
     - Increments the `event_count` by 1.
     - Stores the provided **NFT ID** and **end timestamp** in the global state.
     - Initializes the `event_stopped` flag to `0` (event is active).
   - **Log Output:**
     - `"Handling create_event"`
     - `"Event count is within limit"`
     - `"Incremented event_count"`
     - `"Stored nft_id"`
     - `"Stored end_timestamp"`
     - `"Initialized event_stopped to 0"`

### 3. **Stop Event**
   - **Functionality:** Once an event's end time has passed, the creator can stop the event by specifying the event ID. The contract updates the event's state to indicate it has been stopped.
   - **Steps:**
     - Ensures the event ID is valid (i.e., the ID is less than or equal to the current `event_count`).
     - Verifies that the current timestamp is greater than or equal to the event's end time.
     - Updates the `event_stopped` state to `1` (event is stopped).
   - **Log Output:**
     - `"Handling stop_event"`
     - `"Event ID is valid"`
     - `"Event has reached its end time"`
     - `"Event has been stopped"`

### 4. **Logic Protection (Assertions)**
   - **Functionality:** The contract includes several key assertions to ensure the integrity of the event management process. If any condition fails, the transaction is rejected.
   - **Checks:**
     - The number of events does not exceed the maximum limit (`MAX_EVENTS`).
     - The event ID is valid when attempting to stop an event.
     - The event end time has passed before the event can be stopped.
   - **Purpose:** These checks prevent invalid operations and ensure that all data remains consistent and correct throughout the lifecycle of the contract.

### 5. **Transaction Logging**
   - **Functionality:** Logs are generated at critical points in the contract's execution, helping users and developers trace the execution flow and debug if necessary.
   - **Purpose:** Provides transparency into the contract's operations and helps monitor the contract's behavior during transactions.

### 6. **Application JSON Spec (ARC-4 Compliant)**
   - **Functionality:** The project generates an `application.json` file compliant with the **ARC-4** standard. This file contains details about the smart contract, including supported methods (`create_event`, `stop_event`), global state schema, and descriptions of the available functions.
   - **Purpose:** Ensures that the smart contract can be easily integrated with tools like **Algokit** or other Algorand-compatible platforms.

## How to Use

1. **Contract Creation:**
   Deploy the contract on the Algorand blockchain. The contract will initialize with an event count of `0`.

2. **Create Event:**
   Call the `create_event` method with the following parameters:
   - `nft_id`: The NFT ID associated with the event.
   - `end_timestamp`: The timestamp when the event will end.

   The contract will store the event details and track the number of events.

3. **Stop Event:**
   Once the event has ended (as determined by the `end_timestamp`), call the `stop_event` method with the `event_id` to stop the event. The contract will validate the time and update the event's state accordingly.

## Global State Variables

- **event_count**: Tracks the number of events created.
- **event_x_nft_id**: Stores the NFT ID for each event `x`.
- **event_end_x**: Stores the end timestamp for event `x`.
- **event_stopped_x**: Indicates whether event `x` has been stopped (`1` if stopped, `0` if active).

## Methods

- **create_event(uint64 nft_id, uint64 end_timestamp)**: Creates a new event with a specific NFT ID and end timestamp. Returns `1` on success, `0` on failure.
- **stop_event(uint64 event_id)**: Stops an event once its end timestamp has passed. Returns `1` on success, `0` on failure.

## Installation and Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/FlamoDynamo/NFTicket.git
   cd NFTicket


Welcome to your new AlgoKit project!

This is your workspace root. A `workspace` in AlgoKit is an orchestrated collection of standalone projects (backends, smart contracts, frontend apps and etc).

By default, `projects_root_path` parameter is set to `projects`. Which instructs AlgoKit CLI to create a new directory under `projects` directory when new project is instantiated via `algokit init` at the root of the workspace.

## Getting Started

To get started refer to `README.md` files in respective sub-projects in the `projects` directory.

To learn more about algokit, visit [documentation](https://github.com/algorandfoundation/algokit-cli/blob/main/docs/algokit.md).

### GitHub Codespaces

To get started execute:

1. `algokit generate devcontainer` - invoking this command from the root of this repository will create a `devcontainer.json` file with all the configuration needed to run this project in a GitHub codespace. [Run the repository inside a codespace](https://docs.github.com/en/codespaces/getting-started/quickstart) to get started.
2. `algokit init` - invoke this command inside a github codespace to launch an interactive wizard to guide you through the process of creating a new AlgoKit project

Powered by [Copier templates](https://copier.readthedocs.io/en/stable/).
