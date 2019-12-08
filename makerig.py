import bpy


class created_objects(object):
    # static list of 
    objects_list=[]

class tree_node(object):
    children: None
    parent: None
    edge_index: None
    empty: None
    vertex_index: None
    bone_name: None
    coordinates: None
    def __init__(self):
        self.children = []
    def prettyprint(self, tab):
        result = "\n"
        result += tab + "co " + str(self.coordinates)
        tab += "-"
        for child in self.children:
            result += child.prettyprint(tab)
        return result
    def set_bone_name(self, name):
        self.bone_name = name
    def __str__(self):
        return self.prettyprint("|-")
 
class vertex_map_item(object):
    # vertex_index of vertex in vertices array
    vertex_index = -1
    # distance to reference object
    distance = -1
    # array of edgesindexes for this node
    edgesIdx = None
    # whether the node has been visited (IMPORTANT TO AVOID INFINITE RECURSIONS!!)
    visited = False
    # connected nodes
    neighbors = None

    def __init__(self):
        # set of connections (vertices indexes)
        self.neighbors = set()
        # set of edges indices
        self.edgesIdx = set()
    def add_edge(self, newEdge):
        self.edgesIdx.add(newEdge)
    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)
    def __str__(self):
        return ("Index " + str(self.vertex_index) + " distance " + str(self.distance) + " edges " + str(self.edgesIdx) + " visited " + str(self.visited) + " neighbors " + str(self.neighbors))
    # Comparison operator for sorting
    def __lt__(self, other):
        return self.distance < other.distance
       
        
def make_dictionary(target_object, reference_location):
    edges = target_object.data.edges
    # Our main dictionary
    dictionary = {}
    # we want to obtain a dictionary of vertices, for which we have the list of edges
    # and of neighboring vertices
    for i in range(len(edges)):
        # For both vertices
        for j in range(2):
            entry = dictionary.get(edges[i].vertices[j], None)
            if (entry == None):
                entry = vertex_map_item()
                v2 = target_object.data.vertices[edges[i].vertices[j]].co
                entry.vertex_index = edges[i].vertices[j]
                entry.distance = (v2 - reference_location).length
                entry.add_edge(i)
                # adds the other vertex
                entry.add_neighbor(edges[i].vertices[(j + 1) % 2])
                dictionary[edges[i].vertices[j]] = entry
            else:
                entry.add_edge(i)
                entry.add_neighbor(edges[i].vertices[(j + 1) % 2])
    return dictionary

def get_nodes_of_tree2(dictionary, root_node, vertex_map_item, vertices):
    vertex_map_item.visited = True
    root_node.coordinates = vertices[vertex_map_item.vertex_index].co
    root_node.vertex_index = vertex_map_item.vertex_index
    if len(vertex_map_item.neighbors) == 0:
        return root_node
    for i in vertex_map_item.neighbors:
        child = dictionary.get(i)
        if (child.visited == False):
            child_node_tree = get_nodes_of_tree2(dictionary, tree_node(), child, vertices)
            root_node.add_child(child_node_tree)
    return root_node


def other_vertex_in_edge(vertex_index, edge):
    if (edge.vertices[0] == vertex_index):
        return edge.vertices[1]
    else:
        return edge.vertices[0]
    
    
def get_nodes_of_tree(dictionary, parent_node, via_edge, vertex_map_item, vertices, edges):
    # parent_node.coordinates = vertices[vertex_map_item.vertex_index]
    # parent_node.vertex_index = vertex_map_item.vertex_index
    # if we're on a leaf
    vertex_map_item.visited = True
    this_node = tree_node()
    this_node.vertex_index = vertex_map_item.vertex_index
    this_node.coordinates = vertices[this_node.vertex_index].co
    this_node.parent = parent_node
    this_node.edge_index = via_edge
    for idx_of_edge_around in vertex_map_item.edgesIdx:
        neighbor_vertex_idx = other_vertex_in_edge(vertex_map_item.vertex_index, edges[idx_of_edge_around])
        child = dictionary.get(neighbor_vertex_idx)
        if (child.visited == False):
            child_tree_node = get_nodes_of_tree(dictionary, this_node, idx_of_edge_around, child, vertices, edges)
            this_node.children.append(child_tree_node)
    return this_node

# make one or more node trees
def make_tree_set(sorted_vertices_list, vertices, edges, dictionary):
    tree_set = []
    for vtx_map_item in sorted_vertices_list:
        if not vtx_map_item.visited:
            # start a new tree
            tree_set.append(get_nodes_of_tree(dictionary, None, None, vtx_map_item, vertices, edges))
    return tree_set

def create_empty(vertex_index, target_object):
    # print(location, vertex_index, target_object)
    empty = bpy.data.objects.new( "empty", None )
    bpy.context.scene.collection.objects.link( empty )
    empty.empty_display_type = 'CUBE'
    empty.scale = (0.25, 0.25, 0.25)
    empty.parent = target_object
    empty.parent_type = 'VERTEX'
    # change for vertex index
    empty.parent_vertices[0] = vertex_index
    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.rotation_clear(clear_delta=False)
    created_objects.objects_list.append(empty)
    return empty

def make_empties(node, target_object):
    empty = create_empty(node.vertex_index, target_object)
    node.empty = empty
    for child in node.children:
        make_empties(child, target_object)

