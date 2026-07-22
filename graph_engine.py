import networkx as nx
from pyvis.network import Network
import json
import os

def generate_fraud_graph(json_file_path="data/mock_scams.json"):
    # 1. Load the mock data
    if not os.path.exists(json_file_path):
        # Create an empty graph if file doesn't exist
        return None
        
    with open(json_file_path, 'r') as f:
        scam_data = json.load(f)

    # 2. Initialize NetworkX Graph
    G = nx.Graph()

    # 3. Process each case and create nodes/edges
    for case in scam_data:
        victim = case['victim_name']
        phone = case['scammer_phone']
        upi = case['upi_id']
        imei = case['device_imei']
        
        # Add Nodes with Type Attributes
        G.add_node(victim, label=victim, type='victim', color='#0275d8', size=20)
        G.add_node(phone, label=phone, type='phone', color='#d9534f', size=25)
        G.add_node(upi, label=upi, type='upi', color='#f0ad4e', size=25)
        G.add_node(imei, label=imei, type='device', color='#5bc0de', size=15)

        # Add Edges (Relationships)
        G.add_edge(phone, victim, title=f"Targeted as {case['scammer_alias']}")
        G.add_edge(victim, upi, title=f"Transferred ₹{case['amount_lost']}")
        G.add_edge(phone, imei, title="Device Fingerprint")

    # 4. Convert to PyVis Network
    net = Network(height="500px", width="100%", bgcolor="#ffffff", font_color="#333333", heading="Neural Link Analysis")
    
    # Apply Physics for that "moving" effect
    net.from_nx(G)
    net.toggle_physics(True)
    
    # 5. Save the graph to an HTML file
    output_path = "fraud_graph.html"
    net.save_graph(output_path)
    
    return output_path

if __name__ == "__main__":
    # Test run
    generate_fraud_graph()