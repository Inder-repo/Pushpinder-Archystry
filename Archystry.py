import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
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
        'position': (0, 0),
        'subdomains': {
            'Business Value': {'position': (1, 1), 'id': 'AEF:LOC:0039'},
            'Financial Value': {'position': (0.5, 1), 'id': 'AEF:LOC:0040'},
            'Social Impact': {'position': (1.5, 1), 'id': 'AEF:LOC:0041'}
        }
    },
    'Products': {
        'position': (0, 2),
        'id': 'AEF:LOC:0006',
        'subdomains': {}
    },
    'Services': {
        'position': (1, 2),
        'id': 'AEF:LOC:0002',
        'subdomains': {}
    },
    'Information': {
        'position': (2, 2),
        'id': 'AEF:LOC:0003',
        'subdomains': {}
    },
    'People': {
        'position': (0, 3),
        'id': 'AEF:LOC:0004',
        'subdomains': {
            'Customer': {'position': (0, 3.3)},
            'User': {'position': (0.2, 3.3)},
            'Admin': {'position': (0.4, 3.3)}
        }
    },
    'Process': {
        'position': (1, 3),
        'id': 'AEF:LOC:0005',
        'subdomains': {}
    },
    'Facilities': {
        'position': (2, 3),
        'id': 'AEF:LOC:0007',
        'subdomains': {}
    },
    'Information Technology': {
        'position': (1, 4),
        'subdomains': {
            'Applications': {'position': (0.5, 4.3), 'id': 'AEF:LOC:0016'},
            'Platforms': {'position': (1, 4.3), 'id': 'AEF:LOC:0017'},
            'Network': {'position': (1.5, 4.3), 'id': 'AEF:LOC:0018'},
            'Data': {'position': (2, 4.3), 'id': 'AEF:LOC:0019'}
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

def create_canvas_visualization(project_data=None):
    """Create the security architecture canvas visualization"""
    fig = go.Figure()
    
    # Add domain boxes
    for domain_name, domain_info in DOMAINS.items():
        x, y = domain_info['position']
        
        # Main domain box
        fig.add_shape(
            type="rect",
            x0=x-0.4, y0=y-0.3, x1=x+0.4, y1=y+0.3,
            line=dict(color="black", width=2),
            fillcolor="lightblue",
            opacity=0.7
        )
        
        # Domain label
        domain_id = domain_info.get('id', '')
        label_text = f"{domain_id}<br>{domain_name}" if domain_id else domain_name
        
        fig.add_annotation(
            x=x, y=y,
            text=label_text,
            showarrow=False,
            font=dict(size=10, color="black"),
            bgcolor="white",
            bordercolor="black",
            borderwidth=1
        )
        
        # Add subdomains
        for subdomain_name, subdomain_info in domain_info.get('subdomains', {}).items():
            sx, sy = subdomain_info['position']
            
            # Subdomain box
            fig.add_shape(
                type="rect",
                x0=sx-0.3, y0=sy-0.2, x1=sx+0.3, y1=sy+0.2,
                line=dict(color="gray", width=1),
                fillcolor="lightgreen",
                opacity=0.6
            )
            
            subdomain_id = subdomain_info.get('id', '')
            sub_label = f"{subdomain_id}<br>{subdomain_name}" if subdomain_id else subdomain_name
            
            fig.add_annotation(
                x=sx, y=sy,
                text=sub_label,
                showarrow=False,
                font=dict(size=8, color="black"),
                bgcolor="white",
                bordercolor="gray",
                borderwidth=1
            )
    
    # Add risks and mitigations if project data is provided
    if project_data and 'selected_interactions' in project_data:
        risk_counter = 0
        mitigation_counter = 0
        
        for interaction in project_data['selected_interactions']:
            # Add risks for this interaction
            project_risks = [r for r, info in project_data.get('risks', {}).items() 
                           if info.get('interaction') == interaction]
            
            for risk_id in project_risks:
                risk_counter += 1
                # Position risks near relevant domains
                risk_x = 0.5 + (risk_counter * 0.2)
                risk_y = 1.5
                
                fig.add_shape(
                    type="rect",
                    x0=risk_x-0.1, y0=risk_y-0.1, x1=risk_x+0.1, y1=risk_y+0.1,
                    line=dict(color="red", width=2),
                    fillcolor="orange",
                    opacity=0.8
                )
                
                fig.add_annotation(
                    x=risk_x, y=risk_y,
                    text=risk_id,
                    showarrow=False,
                    font=dict(size=8, color="black", family="Arial Black"),
                    bgcolor="orange",
                    bordercolor="red",
                    borderwidth=1
                )
            
            # Add mitigations
            project_mitigations = [m for m, info in project_data.get('mitigations', {}).items()]
            
            for mit_id in project_mitigations:
                mitigation_counter += 1
                mit_x = 0.3 + (mitigation_counter * 0.2)
                mit_y = 1.2
                
                fig.add_shape(
                    type="rect",
                    x0=mit_x-0.1, y0=mit_y-0.1, x1=mit_x+0.1, y1=mit_y+0.1,
                    line=dict(color="green", width=2),
                    fillcolor="lightgreen",
                    opacity=0.8
                )
                
                fig.add_annotation(
                    x=mit_x, y=mit_y,
                    text=mit_id,
                    showarrow=False,
                    font=dict(size=8, color="black", family="Arial Black"),
                    bgcolor="lightgreen",
                    bordercolor="green",
                    borderwidth=1
                )
    
    # Update layout
    fig.update_layout(
        title="Security Architecture Canvas",
        xaxis=dict(range=[-1, 3], showgrid=False, showticklabels=False),
        yaxis=dict(range=[0, 5], showgrid=False, showticklabels=False),
        height=600,
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

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
        st.subheader("🖼️ Security Architecture Canvas")
        canvas_fig = create_canvas_visualization(project_data)
        st.plotly_chart(canvas_fig, use_container_width=True)

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
    
    # Project status distribution
    status_data = {
        'Status': ['Open', 'In Progress', 'Closed'],
        'Count': [open_projects, in_progress_projects, closed_projects]
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_status = px.pie(
            status_data, 
            values='Count', 
            names='Status',
            title="Project Status Distribution"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
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
                'Total Risks': total_risks,
                'Open Risks': open_risks,
                'Total Mitigations': total_mitigations,
                'Open Mitigations': open_mitigations,
                'Status': project_data['status']
            })
        
        if project_stats:
            stats_df = pd.DataFrame(project_stats)
            fig_risks = px.bar(
                stats_df, 
                x='Project', 
                y=['Open Risks', 'Open Mitigations'],
                title="Open Risks & Mitigations by Project",
                barmode='group'
            )
            st.plotly_chart(fig_risks, use_container_width=True)
    
    # Detailed project table
    st.subheader("Project Details")
    if project_stats:
        detailed_df = pd.DataFrame(project_stats)
        st.dataframe(detailed_df, use_container_width=True)
    
    # Risk heat map
    st.subheader("Risk Impact Analysis")
    if st.session_state.risks:
        risk_impact_data = []
        for risk_id, risk_info in st.session_state.risks.items():
            # Count how many projects this risk appears in
            project_count = sum(1 for p in st.session_state.projects.values() 
                              if risk_id in p.get('risks', {}))
            
            impact_score = {'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}[risk_info['impact']]
            
            risk_impact_data.append({
                'Risk ID': risk_id,
                'Impact Level': risk_info['impact'],
                'Impact Score': impact_score,
                'Projects Affected': project_count,
                'Domain': risk_info['domain']
            })
        
        if risk_impact_data:
            risk_df = pd.DataFrame(risk_impact_data)
            fig_heatmap = px.scatter(
                risk_df,
                x='Projects Affected',
                y='Impact Score',
                size='Impact Score',
                color='Domain',
                hover_data=['Risk ID', 'Impact Level'],
                title="Risk Impact vs Project Coverage"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)

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
    
    # Main content based on selected page
    if page == "Dashboard":
        dashboard()
    elif page == "Project Management":
        project_management()
    elif page == "Administration":
        admin_section()

if __name__ == "__main__":
    main()
