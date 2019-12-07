import bpy

class tree_node(object):
    # members
    coordinates = None
    children = None
    index = -1

    def __init__(self):
        self.children = []

    def prettyprint(self, tab):
        result = "\n"
        result += tab + "co " + str(self.coordinates)
        tab += "-"
        for child in self.children:
            result += child.prettyprint(tab)
        return result

    def __str__(self):
        return self.prettyprint("|-")

    def add_child(self, obj):
        self.children.append(obj)

class vertex_map_item(object):
    # index of vertex in vertices array
    index = -1
    # distance to reference object
    distance = -1
    # array of edgesindexes for this node
    edgesIdx = None
    # whether the node has been visited
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
    # Comparison operator for sorting
    def __lt__(self, other):
        return self.distance < other.distance


def relative_coordinates(coordinates, target_object):
    return coordinates - target_object.location

def make_dictionary(edges, target_object, reference_object):
    # Our main dictionary
    dictionary = {}
    # we want to obtain a dictionary of vertices, for which we have the list of edges
    # and of neighboring vertices
    v1 = reference_object.location
    for i in range(len(edges)):
        # For both vertices
        for j in range(2):
            entry = dictionary.get(edges[i].vertices[j], None)
            if (entry == None):
                entry = vertex_map_item()
                v2 = target_object.data.vertices[edges[i].vertices[j]].co
                entry.index = edges[i].vertices[j]
                entry.distance = (v2 - v1).length
                entry.add_edge(i)
                # adds the other vertex
                entry.add_neighbor(edges[i].vertices[(j + 1) % 2])
                dictionary[edges[i].vertices[j]] = entry
            else:
                entry.add_edge(i)
                entry.add_neighbor(edges[i].vertices[(j + 1) % 2])
    return dictionary


def get_nodes_of_tree(dictionary, root_node, vertex_map_item, vertices):
    vertex_map_item.visited = True
    root_node.coordinates = vertices[vertex_map_item.index].co
    root_node.index = vertex_map_item.index
    if len(vertex_map_item.neighbors) == 0:
        return root_node
    for i in vertex_map_item.neighbors:
        child = dictionary.get(i)
        if (child.visited == False):
            child_node_tree = get_nodes_of_tree(dictionary, tree_node(), child, vertices)
            root_node.add_child(child_node_tree)
    return root_node


# make one or more node trees
def make_tree_set(sorted_vertices_list, vertices, dictionary):
    tree_set = []
    for vertex_map_item in sorted_vertices_list:
        if not vertex_map_item.visited:
            t_node = tree_node()
            t_node.coordinates = vertices[vertex_map_item.index]
            t_node.index = vertex_map_item.index
            # start a new tree
            tree_set.append(get_nodes_of_tree(dictionary, t_node, vertex_map_item, vertices))
    return tree_set


def create_empty(location, index, target_object):
    # print(location, index, target_object)
    empty = bpy.data.objects.new( "empty", None )
    bpy.context.scene.collection.objects.link( empty )
    empty.location = location
    empty.empty_display_type = 'CUBE'
    empty.scale = (0.25, 0.25, 0.25)
    empty.parent = target_object
    empty.parent_type = 'VERTEX'
    # change for vertex index
    empty.parent_vertices[0] = index
    bpy.ops.object.location_clear(clear_delta=False)
    bpy.ops.object.rotation_clear(clear_delta=False)
    return empty

def bone_name(tree_idx, idx):
    return str(1000*tree_idx + idx)

def create_bone2(tree_idx, head_location, tail_location, parent_bone, armature, rig, index, empty):
    bpy.context.view_layer.objects.active = rig
    bpy.context.view_layer.update()
    bpy.ops.object.editmode_toggle()

    # Add and setup bone
    bone = armature.edit_bones.new(bone_name(tree_idx, index))
    if (head_location != None):
         bone.head = head_location
    if (tail_location != None):
        bone.tail = tail_location
    if (parent_bone != None):
        print("Idx", index, "parenting bone", bone, "to", parent_bone)
        bone.parent = parent_bone
        if (bone.parent != parent_bone):
            print("Error parenting")
        bone.use_connect = True
    else:
        print("Idx", index, "not parenting bone", bone)
    bpy.ops.object.editmode_toggle()

    # bpy.ops.object.posemode_toggle()
    # Add IK constraint
    # armature.bones[len(armature.bones) - 1].select = True
    # armature.bones.active = armature.bones[len(armature.bones) - 1]
    # print("Active bone", armature.bones.active)
    # pose_bone = bpy.context.selected_pose_bones_from_active_object[
    #     len(bpy.context.selected_pose_bones_from_active_object) - 1]
    # ik = pose_bone.constraints.new(type='IK')
    # ik.target = empty
    # ik.chain_count = 1
    # bpy.ops.object.posemode_toggle()
    return bone


