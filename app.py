# RightsGuard - Streamlit UI for Multi-Agent Legal Rights Analyzer
import streamlit as st
import json
from datetime import datetime
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
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3cd;
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
        'idle': ['⏸️ Web Scraper', '⏸️ AI Analyzer', '⏸️ Letter Generator'],
        'scraping': ['🔄 Web Scraper', '⏸️ AI Analyzer', '⏸️ Letter Generator'],
        'analyzing': ['✅ Web Scraper', '🔄 AI Analyzer', '⏸️ Letter Generator'],
        'generating': ['✅ Web Scraper', '✅ AI Analyzer', '🔄 Letter Generator'],
        'complete': ['✅ Web Scraper', '✅ AI Analyzer', '✅ Letter Generator']
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
                    st.info("🕷️ Gathering legal information and building history...")
                
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
            analysis_text = result['analysis']['analysis']
            st.write(analysis_text)
            
            # Show sources
            with st.expander("📚 Legal Sources"):
                st.write("**Relevant Laws:**")
                for law in result['sources']['laws']:
                    st.write(f"• {law}")
                
                if result['sources']['violations']:
                    st.write("**NYC Violation Records:**")
                    for violation in result['sources']['violations'][:3]:
                        st.write(f"• {violation.get('violationtype', 'Violation')} - {violation.get('inspectiondate', 'Date unknown')}")
        
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
                **1. 🕷️ Smart Research**
                - Scrapes NYC housing laws
                - Checks violation databases
                - Reviews community complaints
                """)
            
            with demo_cols[1]:
                st.markdown("""
                **2. 🧠 AI Analysis**
                - NVIDIA-powered legal analysis
                - Compares your case to law
                - Identifies strongest arguments
                """)
            
            with demo_cols[2]:
                st.markdown("""
                **3. 📝 Professional Letter**
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