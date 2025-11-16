# dangb's Personal LangFlow Setup

This repository serves as a personal collection of custom components, flows, and configurations for my [LangFlow](https://langflow.org/) environment. It's a central place to manage and document the custom tools I build to extend LangFlow's capabilities.

## Table of Contents
- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [How to Use](#how-to-use)
- [Included Components](#included-components)
  - [SmtpToKindle](#smtptokindle)
- [Included Flows](#included-flows)
  - [Recipe Exporter for Kindle](#recipe-exporter-for-kindle)
- [Requirements](#requirements)

## Overview

This project contains a curated set of tools and workflows designed to integrate with LangFlow. While LangFlow provides a powerful base, its true potential is unlocked by creating custom components tailored to specific needs. This repository is the home for those components, ranging from utility helpers to complex integrations.

## Repository Structure

-   `/components`: Contains the source code for individual custom components that can be loaded into LangFlow.
-   `/flows`: Stores exported JSON files of useful flows that utilize the custom components.
-   `README.md`: This file, providing an overview of the repository and its contents.

## How to Use

The components and flows in this repository can be easily integrated into any LangFlow application.

1.  **Place Files**: Copy the component files (e.g., from `/components`) into the `components` directory of your LangFlow project. Place flow files (e.g., from `/flows`) in your project's `flows` directory.
2.  **Restart LangFlow**: If LangFlow is already running, restart it to ensure it discovers the new items.
3.  **Find and Use**: In the LangFlow UI, search for the component or flow by its name. Drag it onto the canvas and configure its inputs as needed.

## Included Components

Below is a list of the custom components currently available in this repository.

### SmtpToKindle

This component converts HTML content into a properly formatted `.epub` file and emails it as an attachment using a specified SMTP server. It's designed for sending articles and documents to e-reader devices.

**Inputs:**
- **Author/Title**: Metadata for the EPUB file.
- **Content (HTML)**: The main document content in HTML format.
- **Email Configuration**: Sender email, app password, and Kindle/recipient email.
- **SMTP Configuration**: SMTP server address and port.

**Output:**
- **Status Message**: A message indicating the success or failure of the operation.

## Included Flows

### Recipe Exporter for Kindle

This is an advanced, agent-based flow designed to streamline the process of saving online recipes to a Kindle.

**Workflow:**
1.  **User Input**: The flow starts with a **Chat Input**, where the user provides a URL to a recipe, or pastes the recipe.
2.  **Agent Control**: A central **Agent** component orchestrates the entire task. It is given a detailed set of instructions on how to behave.
3.  **Content Fetching**: The agent uses the built-in **URL Component** as a tool to download the HTML content from the provided link.
4.  **Information Extraction & Formatting**: The agent processes the HTML to find and extract the core parts of the recipe (title, author, ingredients, steps), intelligently filtering out ads and backstories.
5.  **Calorie Estimation**: If the recipe is missing calorie information, the agent is instructed to use the **Wikidata Component** as a tool to look up ingredients and provide a calorie estimate.
6.  **User Review**: Before finalizing, the agent presents the cleaned and formatted recipe to the user for review. At this point the user can ask the agent to modify different aspects.
7.  **EPUB Creation & Sending**: Once approved, the agent passes the final HTML to the **SmtpToKindle** component, which creates the `.epub` file and emails it to the pre-configured Kindle address.

**How to Use:**
- Load the flow in LangFlow.
- Ensure the `SmtpToKindle` component has your correct email and SMTP credentials configured.
- Interact with the chat interface, providing it with URLs to recipes you want to export.

## Requirements

Individual components may have their own Python package dependencies. These will be noted in their respective sections.

-   **SmtpToKindle requires:**
    ```bash
    pip install EbookLib
    ```
