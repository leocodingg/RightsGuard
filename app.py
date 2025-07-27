# RightsGuard - Streamlit UI for Multi-Agent Legal Rights Analyzer
import streamlit as st
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file (for local development)
load_dotenv()

# Debug: Check if API key is available
if os.getenv("NVIDIA_API_KEY"):
    print("✅ NVIDIA_API_KEY found in environment")
else:
    print("❌ NVIDIA_API_KEY not found in environment")
    # Check if it's in Streamlit secrets
    try:
        if st.secrets.get("NVIDIA_API_KEY"):
            print("✅ Found NVIDIA_API_KEY in Streamlit secrets")
            os.environ["NVIDIA_API_KEY"] = st.secrets["NVIDIA_API_KEY"]
        else:
            print("❌ NVIDIA_API_KEY not in Streamlit secrets either")
    except:
        print("❌ Error accessing Streamlit secrets")

from workflow import RightsGuardWorkflow

# Page configuration
st.set_page_config(
    page_title="RightsGuard - AI Legal Rights Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .agent-status {
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        font-weight: bold;
    }
    .agent-complete {
        background-color: #d4edda;
        color: #155724;
    }
    .agent-active {
        background-color: #fff3cd;
        color: #856404;
    }
    .agent-pending {
        background-color: #f8f9fa;
        color: #6c757d;
    }
    .community-insight {
        background-color: #e7f3ff;
        color: #1f4e79;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        color: #664d03;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'workflow' not in st.session_state:
        st.session_state.workflow = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def display_agent_status(stage):
    """Display the status of each agent in the workflow"""
    stages = {
        'idle': ['⏸️ Research Agent', '⏸️ Legal Analyst', '⏸️ Document Writer'],
        'scraping': ['🔄 Research Agent', '⏸️ Legal Analyst', '⏸️ Document Writer'],
        'analyzing': ['✅ Research Agent', '🔄 Legal Analyst', '⏸️ Document Writer'],
        'generating': ['✅ Research Agent', '✅ Legal Analyst', '🔄 Document Writer'],
        'complete': ['✅ Research Agent', '✅ Legal Analyst', '✅ Document Writer']
    }
    
    status_container = st.container()
    with status_container:
        st.markdown("### 🤖 Multi-Agent Progress")
        cols = st.columns(3)
        
        for i, agent_status in enumerate(stages.get(stage, stages['idle'])):
            with cols[i]:
                if '✅' in agent_status:
                    st.markdown(f'<div class="agent-status agent-complete">{agent_status}</div>', 
                              unsafe_allow_html=True)
                elif '🔄' in agent_status:
                    st.markdown(f'<div class="agent-status agent-active">{agent_status}</div>', 
                              unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="agent-status agent-pending">{agent_status}</div>', 
                              unsafe_allow_html=True)

def display_community_insights(building_history, total_complaints):
    """Display community insights and building history"""
    st.markdown("### 🏢 Community Legal Memory")
    
    if building_history:
        risk_level = "HIGH" if len(building_history) >= 3 else "MODERATE" if len(building_history) >= 2 else "LOW"
        risk_color = {"HIGH": "🔴", "MODERATE": "🟡", "LOW": "🟢"}[risk_level]
        
        st.markdown(f"""
        <div class="community-insight">
            <h4>{risk_color} Building Risk Level: {risk_level}</h4>
            <p><strong>Previous Complaints:</strong> {len(building_history)}</p>
            <p><strong>Community Database:</strong> {total_complaints} total complaints tracked</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show recent complaints
        st.markdown("#### Recent Building Complaints:")
        for i, complaint in enumerate(building_history[-3:]):  # Show last 3
            date = complaint.get('date', 'Unknown date')
            issue = complaint.get('complaint', 'No details')
            st.write(f"**{date[:10]}:** {issue[:100]}...")
    else:
        st.markdown("""
        <div class="community-insight">
            <h4>🟢 New Building</h4>
            <p>No previous complaints found for this address.</p>
            <p>Your complaint will help future tenants at this location.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">⚖️ RightsGuard</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">AI-Powered Tenant Rights Analyzer with Community Memory</h3>', 
                unsafe_allow_html=True)
    
    # Sidebar for input
    st.sidebar.markdown("## 📝 Your Complaint")
    
    # User inputs
    user_complaint = st.sidebar.text_area(
        "Describe your issue:",
        placeholder="e.g., My landlord entered without notice...",
        height=120
    )
    
    building_address = st.sidebar.text_input(
        "Building Address:",
        placeholder="123 Main St, New York, NY"
    )
    
    st.sidebar.markdown("## 👤 Your Information")
    tenant_name = st.sidebar.text_input("Full Name:", placeholder="John Doe")
    landlord_name = st.sidebar.text_input("Landlord/Company:", placeholder="ABC Property Management")
    
    # Warning disclaimer
    st.sidebar.markdown("""
    <div class="warning-box">
        <strong>⚠️ Legal Disclaimer</strong><br>
        This tool provides information only. Not legal advice. 
        Consult an attorney for legal counsel.
    </div>
    """, unsafe_allow_html=True)
    
    # Process button
    if st.sidebar.button("🚀 Analyze My Rights", type="primary", disabled=st.session_state.processing):
        if user_complaint and building_address and tenant_name:
            st.session_state.processing = True
            
            # Prepare tenant info
            tenant_info = {
                "name": tenant_name,
                "address": building_address,
                "landlord": landlord_name,
                "date": datetime.now().strftime("%B %d, %Y")
            }
            
            # Initialize workflow if not already done
            if st.session_state.workflow is None:
                with st.spinner("🔧 Initializing AI agents..."):
                    try:
                        st.session_state.workflow = RightsGuardWorkflow()
                        st.success("✅ AI agents ready!")
                    except Exception as e:
                        st.error(f"❌ Failed to initialize: {str(e)}")
                        st.session_state.processing = False
                        return
            
            # Process the complaint
            try:
                # Show progress
                progress_placeholder = st.empty()
                
                with progress_placeholder.container():
                    display_agent_status('scraping')
                    st.info("🔍 Researching building records and legal precedents...")
                
                # Run the workflow
                result = st.session_state.workflow.process_complaint(
                    user_complaint=user_complaint,
                    building_address=building_address,
                    tenant_info=tenant_info
                )
                
                st.session_state.result = result
                st.session_state.processing = False
                
                # Clear progress and show completion
                progress_placeholder.empty()
                display_agent_status('complete')
                st.success("🎉 Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Processing failed: {str(e)}")
                st.session_state.processing = False
        else:
            st.sidebar.error("Please fill in all required fields")
    
    # Display results
    if st.session_state.result:
        result = st.session_state.result
        
        # Community insights
        display_community_insights(
            result['community_insights']['building_history'],
            result['community_insights']['total_community_complaints']
        )
        
        # Analysis results
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🧠 AI Analysis")
            
            # Display structured analysis if available
            analysis = result['analysis']
            if 'is_legitimate' in analysis:
                # Structured analysis format
                legitimacy = analysis.get('is_legitimate', 'Unknown')
                case_strength = analysis.get('case_strength', 'Unknown')
                
                # Status indicator
                status_color = "🟢" if legitimacy == "Yes" else "🔴" if legitimacy == "No" else "🟡"
                st.markdown(f"**{status_color} Complaint Status:** {legitimacy}")
                
                strength_color = {"Strong": "🟢", "Moderate": "🟡", "Weak": "🔴"}.get(case_strength, "⚪")
                st.markdown(f"**{strength_color} Case Strength:** {case_strength}")
                
                # Applicable laws
                if analysis.get('applicable_laws'):
                    st.markdown("**📜 Applicable Laws:**")
                    for law in analysis['applicable_laws']:
                        st.write(f"• {law}")
                
                # Evidence needed
                if analysis.get('evidence_needed'):
                    st.markdown("**📋 Evidence to Collect:**")
                    for evidence in analysis['evidence_needed']:
                        st.write(f"• {evidence}")
                
                # Recommended actions
                if analysis.get('recommended_actions'):
                    st.markdown("**⚡ Recommended Actions:**")
                    for action in analysis['recommended_actions']:
                        st.write(f"• {action}")
            else:
                # Fallback to raw analysis text
                analysis_text = analysis.get('analysis', 'No analysis available')
                st.write(analysis_text)
            
            # Show NYC building violations prominently
            if result['sources']['violations']:
                st.markdown("### 🏢 Building Violation History")
                st.markdown(f"Found **{len(result['sources']['violations'])}** official NYC violations for this address:")
                
                for i, violation in enumerate(result['sources']['violations'][:3], 1):
                    # Get the most descriptive field available
                    description = violation.get('novdescription', 'No description available')
                    if description and len(description) > 50:
                        # Clean up the legal description
                        description = description.replace('§', 'Section').replace('ADM CODE', 'Admin Code')
                        # Show first 150 characters
                        description = description[:150] + "..." if len(description) > 150 else description
                    
                    violation_type = violation.get('violationtype', 'Housing Code Violation')
                    inspection_date = violation.get('inspectiondate', 'Date unknown')
                    if inspection_date != 'Date unknown':
                        try:
                            # Format date nicely
                            date_part = inspection_date.split('T')[0]  # Get just the date part
                            inspection_date = date_part
                        except:
                            pass
                    
                    violation_class = violation.get('class', 'Unknown')
                    status = violation.get('currentstatus', 'Unknown status')
                    
                    st.markdown(f"""
                    **{i}. {violation_type}**
                    - **Date:** {inspection_date}
                    - **Class:** {violation_class} | **Status:** {status}
                    - **Details:** {description}
                    """)
                
                if len(result['sources']['violations']) > 3:
                    st.markdown(f"*...and {len(result['sources']['violations']) - 3} more violations in city records*")
                    
                st.markdown("*Source: NYC Department of Housing Preservation & Development*")
            
            # Show sources
            with st.expander("📚 Legal References"):
                if result['sources']['laws']:
                    st.write("**Relevant Laws Referenced:**")
                    for law in result['sources']['laws']:
                        st.write(f"• {law}")
                else:
                    st.write("*Laws identified by AI analysis based on NYC tenant rights*")
        
        with col2:
            st.markdown("### 📄 Generated Letter")
            letter_content = result['letter']['letter_content']
            
            # Show letter in a text area for easy copying
            st.text_area(
                "Your complaint letter:",
                value=letter_content,
                height=400,
                help="Copy this letter to send to your landlord"
            )
            
            # Download button
            st.download_button(
                label="📥 Download Letter",
                data=letter_content,
                file_name=f"complaint_letter_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    # Show demo info if no result
    else:
        if not st.session_state.processing:
            display_agent_status('idle')
            
            # Demo information
            st.markdown("### 🎯 How RightsGuard Works")
            
            demo_cols = st.columns(3)
            with demo_cols[0]:
                st.markdown("""
                **1. 🔍 Research Agent**
                - Searches NYC violation records
                - Checks building complaint history
                - Gathers legal precedents
                """)
            
            with demo_cols[1]:
                st.markdown("""
                **2. 🧠 Legal Analyst**
                - NVIDIA AI-powered analysis
                - Compares case to tenant law
                - Identifies violation strength
                """)
            
            with demo_cols[2]:
                st.markdown("""
                **3. 📝 Document Writer**
                - Generates formal complaint
                - Includes legal citations
                - Ready to send to landlord
                """)
            
            # Sample cases
            st.markdown("### 📋 Example Issues We Handle")
            issues = [
                "🚪 Landlord entering without notice",
                "🌡️ No heat or hot water",
                "🔧 Refusing to make repairs",
                "💰 Illegal fees or rent increases",
                "🐛 Pest infestations ignored",
                "🔒 Security deposit disputes"
            ]
            
            issue_cols = st.columns(2)
            for i, issue in enumerate(issues):
                with issue_cols[i % 2]:
                    st.write(issue)

if __name__ == "__main__":
    main()