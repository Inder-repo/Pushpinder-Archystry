import streamlit as st
import pandas as pd
from datetime import datetime
import json
import uuid
from typing import Dict, List, Any

# Page config
st.set_page_config(
    page_title="Security Architecture Canvas",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
def initialize_session_state():
    if 'projects' not in st.session_state:
        st.session_state.projects = {}
    
    if 'risks' not in st.session_state:
        st.session_state.risks = {
            'ADV001': {
                'description': 'Adversary compromises customer credentials',
                'impact': 'High',
                'domain': 'Services'
            },
            'ADV002': {
                'description': 'Data breach through application vulnerability',
                'impact': 'Critical',
                'domain': 'Applications'
            },
            'ADV003': {
                'description': 'Network intrusion attempt',
                'impact': 'Medium',
                'domain': 'Network'
            },
            'ADV004': {
                'description': 'Unauthorized access to sensitive data',
                'impact': 'High',
                'domain': 'Information'
            },
            'ADV005': {
                'description': 'Social engineering attacks on personnel',
                'impact': 'High',
                'domain': 'People'
            }
        }
    
    if 'mitigations' not in st.session_state:
        st.session_state.mitigations = {
            'MIT001': {
                'description': 'Multi-factor authentication implementation',
                'domain': 'Services',
                'mapped_risks': ['ADV001']
            },
            'MIT002': {
                'description': 'Security code review and testing',
                'domain': 'Applications',
                'mapped_risks': ['ADV002']
            },
            'MIT003': {
                'description': 'Network segmentation and monitoring',
                'domain': 'Network',
                'mapped_risks': ['ADV003']
            },
            'MIT004': {
                'description': 'Data encryption and access controls',
                'domain': 'Information',
                'mapped_risks': ['ADV004']
            },
            'MIT005': {
                'description': 'Security awareness training',
                'domain': 'People',
                'mapped_risks': ['ADV005']
            }
        }
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None

# ArchiMate-style interactions based on the reference image
ARCHIMATE_INTERACTIONS = [
    # Enterprise Domain connections
    "<<creates>>",
    "<<packages>>",
    "<<has>>",
    "<<expose/manipulate>>",
    "<<manipulate>>",
    "<<expose>>",
    
    # Business Layer connections
    "<<define>>",
    "<<builds>>",
    "<<request>>",
    "<<deliver>>",
    "<<manage>>",
    "<<describe>>",
    "<<execute>>",
    "<<structure>>",
    "<<contain>>",
    
    # Operational Layer connections
    "<<support>>",
    "<<use>>",
    "<<connect>>",
    "<<transfer>>",
    "<<represents>>",
    
    # Technology Layer connections
    "<<host>>",
    "<<connects>>",
    "<<transform>>"
]

def render_interactive_canvas(project_data):
    """Render the main interactive canvas matching ArchiMate style"""
    if not project_data:
        st.info("Create or select a project to start building your architecture canvas.")
        return
    
    st.markdown("""
    <style>
    .archimate-domain {
        border: 2px solid;
        border-radius: 8px;
        padding: 20px;
        margin: 10px;
        position: relative;
        background: white;
        min-height: 200px;
    }
    
    .enterprise-domain {
        border-color: #1976D2;
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-style: solid;
    }
    
    .business-domain {
        border-color: #F57C00;
        background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
        border-style: dashed;
    }
    
    .operational-domain {
        border-color: #7B1FA2;
        background: linear-gradient(135deg, #F3E5F5 0%, #E1BEE7 100%);
        border-style: solid;
    }
    
    .technology-domain {
        border-color: #388E3C;
        background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%);
        border-style: solid;
    }
    
    .domain-header {
        font-weight: bold;
        font-size: 14px;
        text-align: center;
        margin-bottom: 15px;
        padding: 5px;
        background: rgba(255,255,255,0.8);
        border-radius: 4px;
    }
    
    .domain-element {
        background: rgba(255,255,255,0.9);
        border: 1px solid #ccc;
        border-radius: 4px;
        padding: 8px;
        margin: 5px;
        display: inline-block;
        font-size: 12px;
        min-width: 80px;
        text-align: center;
    }
    
    .risk-element {
        background: #FFEBEE;
        border: 1px solid #E57373;
        color: #C62828;
        border-radius: 3px;
        padding: 4px 6px;
        margin: 2px;
        font-size: 10px;
        display: inline-block;
    }
    
    .mitigation-element {
        background: #E8F5E8;
        border: 1px solid #66BB6A;
        color: #2E7D32;
        border-radius: 3px;
        padding: 4px 6px;
        margin: 2px;
        font-size: 10px;
        display: inline-block;
    }
    
    .interaction-line {
        position: absolute;
        border-top: 2px solid #424242;
        z-index: 10;
    }
    
    .interaction-label {
        background: white;
        border: 1px solid #424242;
        padding: 2px 6px;
        font-size: 10px;
        position: absolute;
        top: -12px;
        left: 50%;
        transform: translateX(-50%);
    }
    
    .canvas-container {
        position: relative;
        background: #F5F5F5;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 20px;
        min-height: 800px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Canvas container
    st.markdown('<div class="canvas-container">', unsafe_allow_html=True)
    
    # Enterprise Domain (Top Level)
    st.markdown("""
    <div class="archimate-domain enterprise-domain" style="margin-bottom: 20px;">
        <div class="domain-header">AEF:LOC:0000 - Enterprise Domain</div>
        <div style="display: flex; justify-content: space-around;">
            <div class="domain-element">
                <strong>AEF:LOC:0040</strong><br>Financial Value
            </div>
            <div class="domain-element">
                <strong>AEF:LOC:0039</strong><br>Business Value
            </div>
            <div class="domain-element">
                <strong>AEF:LOC:0041</strong><br>Social Impact
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Business Layer
    st.markdown("### Business Layer")
    
    col1, col2, col3 = st.columns(3)
    
    # Products Domain
    with col1:
        render_expandable_domain("Products", "AEF:LOC:0006", "business-domain", project_data)
    
    # Services Domain  
    with col2:
        render_expandable_domain("Services", "AEF:LOC:0002", "business-domain", project_data)
    
    # Information Domain
    with col3:
        render_expandable_domain("Information", "AEF:LOC:0003", "business-domain", project_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Operational Layer
    st.markdown("### Operational Layer")
    
    col1, col2, col3 = st.columns(3)
    
    # People Domain
    with col1:
        render_expandable_domain("People", "AEF:LOC:0004", "operational-domain", project_data)
    
    # Process Domain
    with col2:
        render_expandable_domain("Process", "AEF:LOC:0005", "operational-domain", project_data)
    
    # Facilities Domain
    with col3:
        render_expandable_domain("Facilities", "AEF:LOC:0007", "operational-domain", project_data)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Layer
    st.markdown("### Information Technology Layer")
    
    st.markdown("""
    <div class="archimate-domain technology-domain" style="margin-bottom: 20px;">
        <div class="domain-header">Information Technology</div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Applications
    with col1:
        render_tech_subdomain("Applications", "AEF:LOC:0016", project_data)
    
    # Platforms
    with col2:
        render_tech_subdomain("Platforms", "AEF:LOC:0017", project_data)
    
    # Network
    with col3:
        render_tech_subdomain("Network", "AEF:LOC:0018", project_data)
    
    # Data
    with col4:
        render_tech_subdomain("Data", "AEF:LOC:0019", project_data)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Interaction Controls
    render_interaction_controls(project_data)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_expandable_domain(domain_name, domain_id, css_class, project_data):
    """Render an expandable domain with inline editing capabilities"""
    elements_key = f'{domain_name}_elements'
    risks_key = f'{domain_name}_risks'
    mitigations_key = f'{domain_name}_mitigations'
    
    # Initialize if not exists
    if elements_key not in project_data:
        project_data[elements_key] = ['Customer', 'User', 'Admin'] if domain_name == 'People' else []
    if risks_key not in project_data:
        project_data[risks_key] = []
    if mitigations_key not in project_data:
        project_data[mitigations_key] = []
    
    # Domain container
    domain_html = f"""
    <div class="archimate-domain {css_class}">
        <div class="domain-header">{domain_id}<br>{domain_name}</div>
    """
    
    # Elements section
    if project_data[elements_key]:
        domain_html += "<div style='margin-bottom: 10px;'>"
        for element in project_data[elements_key]:
            domain_html += f'<div class="domain-element">{element}</div>'
        domain_html += "</div>"
    
    # Risks section
    if project_data[risks_key]:
        domain_html += "<div style='margin-bottom: 8px;'><strong style='font-size: 11px;'>Risks:</strong><br>"
        for risk in project_data[risks_key]:
            risk_desc = st.session_state.risks.get(risk, {}).get('description', risk)[:30]
            domain_html += f'<div class="risk-element">⚠️ {risk}</div>'
        domain_html += "</div>"
    
    # Mitigations section
    if project_data[mitigations_key]:
        domain_html += "<div style='margin-bottom: 8px;'><strong style='font-size: 11px;'>Mitigations:</strong><br>"
        for mitigation in project_data[mitigations_key]:
            mit_desc = st.session_state.mitigations.get(mitigation, {}).get('description', mitigation)[:30]
            domain_html += f'<div class="mitigation-element">🛡️ {mitigation}</div>'
        domain_html += "</div>"
    
    domain_html += "</div>"
    
    st.markdown(domain_html, unsafe_allow_html=True)
    
    # Inline editing controls
    with st.expander(f"✏️ Edit {domain_name}", expanded=False):
        # Add elements
        st.write("**Add Elements:**")
        new_element = st.text_input(f"New element for {domain_name}", key=f"add_element_{domain_name}")
        if st.button(f"Add Element", key=f"btn_add_{domain_name}"):
            if new_element and new_element not in project_data[elements_key]:
                project_data[elements_key].append(new_element)
                st.success(f"Added {new_element}")
                st.rerun()
        
        # Manage existing elements
        if project_data[elements_key]:
            st.write("**Current Elements:**")
            for i, element in enumerate(project_data[elements_key]):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"• {element}")
                with col2:
                    if st.button("🗑️", key=f"del_element_{domain_name}_{i}"):
                        project_data[elements_key].remove(element)
                        st.rerun()
        
        # Add risks
        st.write("**Assign Risks:**")
        available_risks = [k for k, v in st.session_state.risks.items() 
                          if v.get('domain') == domain_name or v.get('domain') == '']
        
        if available_risks:
            selected_risks = st.multiselect(
                "Select risks",
                available_risks,
                default=project_data[risks_key],
                key=f"risks_multi_{domain_name}",
                format_func=lambda x: f"{x}: {st.session_state.risks[x]['description'][:40]}..."
            )
            project_data[risks_key] = selected_risks
        
        # Add mitigations
        st.write("**Assign Mitigations:**")
        available_mitigations = [k for k, v in st.session_state.mitigations.items() 
                               if v.get('domain') == domain_name or v.get('domain') == '']
        
        if available_mitigations:
            selected_mitigations = st.multiselect(
                "Select mitigations",
                available_mitigations,
                default=project_data[mitigations_key],
                key=f"mitigations_multi_{domain_name}",
                format_func=lambda x: f"{x}: {st.session_state.mitigations[x]['description'][:40]}..."
            )
            project_data[mitigations_key] = selected_mitigations

def render_tech_subdomain(subdomain_name, subdomain_id, project_data):
    """Render technology subdomains"""
    elements_key = f'{subdomain_name}_elements'
    risks_key = f'{subdomain_name}_risks'
    mitigations_key = f'{subdomain_name}_mitigations'
    
    # Initialize if not exists
    if elements_key not in project_data:
        project_data[elements_key] = []
    if risks_key not in project_data:
        project_data[risks_key] = []
    if mitigations_key not in project_data:
        project_data[mitigations_key] = []
    
    # Subdomain container
    subdomain_html = f"""
    <div style="border: 1px solid #388E3C; border-radius: 4px; padding: 15px; margin: 5px; background: rgba(255,255,255,0.7); min-height: 180px;">
        <div style="font-weight: bold; font-size: 12px; text-align: center; margin-bottom: 10px;">
            {subdomain_id}<br>{subdomain_name}
        </div>
    """
    
    # Elements
    if project_data[elements_key]:
        for element in project_data[elements_key]:
            subdomain_html += f'<div class="domain-element" style="font-size: 10px; padding: 4px; margin: 2px;">{element}</div>'
    
    # Risks
    if project_data[risks_key]:
        subdomain_html += "<br><div style='font-size: 10px; font-weight: bold;'>Risks:</div>"
        for risk in project_data[risks_key]:
            subdomain_html += f'<div class="risk-element" style="font-size: 9px;">⚠️ {risk}</div>'
    
    # Mitigations
    if project_data[mitigations_key]:
        subdomain_html += "<br><div style='font-size: 10px; font-weight: bold;'>Mitigations:</div>"
        for mitigation in project_data[mitigations_key]:
            subdomain_html += f'<div class="mitigation-element" style="font-size: 9px;">🛡️ {mitigation}</div>'
    
    subdomain_html += "</div>"
    
    st.markdown(subdomain_html, unsafe_allow_html=True)
    
    # Inline editing
    with st.expander(f"✏️ {subdomain_name}", expanded=False):
        # Add elements
        new_element = st.text_input(f"Add to {subdomain_name}", key=f"add_{subdomain_name}")
        if st.button(f"Add", key=f"btn_{subdomain_name}"):
            if new_element and new_element not in project_data[elements_key]:
                project_data[elements_key].append(new_element)
                st.rerun()
        
        # Manage risks and mitigations
        available_risks = [k for k, v in st.session_state.risks.items() 
                          if v.get('domain') == subdomain_name]
        if available_risks:
            selected_risks = st.multiselect(
                "Risks", available_risks, default=project_data[risks_key],
                key=f"tech_risks_{subdomain_name}"
            )
            project_data[risks_key] = selected_risks
        
        available_mitigations = [k for k, v in st.session_state.mitigations.items() 
                               if v.get('domain') == subdomain_name]
        if available_mitigations:
            selected_mitigations = st.multiselect(
                "Mitigations", available_mitigations, default=project_data[mitigations_key],
                key=f"tech_mits_{subdomain_name}"
            )
            project_data[mitigations_key] = selected_mitigations

def render_interaction_controls(project_data):
    """Render interaction controls and visual connections"""
    st.markdown("---")
    st.markdown("### 🔄 Architecture Interactions")
    
    # Interaction selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_interactions = st.multiselect(
            "Select Active Interactions (ArchiMate Style)",
            ARCHIMATE_INTERACTIONS,
            default=project_data.get('selected_interactions', []),
            help="Select interactions to show relationships between domains"
        )
        project_data['selected_interactions'] = selected_interactions
    
    with col2:
        if st.button("🔄 Refresh Canvas"):
            st.rerun()
    
    # Display active interactions with visual representation
    if selected_interactions:
        st.markdown("#### Active Interactions:")
        
        interaction_display = """
        <div style='background: #F8F9FA; padding: 15px; border-radius: 8px; border: 1px solid #DEE2E6;'>
        """
        
        for interaction in selected_interactions:
            interaction_display += f"""
            <div style='display: inline-block; background: white; border: 1px solid #6C757D; 
                        border-radius: 20px; padding: 5px 15px; margin: 5px; font-size: 12px;'>
                {interaction}
            </div>
            """
        
        interaction_display += "</div>"
        st.markdown(interaction_display, unsafe_allow_html=True)
        
        # Visual connection representation
        st.markdown("""
        <div style='margin-top: 20px; padding: 15px; background: #FFF3CD; border-radius: 8px; border: 1px solid #FFEAA7;'>
            <strong>📊 Visual Connections:</strong><br>
            The selected interactions create relationships between architecture domains as shown in the canvas above.
            Each interaction type (<<creates>>, <<manages>>, etc.) represents different architectural relationships
            following ArchiMate modeling standards.
        </div>
        """, unsafe_allow_html=True)

def project_management():
    """Streamlined project management focused on canvas work"""
    st.header("📁 Project Management")
    
    # Project selection/creation
    col1, col2 = st.columns([3, 1])
    
    with col1:
        project_names = list(st.session_state.projects.keys()) if st.session_state.projects else []
        selected_project = st.selectbox(
            "Select or Create Project",
            ["➕ Create New Project..."] + project_names,
            index=0 if not st.session_state.current_project else 
            project_names.index(st.session_state.current_project) + 1 if st.session_state.current_project in project_names else 0
        )
    
    with col2:
        if st.button("🗑️ Delete Project", disabled=selected_project == "➕ Create New Project..."):
            if selected_project in st.session_state.projects:
                del st.session_state.projects[selected_project]
                st.session_state.current_project = None
                st.success(f"Project '{selected_project}' deleted!")
                st.rerun()
    
    if selected_project == "➕ Create New Project...":
        st.subheader("🆕 Create New Project")
        
        col1, col2 = st.columns(2)
        with col1:
            new_project_name = st.text_input("Project Name", placeholder="e.g., Customer Portal Security Architecture")
            project_description = st.text_area("Project Description", placeholder="Brief description of the architecture project")
        
        with col2:
            project_owner = st.text_input("Project Owner", placeholder="Your name")
            project_status = st.selectbox("Initial Status", ["Open", "In Progress", "Closed"])
        
        if st.button("🚀 Create Project"):
            if new_project_name:
                project_id = str(uuid.uuid4())[:8]
                st.session_state.projects[new_project_name] = {
                    'id': project_id,
                    'description': project_description,
                    'owner': project_owner,
                    'status': project_status,
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'selected_interactions': [],
                    # Initialize all domain elements
                    'People_elements': ['Customer', 'User', 'Admin'],
                    'Services_elements': [],
                    'Applications_elements': [],
                    'Network_elements': [],
                    'Data_elements': [],
                    'Information_elements': [],
                    'Products_elements': [],
                    'Process_elements': [],
                    'Facilities_elements': [],
                    'Platforms_elements': [],
                    # Initialize risks and mitigations
                    'People_risks': [], 'Services_risks': [], 'Applications_risks': [], 'Network_risks': [],
                    'Data_risks': [], 'Information_risks': [], 'Products_risks': [], 'Process_risks': [],
                    'Facilities_risks': [], 'Platforms_risks': [],
                    'People_mitigations': [], 'Services_mitigations': [], 'Applications_mitigations': [], 
                    'Network_mitigations': [], 'Data_mitigations': [], 'Information_mitigations': [],
                    'Products_mitigations': [], 'Process_mitigations': [], 'Facilities_mitigations': [], 
                    'Platforms_mitigations': []
                }
                st.session_state.current_project = new_project_name
                st.success(f"✅ Project '{new_project_name}' created successfully!")
                st.rerun()
    
    else:
        st.session_state.current_project = selected_project
        project_data = st.session_state.projects[selected_project]
        
        # Project header info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Project ID", project_data['id'])
        with col2:
            new_status = st.selectbox("Status", ["Open", "In Progress", "Closed"], 
                                    index=["Open", "In Progress", "Closed"].index(project_data['status']))
            if new_status != project_data['status']:
                project_data['status'] = new_status
                st.rerun()
        with col3:
            st.write(f"**Owner:** {project_data['owner']}")
            st.write(f"**Created:** {project_data['created_date'][:10]}")
        
        if project_data['description']:
            st.info(f"📋 **Description:** {project_data['description']}")
        
        st.markdown("---")
        
        # Main interactive canvas
        render_interactive_canvas(project_data)
        
        # Project save controls and status management
        render_project_save_controls(selected_project, project_data)

def admin_section():
    """Simplified admin section for managing master data"""
    st.header("🔧 Administration")
    
    tab1, tab2 = st.tabs(["🚨 Risk Library", "🛡️ Mitigation Library"])
    
    with tab1:
        st.subheader("Risk Library Management")
        
        # Add new risk
        with st.expander("➕ Add New Risk"):
            col1, col2 = st.columns(2)
            with col1:
                risk_id = st.text_input("Risk ID", placeholder="ADV006")
                risk_description = st.text_area("Risk Description")
            with col2:
                risk_impact = st.selectbox("Impact Level", ["Low", "Medium", "High", "Critical"])
                risk_domain = st.selectbox("Primary Domain", 
                    ["", "People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"])
            
            if st.button("➕ Add Risk"):
                if risk_id and risk_description:
                    st.session_state.risks[risk_id] = {
                        'description': risk_description,
                        'impact': risk_impact,
                        'domain': risk_domain
                    }
                    st.success(f"✅ Risk {risk_id} added successfully!")
                    st.rerun()
        
        # Display existing risks
        if st.session_state.risks:
            st.subheader("Current Risk Library")
            for risk_id, risk_info in st.session_state.risks.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{risk_id}:** {risk_info['description']}")
                    st.caption(f"Impact: {risk_info['impact']} | Domain: {risk_info.get('domain', 'General')}")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_risk_{risk_id}"):
                        st.info("Edit functionality - to be implemented")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_risk_{risk_id}"):
                        del st.session_state.risks[risk_id]
                        st.success(f"Risk {risk_id} deleted!")
                        st.rerun()
                st.markdown("---")
    
    with tab2:
        st.subheader("Mitigation Library Management")
        
        # Add new mitigation
        with st.expander("➕ Add New Mitigation"):
            col1, col2 = st.columns(2)
            with col1:
                mit_id = st.text_input("Mitigation ID", placeholder="MIT006")
                mit_description = st.text_area("Mitigation Description")
            with col2:
                mit_domain = st.selectbox("Implementation Domain", 
                    ["", "People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"])
                available_risks = list(st.session_state.risks.keys())
                mapped_risks = st.multiselect("Addresses Risks", available_risks)
            
            if st.button("➕ Add Mitigation"):
                if mit_id and mit_description:
                    st.session_state.mitigations[mit_id] = {
                        'description': mit_description,
                        'domain': mit_domain,
                        'mapped_risks': mapped_risks
                    }
                    st.success(f"✅ Mitigation {mit_id} added successfully!")
                    st.rerun()
        
        # Display existing mitigations
        if st.session_state.mitigations:
            st.subheader("Current Mitigation Library")
            for mit_id, mit_info in st.session_state.mitigations.items():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{mit_id}:** {mit_info['description']}")
                    st.caption(f"Domain: {mit_info.get('domain', 'General')} | Addresses: {', '.join(mit_info.get('mapped_risks', []))}")
                with col2:
                    if st.button("✏️ Edit", key=f"edit_mit_{mit_id}"):
                        st.info("Edit functionality - to be implemented")
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_mit_{mit_id}"):
                        del st.session_state.mitigations[mit_id]
                        st.success(f"Mitigation {mit_id} deleted!")
                        st.rerun()
                st.markdown("---")

def dashboard():
    """Dashboard with project overview and statistics"""
    st.header("📊 Architecture Dashboard")
    
    if not st.session_state.projects:
        st.info("🚀 No projects yet. Create your first security architecture project to get started!")
        
        if st.button("➕ Create First Project"):
            st.session_state.redirect_to_projects = True
            st.rerun()
        return
    
    # Overall statistics
    total_projects = len(st.session_state.projects)
    open_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'Open')
    in_progress_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'In Progress')
    closed_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'Closed')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📁 Total Projects", total_projects)
    with col2:
        st.metric("🟢 Open", open_projects)
    with col3:
        st.metric("🟡 In Progress", in_progress_projects)
    with col4:
        st.metric("🟢 Completed", closed_projects)
    
    st.markdown("---")
    
    # Project overview table
    st.subheader("📋 Project Overview")
    
    project_data = []
    domains = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
    
    for project_name, project_info in st.session_state.projects.items():
        # Count elements across domains
        total_elements = sum(len(project_info.get(f'{domain}_elements', [])) for domain in domains)
        # Count risks across domains
        total_risks = sum(len(project_info.get(f'{domain}_risks', [])) for domain in domains)
        # Count mitigations across domains
        total_mitigations = sum(len(project_info.get(f'{domain}_mitigations', [])) for domain in domains)
        # Count interactions
        total_interactions = len(project_info.get('selected_interactions', []))
        
        project_data.append({
            'Project Name': project_name,
            'Status': project_info['status'],
            'Owner': project_info['owner'],
            'Elements': total_elements,
            'Interactions': total_interactions,
            'Risks': total_risks,
            'Mitigations': total_mitigations,
            'Created': project_info['created_date'][:10]
        })
    
    if project_data:
        df = pd.DataFrame(project_data)
        st.dataframe(df, use_container_width=True)
    
    # Analytics section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Project Status Distribution")
        if total_projects > 0:
            status_data = pd.DataFrame({
                'Status': ['Open', 'In Progress', 'Closed'],
                'Count': [open_projects, in_progress_projects, closed_projects]
            })
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("No project data available")
    
    with col2:
        st.subheader("🏗️ Elements by Domain")
        domain_totals = {}
        for domain in domains:
            total = sum(len(project_info.get(f'{domain}_elements', [])) 
                       for project_info in st.session_state.projects.values())
            if total > 0:
                domain_totals[domain] = total
        
        if domain_totals:
            domain_df = pd.DataFrame(list(domain_totals.items()), columns=['Domain', 'Elements'])
            st.bar_chart(domain_df.set_index('Domain'))
        else:
            st.info("No domain elements defined yet")
    
    # Risk and mitigation overview
    st.markdown("---")
    st.subheader("🚨 Security Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Risk Library Summary:**")
        risk_by_impact = {}
        for risk_info in st.session_state.risks.values():
            impact = risk_info.get('impact', 'Unknown')
            risk_by_impact[impact] = risk_by_impact.get(impact, 0) + 1
        
        if risk_by_impact:
            for impact, count in risk_by_impact.items():
                st.write(f"• {impact}: {count} risks")
        else:
            st.info("No risks defined")
    
    with col2:
        st.write("**Mitigation Library Summary:**")
        mit_by_domain = {}
        for mit_info in st.session_state.mitigations.values():
            domain = mit_info.get('domain', 'General')
            mit_by_domain[domain] = mit_by_domain.get(domain, 0) + 1
        
        if mit_by_domain:
            for domain, count in mit_by_domain.items():
                st.write(f"• {domain}: {count} mitigations")
        else:
            st.info("No mitigations defined")

def main():
    """Main application function"""
    initialize_session_state()
    
    # Custom CSS for better visual appearance
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1976D2, #388E3C);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sidebar .sidebar-content {
        background: #F8F9FA;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #E0E0E0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Enterprise Security Architecture Canvas</h1>
        <p>ArchiMate-based Security Architecture Modeling & Risk Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.markdown("### 🧭 Navigation")
    
    page = st.sidebar.selectbox(
        "Select Page:",
        ["🏠 Dashboard", "📁 Project Canvas", "🔧 Administration"],
        format_func=lambda x: x.split(' ', 1)[1]  # Remove emoji from display
    )
    
    st.sidebar.markdown("---")
    
    # Current project information in sidebar
    if st.session_state.current_project:
        st.sidebar.markdown("### 📂 Current Project")
        st.sidebar.info(f"**{st.session_state.current_project}**")
        
        project_data = st.session_state.projects.get(st.session_state.current_project, {})
        st.sidebar.write(f"**Status:** {project_data.get('status', 'Unknown')}")
        st.sidebar.write(f"**Owner:** {project_data.get('owner', 'Unknown')}")
        
        # Quick stats
        domains = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
        total_elements = sum(len(project_data.get(f'{domain}_elements', [])) for domain in domains)
        total_risks = sum(len(project_data.get(f'{domain}_risks', [])) for domain in domains)
        total_mitigations = sum(len(project_data.get(f'{domain}_mitigations', [])) for domain in domains)
        
        st.sidebar.metric("Elements", total_elements)
        st.sidebar.metric("Risks", total_risks)  
        st.sidebar.metric("Mitigations", total_mitigations)
        st.sidebar.metric("Interactions", len(project_data.get('selected_interactions', [])))
    else:
        st.sidebar.markdown("### 📂 No Active Project")
        st.sidebar.info("Select or create a project to begin architecture modeling.")
    
    # Sidebar help and information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### 💡 Quick Help
    
    **🏠 Dashboard**: Overview of all projects and security metrics
    
    **📁 Project Canvas**: Main workspace for architecture modeling:
    - Create/select projects
    - Design interactive canvas
    - Add domain elements
    - Map risks & mitigations
    - Define interactions
    
    **🔧 Administration**: Manage master data:
    - Risk library
    - Mitigation library
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px;'>
        <p>🎯 <strong>Enterprise Security Architecture Canvas</strong></p>
        <p>ArchiMate-based modeling tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content routing
    if page.startswith("🏠"):
        dashboard()
    elif page.startswith("📁"):
        project_management()
    elif page.startswith("🔧"):
        admin_section()

if __name__ == "__main__":
    main()
