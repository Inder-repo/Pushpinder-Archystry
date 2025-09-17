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
                'domain': 'Services',
                'likelihood': 'Medium'
            },
            'ADV002': {
                'description': 'Data breach through application vulnerability',
                'impact': 'Critical',
                'domain': 'Applications',
                'likelihood': 'High'
            },
            'ADV003': {
                'description': 'Network intrusion attempt',
                'impact': 'Medium',
                'domain': 'Network',
                'likelihood': 'Medium'
            },
            'ADV004': {
                'description': 'Unauthorized access to sensitive data',
                'impact': 'High',
                'domain': 'Information',
                'likelihood': 'Medium'
            },
            'ADV005': {
                'description': 'Social engineering attacks on personnel',
                'impact': 'High',
                'domain': 'People',
                'likelihood': 'High'
            }
        }
    
    if 'mitigations' not in st.session_state:
        st.session_state.mitigations = {
            'MIT001': {
                'description': 'Multi-factor authentication implementation',
                'domain': 'Services',
                'mapped_risks': ['ADV001'],
                'effectiveness': 'High',
                'cost': 'Medium'
            },
            'MIT002': {
                'description': 'Security code review and testing',
                'domain': 'Applications',
                'mapped_risks': ['ADV002'],
                'effectiveness': 'High',
                'cost': 'Medium'
            },
            'MIT003': {
                'description': 'Network segmentation and monitoring',
                'domain': 'Network',
                'mapped_risks': ['ADV003'],
                'effectiveness': 'Medium',
                'cost': 'High'
            },
            'MIT004': {
                'description': 'Data encryption and access controls',
                'domain': 'Information',
                'mapped_risks': ['ADV004'],
                'effectiveness': 'High',
                'cost': 'Medium'
            },
            'MIT005': {
                'description': 'Security awareness training',
                'domain': 'People',
                'mapped_risks': ['ADV005'],
                'effectiveness': 'Medium',
                'cost': 'Low'
            }
        }
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None

# Domain positions for visual canvas
DOMAIN_POSITIONS = {
    'Enterprise': {'x': 0.5, 'y': 0.9, 'color': '#1976D2'},
    'Products': {'x': 0.15, 'y': 0.7, 'color': '#F57C00'},
    'Services': {'x': 0.5, 'y': 0.7, 'color': '#F57C00'},
    'Information': {'x': 0.85, 'y': 0.7, 'color': '#F57C00'},
    'People': {'x': 0.15, 'y': 0.5, 'color': '#7B1FA2'},
    'Process': {'x': 0.5, 'y': 0.5, 'color': '#7B1FA2'},
    'Facilities': {'x': 0.85, 'y': 0.5, 'color': '#7B1FA2'},
    'Applications': {'x': 0.2, 'y': 0.2, 'color': '#388E3C'},
    'Platforms': {'x': 0.4, 'y': 0.2, 'color': '#388E3C'},
    'Network': {'x': 0.6, 'y': 0.2, 'color': '#388E3C'},
    'Data': {'x': 0.8, 'y': 0.2, 'color': '#388E3C'}
}

