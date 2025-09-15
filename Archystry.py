# Mitigations section with enhanced display
    if project_data[mitigations_key]:
        domain_html += "<div style='margin-bottom: 8px;'><strong style='font-size: 11px;'>Mitigations:</strong><br>"
        for mit_id in project_data[mitigations_key]:
            mit_info = st.session_state.mitigations.get(mit_id, {})
            eff_color = {
                'High': '#00CC44',
                'Medium': '#FFBB33',
                'Low': '#FF8800'
            }.get(mit_info.get('effectiveness', ''), '#666666')
            
            domain_html += f'''
            <div class="mitigation-element" style="border-color: {eff_color}; background-color: {eff_color}20;">
                🛡️ {mit_id} ({mit_info.get('effectiveness', 'Unknown')})
            </div>
            '''
        domain_html += "</div>"
    
    domain_html += "</div>"
    
    st.markdown(domain_html, unsafe_allow_html=True)
    
    # Enhanced editing controls
    with st.expander(f"✏️ Edit {domain_name}", expanded=False):
        # Show connections for this domain
        if domain_connections:
            st.write("**🔗 Active Connections:**")
            for conn in domain_connections:
                direction = "→" if conn['source'] == domain_name else "←"
                other_domain = conn['target'] if conn['source'] == domain_name else conn['source']
                st.caption(f"{direction} {other_domain} ({conn['type']})")
        
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
        
        # Enhanced risk assignment with filtering
        st.write("**Assign Risks:**")
        available_risks = [(k, v) for k, v in st.session_state.risks.items()]
        
        if available_risks:
            # Show risk details for better selection
            risk_options = []
            for risk_id, risk_info in available_risks:
                risk_label = f"{risk_id}: {risk_info['description'][:40]}... (Impact: {risk_info['impact']})"
                risk_options.append((risk_id, risk_label))
            
            selected_risks = st.multiselect(
                "Select risks",
                [r[0] for r in risk_options],
                default=project_data[risks_key],
                key=f"risks_multi_{domain_name}",
                format_func=lambda x: next(r[1] for r in risk_options if r[0] == x)
            )
            project_data[risks_key] = selected_risks
        
        # Enhanced mitigation assignment
        st.write("**Assign Mitigations:**")
        available_mitigations = [(k, v) for k, v in st.session_state.mitigations.items()]
        
        if available_mitigations:
            mit_options = []
            for mit_id, mit_info in available_mitigations:
                mit_label = f"{mit_id}: {mit_info['description'][:40]}... (Effectiveness: {mit_info.get('effectiveness', 'Unknown')})"
                mit_options.append((mit_id, mit_label))
            
            selected_mitigations = st.multiselect(
                "Select mitigations",
                [m[0] for m in mit_options],
                default=project_data[mitigations_key],
                key=f"mitigations_multi_{domain_name}",
                format_func=lambda x: next(m[1] for m in mit_options if m[0] == x)
            )
            project_data[mitigations_key] = selected_mitigations

