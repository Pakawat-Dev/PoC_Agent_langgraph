"""
Optimized Cross-Functional Product Team Agent System.

Focus: Proof of Concept development with maximum token efficiency
Output: PDF table format instead of JSON files
"""

import argparse
import os
import time
from typing import Any, Dict, List, TypedDict

from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from openai import OpenAI
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ProductState(TypedDict):
    """Optimized state with essential fields only."""

    concept: str
    user_journey: str
    tech_stack: str
    mvp_features: List[str]
    feasibility: int
    timeline_weeks: int
    risks: List[str]
    next_steps: List[str]
    total_tokens: int
    agent_outputs: Dict[str, str]


class RepeatInput:
    """Handles repeat input scenarios for PoC analysis."""
    
    def __init__(self):
        self.history = []
        self.variations = {
            'target_audience': ['B2B', 'B2C', 'Enterprise', 'SMB'],
            'complexity': ['Simple', 'Moderate', 'Complex'],
            'timeline': ['Rush (2-4 weeks)', 'Standard (4-8 weeks)', 'Extended (8+ weeks)']
        }
    
    def save_input(self, concept: str, params: Dict[str, Any] = None):
        """Save input for potential reuse."""
        entry = {
            'concept': concept,
            'params': params or {},
            'timestamp': time.time()
        }
        self.history.append(entry)
    
    def get_variations(self, base_concept: str) -> List[str]:
        """Generate concept variations for repeat analysis."""
        variations = []
        for audience in self.variations['target_audience'][:2]:  # Limit to 2
            variations.append(f"{base_concept} for {audience}")
        return variations
    
    def repeat_with_params(self, concept: str, variation_type: str = 'audience') -> str:
        """Create variation of existing concept."""
        if variation_type == 'audience':
            return f"{concept} (B2B focus)"
        elif variation_type == 'complexity':
            return f"{concept} (simplified version)"
        return concept


class OptimizedAgent:
    """Base agent class with token-efficient API calls."""

    def __init__(self, model: str = "gpt-4o-mini"):
        """Initialize agent with specified model."""
        self.model = model
        self.client = client
        self.tokens_used = 0

    def _call_api(self, prompt: str, max_tokens: int = 300) -> tuple[str, int]:
        """Make efficient API call with token tracking."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3  # Lower temp for more focused responses
            )
            content = response.choices[0].message.content
            tokens = response.usage.total_tokens
            self.tokens_used += tokens
            return content, tokens
        except Exception as e:
            return f"Error: {str(e)}", 0


class UXAgent(OptimizedAgent):
    """User Experience agent focused on MVP design."""

    def design_mvp(self, state: ProductState) -> ProductState:
        """Focus on MVP user experience design."""
        prompt = f"""Product: {state['concept']}

Create concise user journey for MVP in format:
Step 1 → Step 2 → Step 3

Focus on core user value and essential screens only."""

        response, tokens = self._call_api(prompt, 200)

        # Extract journey or use default
        journey = response.strip() if response else "User opens app → Core action → Result"

        state.update({
            "user_journey": journey,
            "total_tokens": state.get("total_tokens", 0) + tokens,
            "agent_outputs": {**state.get("agent_outputs", {}), "ux": response}
        })
        return state


class TechAgent(OptimizedAgent):
    """Technical assessment agent for PoC evaluation."""

    def assess_tech(self, state: ProductState) -> ProductState:
        """Perform quick technical assessment for PoC."""
        prompt = f"""Product: {state['concept']}
Journey: {state['user_journey']}

Provide assessment in format:
Tech Stack: [frontend/backend/database]
Feasibility Score: [1-10]
MVP Timeline: [weeks]
Main Technical Risk: [brief description]

Keep responses concise and focused."""

        response, tokens = self._call_api(prompt, 250)

        # Extract key information with defaults
        tech_stack = "React/FastAPI/SQLite"
        feasibility = 7
        timeline = 4

        lines = response.split('\n')
        for line in lines:
            line_lower = line.lower()
            if 'stack' in line_lower and ':' in line:
                tech_stack = line.split(':')[-1].strip()
            elif 'feasibility' in line_lower or 'score' in line_lower:
                numbers = [int(x) for x in line if x.isdigit()]
                if numbers:
                    feasibility = min(10, max(1, numbers[0]))
            elif ('timeline' in line_lower or 'weeks' in line_lower) and ':' in line:
                numbers = [int(x) for x in line if x.isdigit()]
                if numbers:
                    timeline = numbers[0]

        state.update({
            "tech_stack": tech_stack,
            "feasibility": feasibility,
            "timeline_weeks": timeline,
            "total_tokens": state.get("total_tokens", 0) + tokens,
            "agent_outputs": {**state.get("agent_outputs", {}), "tech": response}
        })
        return state


class ProductAgent(OptimizedAgent):
    """Product planning agent for MVP definition."""

    def plan_mvp(self, state: ProductState) -> ProductState:
        """Create MVP plan with features, risks, and next steps."""
        prompt = f"""Product: {state['concept']}
