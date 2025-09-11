import streamlit as st
import pandas as pd
from datetime import datetime
import json
import uuid
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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
        'position': (5, 8),
        'size': (3, 1),
        'subdomains': {
            'Business Value': {'position': (4, 7), 'id': 'AEF:LOC:0039'},
            'Financial Value': {'position': (3, 7), 'id': 'AEF:LOC:0040'},
            'Social Impact': {'position': (5, 7), 'id': 'AEF:LOC:0041'}
        }
    },
    'Products': {
        'position': (1, 5),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0006',
        'subdomains': {}
    },
    'Services': {
        'position': (3.5, 5),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0002',
        'subdomains': {}
    },
    'Information': {
        'position': (6, 5),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0003',
        'subdomains': {}
    },
    'People': {
        'position': (1, 3),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0004',
        'subdomains': {
            'Customer': {'position': (0.5, 2.2)},
            'User': {'position': (1, 2.2)},
            'Admin': {'position': (1.5, 2.2)}
        }
    },
    'Process': {
        'position': (3.5, 3),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0005',
        'subdomains': {}
    },
    'Facilities': {
        'position': (6, 3),
        'size': (1.5, 0.8),
        'id': 'AEF:LOC:0007',
        'subdomains': {}
    },
    'Information Technology': {
        'position': (3.5, 1),
        'size': (3, 0.6),
        'subdomains': {
            'Applications': {'position': (2.5, 0.3), 'id': 'AEF:LOC:0016'},
            'Platforms': {'position': (3.5, 0.3), 'id': 'AEF:LOC:0017'},
            'Network': {'position': (4.5, 0.3), 'id': 'AEF:LOC:0018'},
            'Data': {'position': (5.5, 0.3), 'id': 'AEF:LOC:0019'}
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
    """Create the security architecture canvas visualization using matplotlib"""
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Set up the plot
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 9)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add domain boxes
    for domain_name, domain_info in DOMAINS.items():
        x, y = domain_info['position']
        width, height = domain_info.get('size', (1.5, 0.8))
        
        # Main domain box
        rect = patches.Rectangle(
            (x - width/2, y - height/2), width, height,
            linewidth=2, edgecolor='black', facecolor='lightblue', alpha=0.7
        )
        ax.add_patch(rect)
        
        # Domain label
        domain_id = domain_info.get('id', '')
        label_text = f"{domain_id}\n{domain_name}" if domain_id else domain_name
        
        ax.text(x, y, label_text, ha='center', va='center', 
                fontsize=8, weight='bold', 
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='black'))
        
        # Add subdomains
        for subdomain_name, subdomain_info in domain_info.get('subdomains', {}).items():
            sx, sy = subdomain_info['position']
            
            # Subdomain box
            sub_rect = patches.Rectangle(
                (sx - 0.4, sy - 0.25), 0.8, 0.5,
                linewidth=1, edgecolor='gray', facecolor='lightgreen', alpha=0.6
            )
            ax.add_patch(sub_rect)
            
            subdomain_id = subdomain_info.get('id', '')
            sub_label = f"{subdomain_id}\n{subdomain_name}" if subdomain_id else subdomain_name
            
            ax.text(sx, sy, sub_label, ha='center', va='center', 
                    fontsize=6, 
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='white', edgecolor='gray'))
    
    # Add risks and mitigations if project data is provided
    if project_data and 'selected_interactions' in project_data:
        risk_counter = 0
        mitigation_counter = 0
        
        # Add risks for selected interactions
        for interaction in project_data['selected_interactions']:
            project_risks = [r for r, info in project_data.get('risks', {}).items() 
                           if info.get('interaction') == interaction]
            
            for risk_id in project_risks:
                risk_counter += 1
                risk_x = 1.5 + (risk_counter * 0.7)
                risk_y = 6.5
                
                # Risk box
                risk_rect = patches.Rectangle(
                    (risk_x - 0.2, risk_y - 0.15), 0.4, 0.3,
                    linewidth=2, edgecolor='red', facecolor='orange', alpha=0.8
                )
                ax.add_patch(risk_rect)
                
                ax.text(risk_x, risk_y, risk_id, ha='center', va='center', 
                        fontsize=8, weight='bold', color='black')
        
        # Add mitigations
        for mit_id in project_data.get('mitigations', {}).keys():
            mitigation_counter += 1
            mit_x = 1 + (mitigation_counter * 0.7)
            mit_y = 6
            
            # Mitigation box
            mit_rect = patches.Rectangle(
                (mit_x - 0.2, mit_y - 0.15), 0.4, 0.3,
                linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.8
            )
            ax.add_patch(mit_rect)
            
            ax.text(mit_x, mit_y, mit_id, ha='center', va='center', 
                    fontsize=8, weight='bold', color='black')
    
    plt.title("Security Architecture Canvas", fontsize=16, weight='bold', pad=20)
    return fig

def create_pie_chart(data, labels, title):
    """Create a pie chart using matplotlib"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Only create pie chart if there's data
    if sum(data) > 0:
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
        wedges, texts, autotexts = ax.pie(data, labels=labels, autopct='%1.1f%%', 
                                         colors=colors[:len(data)], startangle=90)
        
        # Enhance text
        for autotext in autotexts:
            autotext.set_color('black')
            autotext.set_weight('bold')
    else:
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', 
                transform=ax.transAxes, fontsize=14)
    
    ax.set_title(title, fontsize=14, weight='bold')
    return fig

def create_bar_chart(df, x_col, y_cols, title):
    """Create a bar chart using matplotlib"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if not df.empty:
        x = np.arange(len(df[x_col]))
        width = 0.35
        
        if len(y_cols) == 2:
            ax.bar(x - width/2, df[y_cols[0]], width, label=y_cols[0], alpha=0.8)
            ax.bar(x + width/2, df[y_cols[1]], width, label=y_cols[1], alpha=0.8)
        else:
            ax.bar(x, df[y_cols[0]], width, label=y_cols[0], alpha=0.8)
        
        ax.set_xlabel(x_col)
        ax.set_ylabel('Count')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(df[x_col], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)
    else:
        ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', 
                transform=ax.transAxes, fontsize=14)
        ax.set_title(title)
    
    plt.tight_layout()
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
        st.pyplot(canvas_fig, use_container_width=True)

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
    status_counts = [open_projects, in_progress_projects, closed_projects]
    status_labels = ['Open', 'In Progress', 'Closed']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_status = create_pie_chart(status_counts, status_labels, "Project Status Distribution")
        st.pyplot(fig_status, use_container_width=True)
    
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
            fig_risks = create_bar_chart(
                stats_df, 
                'Project', 
                ['Open Risks', 'Open Mitigations'],
                "Open Risks & Mitigations by Project"
            )
            st.pyplot(fig_risks, use_container_width=True)
    
    # Detailed project table
    st.subheader("Project Details")
    if project_stats:
        detailed_df = pd.DataFrame(project_stats)
        st.dataframe(detailed_df, use_container_width=True)
    
    # Risk impact analysis
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
            st.dataframe(risk_df, use_container_width=True)

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