def render_tech_subdomain(subdomain_name, subdomain_id, project_data):
    """Enhanced technology subdomain rendering with connection awareness"""
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
    
    # Check connections
    connections = project_data.get('canvas_connections', [])
    domain_connections = [c for c in connections 
                         if c['source'] == subdomain_name or c['target'] == subdomain_name]
    connection_indicator = f" 🔗({len(domain_connections)})" if domain_connections else ""
    
    # Subdomain container
    subdomain_html = f"""
    <div style="border: 1px solid #388E3C; border-radius: 4px; padding: 15px; margin: 5px; background: rgba(255,255,255,0.7); min-height: 180px;">
        <div style="font-weight: bold; font-size: 12px; text-align: center; margin-bottom: 10px;">
            {subdomain_id}<br>{subdomain_name}{connection_indicator}
        </div>
    """
    
    # Elements
    if project_data[elements_key]:
        for element in project_data[elements_key]:
            subdomain_html += f'<div class="domain-element" style="font-size: 10px; padding: 4px; margin: 2px;">{element}</div>'
    
    # Enhanced risks display
    if project_data[risks_key]:
        subdomain_html += "<br><div style='font-size: 10px; font-weight: bold;'>Risks:</div>"
        for risk_id in project_data[risks_key]:
            risk_info = st.session_state.risks.get(risk_id, {})
            impact = risk_info.get('impact', 'Unknown')
            subdomain_html += f'<div class="risk-element" style="font-size: 9px;">⚠️ {risk_id} ({impact})</div>'
    
    # Enhanced mitigations display
    if project_data[mitigations_key]:
        subdomain_html += "<br><div style='font-size: 10px; font-weight: bold;'>Mitigations:</div>"
        for mit_id in project_data[mitigations_key]:
            mit_info = st.session_state.mitigations.get(mit_id, {})
            effectiveness = mit_info.get('effectiveness', 'Unknown')
            subdomain_html += f'<div class="mitigation-element" style="font-size: 9px;">🛡️ {mit_id} ({effectiveness})</div>'
    
    subdomain_html += "</div>"
    
    st.markdown(subdomain_html, unsafe_allow_html=True)
    
    # Enhanced inline editing
    with st.expander(f"✏️ {subdomain_name}", expanded=False):
        # Show connections
        if domain_connections:
            st.write("**🔗 Connections:**")
            for conn in domain_connections:
                direction = "→" if conn['source'] == subdomain_name else "←"
                other_domain = conn['target'] if conn['source'] == subdomain_name else conn['source']
                st.caption(f"{direction} {other_domain} ({conn['type']})")
        
        # Add elements
        new_element = st.text_input(f"Add to {subdomain_name}", key=f"add_{subdomain_name}")
        if st.button(f"Add", key=f"btn_{subdomain_name}"):
            if new_element and new_element not in project_data[elements_key]:
                project_data[elements_key].append(new_element)
                st.rerun()
        
        # Enhanced risk management
        available_risks = list(st.session_state.risks.keys())
        if available_risks:
            selected_risks = st.multiselect(
                "Risks", 
                available_risks, 
                default=project_data[risks_key],
                key=f"tech_risks_{subdomain_name}",
                format_func=lambda x: f"{x}: {st.session_state.risks[x]['description'][:30]}... ({st.session_state.risks[x]['impact']})"
            )
            project_data[risks_key] = selected_risks
        
        # Enhanced mitigation management
        available_mitigations = list(st.session_state.mitigations.keys())
        if available_mitigations:
            selected_mitigations = st.multiselect(
                "Mitigations", 
                available_mitigations, 
                default=project_data[mitigations_key],
                key=f"tech_mits_{subdomain_name}",
                format_func=lambda x: f"{x}: {st.session_state.mitigations[x]['description'][:30]}... ({st.session_state.mitigations[x].get('effectiveness', 'Unknown')})"
            )
            project_data[mitigations_key] = selected_mitigations

