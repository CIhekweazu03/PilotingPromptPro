# Piloting Prompt Pro

An automated prompt engineering assistant that transforms simple user inputs into optimized prompts for AI systems.

## Overview

Piloting Prompt Pro serves as a layer between users and AI systems, automatically transforming natural user inputs into more optimized prompts. The system analyzes user intent, incorporates relevant context, and applies best practices in prompt engineering without requiring users to understand these technical details.

When additional clarity could significantly improve results, the system asks further questions to gather key information. This approach maintains user agency while eliminating the need for prompt engineering expertise.

## Problem Statement

While large language models have become increasingly powerful, extracting optimal performance often requires expertise in prompt engineering. This creates a barrier for many users who could benefit from AI but lack the technical knowledge to craft effective prompts. Piloting Prompt Pro aims to bridge this gap by automatically handling prompt engineering complexities, making AI systems more accessible to general users.

## Features

- **Natural Language Interface**: Express your needs in plain language
- **Intelligent Clarification**: System asks follow-up questions when beneficial
- **Optimized Prompts**: Automatically generates prompts following best practices
- **Prompt Execution**: Execute the generated prompt and see the results
- **User-Focused Design**: Minimal cognitive load, with complexity hidden unless needed

## Architecture

Piloting Prompt Pro employs a dual-AI approach:
1. **Intent Understanding**: Focuses on understanding user intent and generating clarifying questions when needed
2. **Prompt Optimization**: Specializes in transforming this understanding into optimized prompts

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/piloting-prompt-pro.git
cd piloting-prompt-pro

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env file with your AWS credentials
```

## Usage

```bash
# Start the Streamlit app
streamlit run app.py
```

Then open your browser and navigate to http://localhost:8501

## Example Interactions

### Example 1: Writing Request
**User**: "Help me write a persuasive email to my team about a new initiative"

**Piloting Prompt Pro**: "To optimize your prompt, I need a bit more information:
- What is the specific initiative you're introducing?
- What is your main goal for this email (e.g., get volunteers, inform, gather feedback)?"

### Example 2: Data Visualization
**User**: "I need to create a data visualization of sales trends"

**Piloting Prompt Pro**: "To optimize your prompt, I need a bit more information:
- What specific time period are you interested in visualizing?
- What type of visualization would you prefer (e.g., line chart, bar graph)?"

## Technical Requirements

- Python 3.8+
- Streamlit 1.31.0+
- boto3 1.34.0+
- python-dotenv 1.0.0+

## HCC Perspectives

The system prioritizes:
- **User Agency**: Maintaining transparency about when and why it seeks clarification
- **Privacy**: Minimizing data collection to only what's necessary for prompt optimization
- **Security**: Implementing safeguards against prompt injection and other security concerns

## Future Work

- Adding support for multi-modal prompts (text + images)
- Implementing a history feature to save and reuse optimized prompts
- Developing a plugin system for different AI models and platforms

## Contributors

- Christian C. Ihekweazu (@cihekwe)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Clemson University