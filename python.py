import tkinter as tk
from tkinter import messagebox
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def choose_role(role):
    role_label.config(text=f"Role selected: {role}")
    initialize_army_graph()
    visualize_graph()

def initialize_army_graph():
    global G, home_node, destination_node

    G = nx.Graph()

    nodes = ["A Building", "B Building", "C Junction", "D Enemy Camp", "Home Node"]
    G.add_nodes_from(nodes)

    G.add_edge("A Building", "B Building", cost=random.randint(1, 10))
    G.add_edge("A Building", "C Junction", cost=random.randint(1, 10))
    G.add_edge("B Building", "C Junction", cost=random.randint(1, 10))
    G.add_edge("B Building", "D Enemy Camp", cost=random.randint(1, 10))
    G.add_edge("C Junction", "D Enemy Camp", cost=random.randint(1, 10))
    G.add_edge("C Junction", "Home Node", cost=random.randint(1, 10))
    G.add_edge("D Enemy Camp", "Home Node", cost=random.randint(1, 10))

    home_node = "Home Node"
    destination_node = None

def select_destination(node):
    global destination_node
    destination_node = node
    destination_label.config(text=f"Destination selected: {node}")

def start_simulation():
    if 'G' not in globals():
        messagebox.showwarning("Error", "Please select a role first.")
        return

    if destination_node is None:
        messagebox.showwarning("Error", "Please select a destination node.")
        return

    path = nx.shortest_path(G, source=home_node, target=destination_node, weight='cost')

    result_message = f"Army is going to {destination_node} through the following path: {path}\n"
    total_cost = sum(G[path[i]][path[i+1]]['cost'] for i in range(len(path)-1))
    result_message += f"Total Cost/Injuries: {total_cost}"

    messagebox.showinfo("Simulation Result", result_message)

def visualize_graph():
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_size=8, font_color='black')
    plt.title("Graph Visualization")
    canvas.draw()

root = tk.Tk()
root.title("Graph Traverse Game")

welcome_label = tk.Label(root, text="Welcome to the game", font=("Helvetica", 16))
welcome_label.pack(pady=10)

choose_role_label = tk.Label(root, text="Choose a Role:")
choose_role_label.pack()

roles = ["Army", "Volunteer", "Rescuer"]
for role in roles:
    role_button = tk.Button(root, text=role, command=lambda r=role: choose_role(r))
    role_button.pack(pady=5)

role_label = tk.Label(root, text="Role selected: None", font=("Helvetica", 12))
role_label.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy)
exit_button.pack(pady=10)

destination_label = tk.Label(root, text="Destination selected: None", font=("Helvetica", 12))
destination_label.pack(pady=10)

destination_button_frame = tk.Frame(root)
destination_button_frame.pack(pady=10)

for node in ["A Building", "B Building", "C Junction", "D Enemy Camp"]:
    destination_button = tk.Button(destination_button_frame, text=node, command=lambda n=node: select_destination(n))
    destination_button.pack(side=tk.LEFT, padx=5)

start_simulation_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_simulation_button.pack(pady=10)

# Matplotlib canvas
figure, ax = plt.subplots()
canvas = FigureCanvasTkAgg(figure, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Start the Tkinter event loop
root.mainloop()