def admin_section():
    """Enhanced admin section for managing master data with risk-mitigation relationships"""
    st.header("🔧 Administration")
    
    tab1, tab2, tab3 = st.tabs(["🚨 Risk Library", "🛡️ Mitigation Library", "🔗 Risk-Mitigation Mapping"])
    
    with tab1:
        st.subheader("Risk Library Management")
        
        # Enhanced risk creation
        with st.expander("➕ Add New Risk"):
            col1, col2 = st.columns(2)
            with col1:
                risk_id = st.text_input("Risk ID", placeholder="ADV006")
                risk_description = st.text_area("Risk Description")
                risk_impact = st.selectbox("Impact Level", ["Low", "Medium", "High", "Critical"])
            with col2:
                risk_likelihood = st.selectbox("Likelihood", ["Low", "Medium", "High", "Very High"])
                risk_domain = st.selectbox("Primary Domain", 
                    ["", "People", "Services", "Applications", "Network", "Data", 
                     "Information", "Products", "Process", "Facilities", "Platforms"])
                risk_category = st.selectbox("Risk Category", [
                    "Operational", "Technical", "Strategic", "Compliance", "Financial"
                ])
            
            if st.button("➕ Add Risk"):
                if risk_id and risk_description:
                    st.session_state.risks[risk_id] = {
                        'description': risk_description,
                        'impact': risk_impact,
                        'likelihood': risk_likelihood,
                        'domain': risk_domain,
                        'category': risk_category,
                        'created_date': datetime.now().isoformat()
                    }
                    st.success(f"✅ Risk {risk_id} added successfully!")
                    st.rerun()
        
        # Enhanced risk display with filtering
        if st.session_state.risks:
            st.subheader("Current Risk Library")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                impact_filter = st.selectbox("Filter by Impact", 
                    ["All"] + ["Critical", "High", "Medium", "Low"])
            with col2:
                domain_filter = st.selectbox("Filter by Domain", 
                    ["All"] + ["People", "Services", "Applications", "Network", "Data", 
                              "Information", "Products", "Process", "Facilities", "Platforms"])
            with col3:
                category_filter = st.selectbox("Filter by Category",
                    ["All"] + ["Operational", "Technical", "Strategic", "Compliance", "Financial"])
            
            # Apply filters
            filtered_risks = {}
            for risk_id, risk_info in st.session_state.risks.items():
                if (impact_filter == "All" or risk_info.get('impact') == impact_filter) and \
                   (domain_filter == "All" or risk_info.get('domain') == domain_filter) and \
                   (category_filter == "All" or risk_info.get('category') == category_filter):
                    filtered_risks[risk_id] = risk_info
            
            for risk_id, risk_info in filtered_risks.items():
                with st.container():
                    col1, col2, col3 = st.columns([4, 1, 1])
                    with col1:
                        st.write(f"**{risk_id}:** {risk_info['description']}")
                        impact_color = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}.get(risk_info['impact'], '⚪')
                        st.caption(f"{impact_color} Impact: {risk_info['impact']} | Likelihood: {risk_info.get('likelihood', 'Unknown')} | Domain: {risk_info.get('domain', 'General')} | Category: {risk_info.get('category', 'Unknown')}")
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_risk_{risk_id}"):
                            # Edit functionality placeholder
                            st.info("Edit mode - implementation in progress")
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_risk_{risk_id}"):
                            # Check if risk is used in mitigations
                            used_in_mitigations = [mid for mid, minfo in st.session_state.mitigations.items() 
                                                 if risk_id in minfo.get('mapped_risks', [])]
                            if used_in_mitigations:
                                st.warning(f"Risk {risk_id} is mapped to mitigations: {', '.join(used_in_mitigations)}. Remove mappings first.")
                            else:
                                del st.session_state.risks[risk_id]
                                st.success(f"Risk {risk_id} deleted!")
                                st.rerun()
                    st.markdown("---")
    
    with tab2:
        st.subheader("Mitigation Library Management")
        
        # Enhanced mitigation creation
        with st.expander("➕ Add New Mitigation"):
            col1, col2 = st.columns(2)
            with col1:
                mit_id = st.text_input("Mitigation ID", placeholder="MIT006")
                mit_description = st.text_area("Mitigation Description")
                mit_effectiveness = st.selectbox("Effectiveness", ["Low", "Medium", "High"])
            with col2:
                mit_cost = st.selectbox("Implementation Cost", ["Low", "Medium", "High"])
                mit_domain = st.selectbox("Implementation Domain", 
                    ["", "People", "Services", "Applications", "Network", "Data", 
                     "Information", "Products", "Process", "Facilities", "Platforms"])
                mit_type = st.selectbox("Mitigation Type", [
                    "Preventive", "Detective", "Corrective", "Compensating"
                ])
            
            # Risk mapping
            available_risks = list(st.session_state.risks.keys())
            mapped_risks = st.multiselect(
                "Addresses Risks", 
                available_risks,
                format_func=lambda x: f"{x}: {st.session_state.risks[x]['description'][:50]}..."
            )
            
            if st.button("➕ Add Mitigation"):
                if mit_id and mit_description:
                    st.session_state.mitigations[mit_id] = {
                        'description': mit_description,
                        'effectiveness': mit_effectiveness,
                        'cost': mit_cost,
                        'domain': mit_domain,
                        'type': mit_type,
                        'mapped_risks': mapped_risks,
                        'created_date': datetime.now().isoformat()
                    }
                    st.success(f"✅ Mitigation {mit_id} added successfully!")
                    st.rerun()
        
        # Enhanced mitigation display
        if st.session_state.mitigations:
            st.subheader("Current Mitigation Library")
            
            # Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                eff_filter = st.selectbox("Filter by Effectiveness", 
                    ["All"] + ["High", "Medium", "Low"])
            with col2:
                cost_filter = st.selectbox("Filter by Cost", 
                    ["All"] + ["Low", "Medium", "High"])
            with col3:
                type_filter = st.selectbox("Filter by Type",
                    ["All"] + ["Preventive", "Detective", "Corrective", "Compensating"])
            
            # Apply filters
            filtered_mitigations = {}
            for mit_id, mit_info in st.session_state.mitigations.items():
                if (eff_filter == "All" or mit_info.get('effectiveness') == eff_filter) and \
                   (cost_filter == "All" or mit_info.get('cost') == cost_filter) and \
                   (type_filter == "All" or mit_info.get('type') == type_filter):
                    filtered_mitigations[mit_id] = mit_info
            
            for mit_id, mit_info in filtered_mitigations.items():
                with st.container():
                    col1, col2, col3 = st.columns([4, 1, 1])
                    with col1:
                        st.write(f"**{mit_id}:** {mit_info['description']}")
                        eff_color = {'High': '🟢', 'Medium': '🟡', 'Low': '🔴'}.get(mit_info.get('effectiveness'), '⚪')
                        cost_color = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}.get(mit_info.get('cost'), '⚪')
                        st.caption(f"{eff_color} Effectiveness: {mit_info.get('effectiveness', 'Unknown')} | {cost_color} Cost: {mit_info.get('cost', 'Unknown')} | Type: {mit_info.get('type', 'Unknown')} | Domain: {mit_info.get('domain', 'General')}")
                        
                        if mit_info.get('mapped_risks'):
                            st.caption(f"🔗 Addresses: {', '.join(mit_info['mapped_risks'])}")
                    
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_mit_{mit_id}"):
                            st.info("Edit mode - implementation in progress")
                    with col3:
                        if st.button("🗑️ Delete", key=f"delete_mit_{mit_id}"):
                            del st.session_state.mitigations[mit_id]
                            st.success(f"Mitigation {mit_id} deleted!")
                            st.rerun()
                    st.markdown("---")
    
    with tab3:
        st.subheader("🔗 Risk-Mitigation Mapping Overview")
        
        if st.session_state.risks and st.session_state.mitigations:
            # Create mapping visualization
            mapping_data = []
            
            for mit_id, mit_info in st.session_state.mitigations.items():
                mapped_risks = mit_info.get('mapped_risks', [])
                for risk_id in mapped_risks:
                    if risk_id in st.session_state.risks:
                        risk_info = st.session_state.risks[risk_id]
                        mapping_data.append({
                            'Risk ID': risk_id,
                            'Risk Description': risk_info['description'][:50] + '...',
                            'Risk Impact': risk_info['impact'],
                            'Mitigation ID': mit_id,
                            'Mitigation Description': mit_info['description'][:50] + '...',
                            'Mitigation Effectiveness': mit_info.get('effectiveness', 'Unknown'),
                            'Implementation Cost': mit_info.get('cost', 'Unknown')
                        })
            
            if mapping_data:
                mapping_df = pd.DataFrame(mapping_data)
                st.dataframe(mapping_df, use_container_width=True)
                
                # Summary statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    total_mappings = len(mapping_data)
                    st.metric("Total Mappings", total_mappings)
                
                with col2:
                    covered_risks = len(set([m['Risk ID'] for m in mapping_data]))
                    total_risks = len(st.session_state.risks)
                    st.metric("Covered Risks", f"{covered_risks}/{total_risks}")
                
                with col3:
                    coverage_pct = (covered_risks / total_risks * 100) if total_risks > 0 else 0
                    st.metric("Coverage %", f"{coverage_pct:.1f}%")
                
                # Unmapped risks
                mapped_risk_ids = set([m['Risk ID'] for m in mapping_data])
                unmapped_risks = [rid for rid in st.session_state.risks.keys() if rid not in mapped_risk_ids]
                
                if unmapped_risks:
                    st.warning("**⚠️ Risks without Mitigations:**")
                    for risk_id in unmapped_risks:
                        risk_info = st.session_state.risks[risk_id]
                        st.write(f"• **{risk_id}**: {risk_info['description']} (Impact: {risk_info['impact']})")
            else:
                st.info("No risk-mitigation mappings found. Add mappings in the Mitigation Library.")
        else:
            st.info("Create risks and mitigations first to view mappings.")