def render_interactive_visual_canvas(project_data):
    """Render interactive visual canvas"""
    if not project_data:
        st.info("Create or select a project to start building your architecture canvas.")
        return
    
    st.markdown("### 🎨 Interactive Architecture Canvas")
    
    # Canvas controls
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        connection_mode = st.checkbox("🔗 Connection Mode", 
                                    help="Enable to create connections between domains")
    
    with col2:
        if 'canvas_connections' not in project_data:
            project_data['canvas_connections'] = []
        
        if st.button("🗑️ Clear All Connections"):
            project_data['canvas_connections'] = []
            st.rerun()
    
    with col3:
        show_details = st.checkbox("📋 Show Details", value=True)
    
    # Create visual canvas
    create_visual_canvas_html(project_data, show_details)
    
    # Connection creation interface
    if connection_mode:
        st.markdown("#### 🔗 Create New Connection")
        
        domains = list(DOMAIN_POSITIONS.keys())
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            source_domain = st.selectbox("From Domain", domains, key="conn_source")
        
        with col2:
            target_domain = st.selectbox("To Domain", 
                                       [d for d in domains if d != source_domain], 
                                       key="conn_target")
        
        with col3:
            available_risks = [k for k, v in st.session_state.risks.items()]
            interaction_risk = st.selectbox("Associated Risk", 
                                          ["None"] + available_risks, 
                                          key="conn_risk")
        
        with col4:
            available_mits = [k for k, v in st.session_state.mitigations.items()]
            interaction_mitigation = st.selectbox("Associated Mitigation", 
                                                ["None"] + available_mits, 
                                                key="conn_mitigation")
        
        interaction_type = st.selectbox("Interaction Type", [
            "<<creates>>", "<<manages>>", "<<uses>>", "<<serves>>", 
            "<<connects>>", "<<secures>>", "<<monitors>>", "<<controls>>"
        ], key="conn_type")
        
        if st.button("➕ Add Connection"):
            connection_id = f"{source_domain}-{target_domain}-{len(project_data['canvas_connections'])}"
            
            new_connection = {
                'id': connection_id,
                'source': source_domain,
                'target': target_domain,
                'type': interaction_type,
                'risk': interaction_risk if interaction_risk != "None" else None,
                'mitigation': interaction_mitigation if interaction_mitigation != "None" else None,
                'created': datetime.now().isoformat()
            }
            
            project_data['canvas_connections'].append(new_connection)
            st.success(f"✅ Connection created: {source_domain} {interaction_type} {target_domain}")
            st.rerun()
    
    # Display active connections
    if project_data.get('canvas_connections'):
        st.markdown("#### 🔗 Active Connections")
        
        for idx, conn in enumerate(project_data['canvas_connections']):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                risk_text = f" (Risk: {conn['risk']})" if conn['risk'] else ""
                mit_text = f" (Mitigation: {conn['mitigation']})" if conn['mitigation'] else ""
                st.write(f"**{conn['source']}** {conn['type']} **{conn['target']}**{risk_text}{mit_text}")
            
            with col2:
                if conn['risk'] and conn['risk'] in st.session_state.risks:
                    risk_info = st.session_state.risks[conn['risk']]
                    st.caption(f"🚨 {risk_info['description'][:50]}...")
            
            with col3:
                if st.button("🗑️", key=f"del_conn_{idx}"):
                    project_data['canvas_connections'].pop(idx)
                    st.rerun()