def make_rig(node, tree_idx, parent_node, rig, armature, bone, idx, target_object, empties_dictionary):
    # if we're a leaf (no children), do nothing and return
    # If we're not a leaf (root node or other node)
    if len(node.children) != 0:
        if parent_node == None:
            # no parent: we're the root
            # Create an empty
            empty_root = create_empty(relative_coordinates(node.coordinates, target_object), node.index, target_object)
            empties_dictionary.add(idx, empty_root)
        for child in node.children:
            idx += 1
            print("For idx", idx,"node","Bone " + str(node))
            empty = create_empty(child.coordinates, child.index, target_object)
            empties_dictionary.add(idx, empty)
            # Create a bone
            #child_bone = create_bone(tree_idx, node.coordinates, child.coordinates, bone, armature, rig, idx, empty)
            #idx = make_rig(child, tree_idx, node, rig, armature, child_bone, idx, target_object)
            idx = make_rig(child, tree_idx, node, rig, armature, None, idx, target_object, empties_dictionary)
    return idx



def create_bone(empties_dictionary, bones_dictionary, index, parent_index, rig, armature):
    bpy.context.view_layer.objects.active = rig
    bpy.context.view_layer.update()
    bpy.ops.object.editmode_toggle()
    # Add and setup bone
    print("indexes", index, parent_index)
    bone = armature.edit_bones.new(str(index))
    print("Inserting bone", bone,"at index", index)
    bones_dictionary[index] = bone
    empty = empties_dictionary[parent_index]
    bone.head = empty.location
    empty = empties_dictionary[index]
    bone.tail = empty.location
    print("Bones dictionary", len(bones_dictionary), bones_dictionary)
    for key in bones_dictionary.keys():
        print(key, bones_dictionary[key])
    if (parent_index != 0):
        print("parenting bone", index,"to", parent_index)
        parent_bone = bones_dictionary[parent_index]
        print("Found parent bone", parent_bone)
        bone.parent = parent_bone
        bone.use_connect = True
    bpy.ops.object.editmode_toggle()
    return bone

    
def make_bones(node, idx, bones_dictionary, empties_dictionary, target_object, rig, armature):
    if (len(node.children) != 0):
        my_index = idx
        for child in node.children:
            idx += 1
            bone = create_bone(empties_dictionary, bones_dictionary, idx, my_index, rig, armature)
            idx = make_bones(child, idx, bones_dictionary, empties_dictionary, target_object, rig, armature)
    return idx
            

def make_empties(node, parent_node, idx, empties_dictionary, target_object):
    if len(node.children) != 0:
        if parent_node == None:
            empty = create_empty(node.coordinates, node.index, target_object)
            empties_dictionary[idx] = empty
        for child in node.children:
            idx += 1
            empty = create_empty(child.coordinates, child.index, target_object)
            empties_dictionary[idx] = empty
            idx = make_empties(child, node, idx, empties_dictionary, target_object)
    return idx

# careful: each vertex may have seeral children
# so we can either take the max value or the min or average
# def recursive weight():
#     if len(tree_node.children) == 0:
#         # We're on a leaf
#         # Add to pin vertex group with min value
#         None
#     else
        
# falloff_function: whether we want quadratic, linear, etc
# distance_function: whether we use distance from reference, metric distance from root or chain length from root
# def calculate_weights(tree_node, falloff_function, distance_function, max_value, min_value, pin_vertex_group):
#     None
    

# reference_object
#   object the distance to which will be our sorting criterium
# target_object
#   object from which the armature will be generated and parented to
def make_gravity_rig(reference_object, target_object, context):
    target_object_edges = target_object.data.edges
    target_object_vertices = target_object.data.vertices
    reference_location = reference_object.location
    dictionary = make_dictionary(target_object_edges, target_object, reference_object)

    sorted_vertices_list = []
    for key, value in sorted(dictionary.items(), key=lambda item: item[1]):
        sorted_vertices_list.append(value)

    tree_set = make_tree_set(sorted_vertices_list, target_object_vertices, dictionary)

    print("Got ", len(tree_set), "trees")
    for tree in tree_set:
        print(str(tree))

    # Add armature and rig
    armature = bpy.data.armatures.new(target_object.name + "_vBones")
    rig = bpy.data.objects.new(target_object.name + '_vRig', armature)
    rig.location = target_object.location
    armature.display_type = 'STICK'
    bpy.context.collection.objects.link(rig)
    bpy.context.view_layer.objects.active = rig
    bpy.context.view_layer.update()
    save_location = target_object.location
    empties_dictionary = dict()
    for tree_idx in range(len(tree_set)):
        make_empties(tree_set[tree_idx], None, 0, empties_dictionary, target_object)
    print("Empties", len(empties_dictionary), empties_dictionary)
    for key in empties_dictionary.keys():
        print(key, empties_dictionary[key])
    bones_dictionary = dict()
    for tree_idx in range(len(tree_set)):
        make_bones(tree_set[tree_idx], 0, bones_dictionary, empties_dictionary, target_object, rig, armature)
    
    print("Bones", len(bones_dictionary), bones_dictionary)
    for key in bones_dictionary.keys():
        print(key, bones_dictionary[key])
        #make_rig(tree_set[tree_idx], tree_idx, None, rig, armature, None, 0, target_object, empties_dictionary)
    for key in empties_dictionary.keys():
        empties_dictionary[key].location=(0, 0, 0)
        

    

    # Affects vertex group to target object
    # bpy.context.view_layer.objects.active = target_object
    # target_object.vertex_group_add("gravity_rig")
    # Affect weights to vertex group according to selected falloff/gradient
    #for tree in tree_set:
    #    calculate_weights(rig_vertex_group, falloff, max_value, min_value)
    # Add cloth sim to target object with parameters