def render_project_save_controls(project_name, project_data):
    """Render project save controls and export functionality"""
    st.markdown("---")
    st.markdown("### 💾 Project Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Project", use_container_width=True):
            # Auto-save is handled by session state
            st.success("✅ Project saved successfully!")
    
    with col2:
        # Export project data as JSON
        if st.button("📤 Export Project", use_container_width=True):
            project_json = json.dumps(project_data, indent=2, default=str)
            st.download_button(
                label="⬇️ Download JSON",
                data=project_json,
                file_name=f"{project_name.replace(' ', '_')}_export.json",
                mime="application/json"
            )
    
    with col3:
        # Project statistics
        domains = ["People", "Services", "Applications", "Network", "Data", 
                  "Information", "Products", "Process", "Facilities", "Platforms"]
        total_items = sum(len(project_data.get(f'{domain}_elements', [])) + 
                         len(project_data.get(f'{domain}_risks', [])) + 
                         len(project_data.get(f'{domain}_mitigations', [])) 
                         for domain in domains)
        
        st.info(f"📊 **Total Items:** {total_items}")
    
    # Last updated info
    if 'last_updated' in project_data:
        st.caption(f"Last updated: {project_data['last_updated']}")
    else:
        st.caption(f"Created: {project_data['created_date']}")