def make_empty_rig(target_object):
    armature = bpy.data.armatures.new(target_object.name + "_vBones")
    rig = bpy.data.objects.new(target_object.name + '_vRig', armature)
    rig.location = target_object.location
    armature.display_type = 'STICK'
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.context.view_layer.update()
    created_objects.objects_list.append(rig)
    return rig, armature

def create_bone(head, tail, parent, armature):
    bone = armature.edit_bones.new("Bone")
    bone.head = head
    bone.tail = tail
    if parent != None:
        bone.parent = parent
        bone.use_connect = True
    return bone
    
def make_bones_from_tree(node, parent_node, parent_bone, armature):
    bone = None
    if parent_node != None:
        bone = create_bone(parent_node.coordinates, node.coordinates, parent_bone, armature)
        node.set_bone_name(bone.name)
    else:
        node.bone_name = None
    for child in node.children:
        make_bones_from_tree(child, node, bone, armature)
    
def make_bones(tree, rig, armature):
    bpy.context.view_layer.objects.active = rig
    bpy.context.view_layer.update()
    bpy.ops.object.editmode_toggle()
    make_bones_from_tree(tree, None, None, armature)
    bpy.ops.object.editmode_toggle()


def add_bone_constraint(pose_bone, empty):
    ik = pose_bone.constraints.new(type='IK')
    ik.target = empty
    ik.chain_count = 1

def add_bones_constraints(node, rig, armature):
    if node.bone_name != None:
        # print(node.bone_name)
        # print(rig.data.bones[node.bone_name])
        pose_bone = rig.pose.bones[node.bone_name]
        add_bone_constraint(pose_bone, node.empty)
    for child in node.children:
        add_bones_constraints(child, rig, armature)


def add_index_to_vertex_group(vertex_group, index, value):
    arr=[]
    arr.append(index)
    vertex_group.add(arr, value, 'ADD')

def assign_vertices_to_group(node, vertex_group, min_value, method, depth = 0):
    
    children_number = len(node.children)
    # leaf is always mean
    if (children_number == 0):
        add_index_to_vertex_group(vertex_group, node.vertex_index, min_value)
        print("assigning value of", min_value)
        return depth
    max_depth = depth
    for child in node.children:
        max_depth = max(max_depth, assign_vertices_to_group(child, vertex_group, min_value, method, depth + 1))
    print("Vertex ", node.coordinates, "max depth", max_depth, "depth", depth)
    if (depth == 0):
        # root is always 1
        add_index_to_vertex_group(vertex_group, node.vertex_index, 1.0)    
    else:
        value = 1- ((1 - min_value) * depth/max_depth)
        print("--- Assigning value of", value)
        add_index_to_vertex_group(vertex_group, node.vertex_index, value)
    return max_depth

def cleanup_previous_rigs(target_object, vertex_group_name, cloth_sim_name):
    print("Created previously", len(created_objects.objects_list))
    for obj in created_objects.objects_list:
        print("Removing", obj)
        bpy.data.objects.remove(obj, do_unlink=True )
    # remove cloth sim
    modifier_to_remove = None
    for modifier in target_object.modifiers:
        if modifier.type == 'CLOTH':
            print ("Removing modifier", modifier)
            modifier_to_remove = modifier
            break        
    if (modifier_to_remove != None):
        target_object.modifiers.remove(modifier_to_remove)
    # vertex group
    vg = target_object.vertex_groups.get(vertex_group_name)
    if (vg != None):
        print("Removing", vg)
        target_object.vertex_groups.remove(vg)
    # clean objects list
    created_objects.objects_list = []
    

def make_gravity_rig(reference_object, target_object, min_value, context):
    #cleanup object stuff
    cleanup_previous_rigs(target_object, "__gravity_rig__", "GravityRigCloth")
    
    target_object_edges = target_object.data.edges
    target_object_vertices = target_object.data.vertices
    reference_location = reference_object.location

    # Make dictionary of vertices with distance info
    dictionary = make_dictionary(target_object, reference_location)
    
    sorted_vertices_list = []
    for key, value in sorted(dictionary.items(), key=lambda item: item[1]):
        sorted_vertices_list.append(value)

    tree_set = make_tree_set(sorted_vertices_list, target_object_vertices, target_object_edges, dictionary)
    print("Got ", len(tree_set), "trees")
    for tree in tree_set:
        print(str(tree))
    
    for tree in tree_set:
        make_empties(tree, target_object)
    rig, armature = make_empty_rig(target_object)
    for tree in tree_set:
        make_bones(tree, rig, armature)
    for tree in tree_set:
        add_bones_constraints(tree, rig, armature)
    vertex_group = target_object.vertex_groups.new(name="__gravity_rig__")
    for tree in tree_set:
        assign_vertices_to_group(tree, vertex_group, min_value, 'LINEAR' )
    mod = target_object.modifiers.new("GravityRigCloth", 'CLOTH')
    mod.settings.vertex_group_mass = vertex_group.name

    #mod.shape.
    # Make vertex group
    # Make collection
    # Add cloth sim
    # Address location issue
    # Address modes (edit vs intial mode)
    # Add controls (no faces, vertex #)
    