---
actionability: high
attached_experts: []
channel_name: ''
created_at: '2026-05-28T10:22:10.495693+10:00'
domain: unknown
expert_status: unattached
primary_mode: router
privacy: public
review_status: new
secondary_modes: []
source_type: article
source_url: https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0
status: processed
suggested_experts: []
tags: []
title: Building Personalized Agents with ADK, MCP, and Memory Bank  |  Google Codelabs
transcript_path: ''
type: insight_note
updated_at: '2026-05-28T10:22:10.495693+10:00'
---

# Building Personalized Agents with ADK, MCP, and Memory Bank  |  Google Codelabs

## Summary
AI summarization succeeded, but JSON parsing failed.

## AI Raw Output
```text
Final synthesis failed.
```

## Key Ideas
- Refer to the AI Raw Output above.

## Why this matters for Markus
- Refer to the AI Raw Output above.

## Related Modes
- router

## AI Generation Data
- Provider: Unknown
- Model: Unknown

## Next Action
- [ ] Review raw AI output and extract action items manually.

## Source Reliability
AI summarization was performed but parsing failed.

## Original Content
### Raw User Input
https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0

### Fetched Web Text
Title: Building Personalized Agents with ADK, MCP, and Memory Bank  |  Google Codelabs

URL Source: https://codelabs.developers.google.com/codelabs/christmas-card/instructions