def project_management():
    """Enhanced project management with visual canvas and summary dashboard"""
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
        
        # Project header with enhanced status management
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Project ID", project_data['id'])
        with col2:
            new_status = st.selectbox("Status", ["Open", "In Progress", "Closed"], 
                                    index=["Open", "In Progress", "Closed"].index(project_data['status']))
            if new_status != project_data['status']:
                project_data['status'] = new_status
                project_data['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.rerun()
        with col3:
            st.write(f"**Owner:** {project_data['owner']}")
            st.write(f"**Created:** {project_data['created_date'][:10]}")
        with col4:
            completion = calculate_completion_score(project_data)
            st.metric("Completion", f"{completion}%")
        
        if project_data['description']:
            st.info(f"📋 **Description:** {project_data['description']}")
        
        st.markdown("---")
        
        # Tabbed interface for different views
        canvas_tab, summary_tab, domains_tab = st.tabs([
            "🎨 Visual Canvas", 
            "📊 Project Summary", 
            "🏗️ Domain Details"
        ])
        
        with canvas_tab:
            render_interactive_visual_canvas(project_data)
        
        with summary_tab:
            render_project_summary_dashboard(project_data)
        
        with domains_tab:
            render_domain_details_view(project_data)
        
        # Project save controls
        render_project_save_controls(selected_project, project_data)

def render_domain_details_view(project_data):
    """Render detailed domain management view"""
    st.markdown("### 🏗️ Architecture Domain Details")
    
    # Custom CSS for enhanced styling
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
        border-style: solid;import streamlit as st
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
    
    if 'interactions' not in st.session_state:
        st.session_state.interactions = {}
    
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None

# Domain positions for visual canvas (normalized coordinates)
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
    """Render an interactive visual canvas using pure Streamlit components"""
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
    
    # Create visual canvas using pure HTML/CSS
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
            # Get available risks and mitigations for interaction
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
    """Create a pure HTML/CSS visual canvas representation"""
    
    # Get connection data
    connections = project_data.get('canvas_connections', [])
    
    # Create SVG-style canvas using HTML/CSS
    canvas_html = """
    <div style="width: 100%; height: 600px; background: #F8F9FA; border: 2px solid #E0E0E0; border-radius: 12px; position: relative; overflow: hidden; margin: 20px 0;">
        <h3 style="text-align: center; margin-top: 20px; color: #333;">Security Architecture Canvas - Visual View</h3>
    """
    
    # Add domain nodes
    for domain, pos in DOMAIN_POSITIONS.items():
        # Calculate position in pixels
        x_px = int(pos['x'] * 800)
        y_px = int((1 - pos['y']) * 500) + 60  # Flip Y and add offset
        
        # Count elements, risks, and mitigations
        elements_count = len(project_data.get(f'{domain}_elements', []))
        risks_count = len(project_data.get(f'{domain}_risks', []))
        mits_count = len(project_data.get(f'{domain}_mitigations', []))
        
        # Determine node size based on content
        total_items = elements_count + risks_count + mits_count
        node_size = max(60, min(100, 60 + total_items * 5))
        
        # Connection count
        connection_count = len([c for c in connections if c['source'] == domain or c['target'] == domain])
        
        # Node HTML
        canvas_html += f"""
        <div style="position: absolute; left: {x_px - node_size//2}px; top: {y_px - node_size//2}px; 
                    width: {node_size}px; height: {node_size}px; 
                    background: {pos['color']}; border-radius: 50%; 
                    display: flex; align-items: center; justify-content: center; 
                    color: white; font-weight: bold; font-size: 11px; 
                    border: 3px solid white; box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                    z-index: 10;">
            {domain}
        </div>
        """
        
        # Details box if enabled
        if show_details:
            canvas_html += f"""
            <div style="position: absolute; left: {x_px - 40}px; top: {y_px + node_size//2 + 10}px; 
                        background: white; padding: 4px 8px; border-radius: 8px; 
                        border: 1px solid #DDD; font-size: 10px; color: #666; 
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                E:{elements_count} R:{risks_count} M:{mits_count}<br>
                🔗:{connection_count}
            </div>
            """
    
    # Add connection lines
    for conn in connections:
        source_pos = DOMAIN_POSITIONS[conn['source']]
        target_pos = DOMAIN_POSITIONS[conn['target']]
        
        x1 = int(source_pos['x'] * 800)
        y1 = int((1 - source_pos['y']) * 500) + 60
        x2 = int(target_pos['x'] * 800)
        y2 = int((1 - target_pos['y']) * 500) + 60
        
        # Determine line color and style
        if conn['risk']:
            line_color = '#FF6B6B'
            line_style = 'dashed'
            line_width = '3px'
        elif conn['mitigation']:
            line_color = '#4ECDC4'
            line_style = 'solid'
            line_width = '3px'
        else:
            line_color = '#95A5A6'
            line_style = 'solid'
            line_width = '2px'
        
        # Calculate line properties
        length = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
        angle = 0 if x2 == x1 else (y2 - y1) / (x2 - x1)
        angle_deg = 0 if x2 == x1 else (180/3.14159) * (y2 - y1) / (x2 - x1) if x2 != x1 else 90
        
        # Connection line
        canvas_html += f"""
        <div style="position: absolute; left: {min(x1, x2)}px; top: {min(y1, y2)}px; 
                    width: {abs(x2-x1)}px; height: {abs(y2-y1)}px; 
                    border-top: {line_width} {line_style} {line_color}; 
                    transform-origin: top left;
                    opacity: 0.8; z-index: 1;">
        </div>
        """
        
        # Connection label
        mid_x = (x1 + x2) // 2
        mid_y = (y1 + y2) // 2
        
        canvas_html += f"""
        <div style="position: absolute; left: {mid_x - 30}px; top: {mid_y - 10}px; 
                    background: white; padding: 2px 6px; border-radius: 4px; 
                    border: 1px solid {line_color}; font-size: 9px; color: {line_color}; 
                    z-index: 5;">
            {conn['type'].replace('<<', '').replace('>>', '')}
        </div>
        """
        
        # Arrow
        canvas_html += f"""
        <div style="position: absolute; left: {x2 - 8}px; top: {y2 - 8}px; 
                    width: 0; height: 0; 
                    border-left: 8px solid {line_color}; 
                    border-top: 4px solid transparent; 
                    border-bottom: 4px solid transparent; 
                    z-index: 5;">
        </div>
        """
    
    # Legend
    canvas_html += """
    <div style="position: absolute; right: 20px; top: 60px; background: white; 
                padding: 15px; border-radius: 8px; border: 1px solid #DDD; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.1); z-index: 10;">
        <h4 style="margin: 0 0 10px 0; font-size: 12px;">Legend</h4>
        <div style="margin-bottom: 5px;">
            <span style="display: inline-block; width: 20px; height: 3px; background: #FF6B6B; 
                         border-style: dashed; margin-right: 8px;"></span>
            <span style="font-size: 10px;">Risk Connection</span>
        </div>
        <div style="margin-bottom: 5px;">
            <span style="display: inline-block; width: 20px; height: 3px; background: #4ECDC4; 
                         margin-right: 8px;"></span>
            <span style="font-size: 10px;">Mitigation Connection</span>
        </div>
        <div>
            <span style="display: inline-block; width: 20px; height: 2px; background: #95A5A6; 
                         margin-right: 8px;"></span>
            <span style="font-size: 10px;">General Connection</span>
        </div>
    </div>
    """
    
    canvas_html += "</div>"
    
    st.markdown(canvas_html, unsafe_allow_html=True)

def analyze_risk_coverage(project_risks, project_mitigations):
    """Analyze which risks are covered by mitigations"""
    total_risks = len(project_risks)
    total_mitigations = len(project_mitigations)
    
    # Get all risk IDs that are covered by mitigations
    covered_risk_ids = set()
    for mitigation in project_mitigations:
        mapped_risks = mitigation.get('mapped_risks', [])
        covered_risk_ids.update(mapped_risks)
    
    # Find which project risks are covered
    project_risk_ids = {risk['id'] for risk in project_risks}
    covered_project_risks = project_risk_ids.intersection(covered_risk_ids)
    uncovered_project_risks = project_risk_ids - covered_risk_ids
    
    coverage_percentage = (len(covered_project_risks) / total_risks * 100) if total_risks > 0 else 0
    
    uncovered_risk_details = [
        risk for risk in project_risks 
        if risk['id'] in uncovered_project_risks
    ]
    
    return {
        'total_risks': total_risks,
        'total_mitigations': total_mitigations,
        'covered_risks': len(covered_project_risks),
        'uncovered_risks': len(uncovered_project_risks),
        'coverage_percentage': coverage_percentage,
        'uncovered_risk_details': uncovered_risk_details
    }

def calculate_completion_score(project_data):
    """Calculate project completion percentage based on various factors"""
    score = 0
    max_score = 100
    
    # Domain elements (30 points)
    domains = ["People", "Services", "Applications", "Network", "Data", 
              "Information", "Products", "Process", "Facilities", "Platforms"]
    
    populated_domains = sum(1 for domain in domains 
                           if len(project_data.get(f'{domain}_elements', [])) > 0)
    score += (populated_domains / len(domains)) * 30
    
    # Connections (25 points)
    connections = len(project_data.get('canvas_connections', []))
    if connections > 0:
        score += min(25, connections * 5)  # Max 25 points for connections
    
    # Risk assignment (25 points)
    total_risks = sum(len(project_data.get(f'{domain}_risks', [])) for domain in domains)
    if total_risks > 0:
        score += min(25, total_risks * 3)  # Max 25 points for risks
    
    # Mitigation assignment (20 points)
    total_mitigations = sum(len(project_data.get(f'{domain}_mitigations', [])) for domain in domains)
    if total_mitigations > 0:
        score += min(20, total_mitigations * 3)  # Max 20 points for mitigations
    
    return min(100, int(score))

def render_project_summary_dashboard(project_data):
    """Enhanced project summary with risk/mitigation analysis using ONLY native Streamlit components"""
    if not project_data:
        return
    
    st.markdown("### 📊 Project Summary Dashboard")
    
    # Project status and metadata
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_color = {
            'Open': '🔵',
            'In Progress': '🟡', 
            'Closed': '🟢'
        }
        st.metric("Project Status", 
                 f"{status_color.get(project_data['status'], '⚪')} {project_data['status']}")
    
    with col2:
        domains = ["People", "Services", "Applications", "Network", "Data", 
                  "Information", "Products", "Process", "Facilities", "Platforms"]
        total_elements = sum(len(project_data.get(f'{domain}_elements', [])) for domain in domains)
        st.metric("Total Elements", total_elements)
    
    with col3:
        total_connections = len(project_data.get('canvas_connections', []))
        st.metric("Connections", total_connections)
    
    with col4:
        completion_score = calculate_completion_score(project_data)
        st.metric("Completion", f"{completion_score}%")
    
    # Risk and Mitigation Summary
    st.markdown("#### 🚨 Risk & Mitigation Analysis")
    
    # Collect all risks and mitigations from project
    project_risks = []
    project_mitigations = []
    
    domains = ["People", "Services", "Applications", "Network", "Data", 
              "Information", "Products", "Process", "Facilities", "Platforms"]
    
    for domain in domains:
        domain_risks = project_data.get(f'{domain}_risks', [])
        domain_mits = project_data.get(f'{domain}_mitigations', [])
        
        for risk_id in domain_risks:
            if risk_id in st.session_state.risks:
                risk_info = st.session_state.risks[risk_id].copy()
                risk_info['id'] = risk_id
                risk_info['domain_assigned'] = domain
                project_risks.append(risk_info)
        
        for mit_id in domain_mits:
            if mit_id in st.session_state.mitigations:
                mit_info = st.session_state.mitigations[mit_id].copy()
                mit_info['id'] = mit_id
                mit_info['domain_assigned'] = domain
                project_mitigations.append(mit_info)
    
    # Risk/Mitigation metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### 📈 Risk Summary")
        
        if project_risks:
            # Risk by impact using native Streamlit chart
            risk_impact_counts = {}
            for risk in project_risks:
                impact = risk.get('impact', 'Unknown')
                risk_impact_counts[impact] = risk_impact_counts.get(impact, 0) + 1
            
            if risk_impact_counts:
                impact_df = pd.DataFrame(
                    list(risk_impact_counts.items()), 
                    columns=['Impact', 'Count']
                )
                
                st.bar_chart(impact_df.set_index('Impact'))
                
                # Summary table
                st.write("**Risk Distribution:**")
                for impact, count in risk_impact_counts.items():
                    color = {'Critical': '🔴', 'High': '🟠', 'Medium': '🟡', 'Low': '🟢'}.get(impact, '⚪')
                    st.write(f"{color} {impact}: {count} risks")
            
            # Risk details table
            risk_df = pd.DataFrame([{
                'Risk ID': r['id'],
                'Description': r['description'][:50] + '...',
                'Impact': r['impact'],
                'Domain': r['domain_assigned']
            } for r in project_risks])
            
            st.dataframe(risk_df, use_container_width=True)
        
        else:
            st.info("No risks assigned to this project yet.")
    
    with col2:
        st.markdown("##### 🛡️ Mitigation Summary")
        
        if project_mitigations:
            # Mitigation effectiveness using native chart
            mit_effectiveness = {}
            for mit in project_mitigations:
                eff = mit.get('effectiveness', 'Unknown')
                mit_effectiveness[eff] = mit_effectiveness.get(eff, 0) + 1
            
            if mit_effectiveness:
                eff_df = pd.DataFrame(
                    list(mit_effectiveness.items()), 
                    columns=['Effectiveness', 'Count']
                )
                
                st.bar_chart(eff_df.set_index('Effectiveness'))
                
                # Summary table
                st.write("**Effectiveness Distribution:**")
                for eff, count in mit_effectiveness.items():
                    color = {'High': '🟢', 'Medium': '🟡', 'Low': '🔴'}.get(eff, '⚪')
                    st.write(f"{color} {eff}: {count} mitigations")
            
            # Mitigation details table
            mit_df = pd.DataFrame([{
                'Mitigation ID': m['id'],
                'Description': m['description'][:50] + '...',
                'Effectiveness': m['effectiveness'],
                'Domain': m['domain_assigned']
            } for m in project_mitigations])
            
            st.dataframe(mit_df, use_container_width=True)
        
        else:
            st.info("No mitigations assigned to this project yet.")
    
    # Risk-Mitigation Coverage Analysis
    st.markdown("#### 🎯 Risk Coverage Analysis")
    
    coverage_analysis = analyze_risk_coverage(project_risks, project_mitigations)
    
    if coverage_analysis['total_risks'] > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Covered Risks", 
                f"{coverage_analysis['covered_risks']}/{coverage_analysis['total_risks']}",
                delta=f"{coverage_analysis['coverage_percentage']:.1f}% coverage"
            )
        
        with col2:
            st.metric(
                "Uncovered Risks", 
                coverage_analysis['uncovered_risks'],
                delta=f"{100-coverage_analysis['coverage_percentage']:.1f}% remaining"
            )
        
        with col3:
            st.metric(
                "Total Mitigations", 
                coverage_analysis['total_mitigations']
            )
        
        # Coverage visualization using pure text/emoji representation
        if coverage_analysis['total_risks'] > 0:
            st.markdown("##### 📊 Risk Coverage Visualization")
            
            covered = coverage_analysis['covered_risks']
            uncovered = coverage_analysis['uncovered_risks']
            total = coverage_analysis['total_risks']
            
            # Create a simple text-based progress bar
            coverage_pct = coverage_analysis['coverage_percentage']
            filled_blocks = int(coverage_pct / 5)  # Each block represents 5%
            empty_blocks = 20 - filled_blocks
            
            progress_bar = "🟢" * filled_blocks + "⚪" * empty_blocks
            
            st.write(f"**Coverage Progress:** {coverage_pct:.1f}%")
            st.write(progress_bar)
            
            # Coverage breakdown
            col_a, col_b = st.columns(2)
            with col_a:
                st.success(f"✅ **Covered:** {covered} risks ({covered/total*100:.1f}%)")
            with col_b:
                st.error(f"❌ **Uncovered:** {uncovered} risks ({uncovered/total*100:.1f}%)")
        
        # Show uncovered risks if any
        if coverage_analysis['uncovered_risk_details']:
            st.warning("**⚠️ Uncovered Risks:**")
            for risk in coverage_analysis['uncovered_risk_details']:
                st.write(f"• **{risk['id']}**: {risk['description']} (Impact: {risk['impact']})")

