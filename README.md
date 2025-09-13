# PoC_Agent_langgraph
AI agent system that analyzes product concepts and generates professional PDF reports. This tool helps entrepreneurs, product managers, and developers quickly evaluate the feasibility of their ideas using AI agents specialized in UX design, technical assessment, and product planning.
## What This Tool Does

This system takes your product idea and runs it through three AI specialists:
- **UX Agent**: Designs the user journey and experience
- **Tech Agent**: Evaluates technical feasibility and suggests tech stack
- **Product Agent**: Plans MVP features, identifies risks, and creates next steps

The result is a professional PDF report with tables and structured analysis that you can share with stakeholders.

## Key Features

- 🤖 **Multi-Agent Analysis**: Three specialized AI agents work together
- 📊 **PDF Reports**: Professional table-formatted output instead of JSON
- 🔄 **Batch Processing**: Analyze multiple concepts at once
- 🎯 **Variation Generation**: Create different versions of your concept
- 💰 **Token Efficient**: Optimized to minimize OpenAI API costs
- 📈 **Feasibility Scoring**: Get 1-10 feasibility ratings
- ⏱️ **Timeline Estimates**: Realistic development timelines in weeks

## Prerequisites

Before you start, make sure you have:

1. **Python 3.8+** installed on your computer
2. **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))
3. Basic familiarity with command line/terminal

## Installation

### Step 1: Clone or Download
Download this project to your computer and navigate to the folder.

### Step 2: Install Dependencies
Open your terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- `langgraph` - For agent workflow management
- `openai` - For AI API calls
- `python-dotenv` - For environment variables
- `reportlab` - For PDF generation

### Step 3: Set Up Your API Key
Create a file named `.env` in the project folder and add your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

**Important**: Never share your API key publicly!

## How to Use

### Basic Usage (Single Concept)

Analyze one product concept:

```bash
python PoC_agent_pdf.py --concept "A mobile app for tracking daily water intake"
```

### Generate Variations

Create multiple versions of your concept for comparison:

```bash
python PoC_agent_pdf.py --concept "A mobile app for tracking daily water intake" --repeat
```

This generates variations like:
- Original concept
- B2B version (for businesses)
- B2C version (for consumers)

### Batch Analysis

Analyze multiple different concepts at once:

```bash
python PoC_agent_pdf.py --batch "AI-powered recipe app" "Smart home energy monitor" "Virtual fitness trainer"
```

### Interactive Mode

Run without arguments for step-by-step prompts:

```bash
python PoC_agent_pdf.py
```

## Understanding the Output

### PDF Report Structure

The generated PDF (`poc_analysis_results.pdf`) contains:

1. **Executive Summary Table**
   - Concept overview
   - Feasibility scores (1-10)
   - Timeline estimates
   - Recommended tech stacks

2. **Detailed Analysis for Each Concept**
   - User journey breakdown
   - Technical assessment
   - MVP feature list
   - Risk analysis
   - Next steps roadmap

### Feasibility Scoring

- **8-10**: Highly feasible, low technical risk
- **6-7**: Moderately feasible, some challenges expected
- **4-5**: Challenging but possible, significant effort required
- **1-3**: High risk, major technical hurdles

## Example Concepts to Try

Here are some sample concepts you can test with:

```bash
# E-commerce
python PoC_agent_pdf.py --concept "AI-powered personal shopping assistant"

# Health & Fitness
python PoC_agent_pdf.py --concept "Mental health tracking app with mood analysis"

# Productivity
python PoC_agent_pdf.py --concept "Smart calendar that automatically schedules tasks"

# Education
python PoC_agent_pdf.py --concept "Language learning app using AR technology"
```

## Understanding the Code Structure

### Main Components

1. **OptimizedAgent**: Base class for all AI agents with token tracking
2. **UXAgent**: Focuses on user experience and journey design
3. **TechAgent**: Evaluates technical feasibility and suggests tech stacks
4. **ProductAgent**: Plans MVP features and identifies risks
5. **PDFGenerator**: Creates professional PDF reports
6. **PoCWorkflow**: Orchestrates the entire analysis process

### Agent Workflow

```
Input Concept → UX Agent → Tech Agent → Product Agent → PDF Report
```

Each agent builds upon the previous agent's output, creating a comprehensive analysis.

## Customization Options

### Changing AI Models

Edit the model in the agent initialization:

```python
# In the code, change from gpt-4o-mini to gpt-4
self.model = "gpt-4"  # More powerful but more expensive
```

### Adjusting Token Limits

Modify `max_tokens` in the `_call_api` method for longer/shorter responses:

```python
response, tokens = self._call_api(prompt, 500)  # Increase for longer responses
```

### Custom PDF Styling

Modify the `PDFGenerator` class to change:
- Colors and fonts
- Table layouts
- Page formatting
- Report structure

## Troubleshooting

### Common Issues

**"No module named 'openai'"**
- Run: `pip install -r requirements.txt`

**"Invalid API key"**
- Check your `.env` file has the correct API key
- Ensure no extra spaces around the key

**"PDF not generated"**
- Check file permissions in the directory
- Ensure you have write access to the folder

**High token usage**
- The tool is optimized for efficiency
- Typical usage: 500-1500 tokens per concept
- Monitor usage at [platform.openai.com](https://platform.openai.com)

### Getting Help

1. Check the error message carefully
2. Ensure all dependencies are installed
3. Verify your API key is working
4. Try with a simpler concept first

## Cost Estimation

Using GPT-4o-mini (recommended):
- Single concept: ~$0.01-0.03
- Batch of 5 concepts: ~$0.05-0.15
- 100 concepts: ~$1-3

Using GPT-4:
- Single concept: ~$0.10-0.30
- More accurate but significantly more expensive

## Tips for Better Results

1. **Be Specific**: "Food delivery app for college students" vs "Food app"
2. **Include Context**: Mention target audience, key features, or constraints
3. **Try Variations**: Use the `--repeat` flag to explore different approaches
4. **Batch Similar Ideas**: Analyze related concepts together for comparison

## Next Steps

After getting your analysis:

1. **Review Feasibility Scores**: Focus on concepts rated 6+
2. **Check Timeline Estimates**: Ensure they fit your constraints
3. **Analyze Risks**: Plan mitigation strategies for identified risks
4. **Follow Next Steps**: Use the generated action items as your roadmap
5. **Share with Team**: The PDF format makes it easy to share with stakeholders

## Advanced Usage

### Custom Variations

Modify the `RepeatInput` class to create custom concept variations:

```python
# Add your own variation types
self.variations = {
    'target_audience': ['Students', 'Professionals', 'Seniors'],
    'platform': ['Mobile App', 'Web App', 'Desktop'],
    'business_model': ['Freemium', 'Subscription', 'One-time Purchase']
}
```

### Integration with Other Tools

The analysis results can be exported to:
- Project management tools (Jira, Trello)
- Spreadsheets for further analysis
- Presentation software for pitches

## Contributing

This is a proof-of-concept tool. Feel free to:
- Add new agent types (Marketing Agent, Legal Agent, etc.)
- Improve PDF formatting
- Add new analysis dimensions
- Optimize token usage further

## License

This project is for educational and proof-of-concept purposes. Modify and use as needed for your projects.

---

**Happy analyzing!** 🚀

Remember: This tool provides AI-generated insights to help guide your decision-making, but human judgment and domain expertise remain essential for successful product development.
