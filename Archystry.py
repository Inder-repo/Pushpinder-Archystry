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
                'interaction': 'Customer -> Services',
                'domain': 'Services'
            },
            'ADV002': {
                'description': 'Data breach through application vulnerability',
                'impact': 'Critical',
                'interaction': 'People -> Applications',
                'domain': 'Applications'
            },
            'ADV003': {
                'description': 'Network intrusion attempt',
                'impact': 'Medium',
                'interaction': 'Applications -> Network',
                'domain': 'Network'
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
                'description': 'Security code review process',
                'domain': 'Applications',
                'mapped_risks': ['ADV002']
            }
        }
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None

# Domain definitions based on the canvas
DOMAINS = {
    'Enterprise Domain': {
        'level': 1,
        'color': '#E8F4FD',
        'subdomains': {
            'Business Value': {'id': 'AEF:LOC:0039', 'color': '#B3E5FC'},
            'Financial Value': {'id': 'AEF:LOC:0040', 'color': '#B3E5FC'},
            'Social Impact': {'id': 'AEF:LOC:0041', 'color': '#B3E5FC'}
        }
    },
    'Products': {
        'level': 2,
        'color': '#FFF3E0',
        'id': 'AEF:LOC:0006',
        'subdomains': {}
    },
    'Services': {
        'level': 2,
        'color': '#FFF3E0',
        'id': 'AEF:LOC:0002',
        'subdomains': {}
    },
    'Information': {
        'level': 2,
        'color': '#FFF3E0',
        'id': 'AEF:LOC:0003',
        'subdomains': {}
    },
    'People': {
        'level': 3,
        'color': '#F3E5F5',
        'id': 'AEF:LOC:0004',
        'subdomains': {
            'Customer': {'color': '#E1BEE7'},
            'User': {'color': '#E1BEE7'},
            'Admin': {'color': '#E1BEE7'}
        }
    },
    'Process': {
        'level': 3,
        'color': '#F3E5F5',
        'id': 'AEF:LOC:0005',
        'subdomains': {}
    },
    'Facilities': {
        'level': 3,
        'color': '#F3E5F5',
        'id': 'AEF:LOC:0007',
        'subdomains': {}
    },
    'Information Technology': {
        'level': 4,
        'color': '#E8F5E8',
        'subdomains': {
            'Applications': {'id': 'AEF:LOC:0016', 'color': '#C8E6C9'},
            'Platforms': {'id': 'AEF:LOC:0017', 'color': '#C8E6C9'},
            'Network': {'id': 'AEF:LOC:0018', 'color': '#C8E6C9'},
            'Data': {'id': 'AEF:LOC:0019', 'color': '#C8E6C9'}
        }
    }
}

INTERACTIONS = [
    'Customer -> Services',
    'People -> Applications',
    'Applications -> Network',
    'Services -> Information',
    'People -> Services',
    'Applications -> Data',
    'Network -> Data',
    'Process -> Applications',
    'Services -> Process',
    'Information -> People'
]