def create_visual_canvas_html(project_data, show_details=True):
    """Create visual canvas using a simpler table-based approach"""
    
    connections = project_data.get('canvas_connections', [])
    
    st.markdown("#### Security Architecture Canvas - Visual View")
    
    # Create a simple grid-based representation
    st.markdown("""
    <div style="background: #F8F9FA; padding: 20px; border: 2px solid #E0E0E0; border-radius: 12px;">
    """, unsafe_allow_html=True)
    
    # Enterprise Layer
    st.markdown("**Enterprise Layer**")
    col1, col2, col3 = st.columns(3)
    with col2:
        render_domain_node("Enterprise", DOMAIN_POSITIONS["Enterprise"]["color"], project_data, connections, show_details)
    
    st.markdown("---")
    
    # Business Layer
    st.markdown("**Business Layer**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_domain_node("Products", DOMAIN_POSITIONS["Products"]["color"], project_data, connections, show_details)
    with col2:
        render_domain_node("Services", DOMAIN_POSITIONS["Services"]["color"], project_data, connections, show_details)
    with col3:
        render_domain_node("Information", DOMAIN_POSITIONS["Information"]["color"], project_data, connections, show_details)
    
    st.markdown("---")
    
    # Application Layer  
    st.markdown("**Application Layer**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_domain_node("People", DOMAIN_POSITIONS["People"]["color"], project_data, connections, show_details)
    with col2:
        render_domain_node("Process", DOMAIN_POSITIONS["Process"]["color"], project_data, connections, show_details)
    with col3:
        render_domain_node("Facilities", DOMAIN_POSITIONS["Facilities"]["color"], project_data, connections, show_details)
    
    st.markdown("---")
    
    # Technology Layer
    st.markdown("**Technology Layer**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_domain_node("Applications", DOMAIN_POSITIONS["Applications"]["color"], project_data, connections, show_details)
    with col2:
        render_domain_node("Platforms", DOMAIN_POSITIONS["Platforms"]["color"], project_data, connections, show_details)
    with col3:
        render_domain_node("Network", DOMAIN_POSITIONS["Network"]["color"], project_data, connections, show_details)
    with col4:
        render_domain_node("Data", DOMAIN_POSITIONS["Data"]["color"], project_data, connections, show_details)
    
    # Connection summary
    if connections:
        st.markdown("---")
        st.markdown("**Active Connections:**")
        
        for conn in connections:
            conn_type = conn['type'].replace('<<', '').replace('>>', '')
            
            if conn['risk']:
                st.markdown(f"🔴 **{conn['source']}** {conn_type} **{conn['target']}** ⚠️ (Risk: {conn['risk']})")
            elif conn['mitigation']:
                st.markdown(f"🟢 **{conn['source']}** {conn_type} **{conn['target']}** 🛡️ (Mitigation: {conn['mitigation']})")
            else:
                st.markdown(f"🔵 **{conn['source']}** {conn_type} **{conn['target']}**")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_domain_node(domain_name, color, project_data, connections, show_details):
    """Render a single domain node"""
    
    elements_count = len(project_data.get(f'{domain_name}_elements', []))
    risks_count = len(project_data.get(f'{domain_name}_risks', []))
    mits_count = len(project_data.get(f'{domain_name}_mitigations', []))
    connection_count = len([c for c in connections if c['source'] == domain_name or c['target'] == domain_name])
    
    # Create node styling
    node_html = f"""
    <div style="background: {color}; color: white; padding: 15px; border-radius: 12px; 
                text-align: center; margin: 5px; min-height: 80px;
                border: 3px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h4 style="margin: 0; font-size: 14px;">{domain_name}</h4>
    """
    
    if show_details:
        node_html += f"""
        <div style="font-size: 10px; margin-top: 5px; opacity: 0.9;">
            📦 Elements: {elements_count}<br>
            ⚠️ Risks: {risks_count}<br>
            🛡️ Mitigations: {mits_count}<br>
            🔗 Connections: {connection_count}
        </div>
        """
    
    node_html += "</div>"
    
    st.markdown(node_html, unsafe_allow_html=True)

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
        st.metric("🔵 Open", open_projects)
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
        total_elements = sum(len(project_info.get(f'{domain}_elements', [])) for domain in domains)
        total_risks = sum(len(project_info.get(f'{domain}_risks', [])) for domain in domains)
        total_mitigations = sum(len(project_info.get(f'{domain}_mitigations', [])) for domain in domains)
        total_connections = len(project_info.get('canvas_connections', []))
        completion = calculate_completion_score(project_info)
        
        project_data.append({
            'Project Name': project_name,
            'Status': project_info['status'],
            'Owner': project_info['owner'],
            'Elements': total_elements,
            'Connections': total_connections,
            'Risks': total_risks,
            'Mitigations': total_mitigations,
            'Completion %': completion,
            'Created': project_info['created_date'][:10]
        })
    
    if project_data:
        df = pd.DataFrame(project_data)
        st.dataframe(df, use_container_width=True)
    
    # Analytics section
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Project Analytics")
        
        if total_projects > 0:
            st.write("**Project Status Distribution:**")
            
            open_pct = (open_projects / total_projects) * 100
            progress_pct = (in_progress_projects / total_projects) * 100
            closed_pct = (closed_projects / total_projects) * 100
            
            st.write(f"🔵 **Open:** {open_projects} projects ({open_pct:.1f}%)")
            st.progress(open_pct / 100)
            
            st.write(f"🟡 **In Progress:** {in_progress_projects} projects ({progress_pct:.1f}%)")
            st.progress(progress_pct / 100)
            
            st.write(f"🟢 **Completed:** {closed_projects} projects ({closed_pct:.1f}%)")
            st.progress(closed_pct / 100)
            
            status_df = pd.DataFrame({
                'Status': ['Open', 'In Progress', 'Closed'],
                'Count': [open_projects, in_progress_projects, closed_projects]
            })
            st.bar_chart(status_df.set_index('Status'))
        else:
            st.info("No project data available")
    
    with col2:
        st.subheader("🏗️ Architecture Complexity")
        
        domain_totals = {}
        for domain in domains:
            total = sum(len(project_info.get(f'{domain}_elements', [])) 
                       for project_info in st.session_state.projects.values())
            if total > 0:
                domain_totals[domain] = total
        
        if domain_totals:
            domain_df = pd.DataFrame(
                list(domain_totals.items()), 
                columns=['Domain', 'Elements']
            )
            
            st.bar_chart(domain_df.set_index('Domain'))
            
            st.write("**Domain Element Summary:**")
            for domain, count in sorted(domain_totals.items(), key=lambda x: x[1], reverse=True):
                st.write(f"• **{domain}:** {count} elements")
        else:
            st.info("No domain elements defined yet")

def admin_section():
    """Admin section for managing master data"""
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

def project_management():
    """Project management with canvas and domain management"""
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
                    'canvas_connections': [],
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
        render_interactive_visual_canvas(project_data)
        
        # Domain management interface
        render_domain_management(project_data)

def render_domain_management(project_data):
    """Render domain management interface"""
    st.markdown("### 🏗️ Domain Management")
    
    domains = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
    
    selected_domain = st.selectbox("Select Domain to Manage", domains)
    
    elements_key = f'{selected_domain}_elements'
    risks_key = f'{selected_domain}_risks'
    mitigations_key = f'{selected_domain}_mitigations'
    
    # Initialize if not exists
    if elements_key not in project_data:
        project_data[elements_key] = []
    if risks_key not in project_data:
        project_data[risks_key] = []
    if mitigations_key not in project_data:
        project_data[mitigations_key] = []
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader(f"📦 {selected_domain} Elements")
        
        # Add new element
        new_element = st.text_input(f"Add element to {selected_domain}")
        if st.button(f"Add Element"):
            if new_element and new_element not in project_data[elements_key]:
                project_data[elements_key].append(new_element)
                st.success(f"Added {new_element}")
                st.rerun()
        
        # Display existing elements
        if project_data[elements_key]:
            for i, element in enumerate(project_data[elements_key]):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.write(f"• {element}")
                with col_b:
                    if st.button("🗑️", key=f"del_elem_{selected_domain}_{i}"):
                        project_data[elements_key].remove(element)
                        st.rerun()
        else:
            st.info("No elements defined")
    
    with col2:
        st.subheader(f"⚠️ {selected_domain} Risks")
        
        # Assign risks
        available_risks = list(st.session_state.risks.keys())
        selected_risks = st.multiselect(
            "Assign risks",
            available_risks,
            default=project_data[risks_key],
            format_func=lambda x: f"{x}: {st.session_state.risks[x]['description'][:30]}..."
        )
        project_data[risks_key] = selected_risks
        
        # Display risk details
        if selected_risks:
            for risk_id in selected_risks:
                risk_info = st.session_state.risks[risk_id]
                st.write(f"**{risk_id}:** {risk_info['description'][:50]}...")
                st.caption(f"Impact: {risk_info['impact']}")
        else:
            st.info("No risks assigned")
    
    with col3:
        st.subheader(f"🛡️ {selected_domain} Mitigations")
        
        # Assign mitigations
        available_mitigations = list(st.session_state.mitigations.keys())
        selected_mitigations = st.multiselect(
            "Assign mitigations",
            available_mitigations,
            default=project_data[mitigations_key],
            format_func=lambda x: f"{x}: {st.session_state.mitigations[x]['description'][:30]}..."
        )
        project_data[mitigations_key] = selected_mitigations
        
        # Display mitigation details
        if selected_mitigations:
            for mit_id in selected_mitigations:
                mit_info = st.session_state.mitigations[mit_id]
                st.write(f"**{mit_id}:** {mit_info['description'][:50]}...")
                if mit_info.get('mapped_risks'):
                    st.caption(f"Addresses: {', '.join(mit_info['mapped_risks'])}")
        else:
            st.info("No mitigations assigned")

def calculate_completion_score(project_data):
    """Calculate project completion percentage"""
    score = 0
    domains = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
    
    # Domain elements (30 points)
    populated_domains = sum(1 for domain in domains 
                           if len(project_data.get(f'{domain}_elements', [])) > 0)
    score += (populated_domains / len(domains)) * 30
    
    # Connections (25 points)
    connections = len(project_data.get('canvas_connections', []))
    if connections > 0:
        score += min(25, connections * 5)
    
    # Risk assignment (25 points)
    total_risks = sum(len(project_data.get(f'{domain}_risks', [])) for domain in domains)
    if total_risks > 0:
        score += min(25, total_risks * 3)
    
    # Mitigation assignment (20 points)
    total_mitigations = sum(len(project_data.get(f'{domain}_mitigations', [])) for domain in domains)
    if total_mitigations > 0:
        score += min(20, total_mitigations * 3)
    
    return min(100, int(score))

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
        st.sidebar.metric("Connections", len(project_data.get('canvas_connections', [])))
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
    
    # Handle redirects
    if getattr(st.session_state, 'redirect_to_projects', False):
        st.session_state.redirect_to_projects = False
        page = "📁 Project Canvas"
    
    # Main content routing
    try:
        if page.startswith("🏠"):
            dashboard()
        elif page.startswith("📁"):
            project_management()
        elif page.startswith("🔧"):
            admin_section()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()