def render_expandable_domain(domain_name, domain_id, css_class, project_data):
    """Enhanced domain rendering with connection awareness"""
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
    
    # Check connections involving this domain
    connections = project_data.get('canvas_connections', [])
    domain_connections = [c for c in connections 
                         if c['source'] == domain_name or c['target'] == domain_name]
    
    # Domain container with connection indicator
    connection_indicator = f" 🔗({len(domain_connections)})" if domain_connections else ""
    
    domain_html = f"""
    <div class="archimate-domain {css_class}" style="position: relative;">
        <div class="domain-header">{domain_id}<br>{domain_name}{connection_indicator}</div>
    """
    
    # Elements section
    if project_data[elements_key]:
        domain_html += "<div style='margin-bottom: 10px;'>"
        for element in project_data[elements_key]:
            domain_html += f'<div class="domain-element">{element}</div>'
        domain_html += "</div>"
    
    # Risks section with enhanced display
    if project_data[risks_key]:
        domain_html += "<div style='margin-bottom: 8px;'><strong style='font-size: 11px;'>Risks:</strong><br>"
        for risk_id in project_data[risks_key]:
            risk_info = st.session_state.risks.get(risk_id, {})
            impact_color = {
                'Critical': '#FF4444',
                'High': '#FF8800',
                'Medium': '#FFBB33', 
                'Low': '#00CC44'
            }.get(risk_info.get('impact', ''), '#666666')
            
            domain_html += f'''
            <div class="risk-element" style="border-color: {impact_color}; background-color: {impact_color}20;">
                ⚠️ {risk_id} ({risk_info.get('impact', 'Unknown')})
            </div>
            '''
        domain_html += "</div>"
    
    # Mitigations section with enhanced display
    if project_data[mitigations_key]:
        domain_html += "<div style='margin-bottom: 8px;'><strong