def display_canvas_text_based(project_data=None):
    """Display the security architecture canvas in text-based format"""
    st.markdown("### 🏗️ Security Architecture Canvas")
    
    # Enterprise Domain (Top Level)
    st.markdown("---")
    st.markdown("#### 🏢 Enterprise Domain (AEF:LOC:0000)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background-color: #B3E5FC; padding: 15px; border-radius: 10px; border: 2px solid #0288D1; text-align: center;'>
            <strong>AEF:LOC:0040</strong><br>
            <strong>Financial Value</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #B3E5FC; padding: 15px; border-radius: 10px; border: 2px solid #0288D1; text-align: center;'>
            <strong>AEF:LOC:0039</strong><br>
            <strong>Business Value</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #B3E5FC; padding: 15px; border-radius: 10px; border: 2px solid #0288D1; text-align: center;'>
            <strong>AEF:LOC:0041</strong><br>
            <strong>Social Impact</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Business Layer
    st.markdown("#### 📋 Business Layer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 10px; border: 2px solid #FF9800; text-align: center;'>
            <strong>AEF:LOC:0006</strong><br>
            <strong>Products</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 10px; border: 2px solid #FF9800; text-align: center;'>
            <strong>AEF:LOC:0002</strong><br>
            <strong>Services</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #FFF3E0; padding: 15px; border-radius: 10px; border: 2px solid #FF9800; text-align: center;'>
            <strong>AEF:LOC:0003</strong><br>
            <strong>Information</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Operational Layer
    st.markdown("#### ⚙️ Operational Layer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #F3E5F5; padding: 15px; border-radius: 10px; border: 2px solid #9C27B0; text-align: center;'>
            <strong>AEF:LOC:0004</strong><br>
            <strong>People</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # People subdomains
        st.markdown("<div style='margin-top: 10px;'>", unsafe_allow_html=True)
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            st.markdown("""
            <div style='background-color: #E1BEE7; padding: 8px; border-radius: 5px; border: 1px solid #9C27B0; text-align: center; font-size: 12px;'>
                <strong>Customer</strong>
            </div>
            """, unsafe_allow_html=True)
        with subcol2:
            st.markdown("""
            <div style='background-color: #E1BEE7; padding: 8px; border-radius: 5px; border: 1px solid #9C27B0; text-align: center; font-size: 12px;'>
                <strong>User</strong>
            </div>
            """, unsafe_allow_html=True)
        with subcol3:
            st.markdown("""
            <div style='background-color: #E1BEE7; padding: 8px; border-radius: 5px; border: 1px solid #9C27B0; text-align: center; font-size: 12px;'>
                <strong>Admin</strong>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #F3E5F5; padding: 15px; border-radius: 10px; border: 2px solid #9C27B0; text-align: center;'>
            <strong>AEF:LOC:0005</strong><br>
            <strong>Process</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #F3E5F5; padding: 15px; border-radius: 10px; border: 2px solid #9C27B0; text-align: center;'>
            <strong>AEF:LOC:0007</strong><br>
            <strong>Facilities</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technology Layer
    st.markdown("#### 💻 Information Technology Layer")
    st.markdown("""
    <div style='background-color: #E8F5E8; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center; margin-bottom: 15px;'>
        <strong>Information Technology</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style='background-color: #C8E6C9; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center;'>
            <strong>AEF:LOC:0016</strong><br>
            <strong>Applications</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #C8E6C9; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center;'>
            <strong>AEF:LOC:0017</strong><br>
            <strong>Platforms</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background-color: #C8E6C9; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center;'>
            <strong>AEF:LOC:0018</strong><br>
            <strong>Network</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background-color: #C8E6C9; padding: 15px; border-radius: 10px; border: 2px solid #4CAF50; text-align: center;'>
            <strong>AEF:LOC:0019</strong><br>
            <strong>Data</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Display Risks and Mitigations if project data is available
    if project_data and project_data.get('selected_interactions'):
        st.markdown("---")
        st.markdown("#### ⚠️ Security Elements")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🚨 Identified Risks:**")
            for risk_id, risk_info in project_data.get('risks', {}).items():
                status = project_data.get('risk_status', {}).get(risk_id, 'Open')
                status_color = {'Open': '#FF5722', 'In Progress': '#FF9800', 'Closed': '#4CAF50'}[status]
                
                st.markdown(f"""
                <div style='background-color: #FFECB3; padding: 10px; border-radius: 5px; border: 2px solid #FF9800; margin: 5px 0;'>
                    <strong style='color: #E65100;'>{risk_id}</strong><br>
                    <small>{risk_info['description']}</small><br>
                    <span style='background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px;'>{status}</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🛡️ Implemented Mitigations:**")
            for mit_id, mit_info in project_data.get('mitigations', {}).items():
                status = project_data.get('mitigation_status', {}).get(mit_id, 'Open')
                status_color = {'Open': '#FF5722', 'In Progress': '#FF9800', 'Closed': '#4CAF50'}[status]
                
                st.markdown(f"""
                <div style='background-color: #E8F5E8; padding: 10px; border-radius: 5px; border: 2px solid #4CAF50; margin: 5px 0;'>
                    <strong style='color: #1B5E20;'>{mit_id}</strong><br>
                    <small>{mit_info['description']}</small><br>
                    <span style='background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 3px; font-size: 10px;'>{status}</span>
                </div>
                """, unsafe_allow_html=True)

def display_interactions_flow(selected_interactions):
    """Display selected interactions as a flow"""
    if selected_interactions:
        st.markdown("#### 🔄 Active Interactions")
        for i, interaction in enumerate(selected_interactions):
            source, target = interaction.split(' -> ')
            st.markdown(f"""
            <div style='background-color: #F5F5F5; padding: 8px; border-radius: 5px; border-left: 4px solid #2196F3; margin: 5px 0;'>
                <strong>{source}</strong> → <strong>{target}</strong>
            </div>
            """, unsafe_allow_html=True)

def admin_section():
    """Admin section for managing risks and mitigations"""
    st.header("🔧 Administration Panel")
    
    tab1, tab2 = st.tabs(["Risk Management", "Mitigation Management"])
    
    with tab1:
        st.subheader("Risk Database")
        
        # Add new risk
        with st.expander("Add New Risk"):
            col1, col2 = st.columns(2)
            with col1:
                risk_id = st.text_input("Risk ID", placeholder="ADV004")
                risk_description = st.text_area("Risk Description")
                risk_impact = st.selectbox("Impact Level", ["Low", "Medium", "High", "Critical"])
            
            with col2:
                risk_interaction = st.selectbox("Associated Interaction", INTERACTIONS)
                risk_domain = st.selectbox("Primary Domain", list(DOMAINS.keys()))
            
            if st.button("Add Risk"):
                if risk_id and risk_description:
                    st.session_state.risks[risk_id] = {
                        'description': risk_description,
                        'impact': risk_impact,
                        'interaction': risk_interaction,
                        'domain': risk_domain
                    }
                    st.success(f"Risk {risk_id} added successfully!")
                    st.rerun()
        
        # Display existing risks
        st.subheader("Existing Risks")
        if st.session_state.risks:
            risks_df = pd.DataFrame.from_dict(st.session_state.risks, orient='index')
            risks_df.index.name = 'Risk ID'
            st.dataframe(risks_df, use_container_width=True)
        else:
            st.info("No risks defined yet.")
    
    with tab2:
        st.subheader("Mitigation Database")
        
        # Add new mitigation
        with st.expander("Add New Mitigation"):
            col1, col2 = st.columns(2)
            with col1:
                mit_id = st.text_input("Mitigation ID", placeholder="MIT003")
                mit_description = st.text_area("Mitigation Description")
                mit_domain = st.selectbox("Implementation Domain", list(DOMAINS.keys()))
            
            with col2:
                available_risks = list(st.session_state.risks.keys())
                mapped_risks = st.multiselect("Mapped Risks", available_risks)
            
            if st.button("Add Mitigation"):
                if mit_id and mit_description:
                    st.session_state.mitigations[mit_id] = {
                        'description': mit_description,
                        'domain': mit_domain,
                        'mapped_risks': mapped_risks
                    }
                    st.success(f"Mitigation {mit_id} added successfully!")
                    st.rerun()
        
        # Display existing mitigations
        st.subheader("Existing Mitigations")
        if st.session_state.mitigations:
            mitigations_data = []
            for mit_id, mit_info in st.session_state.mitigations.items():
                mitigations_data.append({
                    'Mitigation ID': mit_id,
                    'Description': mit_info['description'],
                    'Domain': mit_info['domain'],
                    'Mapped Risks': ', '.join(mit_info['mapped_risks'])
                })
            
            mitigations_df = pd.DataFrame(mitigations_data)
            st.dataframe(mitigations_df, use_container_width=True)
        else:
            st.info("No mitigations defined yet.")

def project_management():
    """Project management section"""
    st.header("📁 Project Management")
    
    # Project selection/creation
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        project_names = list(st.session_state.projects.keys()) if st.session_state.projects else []
        selected_project = st.selectbox(
            "Select Project",
            ["Create New Project..."] + project_names,
            index=0 if not st.session_state.current_project else 
            project_names.index(st.session_state.current_project) + 1 if st.session_state.current_project in project_names else 0
        )
    
    with col2:
        if st.button("🗑️ Delete Project", disabled=selected_project == "Create New Project..."):
            if selected_project in st.session_state.projects:
                del st.session_state.projects[selected_project]
                st.session_state.current_project = None
                st.success(f"Project '{selected_project}' deleted!")
                st.rerun()
    
    if selected_project == "Create New Project...":
        st.subheader("Create New Project")
        
        col1, col2 = st.columns(2)
        with col1:
            new_project_name = st.text_input("Project Name")
            project_description = st.text_area("Project Description")
        
        with col2:
            project_owner = st.text_input("Project Owner")
            project_status = st.selectbox("Initial Status", ["Open", "In Progress", "Closed"])
        
        if st.button("Create Project"):
            if new_project_name:
                project_id = str(uuid.uuid4())[:8]
                st.session_state.projects[new_project_name] = {
                    'id': project_id,
                    'description': project_description,
                    'owner': project_owner,
                    'status': project_status,
                    'created_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'selected_interactions': [],
                    'risks': {},
                    'mitigations': {},
                    'risk_status': {},
                    'mitigation_status': {}
                }
                st.session_state.current_project = new_project_name
                st.success(f"Project '{new_project_name}' created successfully!")
                st.rerun()
    
    else:
        st.session_state.current_project = selected_project
        project_data = st.session_state.projects[selected_project]
        
        # Project details
        st.subheader(f"Project: {selected_project}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Project ID", project_data['id'])
            st.write(f"**Owner:** {project_data['owner']}")
        with col2:
            new_status = st.selectbox("Status", ["Open", "In Progress", "Closed"], 
                                    index=["Open", "In Progress", "Closed"].index(project_data['status']))
            if new_status != project_data['status']:
                project_data['status'] = new_status
                st.rerun()
        with col3:
            st.write(f"**Created:** {project_data['created_date']}")
        
        st.write(f"**Description:** {project_data['description']}")
        
        # Interaction selection
        st.subheader("🔄 Interaction Selection")
        selected_interactions = st.multiselect(
            "Select Interactions for this Architecture",
            INTERACTIONS,
            default=project_data.get('selected_interactions', [])
        )
        project_data['selected_interactions'] = selected_interactions
        
        # Display selected interactions
        if selected_interactions:
            display_interactions_flow(selected_interactions)
        
        # Risk management for project
        st.subheader("⚠️ Project Risk Management")
        
        if selected_interactions:
            # Filter risks based on selected interactions
            relevant_risks = {k: v for k, v in st.session_state.risks.items() 
                            if v['interaction'] in selected_interactions}
            
            if relevant_risks:
                selected_risks = st.multiselect(
                    "Select Relevant Risks",
                    list(relevant_risks.keys()),
                    default=list(project_data.get('risks', {}).keys())
                )
                
                # Update project risks
                project_data['risks'] = {k: relevant_risks[k] for k in selected_risks}
                
                # Risk status management
                if selected_risks:
                    st.write("**Risk Status Management:**")
                    for risk_id in selected_risks:
                        col1, col2, col3 = st.columns([2, 1, 3])
                        with col1:
                            st.write(f"**{risk_id}**")
                        with col2:
                            risk_status = st.selectbox(
                                f"Status",
                                ["Open", "In Progress", "Closed"],
                                key=f"risk_status_{risk_id}",
                                index=["Open", "In Progress", "Closed"].index(
                                    project_data.get('risk_status', {}).get(risk_id, "Open")
                                )
                            )
                            project_data.setdefault('risk_status', {})[risk_id] = risk_status
                        with col3:
                            st.write(st.session_state.risks[risk_id]['description'])
        
        # Mitigation management for project
        st.subheader("🛡️ Project Mitigation Management")
        
        if project_data.get('risks'):
            # Find relevant mitigations
            project_risk_ids = list(project_data['risks'].keys())
            relevant_mitigations = {}
            
            for mit_id, mit_info in st.session_state.mitigations.items():
                if any(risk_id in project_risk_ids for risk_id in mit_info['mapped_risks']):
                    relevant_mitigations[mit_id] = mit_info
            
            if relevant_mitigations:
                selected_mitigations = st.multiselect(
                    "Select Mitigations",
                    list(relevant_mitigations.keys()),
                    default=list(project_data.get('mitigations', {}).keys())
                )
                
                project_data['mitigations'] = {k: relevant_mitigations[k] for k in selected_mitigations}
                
                # Mitigation status management
                if selected_mitigations:
                    st.write("**Mitigation Status Management:**")
                    for mit_id in selected_mitigations:
                        col1, col2, col3 = st.columns([2, 1, 3])
                        with col1:
                            st.write(f"**{mit_id}**")
                        with col2:
                            mit_status = st.selectbox(
                                f"Status",
                                ["Open", "In Progress", "Closed"],
                                key=f"mit_status_{mit_id}",
                                index=["Open", "In Progress", "Closed"].index(
                                    project_data.get('mitigation_status', {}).get(mit_id, "Open")
                                )
                            )
                            project_data.setdefault('mitigation_status', {})[mit_id] = mit_status
                        with col3:
                            st.write(st.session_state.mitigations[mit_id]['description'])
        
        # Canvas visualization
        display_canvas_text_based(project_data)

def dashboard():
    """Dashboard showing project statistics"""
    st.header("📊 Security Architecture Dashboard")
    
    if not st.session_state.projects:
        st.info("No projects created yet. Go to Project Management to create your first project.")
        return
    
    # Overall statistics
    total_projects = len(st.session_state.projects)
    open_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'Open')
    in_progress_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'In Progress')
    closed_projects = sum(1 for p in st.session_state.projects.values() if p['status'] == 'Closed')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Projects", total_projects)
    with col2:
        st.metric("Open Projects", open_projects)
    with col3:
        st.metric("In Progress", in_progress_projects)
    with col4:
        st.metric("Closed Projects", closed_projects)
    
    # Project status charts using Streamlit's built-in chart functions
    st.subheader("📈 Project Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Project status distribution
        status_data = pd.DataFrame({
            'Status': ['Open', 'In Progress', 'Closed'],
            'Count': [open_projects, in_progress_projects, closed_projects]
        })
        
        if status_data['Count'].sum() > 0:
            st.subheader("Project Status Distribution")
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("No project data to display")
    
    with col2:
        # Risk and mitigation statistics per project
        project_stats = []
        for project_name, project_data in st.session_state.projects.items():
            total_risks = len(project_data.get('risks', {}))
            open_risks = sum(1 for status in project_data.get('risk_status', {}).values() if status == 'Open')
            total_mitigations = len(project_data.get('mitigations', {}))
            open_mitigations = sum(1 for status in project_data.get('mitigation_status', {}).values() if status == 'Open')
            
            project_stats.append({
                'Project': project_name,
                'Open Risks': open_risks,
                'Open Mitigations': open_mitigations,
                'Total Risks': total_risks,
                'Total Mitigations': total_mitigations,
                'Status': project_data['status']
            })
        
        if project_stats:
            stats_df = pd.DataFrame(project_stats)
            st.subheader("Risks & Mitigations by Project")
            chart_data = stats_df[['Project', 'Open Risks', 'Open Mitigations']].set_index('Project')
            st.bar_chart(chart_data)
    
    # Detailed project table
    st.subheader("📋 Project Details")
    if project_stats:
        detailed_df = pd.DataFrame(project_stats)
        st.dataframe(detailed_df, use_container_width=True)
    
    # Risk summary
    st.subheader("⚠️ Risk Analysis")
    if st.session_state.risks:
        risk_impact_data = []
        for risk_id, risk_info in st.session_state.risks.items():
            # Count how many projects this risk appears in
            project_count = sum(1 for p in st.session_state.projects.values() 
                              if risk_id in p.get('risks', {}))
            
            risk_impact_data.append({
                'Risk ID': risk_id,
                'Description': risk_info['description'],
                'Impact Level': risk_info['impact'],
                'Projects Affected': project_count,
                'Domain': risk_info['domain'],
                'Interaction': risk_info['interaction']
            })
        
        if risk_impact_data:
            risk_df = pd.DataFrame(risk_impact_data)
            st.dataframe(risk_df, use_container_width=True)
            
            # Risk impact chart
            impact_counts = risk_df['Impact Level'].value_counts()
            if not impact_counts.empty:
                st.subheader("Risk Impact Distribution")
                st.bar_chart(impact_counts)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("🛡️ Security Architecture")
    st.sidebar.markdown("---")
    
    page = st.sidebar.selectbox(
        "Navigate to:",
        ["Dashboard", "Project Management", "Administration"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Enterprise Security Architecture Canvas**\n\n"
        "Create and manage security architectures with:\n"
        "- Interactive domain canvas\n"
        "- Risk assessment & tracking\n"
        "- Mitigation management\n"
        "- Project oversight"
    )
    
    # Display current project info in sidebar if available
    if st.session_state.current_project:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### Current Project")
        st.sidebar.info(f"📁 **{st.session_state.current_project}**")
        
        project_data = st.session_state.projects[st.session_state.current_project]
        st.sidebar.write(f"Status: **{project_data['status']}**")
        st.sidebar.write(f"Risks: **{len(project_data.get('risks', {}))}**")
        st.sidebar.write(f"Mitigations: **{len(project_data.get('mitigations', {}))}**")
    
    # Main content based on selected page
    if page == "Dashboard":
        dashboard()
    elif page == "Project Management":
        project_management()
    elif page == "Administration":
        admin_section()

if __name__ == "__main__":
    main()