Markdown Content:
[Skip to main content](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#main-content)
*   On this page
*   [Introduction](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0)
*   [The Modern Agent Stack](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#the-modern-agent-stack)
*   [Core Concepts](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#core-concepts)
*   [What You Will Build](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#what-you-will-build)
*   [Set Up](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#1)
*   [Part One: Enable Billing Account](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#part-one:-enable-billing-account)
*   [Part Two: Open Environment](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#part-two:-open-environment)
*   [Part Three: Setting up permission](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#part-three:-setting-up-permission)
*   [Powering Up with MCP](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#2)
*   [The "USB-C" Moment for AI](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#the-usb-c-moment-for-ai)
*   [What You Will Build](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#what-you-will-build_1)
*   [Building the Server Logic](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#building-the-server-logic)
*   [Environment Setup](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#environment-setup)
*   [Testing with Gemini CLI for MCP Server](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#3)
*   [Conclusion & Next Steps](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#conclusion-next-steps)
*   [Vibe-Coding an ADK Agent](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#4)
*   [What is an Agent?](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#what-is-an-agent)
*   [What is ADK?](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#what-is-adk)
*   [Context-Based Vibe-Coding](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#context-based-vibe-coding)
*   [Run the Agent Web Interface](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#5)
*   [Test the Agent](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#test-the-agent)
*   [Conclusion & Next Steps](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#conclusion-next-steps_1)
*   [Connecting ADK with UI](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#6)
*   [Implementation](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#implementation)
*   [Deep Dive: Architecture & Deployment](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#deep-dive:-architecture-deployment)
*   [Try the application with the agent magic](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#7)
*   [Vertex AI Memory Bank](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#8)
*   [Short-term vs. Long-term Memory](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#short-term-vs.-long-term-memory)
*   [Sessions vs. Memory Bank](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#sessions-vs.-memory-bank)
*   [Memory Bank In Action](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#9)
*   [Conclusion](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#10)
*   [Summary](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#summary)
*   [Next Steps](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#next-steps)

1.   [Introduction](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0)
2.   [Set Up](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#1)
3.   [Powering Up with MCP](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#2)
4.   [Testing with Gemini CLI for MCP Server](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#3)
5.   [Vibe-Coding an ADK Agent](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#4)
6.   [Run the Agent Web Interface](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#5)
7.   [Connecting ADK with UI](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#6)
8.   [Try the application with the agent magic](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#7)
9.   [Vertex AI Memory Bank](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#8)
10.   [Memory Bank In Action](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#9)
11.   [Conclusion](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#10)

Building Personalized Agents with ADK, MCP, and Memory Bank

## About this codelab

_subject_ Last updated Apr 16, 2026

## [1. Introduction](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0)

## The Modern Agent Stack

Building a production-grade AI agent requires more than just a large language model (LLM). While an LLM provides the reasoning capabilities, a robust agent needs to interact with the outside world, manage conversation state, and remember user preferences over time.

![Image 1: demo1](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/demo_01.png)![Image 2: demo2](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/demo_02.png)

In this workshop, you will learn how to architect and build a comprehensive agentic system using three foundational technologies:

1.   **Connectivity (MCP)**: To give your agent access to local tools and data.
2.   **Orchestration (ADK)**: To manage the agent's reasoning loop and state.
3.   **Memory (Memory Bank)**: To provide long-term, personalized context.

![Image 3: workshop_overview](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/diagram_memory.png)

## Core Concepts

Component Function
**Model Context Protocol (MCP)**A universal standard that connects AI models to external systems (databases, filesystems, APIs) without custom integrations.
**Agent Development Kit (ADK)**A framework that provides the runtime environment for agents, managing the event loop, state transitions, and tool execution.
**Session Service**Handles **short-term memory**. It preserves the immediate conversation context (e.g., "What did the user just ask?") but is cleared when the session ends.
**Vertex AI Memory Bank**Handles **long-term memory**. It persists user-specific facts and preferences (e.g., "User prefers Python") indefinitely, allowing the agent to personalize future interactions.
**Vertex AI Agent Engine**The managed infrastructure service that hosts your agent logic and memory components at scale.

## What You Will Build

To demonstrate these concepts, you will build a **Holiday Design Assistant**. This agent will be capable of taking high-level user requests and autonomously orchestrating local Python tools to generate personalized code and images.

You will progress through three stages:

1.   **Tooling Layer**: Create an MCP server to expose local Python functions to the AI.
2.   **Agent Layer**: Use ADK to build an agent that plans and executes multi-step workflows.
3.   **Memory Layer**: Integrate Memory Bank to enable the agent to learn and remember user style preferences.

## [2. Set Up](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#1)

To power our AI agents, we need two things: a Google Cloud Project to provide the foundation.

## Part One: Enable Billing Account

To run this codelab, you need a billing account with some credit. Use the credits from the banner at the top of this codelab to get started. If you are already connected to a billing account, you can skip this step.

## Part Two: Open Environment

1.   👉 Click this link to navigate directly to [Cloud Shell Editor](https://ide.cloud.google.com/)
2.   👉 If prompted to authorize at any point today, click **Authorize** to continue. ![Image 4: Click to authorize Cloud Shell](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/authorize-cloud-shell.png)
3.   👉 If the terminal doesn't appear at the bottom of the screen, open it:
    *   Click **View**
    *   Click **Terminal**![Image 5: Open new terminal in Cloud Shell Editor](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/open-new-terminal.png)

4.   👉💻 In the terminal, verify that you're already authenticated and that the project is set to your project ID using the following command:`gcloud auth list`
5.   👉💻 Clone the bootstrap project from GitHub:`git clone https://github.com/cuppibla/holiday_workshop`
6.   👉💻 Run the setup script from the project directory.`cd ~/holiday_workshop./init.sh` The script will handle the rest of the setup process automatically.
7.   👉💻 Set the Project ID needed:`gcloud config set project $(cat ~/project_id.txt) --quiet`

## Part Three: Setting up permission

1.   👉💻 Enable the required APIs using the following command. This could take a few minutes.`gcloud services enable \    cloudresourcemanager.googleapis.com \    servicenetworking.googleapis.com \    run.googleapis.com \    aiplatform.googleapis.com \    compute.googleapis.com`
2.   👉💻 Grant the necessary permissions by running the following commands in the terminal:`. ~/holiday_workshop/set_env.sh`

Notice that a `.env` file is created for you. That shows your project information.

## [3. Powering Up with MCP](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#2)

## The "USB-C" Moment for AI

Imagine if every time you bought a new mouse, you had to solder it to your motherboard. That was the state of AI tools until recently. Developers had to write custom "glue code" to connect LLMs to databases, filesystems, or APIs.

Enter the **Model Context Protocol (MCP)**. Think of MCP as the **USB-C port for AI applications**. It provides a standardized way to connect AI models to data sources and tools.

If you build an MCP server for your tools _once_, you can plug it into Gemini CLI, an IDE, or any other MCP-compliant client without changing a single line of code.

## What You Will Build

![Image 6: mcp_server](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/mcp_server.png)

In this codelab, you will build a **Holiday Design Assistant** that:

1.   **Connects to your local environment** (studio tools) using **MCP**.
2.   **Manages conversation context** reliably using the **Agent Development Kit (ADK)**.
3.   **Remembers your preferences** (e.g., "I prefer Python code") across different sessions using **Vertex AI Memory Bank**.

## Building the Server Logic

We have prepared the environment, but the server logic is incomplete. We need to implement the four specific tools that our Agent will eventually use to build our holiday card.

### Part One: Open the Server Skeleton

We will be working in the `01-MCP-Files-Testing/01-starter` directory.

1.   In your Cloud Shell terminal, make sure you are in the correct directory:`cd ~/holiday_workshop/01-MCP-Files-Testing/01-starter/`
2.   Open the file in the Cloud Shell Editor by running:`cloudshell edit ~/holiday_workshop/01-MCP-Files-Testing/01-starter/mcp_server.py`

You will notice the boilerplate code (setting up the MCP server, handling connections, and initializing the Vertex AI client) is already done. However, the four core functions are currently empty placeholders.

### Part Two: Implement the Holiday Scene Generator

First, we need a tool that takes a user's interest (e.g., "birds") and turns it into a rich, detailed prompt optimized for image generation.

Locate the comment `#REPLACE_GENERATE_HOLIDAY_SCENE` inside the `generate_holiday_scene` function.

**Replace this whole line** with the following code:

`prompt = (        f"""        Create a cozy, high-fidelity 3D render of a winter holiday scene.        The scene should be warm and inviting with soft cinematic lighting.                Seamlessly integrate the following specific theme/interest into the         holiday decor or landscape: {interest}.                The style should be whimsical but detailed.        Aspect Ratio: 16:9 Landscape.        """    )    generate_image(prompt, "16:9", "static/generated_scene.png")    return "Done! Saved at generated_scene.png"`
### Part Three: Implement the Final Photo Result

Finally, we want to ensure the lighting and style look photorealistic and festive.

Locate the comment `#REPLACE_GENERATE_FINAL_PHOTO`.

**Replace this whole line** with the following code to perform the final style transfer and rendering:

`prompt = (        """        Generate a photorealistic close-up shot of a rustic wooden fireplace mantle.                Lighting: Warm, glowing ambient light from a fire below (out of frame).        Background: Softly blurred (bokeh) pine garland and twinkling lights.                Foreground Composition:        1. A wooden picture frame containing the [attached selfie image].            The face in the photo must be clearly visible.        2. A folded holiday greeting card standing upright next to the frame.            The front of the card displays the [attached holiday scene image] as a print.                   Ensure the perspective is grounded and realistic, as if taken with a 50mm lens.        """    )    generate_image(prompt, "16:9", "static/generated_final_photo.png", ["static/generated_selfie.png", "static/generated_scene.png"])    return "Done! Saved at generated_final_photo.png"`
## Environment Setup

Now that the code is in place, we need to ensure our dependencies are installed. We will use `uv`, a fast Python package and project manager.

👉💻 In your **terminal**, run the following to add FastMCP as a dependency of our project:

`cd ~/holiday_workshop/01-MCP-Files-Testing/01-starter/uv add fastmcp`
You will see a new dependency `fastmcp>=2.13.3` is added to your `~/holiday_workshop/01-MCP-Files-Testing/01-starter/pyproject.toml` file.

## [4. Testing with Gemini CLI for MCP Server](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#3)

Now that our server code is complete, how do we test it?

Usually, testing a backend server requires building a frontend UI or writing complex `curl` requests. However, here we can use the **Gemini CLI**.

This is incredibly useful for development because it isolates the logic. You can verify that the model understands your tools and calls them correctly _before_ you ever worry about building a web interface or an agent framework.

![Image 7](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/gemini_cli.png)

### Connect and Run

We will tell Gemini CLI to manage our server using the `mcp add` command.

In your terminal, run:

`gemini mcp add holidays uv run ~/holiday_workshop/01-MCP-Files-Testing/01-starter/mcp_server.py`
*   **`add holidays`**: We gave our server a nickname ("holidays").
*   **`uv run ...`**: We provided the explicit command to start the Python server we just modified.

### Let's Make Magic!

Now, start the chat session:

`gemini`
Try the following prompt to test if Gemini can "see" your new tools. Note that you may need to allow Gemini CLI the use of our holidays tool.

*   👉 **User:**`"I want to create a festive holiday photo. I like birds a lot."`
*   **Gemini:**`*Thinking...**Calling tool: generate_holiday_scene(interest='birds')*Done! Saved at generated_scene.png`
*   👉 **User:**`"Great! Now generate a knitting pattern for a sweater with reindeer on it."`
*   **Gemini:**`*Thinking...**Calling tool: generate_sweater_pattern(motif='reindeer')*Done! Saved at generated_pattern.png` Because you used MCP, the AI understood exactly which Python function to call to satisfy your request!![Image 8](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/gemini_cli_done.png)

### Review the Picture

*   End the Gemini CLI by pressing **`Control+C`**.
*   Check the generated picture in your folder: `~/holiday_workshop/01-MCP-Files-Testing/01-starter/static`.

Review your photo here: ![Image 9](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/generated_pic.png)

## Conclusion & Next Steps

Congratulations! You have successfully built a working MCP server. You now have a functional set of "AI tools" that can generate patterns, composite images, and refine scenes.

However, did you notice something in the test above? **You** had to drive the process. You had to ask for the scene, _then_ ask for the pattern, _then_ ask to combine them.

While Gemini is smart, for a complex production workflow—where we need to generate a pattern _before_ we can put it on a sweater, and handle errors if the image generation fails—we want more control. We want a dedicated system that can plan, critique its own work, and manage the state of our holiday card without us holding its hand every step of the way.

In the next section, we will bring order to this creative chaos. We are going to implement the **Agent Development Kit (ADK)** to build a structured Agent that orchestrates these MCP tools into a perfect production pipeline.

## [5. Vibe-Coding an ADK Agent](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#4)

We have a working set of tools (our MCP server), but currently, we are the ones doing all the heavy lifting—telling Gemini exactly which tool to call and when.

In this section, we will build an **AI agent**: a system that can reason, plan, and execute multi-step tasks autonomously. To do this, we will use the **Agent Development Kit (ADK)**.

![Image 10: agent_mcp](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/agent_mcp_1.png)

## What is an Agent?

If the MCP tools are the "hands" (doing the work), the **Agent** is the "brain." An agent uses an LLM to understand a user's intent ("Make me a holiday card"), breaks it down into steps ("First I need a scene, then a pattern..."), and decides which tools to use to achieve the goal.

## What is ADK?

The **Agent Development Kit (ADK)** is a framework from Google that makes building these agents easy. It handles the complex "plumbing", like managing chat history, connecting to tools, and switching between different models—so you can focus on the personality and logic of your app.

## Context-Based Vibe-Coding

It's a common pattern to use a single, massive prompt to generate code. However, when building complex applications, it is often better to treat the AI as a partner that maintains **context** over time.

We will use Gemini CLI's **Memory** features to set the stage before we write a single line of code.

### 1. Prepare the Environment

Open your terminal and navigate to the starter directory:

`cd ~/holiday_workshop/02-Vibe-Coding-ADK-Agent/01-starter`
Start Gemini CLI:

`gemini`
### 2. Managing Context and Memory

When vibe-coding, the AI needs to know _who_ it is and _what_ it knows. Gemini CLI allows us to manage this explicitly.

*   **`/memory show`**: Type this to see what the AI currently knows about your project and session.
*   **`/memory add`**: Use this to inject foundational knowledge that the AI should remember throughout the conversation.

Let's start by defining our coding partner's persona. Run the following command inside Gemini CLI:

`/memory add "You are an expert Python developer specialized in the Google Agent Development Kit (ADK). You write clean, modular code and prefer using the latest ADK patterns."`
Gemini now understands its role. This context will influence every subsequent response, ensuring high-quality ADK-compliant code.

### 3. Step 1: Vibe-Coding the Basic Agent

Instead of trying to generate the whole system at once, let's start with the skeleton. We want to establish the file structure and the basic agent personality.

**Enter the following prompt into Gemini CLI:**

`Let's start by building the basic agent structure. Please create a file structure for a `root_agent`. 1. Create `root_agent/__init__.py` that imports `agent`.2. Create `root_agent/agent.py` by following exactly how this file is doing import and agent creation @~/holiday_workshop/02-Vibe-Coding-ADK-Agent/01-starter/agent_reference.pyIn `agent.py`:- Create an `Agent` named "root_agent" using the model "gemini-2.5-flash".- The instruction string should define a "Holiday Magic Assistant". - The personality should be enthusiastic (`🎄✨`) and prefer "cute, kawaii, cartoon" styles for any visual tasks.`
Gemini will generate the file structure and the initial Python code. Review it to ensure it looks correct, then apply/accept the changes.

### 4. Step 2: Adding the MCP Server (The Tools)

Now that we have a basic agent, we need to give it "hands." We need to connect the agent to the MCP server we built in the previous lab.

**Enter the following prompt into Gemini CLI:**

`Now, let's give the agent access to tools. Update `agent.py` to include our local MCP server. By following exactly how this agent is connecting to mcp tool @~/holiday_workshop/02-Vibe-Coding-ADK-Agent/01-starter/agent_reference.pyIn `agent.py`:- Import `McpToolset` to define our STDIO MCP server. as @~/holiday_workshop/02-Vibe-Coding-ADK-Agent/01-starter/agent_reference.py- Connect to the python file located at `../mcp_server.py` relative to agent.py.`
Gemini will now refactor your existing `agent.py` to include the tool definitions and connection logic.

**Note:** If you want to check your work or if the generated code isn't working as expected, you can compare your files against the reference solution located in: `~/holiday_workshop/02-Vibe-Coding-ADK-Agent/solution`

## [6. Run the Agent Web Interface](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#5)

The ADK comes with a built-in testing interface called `adk web`. This spins up a lightweight chat UI so we can talk to our agent immediately.

1.   If you still have GeminiCLI open, press `control+C` to close it. Now in your terminal(this is in `solution` folder, you can go to `starter` to test your code by running `uv run adk web` in your `starter` folder), run:`cd ~/holiday_workshop/02-Vibe-Coding-ADK-Agent/02-solutionuv run adk web --port 8000`
2.   Cloud Shell will alert you that a service is running on port 8000. Click **"Web Preview"** ->**"Preview on port 8000"**.

## Test the Agent

You should now see a chat interface. Let's see if our Agent follows its new instructions and correctly accesses the MCP tools.

**Try these prompts:**

*   "Hi! Who are you?" 
    *   _(Expect a festive, enthusiastic response)._

*   "I need a background for my holiday card. Make it a snowy village." 
    *   _(The Agent should call_ _`generate\_holiday\_scene`_ _. Notice how it automatically applies the "cute/cartoon" style defined in the system instructions)._

*   "Generate a sweater pattern with little pizza slices on it." 
    *   _(The Agent should call_ _`generate\_sweater\_pattern`_ _)._

![Image 11](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/adk_ui.png)

You can view the image generated here:

![Image 12](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/06-01.png)

Press `Control+C` to exit if you finish testing.

## Conclusion & Next Steps

You have now successfully "Vibe-Coded" a Google ADK Agent using a context-aware approach!

*   **We established Context:** We used `/memory add` to define an expert persona.
*   **We built Iteratively:** We created the skeleton first, then added the tool connections.

The built-in ADK web preview is great for testing, but for our final product, we want a custom, branded experience. In the next section, we will integrate this Agent into a custom web frontend.

## [7. Connecting ADK with UI](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#6)

![Image 13: backend_architecture](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/backend_diagram.png)

Now that we have an Agent definition, we need to run it. This is where the **Runner** and **Session Service** come in.

## Implementation

1.   👉 Type the following in your command:`cloudshell edit ~/holiday_workshop/03-Connect-ADK-MCP-UI/01-starter/backend/main.py` This opens `~/holiday_workshop/03-Connect-ADK-MCP-UI/01-starter/backend/main.py` in your editor.
2.   Replace the `# TODO: Create Session Service` with the following:`from google.adk.sessions import InMemorySessionServicefrom google.adk.memory import InMemoryMemoryServicesession_service = InMemorySessionService()memory_service = InMemoryMemoryService()`
3.   Replace the `# TODO: Initialize Runner` with the following:`runner = Runner(    app_name="agents",    agent=christmas_agent,    session_service=session_service,    memory_service=memory_service,)`

1.   Review line 158 at this `~/holiday_workshop/03-Connect-ADK-MCP-UI/01-starter/backend/main.py`(**no action needed**): If you wonder how the application get the final response? Below is event loop that powered by runner:`async for event in runner.run_async(    user_id=user_id,    session_id=session_id,    new_message=content)`

## Deep Dive: Architecture & Deployment

We are using **FastAPI** to serve this agent.

*   **Why FastAPI?**: Agents are often I/O bound (waiting for LLMs). FastAPI's async nature handles this perfectly.
*   **Statelessness**: Notice our API endpoint is _stateless_. We don't save variables in global scope. We rely on `session_id` and the `SessionService` to reconstruct the state for every single request. This means you can deploy this to **Cloud Run** (Serverless) and scale to zero!

## [9. Vertex AI Memory Bank](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#8)

![Image 14: agent_memory](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/memorybank_custom.png)

## Short-term vs. Long-term Memory

*   **Short-term Context**: "What did I just say?" (Session history). This is lost when the chat window closes.
*   **Long-term Memory**: "What is my favorite programming language?" (User preferences). This should persist forever.

**Vertex AI Memory Bank** provides this long-term storage. It allows the agent to store and retrieve personalized information about the user.

## Sessions vs. Memory Bank

*   **Sessions** (`VertexAiSessionService`): This is the **Log**. It stores the raw, chronological sequence of every message, tool call, and event (`AppendEvent`, `ListEvents`). It provides the ground truth for _what happened_.
*   **Memory Bank** (`VertexAiMemoryBankService`): This is the **Knowledge**. It stores synthesized, long-term facts (`GenerateMemories`, `RetrieveMemories`). It is scoped to a specific `user_id`, ensuring privacy and isolation.

1.   👉💻 Type the following in your command:`cloudshell edit ~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/main.py` This opens `~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/main.py` in your editor.
2.   Find `# TODO: Create Vertex AI Session Service & Memory Bank Service`, replace the **whole line** with the following:`session_service = VertexAiSessionService(        project=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID    )    memory_service = VertexAiMemoryBankService(        project=PROJECT_ID, location=LOCATION, agent_engine_id=AGENT_ENGINE_ID    )`

![Image 15: memory_compare](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/memory_compare.png)

1.   👉💻 Type the following in your command:`cloudshell edit ~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/deploy_agent.py` This opens `~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/deploy_agent.py` in your editor.
2.   Replace the `# TODO: Set Up Configuration` with the following:`# Basic configuration typesMemoryBankConfig = types.ReasoningEngineContextSpecMemoryBankConfigSimilaritySearchConfig = (    types.ReasoningEngineContextSpecMemoryBankConfigSimilaritySearchConfig)GenerationConfig = types.ReasoningEngineContextSpecMemoryBankConfigGenerationConfig# Advanced configuration typesCustomizationConfig = types.MemoryBankCustomizationConfigMemoryTopic = types.MemoryBankCustomizationConfigMemoryTopicCustomMemoryTopic = types.MemoryBankCustomizationConfigMemoryTopicCustomMemoryTopicGenerateMemoriesExample = types.MemoryBankCustomizationConfigGenerateMemoriesExampleConversationSource = (    types.MemoryBankCustomizationConfigGenerateMemoriesExampleConversationSource)ConversationSourceEvent = (    types.MemoryBankCustomizationConfigGenerateMemoriesExampleConversationSourceEvent)ExampleGeneratedMemory = (    types.MemoryBankCustomizationConfigGenerateMemoriesExampleGeneratedMemory)`

![Image 16: memory_process](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/memory_process.png)

1.   👉 In the **same** file: `04-Adding-Memory-Bank/01-starter/backend/deploy_agent.py`. Look for the `# TODO: Set up topic`, replace the **whole line** with the following:`custom_topics = [        # Topic 1: Sweater Preference        MemoryTopic(            custom_memory_topic=CustomMemoryTopic(                label="sweater_preference",                description="""Extract the user's preferences for sweater styles, patterns, and designs. Include:                - Specific patterns (snowflake, reindeer, geometric, fair isle, solid, etc.)                - Style preferences (chunky knit, cardigan, pullover, turtleneck, oversized, fitted)                - Color preferences (red, green, navy, pastel, etc.)                - Material preferences if mentioned (wool, cotton, cashmere, itchy/soft)                - Themes (retro, modern, ugly christmas sweater, elegant)                Example: "User wants a retro style sweater with a pixelated reindeer pattern."                Example: "User prefers dark blue colors and hates itchy wool."                """,            )        ),        # Topic 2: Personal Context        MemoryTopic(            custom_memory_topic=CustomMemoryTopic(                label="personal_context",                description="""Extract the user's personal context including hobbies, pets, interests, job, and preferred scenes. Include:                - Hobbies and activities (skiing, reading, gaming, cooking, etc.)                - Pets (type, breed, name, color)                - Job or profession if relevant to their style                - General interests (sci-fi, nature, vintage, tech)                - Preferred scenes or vibes (cozy fireplace, snowy mountain, cyberpunk city, beach)                Example: "User has a golden retriever named Max."                Example: "User loves skiing and wants a snowy mountain background."                Example: "User is a software engineer who likes cyberpunk aesthetics."                """,            )        )    ]`
2.   👉 In the same file: `04-Adding-Memory-Bank/01-starter/backend/deploy_agent.py`. Look for the `# TODO: Create Agent Engine` , replace the **whole line** with the following:`agent_engine = client.agent_engines.create(        config={            "display_name": AGENT_DISPLAY_NAME,            "context_spec": {                "memory_bank_config": {                    "generation_config": {                        "model": f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/gemini-2.5-flash"                    },                    "customization_configs": [customization_config]                }            },        }    )`

### Why not just use the Prompt?

You might ask, "Why don't we just paste the user's history into the prompt?"

*   **Size Limits**: Context windows are large, but not infinite. You can't fit 5 years of history.
*   **Cost**: Processing 1 million tokens for every "Hello" is prohibitively expensive.
*   **Focus**: Memory Bank acts as a **Search Engine** for your agent. It retrieves only the _relevant_ facts.

1.   👉💻 Type the following in your command:`cloudshell edit ~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/agent.py` This opens `~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/agent.py` in your editor.
2.   In the file: `~/holiday_workshop/04-Adding-Memory-Bank/01-starter/backend/agent.py`Replace the `# TODO: Add PreloadMemoryTool` with the following:`if USE_MEMORY_BANK:    agent_tools.append(PreloadMemoryTool())`

### `PreloadMemoryTool`&`add_session_to_memory`

In `agent.py`, you'll see two key components:

*   **`PreloadMemoryTool`**: This is a tool that allows the agent to "Google itself." If the user asks something vague like "Get me my usual coffee," the agent can use this tool to query the Memory Bank for "coffee preferences" before answering.
*   **`add_session_to_memory`**: This is a background callback. 
    *   **Why Async?** Saving memory takes time (summarizing the chat, extracting facts). We don't want the user to wait for this. We run it in the background (`add_session_to_memory`) using `after_agent_callback`.

## [10. Memory Bank In Action](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#9)

1.   👉💻 Type the following in your command:`cd ~/holiday_workshop/04-Adding-Memory-Bank/01-starter./use_memory_bank.sh` You will see the result as below:![Image 17: deploy_agent_result](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/deploy_agent.png) Check you `~/holiday_workshop/.env` file, you will see (**no action needed**)`USE_MEMORY_BANK=TRUEAGENT_ENGINE_ID={agent_engine_id}`
2.   👉💻 Test the memory with application UI. Type the following in your command:`cd ~/holiday_workshop/04-Adding-Memory-Bank/01-starter./start_app.sh` Make sure you click into **`http://localhost:5173/`**, or open a new window and type **`http://localhost:5173/`**.Note that `Uvicorn running on http://0.0.0.0:8000` is just backend server, **not** the actual link we want to click into.Now the chat interface in website has become your personalized agent!![Image 18: website](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/08-01.png)
3.   👉Test the memory. If you type in the UI:`I want a sweater that matches my dog. He's a golden retriever.``I'm a programmer, so I want something geeky. Maybe a matrix style?``I like snowflake sweater pattern`

The agent will identify this as a preference and store it in the Memory Bank.

Next week(or anytime you restart the application by `Control+C` and `./start_app.sh`), if you ask:

`what is my preference on sweater pattern?`
The agent will query the **Memory Bank**, see your **preference**, and generate sweater pattern without being asked. ![Image 19: 10-result](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/10-result.png)

1.   Verify in Vertex AI Agent Engine, by go to [Google Cloud Console Agent Engine](https://console.cloud.google.com/vertex-ai/agents/agent-engines)
2.   Click the **`Memories`** Tab in this deployed agent, you can view all the memory here.![Image 20: view memory](https://codelabs.developers.google.com/static/codelabs/christmas-card/img/view_memory.png)

Congratulations! You just attached the meomory bank to your agent!

## [11. Conclusion](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#10)

## Summary

You have successfully architected and built a complete agentic system.

*   **Connectivity**: You used **MCP** to standardize how your agent accesses local tools.
*   **Orchestration**: You used **ADK** to manage the complex reasoning loop required for multi-step tasks.
*   **Personalization**: You used **Memory Bank** to create a persistent, learning layer that remembers user context.

## Next Steps

*   **Build your own MCP Server**: Create a server for your internal API or database.
*   **Explore ADK Patterns**: Learn about "Reasoning Loops" and "Orchestration" in the ADK documentation.
*   **Deploy**: Take your agent from a local script to a production service on Cloud Run.

[Back](https://codelabs.developers.google.com/codelabs/christmas-card/instructions# "Previous step")

*   [English](https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0)
*   [Deutsch](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=de#0)
*   [Español](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=es#0)
*   [Español – América Latina](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=es-419#0)
*   [Français](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=fr#0)
*   [Indonesia](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=id#0)
*   [Italiano](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=it#0)
*   [Polski](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=pl#0)
*   [Português – Brasil](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=pt-br#0)
*   [Tiếng Việt](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=vi#0)
*   [Türkçe](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=tr#0)
*   [Русский](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=ru#0)
*   [עברית](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=he#0)
*   [العربيّة](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=ar#0)
*   [فارسی](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=fa#0)
*   [हिंदी](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=hi#0)
*   [বাংলা](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=bn#0)
*   [ภาษาไทย](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=th#0)
*   [中文 – 简体](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=zh-cn#0)
*   [中文 – 繁體](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=zh-tw#0)
*   [日本語](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=ja#0)
*   [한국어](https://codelabs.developers.google.com/codelabs/christmas-card/instructions?hl=ko#0)

[Next](https://codelabs.developers.google.com/codelabs/christmas-card/instructions# "Next step")

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

### Source URL
https://codelabs.developers.google.com/codelabs/christmas-card/instructions#0