Tech: {state['tech_stack']} (feasibility: {state['feasibility']}/10)
Timeline: {state['timeline_weeks']} weeks

Provide structured output:
MVP Features:
- [essential feature 1]
- [essential feature 2] 
- [essential feature 3]

Key Risks:
- [primary risk]
- [secondary risk]

Next Steps:
- [immediate action]
- [week 1 milestone]
- [validation approach]

Keep each item brief and actionable."""

        response, tokens = self._call_api(prompt, 300)

        # Parse response into structured lists
        mvp_features = []
        risks = []
        next_steps = []
        current_section = ""

        for line in response.split('\n'):
            line = line.strip()
            line_lower = line.lower()
            
            if 'mvp features' in line_lower:
                current_section = "mvp"
            elif 'risks' in line_lower:
                current_section = "risks"
            elif 'next steps' in line_lower:
                current_section = "next"
            elif line.startswith(('-', '•', '*')):
                item = line[1:].strip()
                if current_section == "mvp" and len(mvp_features) < 3:
                    mvp_features.append(item)
                elif current_section == "risks" and len(risks) < 2:
                    risks.append(item)
                elif current_section == "next" and len(next_steps) < 3:
                    next_steps.append(item)

        # Provide fallbacks if parsing failed
        if not mvp_features:
            mvp_features = ["Core functionality", "User authentication", "Basic UI"]
        if not risks:
            risks = ["Technical complexity", "User adoption challenges"]
        if not next_steps:
            next_steps = ["Create mockups", "Setup development", "Conduct user research"]

        state.update({
            "mvp_features": mvp_features,
            "risks": risks,
            "next_steps": next_steps,
            "total_tokens": state.get("total_tokens", 0) + tokens,
            "agent_outputs": {**state.get("agent_outputs", {}), "product": response}
        })
        return state


class PDFGenerator:
    """PDF report generator for PoC analysis results."""

    def __init__(self, filename: str = "poc_analysis_results.pdf"):
        """Initialize PDF generator with filename."""
        self.filename = filename
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=1  # Center alignment
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.darkgreen
        ))

    def generate_report(self, results: List[ProductState]):
        """Generate comprehensive PDF report with table format."""
        doc = BaseDocTemplate(self.filename, pagesize=letter)
        frame = Frame(
            doc.leftMargin,
            doc.bottomMargin,
            doc.width,
            doc.height,
            id='normal'
        )
        template = PageTemplate(id='main', frames=frame)
        doc.addPageTemplates([template])

        story = []
        
        # Title
        title = Paragraph("PoC Analysis Results", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 20))

        # Summary table
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        summary_data = self._create_summary_table(results)
        summary_table = Table(summary_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
        summary_table.setStyle(self._get_table_style())
        story.append(summary_table)
        story.append(Spacer(1, 30))

        # Detailed analysis for each concept
        for i, result in enumerate(results, 1):
            story.append(Paragraph(
                f"Concept {i}: Analysis Details",
                self.styles['SectionHeader']
            ))
            
            # Concept details table
            concept_data = self._create_concept_table(result)
            concept_table = Table(concept_data, colWidths=[2*inch, 4*inch])
            concept_table.setStyle(self._get_table_style())
            story.append(concept_table)
            story.append(Spacer(1, 20))

        doc.build(story)
        print(f"Report generated: {self.filename}")

    def _create_summary_table(self, results: List[ProductState]) -> List[List[str]]:
        """Create summary table data with proper text wrapping."""
        headers = ['Concept', 'Feasibility', 'Timeline', 'Tech Stack']
        data = [headers]
        
        for result in results:
            row = [
                Paragraph(result['concept'], self.styles['Normal']),
                f"{result['feasibility']}/10",
                f"{result['timeline_weeks']} weeks",
                Paragraph(result['tech_stack'], self.styles['Normal'])
            ]
            data.append(row)
        
        return data

    def _create_concept_table(self, result: ProductState) -> List[List[str]]:
        """Create detailed concept table with proper text wrapping."""
        data = [
            ['Concept', Paragraph(result['concept'], self.styles['Normal'])],
            ['User Journey', Paragraph(result['user_journey'], self.styles['Normal'])],
            ['Tech Stack', Paragraph(result['tech_stack'], self.styles['Normal'])],
            ['Feasibility', f"{result['feasibility']}/10"],
            ['Timeline', f"{result['timeline_weeks']} weeks"],
            ['MVP Features', Paragraph('<br/>'.join(f"• {f}" for f in result['mvp_features']), self.styles['Normal'])],
            ['Key Risks', Paragraph('<br/>'.join(f"• {r}" for r in result['risks']), self.styles['Normal'])],
            ['Next Steps', Paragraph('<br/>'.join(f"• {s}" for s in result['next_steps']), self.styles['Normal'])],
            ['Tokens Used', str(result['total_tokens'])]
        ]
        return data

    def _get_table_style(self) -> TableStyle:
        """Get standard table styling."""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTSIZE', (0, 1), (-1, -1), 9)
        ])


class PoCWorkflow:
    """Main workflow orchestrator with repeat input support."""
    
    def __init__(self):
        self.repeat_handler = RepeatInput()
        self.ux_agent = UXAgent()
        self.tech_agent = TechAgent()
        self.product_agent = ProductAgent()
        self.pdf_generator = PDFGenerator()
        self.results = []
    
    def analyze_concept(self, concept: str, save_for_repeat: bool = True) -> ProductState:
        """Analyze single concept through agent workflow."""
        if save_for_repeat:
            self.repeat_handler.save_input(concept)
        
        # Initialize state
        state = ProductState(
            concept=concept,
            user_journey="",
            tech_stack="",
            mvp_features=[],
            feasibility=0,
            timeline_weeks=0,
            risks=[],
            next_steps=[],
            total_tokens=0,
            agent_outputs={}
        )
        
        # Run agent workflow
        state = self.ux_agent.design_mvp(state)
        state = self.tech_agent.assess_tech(state)
        state = self.product_agent.plan_mvp(state)
        
        return state
    
    def repeat_analysis(self, base_concept: str, variation_count: int = 2) -> List[ProductState]:
        """Repeat analysis with variations."""
        results = []
        
        # Original concept
        original = self.analyze_concept(base_concept, save_for_repeat=False)
        results.append(original)
        
        # Generate variations
        variations = self.repeat_handler.get_variations(base_concept)
        for i, variation in enumerate(variations[:variation_count]):
            result = self.analyze_concept(variation, save_for_repeat=False)
            results.append(result)
        
        return results
    
    def run_batch_analysis(self, concepts: List[str]) -> List[ProductState]:
        """Run analysis on multiple concepts."""
        results = []
        for concept in concepts:
            result = self.analyze_concept(concept)
            results.append(result)
            print(f"✓ Analyzed: {concept[:50]}...")
        
        self.results = results
        return results
    
    def generate_report(self, results: List[ProductState] = None):
        """Generate PDF report from results."""
        if results is None:
            results = self.results
        
        if not results:
            print("No results to generate report from.")
            return
        
        self.pdf_generator.generate_report(results)


def main():
    """Main execution function with repeat input support."""
    parser = argparse.ArgumentParser(description='PoC Agent Analysis with Repeat Input')
    parser.add_argument('--concept', type=str, help='Product concept to analyze')
    parser.add_argument('--repeat', action='store_true', help='Generate variations of the concept')
    parser.add_argument('--batch', nargs='+', help='Multiple concepts to analyze')
    
    args = parser.parse_args()
    
    workflow = PoCWorkflow()
    
    if args.batch:
        # Batch analysis
        print(f"Analyzing {len(args.batch)} concepts...")
        results = workflow.run_batch_analysis(args.batch)
        
    elif args.concept:
        if args.repeat:
            # Repeat with variations
            print(f"Analyzing concept with variations: {args.concept}")
            results = workflow.repeat_analysis(args.concept)
        else:
            # Single analysis
            print(f"Analyzing concept: {args.concept}")
            result = workflow.analyze_concept(args.concept)
            results = [result]
    else:
        # Interactive mode
        concept = input("Enter product concept: ")
        repeat_choice = input("Generate variations? (y/n): ").lower() == 'y'
        
        if repeat_choice:
            results = workflow.repeat_analysis(concept)
        else:
            result = workflow.analyze_concept(concept)
            results = [result]
    
    # Generate report
    workflow.generate_report(results)
    
    # Summary
    total_tokens = sum(r['total_tokens'] for r in results)
    print(f"\nAnalysis complete:")
    print(f"- Concepts analyzed: {len(results)}")
    print(f"- Total tokens used: {total_tokens}")
    print(f"- Report saved: {workflow.pdf_generator.filename}")


if __name__ == "__main__":
    main()
