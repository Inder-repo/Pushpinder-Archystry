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
            },
            'ADV004': {
                'description': 'Unauthorized access to sensitive data',
                'impact': 'High',
                'interaction': 'Services -> Information',
                'domain': 'Information'
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
            },
            'MIT003': {
                'description': 'Network segmentation and monitoring',
                'domain': 'Network',
                'mapped_risks': ['ADV003']
            },
            'MIT004': {
                'description': 'Data encryption at rest and in transit',
                'domain': 'Information',
                'mapped_risks': ['ADV004']
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
    'User -> Applications', 
    'Admin -> Applications',
    'People -> Applications',
    'Applications -> Network',
    'Applications -> Data',
    'Services -> Information',
    'People -> Services',
    'Network -> Data',
    'Process -> Applications',
    'Services -> Process',
    'Information -> People',
    'Platforms -> Applications',
    'Data -> Information',
    'Network -> Services'
]

def manage_domain_elements(domain_name, project_data):
    """Manage dynamic elements within a domain"""
    if not project_data:
        return []
    
    elements_key = f'{domain_name}_elements'
    if elements_key not in project_data:
        project_data[elements_key] = []
    
    st.write(f"**Manage {domain_name} Elements:**")
    
    # Add new element
    col1, col2 = st.columns([3, 1])
    with col1:
        new_element = st.text_input(f"Add element to {domain_name}", 
                                  key=f"new_element_{domain_name}",
                                  placeholder="Enter element name")
    with col2:
        if st.button(f"Add", key=f"add_element_{domain_name}"):
            if new_element and new_element not in project_data[elements_key]:
                project_data[elements_key].append(new_element)
                st.success(f"Added {new_element} to {domain_name}")
                st.rerun()
    
    # Display existing elements with delete option
    if project_data[elements_key]:
        for i, element in enumerate(project_data[elements_key]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {element}")
            with col2:
                if st.button("🗑️", key=f"delete_{domain_name}_{i}"):
                    project_data[elements_key].remove(element)
                    st.rerun()
    
    return project_data[elements_key]

def manage_domain_risks(domain_name, project_data, available_risks):
    """Manage risks assigned to a domain"""
    if not project_data:
        return []
    
    risks_key = f'{domain_name}_risks'
    if risks_key not in project_data:
        project_data[risks_key] = []
    
    st.write(f"**Assign Risks to {domain_name}:**")
    
    # Filter risks relevant to this domain
    domain_risks = {k: v for k, v in available_risks.items() 
                   if v.get('domain') == domain_name or v.get('domain') in DOMAINS.get(domain_name, {}).get('subdomains', {})}
    
    if domain_risks:
        selected_risks = st.multiselect(
            f"Select risks for {domain_name}",
            list(domain_risks.keys()),
            default=project_data[risks_key],
            key=f"risks_{domain_name}",
            format_func=lambda x: f"{x}: {domain_risks[x]['description'][:50]}..."
        )
        project_data[risks_key] = selected_risks
        return selected_risks
    else:
        st.info(f"No risks available for {domain_name}")
        return []

def manage_domain_mitigations(domain_name, project_data, available_mitigations):
    """Manage mitigations assigned to a domain"""
    if not project_data:
        return []
    
    mitigations_key = f'{domain_name}_mitigations'
    if mitigations_key not in project_data:
        project_data[mitigations_key] = []
    
    st.write(f"**Assign Mitigations to {domain_name}:**")
    
    # Filter mitigations relevant to this domain
    domain_mitigations = {k: v for k, v in available_mitigations.items() 
                         if v.get('domain') == domain_name or v.get('domain') in DOMAINS.get(domain_name, {}).get('subdomains', {})}
    
    if domain_mitigations:
        selected_mitigations = st.multiselect(
            f"Select mitigations for {domain_name}",
            list(domain_mitigations.keys()),
            default=project_data[mitigations_key],
            key=f"mitigations_{domain_name}",
            format_func=lambda x: f"{x}: {domain_mitigations[x]['description'][:50]}..."
        )
        project_data[mitigations_key] = selected_mitigations
        return selected_mitigations
    else:
        st.info(f"No mitigations available for {domain_name}")
        return []

def display_canvas_with_interactions(project_data=None):
    """Display the security architecture canvas with visual interactions"""
    st.markdown("### 🏗️ Enhanced Security Architecture Canvas")
    
    if not project_data:
        st.info("Select or create a project to see the interactive canvas.")
        return
    
    # CSS for styling and connection lines
    st.markdown("""
    <style>
    .domain-box {
        position: relative;
        margin: 10px;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid;
        text-align: center;
    }
    .element-item {
        background-color: rgba(255,255,255,0.8);
        padding: 5px;
        margin: 3px;
        border-radius: 5px;
        border: 1px solid #ccc;
        display: inline-block;
        font-size: 12px;
    }
    .risk-item {
        background-color: #ffebee;
        padding: 3px 6px;
        margin: 2px;
        border-radius: 3px;
        border: 1px solid #f44336;
        font-size: 10px;
        color: #c62828;
    }
    .mitigation-item {
        background-color: #e8f5e8;
        padding: 3px 6px;
        margin: 2px;
        border-radius: 3px;
        border: 1px solid #4caf50;
        font-size: 10px;
        color: #2e7d32;
    }
    .interaction-line {
        stroke: #2196F3;
        stroke-width: 2;
        marker-end: url(#arrowhead);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enterprise Domain (Top Level)
    st.markdown("---")
    st.markdown("#### 🏢 Enterprise Domain")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='domain-box' style='background-color: #B3E5FC; border-color: #0288D1;'>
            <strong>AEF:LOC:0040</strong><br>
            <strong>Financial Value</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='domain-box' style='background-color: #B3E5FC; border-color: #0288D1;'>
            <strong>AEF:LOC:0039</strong><br>
            <strong>Business Value</strong>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='domain-box' style='background-color: #B3E5FC; border-color: #0288D1;'>
            <strong>AEF:LOC:0041</strong><br>
            <strong>Social Impact</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Business Layer with enhanced content
    st.markdown("#### 📋 Business Layer")
    col1, col2, col3 = st.columns(3)
    
    # Products Domain
    with col1:
        st.markdown("**Products Domain**")
        products_html = """
        <div class='domain-box' style='background-color: #FFF3E0; border-color: #FF9800;'>
            <strong>AEF:LOC:0006</strong><br>
            <strong>Products</strong><br>
        """
        
        # Add elements
        products_elements = project_data.get('Products_elements', [])
        for element in products_elements:
            products_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        products_risks = project_data.get('Products_risks', [])
        for risk in products_risks:
            products_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        products_mitigations = project_data.get('Products_mitigations', [])
        for mitigation in products_mitigations:
            products_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        products_html += "</div>"
        st.markdown(products_html, unsafe_allow_html=True)
    
    # Services Domain
    with col2:
        st.markdown("**Services Domain**")
        services_html = """
        <div class='domain-box' style='background-color: #FFF3E0; border-color: #FF9800;'>
            <strong>AEF:LOC:0002</strong><br>
            <strong>Services</strong><br>
        """
        
        # Add elements
        services_elements = project_data.get('Services_elements', [])
        for element in services_elements:
            services_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        services_risks = project_data.get('Services_risks', [])
        for risk in services_risks:
            services_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        services_mitigations = project_data.get('Services_mitigations', [])
        for mitigation in services_mitigations:
            services_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        services_html += "</div>"
        st.markdown(services_html, unsafe_allow_html=True)
    
    # Information Domain
    with col3:
        st.markdown("**Information Domain**")
        information_html = """
        <div class='domain-box' style='background-color: #FFF3E0; border-color: #FF9800;'>
            <strong>AEF:LOC:0003</strong><br>
            <strong>Information</strong><br>
        """
        
        # Add elements
        information_elements = project_data.get('Information_elements', [])
        for element in information_elements:
            information_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        information_risks = project_data.get('Information_risks', [])
        for risk in information_risks:
            information_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        information_mitigations = project_data.get('Information_mitigations', [])
        for mitigation in information_mitigations:
            information_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        information_html += "</div>"
        st.markdown(information_html, unsafe_allow_html=True)
    
    # Operational Layer with enhanced People domain
    st.markdown("#### ⚙️ Operational Layer")
    col1, col2, col3 = st.columns(3)
    
    # People Domain with dynamic elements
    with col1:
        st.markdown("**People Domain**")
        people_html = """
        <div class='domain-box' style='background-color: #F3E5F5; border-color: #9C27B0;'>
            <strong>AEF:LOC:0004</strong><br>
            <strong>People</strong><br>
        """
        
        # Add dynamic elements
        people_elements = project_data.get('People_elements', ['Customer', 'User', 'Admin'])  # Default elements
        for element in people_elements:
            people_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        people_risks = project_data.get('People_risks', [])
        for risk in people_risks:
            people_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        people_mitigations = project_data.get('People_mitigations', [])
        for mitigation in people_mitigations:
            people_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        people_html += "</div>"
        st.markdown(people_html, unsafe_allow_html=True)
    
    # Process Domain
    with col2:
        st.markdown("**Process Domain**")
        process_html = """
        <div class='domain-box' style='background-color: #F3E5F5; border-color: #9C27B0;'>
            <strong>AEF:LOC:0005</strong><br>
            <strong>Process</strong><br>
        """
        
        # Add elements
        process_elements = project_data.get('Process_elements', [])
        for element in process_elements:
            process_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        process_risks = project_data.get('Process_risks', [])
        for risk in process_risks:
            process_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        process_mitigations = project_data.get('Process_mitigations', [])
        for mitigation in process_mitigations:
            process_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        process_html += "</div>"
        st.markdown(process_html, unsafe_allow_html=True)
    
    # Facilities Domain
    with col3:
        st.markdown("**Facilities Domain**")
        facilities_html = """
        <div class='domain-box' style='background-color: #F3E5F5; border-color: #9C27B0;'>
            <strong>AEF:LOC:0007</strong><br>
            <strong>Facilities</strong><br>
        """
        
        # Add elements
        facilities_elements = project_data.get('Facilities_elements', [])
        for element in facilities_elements:
            facilities_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        facilities_risks = project_data.get('Facilities_risks', [])
        for risk in facilities_risks:
            facilities_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        facilities_mitigations = project_data.get('Facilities_mitigations', [])
        for mitigation in facilities_mitigations:
            facilities_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        facilities_html += "</div>"
        st.markdown(facilities_html, unsafe_allow_html=True)
    
    # Technology Layer
    st.markdown("#### 💻 Information Technology Layer")
    col1, col2, col3, col4 = st.columns(4)
    
    # Applications
    with col1:
        st.markdown("**Applications**")
        applications_html = """
        <div class='domain-box' style='background-color: #C8E6C9; border-color: #4CAF50;'>
            <strong>AEF:LOC:0016</strong><br>
            <strong>Applications</strong><br>
        """
        
        # Add elements
        applications_elements = project_data.get('Applications_elements', [])
        for element in applications_elements:
            applications_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        applications_risks = project_data.get('Applications_risks', [])
        for risk in applications_risks:
            applications_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        applications_mitigations = project_data.get('Applications_mitigations', [])
        for mitigation in applications_mitigations:
            applications_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        applications_html += "</div>"
        st.markdown(applications_html, unsafe_allow_html=True)
    
    # Platforms
    with col2:
        st.markdown("**Platforms**")
        platforms_html = """
        <div class='domain-box' style='background-color: #C8E6C9; border-color: #4CAF50;'>
            <strong>AEF:LOC:0017</strong><br>
            <strong>Platforms</strong><br>
        """
        
        # Add elements
        platforms_elements = project_data.get('Platforms_elements', [])
        for element in platforms_elements:
            platforms_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        platforms_risks = project_data.get('Platforms_risks', [])
        for risk in platforms_risks:
            platforms_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        platforms_mitigations = project_data.get('Platforms_mitigations', [])
        for mitigation in platforms_mitigations:
            platforms_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        platforms_html += "</div>"
        st.markdown(platforms_html, unsafe_allow_html=True)
    
    # Network
    with col3:
        st.markdown("**Network**")
        network_html = """
        <div class='domain-box' style='background-color: #C8E6C9; border-color: #4CAF50;'>
            <strong>AEF:LOC:0018</strong><br>
            <strong>Network</strong><br>
        """
        
        # Add elements
        network_elements = project_data.get('Network_elements', [])
        for element in network_elements:
            network_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        network_risks = project_data.get('Network_risks', [])
        for risk in network_risks:
            network_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        network_mitigations = project_data.get('Network_mitigations', [])
        for mitigation in network_mitigations:
            network_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        network_html += "</div>"
        st.markdown(network_html, unsafe_allow_html=True)
    
    # Data
    with col4:
        st.markdown("**Data**")
        data_html = """
        <div class='domain-box' style='background-color: #C8E6C9; border-color: #4CAF50;'>
            <strong>AEF:LOC:0019</strong><br>
            <strong>Data</strong><br>
        """
        
        # Add elements
        data_elements = project_data.get('Data_elements', [])
        for element in data_elements:
            data_html += f"<div class='element-item'>{element}</div>"
        
        # Add risks
        data_risks = project_data.get('Data_risks', [])
        for risk in data_risks:
            data_html += f"<div class='risk-item'>⚠️ {risk}</div>"
        
        # Add mitigations
        data_mitigations = project_data.get('Data_mitigations', [])
        for mitigation in data_mitigations:
            data_html += f"<div class='mitigation-item'>🛡️ {mitigation}</div>"
        
        data_html += "</div>"
        st.markdown(data_html, unsafe_allow_html=True)
    
    # Display selected interactions as visual connections
    if project_data.get('selected_interactions'):
        st.markdown("---")
        st.markdown("#### 🔄 Active Interactions & Connections")
        
        for interaction in project_data['selected_interactions']:
            source, target = interaction.split(' -> ')
            
            # Get risks and mitigations for this interaction
            interaction_risks = [k for k, v in st.session_state.risks.items() 
                               if v.get('interaction') == interaction]
            interaction_mitigations = [k for k, v in st.session_state.mitigations.items() 
                                     if any(risk in interaction_risks for risk in v.get('mapped_risks', []))]
            
            # Create visual representation
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.markdown(f"""
                <div style='background-color: #E3F2FD; padding: 10px; border-radius: 5px; text-align: center;'>
                    <strong>{source}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                connection_html = f"""
                <div style='background-color: #F5F5F5; padding: 10px; border-radius: 5px; text-align: center;'>
                    <strong>→ {interaction} →</strong><br>
                """
                
                if interaction_risks:
                    connection_html += "<br><strong>Risks:</strong><br>"
                    for risk in interaction_risks:
                        connection_html += f"<span class='risk-item'>⚠️ {risk}</span>"
                
                if interaction_mitigations:
                    connection_html += "<br><strong>Mitigations:</strong><br>"
                    for mitigation in interaction_mitigations:
                        connection_html += f"<span class='mitigation-item'>🛡️ {mitigation}</span>"
                
                connection_html += "</div>"
                st.markdown(connection_html, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='background-color: #E8F5E8; padding: 10px; border-radius: 5px; text-align: center;'>
                    <strong>{target}</strong>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)

def admin_section():
    """Enhanced admin section for managing risks and mitigations"""
    st.header("🔧 Administration Panel")
    
    tab1, tab2 = st.tabs(["Risk Management", "Mitigation Management"])
    
    with tab1:
        st.subheader("Risk Database")
        
        # Add new risk
        with st.expander("Add New Risk"):
            col1, col2 = st.columns(2)
            with col1:
                risk_id = st.text_input("Risk ID", placeholder="ADV005")
                risk_description = st.text_area("Risk Description")
                risk_impact = st.selectbox("Impact Level", ["Low", "Medium", "High", "Critical"])
            
            with col2:
                risk_interaction = st.selectbox("Associated Interaction", ["None"] + INTERACTIONS)
                risk_domain = st.selectbox("Primary Domain", ["None"] + list(DOMAINS.keys()))
            
            if st.button("Add Risk"):
                if risk_id and risk_description:
                    st.session_state.risks[risk_id] = {
                        'description': risk_description,
                        'impact': risk_impact,
                        'interaction': risk_interaction if risk_interaction != "None" else "",
                        'domain': risk_domain if risk_domain != "None" else ""
                    }
                    st.success(f"Risk {risk_id} added successfully!")
                    st.rerun()
        
        # Display existing risks with edit capability
        st.subheader("Existing Risks")
        if st.session_state.risks:
            for risk_id, risk_info in st.session_state.risks.items():
                with st.expander(f"Risk: {risk_id}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Description:** {risk_info['description']}")
                        st.write(f"**Impact:** {risk_info['impact']}")
                        st.write(f"**Domain:** {risk_info.get('domain', 'None')}")
                        st.write(f"**Interaction:** {risk_info.get('interaction', 'None')}")
                    
                    with col2:
                        if st.button(f"Edit {risk_id}", key=f"edit_risk_{risk_id}"):
                            st.session_state[f'editing_risk_{risk_id}'] = True
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Delete {risk_id}", key=f"delete_risk_{risk_id}"):
                            del st.session_state.risks[risk_id]
                            st.success(f"Risk {risk_id} deleted!")
                            st.rerun()
        else:
            st.info("No risks defined yet.")
    
    with tab2:
        st.subheader("Mitigation Database")
        
        # Add new mitigation
        with st.expander("Add New Mitigation"):
            col1, col2 = st.columns(2)
            with col1:
                mit_id = st.text_input("Mitigation ID", placeholder="MIT005")
                mit_description = st.text_area("Mitigation Description")
                mit_domain = st.selectbox("Implementation Domain", ["None"] + list(DOMAINS.keys()))
            
            with col2:
                available_risks = list(st.session_state.risks.keys())
                mapped_risks = st.multiselect("Mapped Risks", available_risks)
                mit_interaction = st.selectbox("Associated Interaction", ["None"] + INTERACTIONS)
            
            if st.button("Add Mitigation"):
                if mit_id and mit_description:
                    st.session_state.mitigations[mit_id] = {
                        'description': mit_description,
                        'domain': mit_domain if mit_domain != "None" else "",
                        'mapped_risks': mapped_risks,
                        'interaction': mit_interaction if mit_interaction != "None" else ""
                    }
                    st.success(f"Mitigation {mit_id} added successfully!")
                    st.rerun()
        
        # Display existing mitigations with edit capability
        st.subheader("Existing Mitigations")
        if st.session_state.mitigations:
            for mit_id, mit_info in st.session_state.mitigations.items():
                with st.expander(f"Mitigation: {mit_id}"):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        st.write(f"**Description:** {mit_info['description']}")
                        st.write(f"**Domain:** {mit_info.get('domain', 'None')}")
                        st.write(f"**Mapped Risks:** {', '.join(mit_info.get('mapped_risks', []))}")
                        st.write(f"**Interaction:** {mit_info.get('interaction', 'None')}")
                    
                    with col2:
                        if st.button(f"Edit {mit_id}", key=f"edit_mit_{mit_id}"):
                            st.session_state[f'editing_mit_{mit_id}'] = True
                            st.rerun()
                    
                    with col3:
                        if st.button(f"Delete {mit_id}", key=f"delete_mit_{mit_id}"):
                            del st.session_state.mitigations[mit_id]
                            st.success(f"Mitigation {mit_id} deleted!")
                            st.rerun()
        else:
            st.info("No mitigations defined yet.")

def project_management():
    """Enhanced project management section with domain element management"""
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
                    'mitigation_status': {},
                    # Initialize domain elements
                    'People_elements': ['Customer', 'User', 'Admin'],  # Default elements
                    'Services_elements': [],
                    'Applications_elements': [],
                    'Network_elements': [],
                    'Data_elements': [],
                    'Information_elements': [],
                    'Products_elements': [],
                    'Process_elements': [],
                    'Facilities_elements': [],
                    'Platforms_elements': []
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
        
        # Tabs for different management aspects
        tab1, tab2, tab3, tab4 = st.tabs(["Interactions & Canvas", "Domain Elements", "Risk Management", "Mitigation Management"])
        
        with tab1:
            # Interaction selection
            st.subheader("🔄 Interaction Selection")
            selected_interactions = st.multiselect(
                "Select Interactions for this Architecture",
                INTERACTIONS,
                default=project_data.get('selected_interactions', [])
            )
            project_data['selected_interactions'] = selected_interactions
            
            # Display the enhanced canvas
            display_canvas_with_interactions(project_data)
        
        with tab2:
            st.subheader("🏗️ Domain Element Management")
            
            # Create tabs for each major domain
            domain_tabs = st.tabs(["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"])
            
            domains_to_manage = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
            
            for i, domain_name in enumerate(domains_to_manage):
                with domain_tabs[i]:
                    st.write(f"### {domain_name} Domain")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        manage_domain_elements(domain_name, project_data)
                    
                    with col2:
                        # Show current risks and mitigations for this domain
                        domain_risks = project_data.get(f'{domain_name}_risks', [])
                        domain_mitigations = project_data.get(f'{domain_name}_mitigations', [])
                        
                        if domain_risks:
                            st.write("**Current Risks:**")
                            for risk in domain_risks:
                                st.write(f"• ⚠️ {risk}")
                        
                        if domain_mitigations:
                            st.write("**Current Mitigations:**")
                            for mitigation in domain_mitigations:
                                st.write(f"• 🛡️ {mitigation}")
        
        with tab3:
            st.subheader("⚠️ Project Risk Management")
            
            # Risk assignment by domain
            st.write("#### Assign Risks to Domains")
            
            domain_cols = st.columns(2)
            domains_to_manage = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
            
            for i, domain_name in enumerate(domains_to_manage):
                with domain_cols[i % 2]:
                    with st.expander(f"{domain_name} Domain Risks"):
                        manage_domain_risks(domain_name, project_data, st.session_state.risks)
            
            # Interaction-based risk assignment
            st.write("#### Risks by Interaction")
            if selected_interactions:
                for interaction in selected_interactions:
                    with st.expander(f"Risks for: {interaction}"):
                        interaction_risks = {k: v for k, v in st.session_state.risks.items() 
                                           if v.get('interaction') == interaction}
                        
                        if interaction_risks:
                            selected_interaction_risks = st.multiselect(
                                f"Select risks for {interaction}",
                                list(interaction_risks.keys()),
                                key=f"interaction_risks_{interaction.replace(' ', '_').replace('->', '_to_')}",
                                format_func=lambda x: f"{x}: {interaction_risks[x]['description'][:50]}..."
                            )
                            
                            # Update project data
                            interaction_key = f"interaction_risks_{interaction.replace(' ', '_').replace('->', '_to_')}"
                            project_data[interaction_key] = selected_interaction_risks
                        else:
                            st.info(f"No risks available for interaction: {interaction}")
        
        with tab4:
            st.subheader("🛡️ Project Mitigation Management")
            
            # Mitigation assignment by domain
            st.write("#### Assign Mitigations to Domains")
            
            domain_cols = st.columns(2)
            
            for i, domain_name in enumerate(domains_to_manage):
                with domain_cols[i % 2]:
                    with st.expander(f"{domain_name} Domain Mitigations"):
                        manage_domain_mitigations(domain_name, project_data, st.session_state.mitigations)
            
            # Interaction-based mitigation assignment
            st.write("#### Mitigations by Interaction")
            if selected_interactions:
                for interaction in selected_interactions:
                    with st.expander(f"Mitigations for: {interaction}"):
                        interaction_mitigations = {k: v for k, v in st.session_state.mitigations.items() 
                                                 if v.get('interaction') == interaction}
                        
                        if interaction_mitigations:
                            selected_interaction_mitigations = st.multiselect(
                                f"Select mitigations for {interaction}",
                                list(interaction_mitigations.keys()),
                                key=f"interaction_mitigations_{interaction.replace(' ', '_').replace('->', '_to_')}",
                                format_func=lambda x: f"{x}: {interaction_mitigations[x]['description'][:50]}..."
                            )
                            
                            # Update project data
                            interaction_key = f"interaction_mitigations_{interaction.replace(' ', '_').replace('->', '_to_')}"
                            project_data[interaction_key] = selected_interaction_mitigations
                        else:
                            st.info(f"No mitigations available for interaction: {interaction}")

def dashboard():
    """Enhanced dashboard showing project statistics"""
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
    
    # Project status charts
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
    
    with col2:
        # Domain element statistics
        domain_stats = {}
        domains_to_analyze = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
        
        for domain in domains_to_analyze:
            total_elements = 0
            for project_data in st.session_state.projects.values():
                total_elements += len(project_data.get(f'{domain}_elements', []))
            domain_stats[domain] = total_elements
        
        if any(count > 0 for count in domain_stats.values()):
            st.subheader("Elements per Domain (All Projects)")
            domain_df = pd.DataFrame(list(domain_stats.items()), columns=['Domain', 'Elements'])
            domain_df = domain_df[domain_df['Elements'] > 0]  # Only show domains with elements
            st.bar_chart(domain_df.set_index('Domain'))
    
    # Detailed project table with enhanced information
    st.subheader("📋 Detailed Project Analysis")
    project_details = []
    
    for project_name, project_data in st.session_state.projects.items():
        # Count elements across all domains
        total_elements = sum(len(project_data.get(f'{domain}_elements', [])) for domain in domains_to_analyze)
        
        # Count risks and mitigations across all domains
        total_risks = sum(len(project_data.get(f'{domain}_risks', [])) for domain in domains_to_analyze)
        total_mitigations = sum(len(project_data.get(f'{domain}_mitigations', [])) for domain in domains_to_analyze)
        
        project_details.append({
            'Project': project_name,
            'Status': project_data['status'],
            'Owner': project_data['owner'],
            'Interactions': len(project_data.get('selected_interactions', [])),
            'Elements': total_elements,
            'Risks': total_risks,
            'Mitigations': total_mitigations,
            'Created': project_data['created_date'][:10]  # Just the date part
        })
    
    if project_details:
        details_df = pd.DataFrame(project_details)
        st.dataframe(details_df, use_container_width=True)
    
    # Risk and mitigation analysis
    st.subheader("⚠️ Risk & Mitigation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Risk Impact Distribution**")
        risk_impacts = [risk['impact'] for risk in st.session_state.risks.values()]
        if risk_impacts:
            impact_df = pd.DataFrame({'Impact': risk_impacts})
            impact_counts = impact_df['Impact'].value_counts()
            st.bar_chart(impact_counts)
        else:
            st.info("No risks defined yet.")
    
    with col2:
        st.write("**Mitigation Coverage by Domain**")
        mitigation_domains = [mit['domain'] for mit in st.session_state.mitigations.values() if mit.get('domain')]
        if mitigation_domains:
            mitigation_df = pd.DataFrame({'Domain': mitigation_domains})
            mitigation_counts = mitigation_df['Domain'].value_counts()
            st.bar_chart(mitigation_counts)
        else:
            st.info("No mitigations defined yet.")

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
        "**Enhanced Enterprise Security Architecture Canvas**\n\n"
        "Features:\n"
        "- 🏗️ Dynamic domain elements\n"
        "- 🔄 Visual interaction mapping\n"
        "- ⚠️ Risk assignment to domains\n"
        "- 🛡️ Mitigation management\n"
        "- 📊 Comprehensive analytics"
    )
    
    # Display current project info in sidebar if available
    if st.session_state.current_project:
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📁 Current Project")
        st.sidebar.info(f"**{st.session_state.current_project}**")
        
        project_data = st.session_state.projects[st.session_state.current_project]
        st.sidebar.write(f"**Status:** {project_data['status']}")
        st.sidebar.write(f"**Interactions:** {len(project_data.get('selected_interactions', []))}")
        
        # Count total elements, risks, and mitigations
        domains = ["People", "Services", "Applications", "Network", "Data", "Information", "Products", "Process", "Facilities", "Platforms"]
        total_elements = sum(len(project_data.get(f'{domain}_elements', [])) for domain in domains)
        total_risks = sum(len(project_data.get(f'{domain}_risks', [])) for domain in domains)
        total_mitigations = sum(len(project_data.get(f'{domain}_mitigations', [])) for domain in domains)
        
        st.sidebar.write(f"**Elements:** {total_elements}")
        st.sidebar.write(f"**Risks:** {total_risks}")
        st.sidebar.write(f"**Mitigations:** {total_mitigations}")
    
    # Main content based on selected page
    if page == "Dashboard":
        dashboard()
    elif page == "Project Management":
        project_management()
    elif page == "Administration":
        admin_section()

if __name__ == "__main__":
    main()
