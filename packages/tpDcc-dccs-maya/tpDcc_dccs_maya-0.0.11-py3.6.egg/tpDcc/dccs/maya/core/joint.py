#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains functions and classes related with joints
"""

from __future__ import print_function, division, absolute_import

import math
import logging

import tpDcc.dccs.maya as maya
from tpDcc.libs.python import strings, python
from tpDcc.dccs.maya.core import exceptions, decorators, mathutils, scene, attribute, transform, node
from tpDcc.dccs.maya.core import transform as xform_utils, constraint as cns_utils, matrix as matrix_utils
from tpDcc.dccs.maya.core import name as name_utils, curve as curve_utils

LOGGER = logging.getLogger()


class BuildJointHierarchy(object):
    def __init__(self):
        self._transforms = list()
        self._replace_old = None
        self._replace_new = None

    def create(self):
        """
        Creates the new joint hierarchy
        :return: list<str>
        """

        new_joints = self._build_hierarchy()

        return new_joints

    def set_transforms(self, transform_list):
        """
        Set the list of transform that we need to create joint hierarchy for
        :param transform_list: list<str>
        """

        self._transforms = transform_list

    def set_replace(self, old, new):
        """
        Replace the naming in the new joints
        :param old: str, string in the duplicate name to replace
        :param new: str, string in the duplicate to replace with
        """

        self._replace_old = old
        self._replace_new = new

    def _build_hierarchy(self):
        new_joints = list()
        last_transform = None

        for xform in self._transforms:
            maya.cmds.select(clear=True)
            joint = maya.cmds.joint()
            xform_utils.MatchTransform(xform, joint).translation_rotation()
            xform_utils.MatchTransform(xform, joint).world_pivots()
            new_joints.append(joint)
            if last_transform:
                maya.cmds.parent(joint, last_transform)
            last_transform = joint

        return new_joints


class AttachJoints(object):
    """
    Attaches a chain of joints to a matching chain using parent and scale constraints
    """

    class AttachType(object):
        CONSTRAINT = 0
        MATRIX = 1

        @staticmethod
        def get_string_list():
            """
            Returns a list with the attach types as strings
            :return: list<str>
            """

            return ['Constraint', 'Matrix']

    def __init__(self, source_joints, target_joints):
        self._source_joints = source_joints
        self._target_joints = target_joints
        self._attach_type = AttachJoints.AttachType.CONSTRAINT

    # region Public Functions
    def create(self):
        """
        Creates the attachments
        """

        self._attach_joints(self._source_joints, self._target_joints)

    def set_source_and_target_joints(self, source_joints, target_joints):
        """
        :param source_joints: list<str>, list of joint names that should move the target
        :param target_joints: list<str>, list of joint names that should be moved by the source
        """

        self._source_joints = source_joints
        self._target_joints = target_joints

    def set_attach_type(self, attach_type):
        self._attach_type = attach_type

    # endregion

    # region Private Functions
    def _hook_scale_constraint(self, node):
        cns = cns_utils.Constraint()
        scale_cns = cns.get_constraint(node, cns_utils.Constraints.SCALE)
        if not scale_cns:
            return
        cns_utils.scale_constraint_to_world(scale_cns)

    def _unhook_scale_constraint(self, scale_constraint):
        cns_utils.scale_constraint_to_local(scale_constraint)

    def _attach_joint(self, source_joint, target_joint):
        if self._attach_type == AttachJoints.AttachType.CONSTRAINT:
            self._hook_scale_constraint(target_joint)
            parent_cns = maya.cmds.parentConstraint(source_joint, target_joint, mo=True)[0]
            maya.cmds.setAttr('{}.interpType'.format(parent_cns), 2)
            scale_cns = maya.cmds.scaleConstraint(source_joint, target_joint)[0]
            cns = cns_utils.Constraint()
            cns.create_switch(self._target_joints[0], 'switch', parent_cns)
            cns.create_switch(self._target_joints[0], 'switch', scale_cns)
            self._unhook_scale_constraint(scale_cns)
        elif self._attach_type == AttachJoints.AttachType.MATRIX:
            switches = cns_utils.SpaceSwitch().get_space_switches(target_joint)
            if switches:
                cns_utils.SpaceSwitch().add_source(source_joint, target_joint, switches[0])
                cns_utils.SpaceSwitch().create_switch(self._target_joints[0], 'switch', switches[0])
            else:
                switch = cns_utils.SpaceSwitch(source_joint, target_joint)
                switch.set_use_weight(True)
                switch_node = switch.create()
                switch.create_switch(self._target_joints[0], 'switch', switch_node)

    def _attach_joints(self, source_chain, target_chain):
        for i in range(len(source_chain)):
            self._attach_joint(source_chain[i], target_chain[i])
    # endregion


class OrientJointAttributes(object):
    """
    Creates attributes on a node that can be used with OrientAttributes
    """

    def __init__(self, joint):
        """
        Constructor
        :param joint: str, name of the joint we want to create orient attributes to
        """

        self.joint = None
        self.attributes = list()
        self.title = None

        if is_joint(joint) or xform_utils.is_transform(joint):
            self.joint = joint
            self._create_attributes()

    @staticmethod
    @decorators.undo_chunk
    def add_orient_attributes(obj):
        """
        Adds orient attributes to the given joint node
        :param obj: str, name of a valid joint node
        """

        if type(obj) is not list:
            obj = [obj]

        for o in obj:
            if not is_joint(o) and not xform_utils.is_transform(o):
                continue
            ori = OrientJointAttributes(joint=o)
            ori.set_default_values()

    @staticmethod
    @decorators.undo_chunk
    def zero_orient_joint(joint):
        """
        Move orientation to orient joint attributes and zero out orient attributes from the given joint node
        :param joint: str, name of valid joint node
        """

        joint = python.force_list(joint)

        for jnt in joint:
            if not is_joint(jnt):
                continue
            for axis in 'XYZ':
                rotate_value = maya.cmds.getAttr('{}.rotate{}'.format(jnt, axis))
                maya.cmds.setAttr('{}.rotate{}'.format(jnt, axis), 0)
                maya.cmds.setAttr('{}.jointOrient{}'.format(jnt, axis), rotate_value)

    @staticmethod
    @decorators.undo_chunk
    def remove_orient_attributes(joint):
        """
        Removes orient attributes from the given joint node
        :param joint: str, name of valid joint node
        """

        if type(joint) is not list:
            joint = [joint]

        for jnt in joint:
            if not is_joint(jnt):
                continue
            ori = OrientJointAttributes(joint=jnt)
            ori.delete()

    @classmethod
    @decorators.undo_chunk
    def orient_with_attributes(cls, objects_to_orient=None, force_orient_attributes=False):
        """
        Orients all joints and transforms with OrientJointAttribute added on them
        :param objects_to_orient: list<str>, if given, only given objects will be oriented
        """

        if not objects_to_orient:
            objects_to_orient = scene.get_top_dag_nodes()

        LOGGER.debug('Orienting {}'.format(objects_to_orient))

        oriented = False
        for obj in objects_to_orient:
            relatives = maya.cmds.listRelatives(obj, f=True)
            if not maya.cmds.objExists('{}.ORIENT_INFO'.format(obj)):
                if force_orient_attributes:
                    cls.add_orient_attributes(obj)
                else:
                    if relatives:
                        cls.orient_with_attributes(
                            objects_to_orient=relatives, force_orient_attributes=force_orient_attributes)
                        oriented = True
                    continue

            if maya.cmds.nodeType(obj) in ['joint', 'transform']:
                orient = OrientJoint(joint_name=obj)
                orient.run()
                if relatives:
                    cls.orient_with_attributes(
                        objects_to_orient=relatives, force_orient_attributes=force_orient_attributes)
                    oriented = True

        return oriented

    def set_joint(self, joint):
        """
        Set a joint to create attributes on
        :param joint: str, name of the joint
        """

        if not is_joint(joint):
            return

        self.joint = joint

        self._create_attributes()

    def get_values(self):
        """
        Returns all orient settings attributes as a dictionary
        :return: dict
        """

        values_dict = dict()
        for attr in self.attributes:
            values_dict[attr.get_name()] = attr.get_value()

        return values_dict

    def set_values(self, value_dict):
        """
        Set joint orient attributes by the values stored in the given dictionary (get_values()
        function generates that dict)
        :param value_dict: dict
        """

        for attr in self.attributes:
            attr.set_value(value_dict[attr.get_name()])

    def set_default_values(self):
        """
        Set all joint orient axis to their default values
        """

        for attr in self.attributes:
            attr.set_default_value()

    def delete(self):
        """
        Removes all joint orient attributes (created on _create_attribute() function)
        """

        if self.title:
            self.title.delete()

        for attr in self.attributes:
            attr.delete()

    def _create_attributes(self):
        """
        Internal function that creates joint orient attributes
        """

        self.title = attribute.EnumAttribute('Orient_Info'.upper())
        if not maya.cmds.objExists('{}.ORIENT_INFO'.format(self.joint)):
            self.title.create(self.joint)
            self.title.set_locked(True)
        else:
            self.title.set_node(self.joint)

        self.attributes.append(attribute.create_axis_attribute(name='aimAxis', node=self.joint, value=0))
        self.attributes.append(attribute.create_axis_attribute(name='upAxis', node=self.joint, value=1))
        self.attributes.append(attribute.create_axis_attribute(name='worldUpAxis', node=self.joint, value=1))

        aim_at_attr = attribute.EnumAttribute('aimAt', value=3)
        aim_at_attr.set_enum_names(['worldX', 'worldY', 'worldZ', 'child', 'parent', 'localParent'])
        aim_at_attr.create(self.joint)
        self.attributes.append(aim_at_attr)

        aim_up_attr = attribute.EnumAttribute('aimUpAt', value=0)
        aim_up_attr.set_node(self.joint)
        aim_up_attr.set_enum_names(['world', 'parentRotate', 'childPosition', 'trianglePlane', '2ndChildPosition'])
        aim_at_attr.create(self.joint)
        self.attributes.append(aim_up_attr)

        self.attributes.append(attribute.create_triangle_attribute(name='triangleTop', node=self.joint, value=1))
        self.attributes.append(attribute.create_triangle_attribute(name='triangleMid', node=self.joint, value=2))
        self.attributes.append(attribute.create_triangle_attribute(name='triangleBottom', node=self.joint, value=3))

        active_attr = attribute.NumericAttribute('active', value=1)
        active_attr.set_variable_type(attribute.AttributeTypes.Bool)
        active_attr.set_keyable(True)
        active_attr.create(self.joint)
        self.attributes.append(active_attr)


class OrientJoint(object):
    """
    Orient the joint using attributes created with OrientJointAttributes
    """

    def __init__(self, joint_name):
        """
        Constructor
        :param joint_name: str, name of the joint we want to orient
        """

        self.joint = joint_name
        self.orient_values = None
        self.aim_vector = [1, 0, 0]
        self.up_vector = [0, 1, 0]
        self.world_up_vector = [0, 1, 0]

        self.aim_at = 3
        self.aim_up_at = 0

        self.child = None
        self.chidl2 = None
        self.grand_child = None
        self.parent = None
        self.grand_parent = None

        self.delete_later = list()
        self.world_up_vector = self.get_vector_from_axis(1)
        self.up_space_type = 'vector'

        self._get_relatives()

    @staticmethod
    def get_vector_from_axis(axis_index):
        """
        Returns vector from the given axis type
        :param axis_index: int
        :return: list<int, int, int>
        """

        vectors = [[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1],
                   [-1, 0, 0],
                   [0, -1, 0],
                   [0, 0, -1],
                   [0, 0, 0]]

        return vectors[axis_index]

    def set_aim_vector(self, vector_list):
        """
        Set the aim vector for the orient process
        :param vector_list: list<float, float, float>, vector that defines what axis should aim
        """

        self.aim_vector = vector_list

    def set_up_vector(self, vector_list):
        """
        Set the up vector for the orient process
        :param vector_list: list<float, float, float>, vector that defines what axis should aim up
        """

        self.up_vector = vector_list

    def set_world_up_vector(self, vector_list):
        """
        Set the world up axis for the orient process
        :param vector_list: list<float, float, float>, vector that defines what world up axis be
        """

        self.world_up_vector = vector_list

    def set_aim_at(self, index):
        """
        Defines how the joint will aim
        :param index: int, aim at index value
                                0: aim at world X
                                1: aim at world Y
                                2: aim at world Z
                                3: aim at inmediate child
                                4: aim at inmediate parent
                                5: aim at local parent (aiming at the parent and then reversing the direction)
        """

        self.aim_at = self._get_aim_at(index=index)

    def set_aim_up_at(self, index):
        """
        Defines how the will aim up
        :param index: int, aim up at index value
                                0: parent rotate
                                1: child position
                                2: parent position
                                3: triangle plane (need to be configured before)
        """

        self.aim_up_at = self._get_aim_up_at(index=index)

    def set_aim_up_at_object(self, transform_name):
        """
        Defines the object used for aim up
        :param transform_name: str, name of the object
        """

        self.aim_up_at = self._get_local_up_group(transform_name=transform_name)
        self.up_space_type = 'objectrotation'
        self.world_up_vector = [0, 1, 0]

    def run(self):
        """
        Orients joints
        """

        if maya.cmds.objExists('{}.active'.format(self.joint)):
            if not maya.cmds.getAttr('{}.active'.format(self.joint)):
                LOGGER.warning('{} has orientation attributes but is not acitve. Skipping ...'.format(self.joint))
                return

        self._freeze()
        self._get_relatives()
        self._pin()

        try:
            for axis in 'xyz':
                maya.cmds.setAttr('{}.rotateAxis{}'.format(self.joint, axis.upper()), 0)
        except Exception:
            LOGGER.warning('Could not zero our rotateAxis on {}. This can cause rig errors!'.format(self.joint))

        self.orient_values = self._get_values()

        if self.orient_values:
            self.aim_vector = self.get_vector_from_axis(self.orient_values['aimAxis'])
            self.up_vector = self.get_vector_from_axis(self.orient_values['upAxis'])
            self.world_up_vector = self.get_vector_from_axis(self.orient_values['worldUpAxis'])
            self.aim_at = self._get_aim_at(self.orient_values['aimAt'])
            self.aim_up_at = self._get_aim_up_at(self.orient_values['aimUpAt'])
        else:
            if type(self.aim_at) == int:
                self.aim_at = self._get_aim_at(self.aim_at)
            if type(self.aim_up_at) == int:
                self.aim_up_at = self._get_aim_up_at(self.aim_up_at)

        self._create_aim()
        self._cleanup()
        self._freeze()

    def _get_values(self):
        """
        Returns orient joint attributes stored in the wrapped joint node
        :return: dict<str, Attribute>
        """

        if not maya.cmds.objExists('{}.ORIENT_INFO'.format(self.joint)):
            LOGGER.warning(
                'Impossible to get orient attributes from {} because they do not exists!'.format(self.joint))
            return

        ori_attrs = OrientJointAttributes(joint=self.joint)
        return ori_attrs.get_values()

    def _get_relatives(self):
        """
        Internal function that returns all relatives joints of the given joint
        """

        # Get parent and grand parent nodes
        parent = maya.cmds.listRelatives(self.joint, p=True, f=True)
        if parent:
            self.parent = parent[0]
            grand_parent = maya.cmds.listRelatives(self.parent, p=True, f=True)
            if grand_parent:
                self.grand_parent = grand_parent[0]

        # Get children and grand children
        children = maya.cmds.listRelatives(self.joint, f=True, type='transform')
        if children:
            self.child = children[0]
            if len(children) > 1:
                self.child2 = children[1]
            grand_children = maya.cmds.listRelatives(self.child, f=True)
            if grand_children:
                self.grand_child = grand_children[0]

    def _get_aim_at(self, index):
        """
        Creates and returns the group we want to aim depending of the given index option
        :param index: int, index that defines how we want to create the aim group
        :return: str, created group positioned where lookAt constraint should aim
        """

        # World Axis (0=X, 1=Y, 2=Z)
        if index < 3:
            world_aim = maya.cmds.group(empty=True, n='world_aim')
            transform.MatchTransform(source_transform=self.joint, target_transform=world_aim).translation()

            if index == 0:
                maya.cmds.move(1, 0, 0, world_aim, r=True)
            elif index == 1:
                maya.cmds.move(0, 1, 0, world_aim, r=True)
            elif index == 2:
                maya.cmds.move(0, 0, 1, world_aim, r=True)

            self.delete_later.append(world_aim)
            return world_aim

        # Child
        elif index == 3:
            child_aim = self._get_position_group(self.child)
            return child_aim

        # Parent
        elif index == 4:
            parent_aim = self._get_position_group(self.parent)
            return parent_aim

        # Front (in X axis) of wrapped joint
        elif index == 5:
            aim = self._get_local_up_group(self.parent)
            return aim

    def _get_aim_up_at(self, index):
        """
        Creates and returns the group we want to set as up group depending of the given index option
        :param index: int, index that defines how we want to create the aim up group
        :return: str, created group positioned where lookAt up axis should look
        """

        if index == 1:
            self.up_space_type = 'objectrotation'
            return self._get_local_up_group(self.parent)

        elif index == 2:
            child_group = self._get_position_group(self.child)
            self.up_space_type = 'object'
            return child_group

        elif index == 3:
            parent_group = self._get_position_group(self.parent)
            self.up_space_type = 'object'
            return parent_group

        elif index == 4:
            top = self._get_triangle_group(self.orient_values['triangleTop'])
            mid = self._get_triangle_group(self.orient_values['triangleMid'])
            btm = self._get_triangle_group(self.orient_values['triangleBottom'])
            if not top or not mid or not btm:
                LOGGER.warning('Could not orient {} fully with current triangle plane settings'.format(self.joint))
                return

            plane_grp = xform_utils.create_group_in_plane(top, mid, btm)
            maya.cmds.move(0, 10, 0, plane_grp, r=True, os=True)
            self.delete_later.append(plane_grp)
            self.up_space_type = 'object'
            return plane_grp

        elif index == 5:
            self.up_space_type = 'object'
            child_grp = None

            if self.child2 and maya.cmds.objExists(self.child2):
                child_grp = self._get_position_group(self.child2)
            if not self.child2 or not maya.cmds.objExists(self.child2):
                LOGGER.warning(
                    'Child2 specified as up in orient attribute but {} has no 2nd child'.format(self.joint))

            return child_grp

    def _freeze(self):
        """
        Internal function that freezes wrapped joint without touching its hierarchy
        """

        children = maya.cmds.listRelatives(self.joint, f=True)

        found_children = list()
        if children:
            for child in children:
                if xform_utils.is_transform(child):
                    child_parented = maya.cmds.parent(child, w=True)[0]
                    found_children.append(child_parented)

        maya.cmds.makeIdentity(self.joint, apply=True, r=True, s=True)

        if found_children:
            maya.cmds.parent(found_children, self.joint)

    def _pin(self):
        """
        Internal function that pin joint so its children and parent does not move when transforming
        Updates list of nodes to remove so pin is removed after orienting
        """

        pin = transform.PinTransform(transform_name=self.joint)
        pin.pin()

        nodes = pin.get_pin_nodes()
        self.delete_later += nodes

    def _get_local_up_group(self, transform_name):
        """
        Creates an empty group matching give transform rotation but positioned in front of the
        current wrapped joint (moved in X axis)
        :param transform_name: str, transform we want to match position to
        :return: str, new created local up group
        """

        local_up_group = maya.cmds.group(empty=True, n='local_up_{}'.format(transform))
        transform.MatchTransform(source_transform=transform_name, target_transform=local_up_group).rotation()
        transform.MatchTransform(source_transform=self.joint, target_transform=local_up_group).translation()
        maya.cmds.move(1, 0, 0, local_up_group, relative=True, objectSpace=True)
        self.delete_later.append(local_up_group)

        return local_up_group

    def _get_position_group(self, transfrom_name):
        """
        Creates an empty group with its transformations matching the given transform node
        :param transfrom_name: str, transform we want to match new group to
        :return: str, new created position group
        """

        position_group = maya.cmds.group(empty=True, name='position_group')
        transform.MatchTransform(source_transform=transfrom_name,
                                 target_transform=position_group).translation_rotation()
        self.delete_later.append(position_group)

        return position_group

    def _get_triangle_group(self, index):
        """
        Creates an empty group positioned based on the childs/parents based on given index
        :param index: int, index that defines position of the group
        (0=grand_parent, 1=parent, 2=joint, 3=child, 4=grand_child)
        :return: str, new created triangle position group
        """

        target_transform = None
        if index == 0:
            target_transform = self.grand_parent
        elif index == 1:
            target_transform = self.parent
        elif index == 2:
            target_transform = self.joint
        elif index == 4:
            target_transform = self.child
        elif index == 4:
            target_transform = self.grand_child
        if not target_transform:
            return

        return self._get_position_group(target_transform)

    def _create_aim(self):
        """
        Create aim constraints used to orient the joint
        """

        if self.aim_up_at:
            aim = maya.cmds.aimConstraint(
                self.aim_at,
                self.joint,
                aimVector=self.aim_vector,
                upVector=self.up_vector,
                worldUpObject=self.aim_up_at,
                worldUpVector=self.world_up_vector,
                worldUpType=self.up_space_type)[0]
        else:
            aim = maya.cmds.aimConstraint(
                self.aim_at,
                self.joint,
                aimVector=self.aim_vector,
                upVector=self.up_vector,
                worldUpVector=self.world_up_vector,
                worldUpType=self.up_space_type)[0]

        self.delete_later.append(aim)

    def _cleanup(self):
        """
        Removes all extra nodes created during orient process
        """

        maya.cmds.delete(self.delete_later)


def check_joint(joint):
    """
    Checks if a node is a valid joint and raise and exception if the joint is not valid
    :param joint: str, name of the node to be checked
    :return: bool, True if the give node is a joint node or False otherwise
    """

    if not is_joint(joint):
        raise exceptions.JointException(joint)


def is_joint(joint):
    """
    Checks if the given object is a joint
    :param joint: str, object to query
    :return: bool, True if the given object is a valid joint or False otherwise
    """

    if not maya.cmds.objExists(joint):
        return False

    if not maya.cmds.ls(type='joint').count(joint):
        return False

    return True


def is_end_joint(joint):
    """
    Returns True if the given joint is an end joint (last child of hierarchy) or False otherwise
    :param joint: str, name of the joint to check
    :return: bool
    """

    check_joint(joint)

    joint_descendants = maya.cmds.ls(maya.cmds.listRelatives(joint, ad=True) or [], type='joint')
    if not joint_descendants:
        return True

    return False


def get_end_joint(start_joint, include_transforms=False):
    """
    Find the end joint of a chain from the given start joint
    :param start_joint: str, joint to find end joint from
    :param include_transforms: bool, Include non-joint transforms in the chain
    :return: str
    """

    check_joint(start_joint)

    end_joint = None
    next_joint = start_joint
    while next_joint:
        child_list = maya.cmds.listRelatives(next_joint, c=True) or []
        child_joints = maya.cmds.ls(child_list, type='joint') or []
        if include_transforms:
            child_joints = list(set(child_joints + maya.cmds.ls(child_list, transforms=True) or []))
        if child_joints:
            next_joint = child_joints[0]
        else:
            end_joint = next_joint
            next_joint = None

    return end_joint


def get_joint_list(start_joint, end_joint):
    """
    Get list of joints between and including given start and end joint
    :param start_joint: str, start joint of joint list
    :param end_joint: str, end joint of joint list
    :return: list<str>
    """

    check_joint(start_joint)
    check_joint(end_joint)

    if start_joint == end_joint:
        return [start_joint]

    # Check hierarchy
    descendant_list = maya.cmds.ls(maya.cmds.listRelatives(start_joint, ad=True), type='joint')
    if not descendant_list.count(end_joint):
        raise Exception('End joint "{}" is not a descendant of start joint "{}"'.format(end_joint, start_joint))

    joint_list = [end_joint]
    while joint_list[-1] != start_joint:
        parent_jnt = maya.cmds.listRelatives(joint_list[-1], p=True, pa=True)
        if not parent_jnt:
            raise Exception('Found root joint while searching for start joint "{}"'.format(start_joint))
        joint_list.append(parent_jnt[0])

    joint_list.reverse()

    return joint_list


def get_length(joint):
    """
    Returns the length of a given joint
    :param joint: str, joint to query length from
    :return: str
    """

    check_joint(joint)

    child_joints = maya.cmds.ls(maya.cmds.listRelatives(joint, c=True, pa=True) or [], type='joint')
    if not child_joints:
        return 0.0

    max_length = 0.0
    for child_jnt in child_joints:
        pt1 = transform.get_position(joint)
        pt2 = transform.get_position(child_jnt)
        offset = mathutils.offset_vector(pt1, pt2)
        length = mathutils.magnitude(offset)
        if length > max_length:
            max_length = length

    return max_length


def duplicate_joint(joint, name=None):
    """
    Duplicates a given joint
    :param joint: str, joint to duplicate
    :param name: variant, str || None, new name for duplicated joint. If None, leave as default
    :return: str
    """

    check_joint(joint)
    if not name:
        name = joint + '_dup'
    if maya.cmds.objExists(str(name)):
        raise Exception('Joint "{}" already exists!'.format(name))

    dup_joint = maya.cmds.duplicate(joint, po=True)[0]
    if name:
        dup_joint = maya.cmds.rename(dup_joint, name)

    # Unlock transforms
    for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v', 'radius']:
        maya.cmds.setAttr(dup_joint + '.' + attr, long=False, cb=True)

    return dup_joint


def duplicate_chain(start_jnt, end_jnt=None, parent=None, skip_jnt=None, prefix=None):
    """
    Duplicats a joint chain based on start and en joint
    :param start_jnt: str, start joint of chain
    :param end_jnt: str, end joint of chain. If None, use end of current chain
    :param parent: str, parent transform for new chain
    :param skip_jnt: variant, str ||None, skip joints in chain that match name pattern
    :param prefix: variant, str ||None, new name prefix
    :return: list<str>, list of duplicate joints
    """

    if not maya.cmds.objExists(start_jnt):
        raise Exception('Start joint "{}" does not exists!'.format(start_jnt))
    if end_jnt and not maya.cmds.objExists(str(end_jnt)):
        raise Exception('End joint "{}" does not exists!'.format(end_jnt))

    if parent:
        if not maya.cmds.objExists(parent):
            raise Exception('Given parent transform "{}" does not eixsts!'.format(parent))
        if not transform.is_transform(parent):
            raise Exception('Parent object "{}" is not a valid transform!'.format(parent))

    if not end_jnt:
        end_jnt = get_end_joint(start_jnt=start_jnt)
    joints = get_joint_list(start_joint=start_jnt, end_joint=end_jnt)

    skip_joints = maya.cmds.ls(skip_jnt) if skip_jnt else list()

    dup_chain = list()
    for i in range(len(joints)):
        if joints[i] in skip_joints:
            continue

        name = None
        if prefix:
            jnt_index = strings.get_alpha(i, capitalong=True)
            if i == (len(joints) - 1):
                jnt_index = 'End'
            name = prefix + jnt_index + '_jnt'

        jnt = duplicate_joint(joint=joints[i], name=name)

        if not i:
            if not parent:
                if maya.cmds.listRelatives(jnt, p=True):
                    try:
                        maya.cmds.parent(jnt, w=True)
                    except Exception:
                        pass
            else:
                try:
                    maya.cmds.parent(jnt, parent)
                except Exception:
                    pass
        else:
            try:
                maya.cmds.parent(jnt, dup_chain[-1])
                if not maya.cmds.isConnected(dup_chain[-1] + '.scale', jnt + '.inverseScale'):
                    maya.cmds.connectAttr(dup_chain[-1] + '.scale', jnt + '.inverseScale', f=True)
            except Exception as e:
                raise Exception('Error while duplicating joint chain! - {}'.format(str(e)))

        dup_chain.append(jnt)

    return dup_chain


def joint_buffer(joint, index_str=0):
    """
    Creates a joint buffer group in the given joint
    :param joint: str, name of the joint we want to create buffer for
    :param index_str: int, string index
    :return: str, name of the joint buffer group created
    """

    if not maya.cmds.objExists(joint):
        raise Exception('Joint "{}" does not exists!'.format(joint))

    if not index_str:
        result = maya.cmds.promptDialog(
            title='Index String',
            message='Joint Group Index',
            text='0',
            button=['Create', 'Cancel'],
            defaultButton='Create',
            cancelButton='Cancel',
            dismissString='Cancel'
        )

        if result == 'Create':
            index_str = maya.cmds.promptDialog(q=True, text=True)
        else:
            LOGGER.warning('User canceled joint group creation ...')
            return

        # Get joint prefix and create joint buffer group
        prefix = strings.strip_suffix(joint)
        grp = maya.cmds.duplicate(joint, po=True, n=prefix + 'Buffer' + index_str + '_jnt')[0]
        maya.cmds.parent(joint, grp)

        if maya.cmds.getAttr(grp + '.radius', se=True):
            try:
                maya.cmds.setAttr(grp + '.radius', 0)
            except Exception:
                pass

        # Connect inverse scale
        inverse_scale_cnt = maya.cmds.listConnections(joint + '.inverseScale', s=True, d=False)
        if not inverse_scale_cnt:
            inverse_scale_cnt = list()
        if not inverse_scale_cnt.count(grp):
            try:
                maya.cmds.connectAttr(grp + '.scale', joint + '.inverseScale', f=True)
            except Exception:
                pass

        # Delete user attributes
        user_attrs = maya.cmds.listAttr(grp, ud=True)
        if user_attrs:
            for attr in user_attrs:
                if maya.cmds.objExists(grp + '.' + attr):
                    maya.cmds.setAttr(grp + '.' + attr, long=False)
                    maya.cmds.deleteAttr(grp + '.' + attr)

        node.display_override(obj=joint, override_enabled=True, override_lod=0)
        node.display_override(obj=grp, override_enabled=True, override_display=2, override_lod=1)


def set_draw_style(joints, draw_style='bone'):
    """
    Set joint draw style for the given joints
    :param joints: list<str>, list of joints to set draw style for
    :param draw_style: str, draw style to apply to the given joints ("bone", "box", "none")
    :return: list<str>, list of joints which draw styles have been changed
    """

    if not joints:
        raise Exception('No joints given!')

    draw_style = draw_style.lower()
    if draw_style not in ['bone', 'box', 'none']:
        raise Exception('Invalid draw style ("{}")! Accepted values are "bone", "box", "none"'.format(draw_style))

    if type(joints) not in [list, tuple]:
        joints = [joints]

    for jnt in joints:
        if not is_joint(jnt):
            continue
        if draw_style == 'bone':
            maya.cmds.setAttr('{}.drawStyle'.format(jnt), 0)
        elif draw_style == 'box':
            maya.cmds.setAttr('{}.drawStyle'.format(jnt), 1)
        elif draw_style == 'none':
            maya.cmds.setAttr('{}.drawStyle'.format(jnt), 2)

    return joints


def create_from_point_list(point_list, orient=False, side='c', part='chain', suffix='jnt'):
    """
    Create joint chain from a list of point positions
    :param point_list: list<tuple>, list of points to create joint chain from
    :param orient: bool, Whether to orient or not the joints
    :param side: str, joint side name prefix
    :param part: str, joint part name
    :param suffix: str, joint suffix name
    :return: list<str>, list of new created joints
    """

    maya.cmds.select(clong=True)

    joint_list = list()
    for i in range(len(point_list)):
        jnt = maya.cmds.joint(p=point_list[i], n='{}_{}{}_{}'.format(side, part, str(i + 1), suffix))
        if i and orient:
            maya.cmds.joint(joint_list[-1], e=True, zso=True, oj='xyz', sao='yup')
        joint_list.append(jnt)

    return joint_list


def orient(joint, aim_axis='x', up_axis='y', up_vector=(0, 1, 0)):
    """
    Orient joints based on user defined vectors
    :param joint: str, joints to orient
    :param aim_axis: str, axis to be aligned down the length of the joint
    :param up_axis: str, axis to be aligned with the world vector given by up vector
    :param up_vector: tuple<int>, world vector to align up axis to
    """

    check_joint(joint)

    child_list = maya.cmds.listRelatives(joint, c=True)
    child_joint_list = maya.cmds.listRelatives(joint, c=True, type='joint', pa=True)

    if child_list:
        child_list = maya.cmds.parent(child_list, world=True)

    if not child_joint_list:
        maya.cmds.setAttr('{}.jo'.format(joint), 0, 0, 0)
    else:
        parent_matrix = maya.OpenMaya.MMatrix()
        parent_joint = maya.cmds.listRelatives(joint, p=True, pa=True)
        if parent_joint:
            parent_matrix = transform.get_matrix(parent_joint[0])

        # Aim Vector
        aim_point_1 = transform.get_position(joint)
        aim_point_2 = transform.get_position(child_joint_list[0])
        aim_vector = mathutils.offset_vector(aim_point_1, aim_point_2)

        target_matrix = matrix_utils.build_rotation(aim_vector, up_vector, aim_axis, up_axis)
        orient_matrix = target_matrix * parent_matrix.inverse()

        # Extract joint orient values
        rotation_order = maya.cmds.getAttr('{}.ro'.format(joint))
        orient_rotation = matrix_utils.get_rotation(orient_matrix, rotation_order=rotation_order)

        # Reset joint rotation and orientation
        maya.cmds.setAttr('{}.r'.format(joint), 0, 0, 0)
        maya.cmds.setAttr('{}.jo'.format(orient_rotation[0], orient_rotation[1], orient_rotation[2]))

    # Reparent children
    if child_list:
        maya.cmds.aprent(child_list, joint)


def orient_to(joint, target):
    """
    Matches given joint orientation to given transform
    :param joint: str, joint to set orientation for
    :param target: str, transform to match joint orientation to
    """

    if not maya.cmds.objExists(joint):
        raise Exception('Joint "{}" does not exist!'.format(joint))
    if not maya.cmds.objExists(target):
        raise Exception('Target "{}" does not exist!'.format(target))
    if not transform.is_transform(target):
        raise Exception('Target "{}" is not a valid transform!'.format(target))

    # Unparent children
    child_list = maya.cmds.listRelatives(joint, c=True, type=['joint', 'transform'])
    if child_list:
        child_list = maya.cmds.parent(child_list, world=True)

    # Get parent joint matrix
    parent_matrix = maya.OpenMaya.MMatrix()
    parent_joint = maya.cmds.listRelatives(joint, p=True, pa=True)
    if parent_joint:
        parent_matrix = transform.get_matrix(parent_joint[0])

    target_matrix = transform.get_matrix(target)
    orient_matrix = target_matrix * parent_matrix.inverse()

    # Extract joint orient values
    rotation_order = maya.cmds.getAttr('{}.ro'.format(joint))
    orient_rotation = matrix_utils.get_rotation(orient_matrix, rotation_order=rotation_order)

    # Reset joint rotation and orientation
    maya.cmds.setAttr('{}.r'.format(joint), 0, 0, 0)
    maya.cmds.setAttr('{}.jo'.format(orient_rotation[0], orient_rotation[1], orient_rotation[2]))

    # Reparent children
    if child_list:
        maya.cmds.aprent(child_list, joint)


def flip_orient(joint, target=None, axis='x'):
    """
    Flips the given joint orient across the given axis
    Flipped orientation will be applied to target joint or to original one if target is not specified
    :param joint: str, joint to flip orientation of
    :param target: str or None, joint to apply flipped orientation to
    :param axis: str, axis to flip orientation across
    """

    check_joint(joint)

    rad_to_deg = 100.0 / math.pi

    if not target:
        target = joint

    joint_matrix = transform.get_matrix(joint)

    # Build flip matrix
    flip_matrix = None
    if axis == 'x':
        flip_matrix = matrix_utils.build_matrix(x_axis=(-1, 0, 0))
    if axis == 'y':
        flip_matrix = matrix_utils.build_matrix(x_axis=('', -1, 0))
    if axis == 'z':
        flip_matrix = matrix_utils.build_matrix(x_axis=(0, 0, -1))

    target_matrix = maya.OpenMaya.MTransformationMatrix(joint_matrix * flip_matrix.inverse())
    flip_rotation = target_matrix.eulerRotation()
    flip_rotation_list = (flip_rotation.x * rad_to_deg, flip_rotation.y * rad_to_deg, flip_rotation.z * rad_to_deg)
    maya.cmds.setAttr('{}.jo'.format(target), *flip_rotation_list)

    return flip_rotation_list


def mirror_orient(joint, roll_axis):
    """
    Reorients joint to replicate mirrored behaviour
    :param joint: str, joint to mirror orientation for
    :param roll_axis: str, axis to maintain orientation for
    """

    check_joint(joint)

    if not ['x', 'y', 'z'].count(roll_axis):
        raise Exception('Invalid roll axis "{}"!'.format(roll_axis))

    # Unparent children
    child_list = maya.cmds.listRelatives(joint, c=True)
    if child_list:
        maya.cmds.parent(child_list, world=True)

    # Reorient joint
    rotation_list = [0, 0, 0]
    axis_dict = {'x': 0, 'y': 1, 'z': 2}
    rotation_list[axis_dict[roll_axis]] = 180
    maya.cmds.setAttr('{}.r'.format(joint), *rotation_list)
    maya.cmds.makeIdentity(joint, apply=True, t=True, r=True, s=True)

    # Reparent children
    if child_list:
        maya.cmds.parent(child_list, joint)


def start_joint_tool():
    """
    Initializes Maya joint creation tool
    """

    maya.cmds.JointTool()


def set_joint_local_rotation_axis_visibility(joints=None, bool_value=None):
    """
    Sets the joint visibility of the given node or given nodes
    :param joints: list<str>, list of joints to set axis visibility of. If None, given, all joints of the scene
        will be used
    :param bool_value: bool, value of the local rotation axis visibility. If None given, current joint visibility
        will be toggled
    :return:
    """

    if joints is None:
        joints = maya.cmds.ls(type='joint')
    else:
        joints = python.force_list(joints)

    for jnt in joints:
        if bool_value is None:
            new_value = not maya.cmds.getAttr('{}.displayLocalAxis'.format(jnt))
        else:
            new_value = bool_value
        maya.cmds.setAttr('{}.displayLocalAxis'.format(jnt), new_value)

    return True


def connect_inverse_scale(joint, inverse_scale_object=None, force=False):
    """
    Connects joints inverseScale attribute
    :param joint: str, joint to connect inverseScale for
    :param inverse_scale_object: str, object to connect to joint inverseScale attribute. If None, joint parent is use.
    :param force: bool, Whether to force the connection or not
    """

    check_joint(joint)

    # Get inverse scale object if not given
    if not inverse_scale_object or not maya.cmds.objExists(inverse_scale_object):
        parent = maya.cmds.listRelatives(joint, p=True) or list()
        if parent and force:
            parent = maya.cmd.sls(parent, type='joint') or list()
        if not parent:
            LOGGER.warning(
                'No source object specified and no parent joint found for joint "{}". Skipping connection ...'.format(
                    joint))
            return None
        inverse_scale_object = parent[0]

    # Connect inverse scale
    inverse_scale_connections = maya.cmds.listConnections('{}.inverseScale'.format(joint), s=True, d=False) or list()
    if inverse_scale_object not in inverse_scale_connections:
        try:
            maya.cmds.connectAttr('{}.scale'.format(inverse_scale_object), '{}.inverseScale'.format(joint), f=True)
        except Exception as exc:
            LOGGER.error('Error connection "{}.scale" to "{}.inverseScale! {}'.format(inverse_scale_object, joint, exc))
            return None

    return '{}.scale'.format(inverse_scale_object)


@decorators.undo_chunk
def create_joints_along_curve(curve, joint_count, joint_description='new', attach=True, create_controls=False):
    """
    Create joints on curve that do not aim at child
    :param curve: str, name of a curve
    :param joint_count: int, number of joints to create
    :param joint_description: str, description for the new created joints
    :param attach: bool, Whether to attach the joints to the curve or not
    :param create_controls: bool, Whether to create new controls on the joints
    :return: list(joint, group, control_group)
        joints: list of joints
        group: main group for the joints
        control_group: main group above the controls (None if controls are not created)
    """

    group = maya.cmds.group(empty=True, n=name_utils.find_unique_name('{}_joints_grp'.format(curve)))

    control_group = None
    if create_controls:
        control_group = maya.cmds.group(empty=True, n=name_utils.find_unique_name('{}_controls_grp'.format(curve)))
        maya.cmds.addAttr(control_group, ln='twist', k=True)
        maya.cmds.addAttr(control_group, ln='offsetScale', min=-1, dv=0, k=True)

    maya.cmds.select(clear=True)

    total_length = maya.cmds.arclen(curve)
    part_length = total_length / (joint_count - 1)

    joints = list()
    current_length = 0
    percent = 0
    segment = 1.0 / joint_count
    for i in range(joint_count):
        param = curve_utils.get_parameter_from_curve_length(curve, current_length)
        position = curve_utils.get_point_from_curve_parameter(curve, param)
        if attach:
            maya.cmds.select(clear=True)
        new_joint = maya.cmds.joint(p=position, n=name_utils.find_unique_name('{}_jnt'.format(joint_description)))
        maya.cmds.addAttr(new_joint, ln='param', at='double', dv=param, k=True)
        if joints:
            maya.cmds.joint(joints[-1], e=True, zso=True, oj='xyz', sao='yup')
        if attach:
            attach_node = curve_utils.attach_to_curve(new_joint, curve, parameter=param)
            maya.cmds.parent(new_joint, group)
            maya.cmds.connectAttr('{}.param'.format(new_joint), '{}.parameter'.format(attach_node))
        current_length += part_length
        if create_controls:
            raise NotImplementedError('create controls functionality not implemented yet!')

        joints.append(new_joint)
        percent += segment

    if not attach:
        maya.cmds.parent(joints[0], group)

    return joints, group, control_group


def create_joint_along_curve_in_intersection_curves(
        curve, intersect_curves_list, joint_at_base=True, joint_at_tip=True, use_direction=False,
        intersect_direction=(0, 0, 0), prefix=''):
    """
    Creates joints along a curves at the point of intersection with a list of secondary curves
    :param curve: str, curve to create joint along
    :param intersect_curves_list: list, list of intersection curves
    :param joint_at_base: bool, creates a joint at the base of the curve
    :param joint_at_tip: bool, creates a joint at the tip of the curve
    :param use_direction: bool, project the curves in a given direction before intersecting
    :param intersect_direction: tuple or list, the direction to project the curves before intersecting
    :param prefix: str, name prefix for newly created joints
    :return: list(str), list of new created joints
    """

    if not maya.cmds.objExists(curve):
        raise Exception('Curve object "{}" does not exist!'.format(curve))
    for i in range(len(intersect_curves_list)):
        if not maya.cmds.objExists(intersect_curves_list[i]):
            raise Exception('Object "{}" does not exist!'.format(intersect_curves_list[i]))

    if not prefix:
        prefix = strings.strip_suffix(curve)

    # Get curve range
    min_u = maya.cmds.getAttr('{}.minValue'.format(curve))
    max_u = maya.cmds.getAttr('{}.maxValue'.format(curve))

    maya.cmds.select(clear=True)
    joint_list = list()

    # TODO: We should use nameit library to rename new joints
    joint_name_format = '{}_new{}_jnt'

    # Create base joint if necessary
    if joint_at_base:
        pos = maya.cmds.pointOnCurve(curve, pr=min_u, p=True)
        joint_index = '01'
        new_joint_name = joint_name_format.format(prefix, joint_index)
        new_joint = maya.cmds.joint(p=pos, n=new_joint_name)
        joint_list.append(new_joint)

    # Create joints at curve intersections
    for n in range(len(intersect_curves_list)):
        joint_index = str(n + 1 + int(joint_at_base))
        if i < (9 - int(joint_at_base)):
            joint_index = '0{}'.format(joint_index)
        u_list = maya.cmds.curveIntersect(curve, intersect_curves_list[n], ud=use_direction, d=intersect_direction)
        if not u_list:
            continue
        u_list = u_list.split(' ')
        for u in range(int(len(u_list) / 2)):
            pos = maya.cmds.pointOnCurve(curve, pr=float(u_list[u * 2]), p=True)
            new_joint_name = joint_name_format.format(prefix, joint_index)
            new_joint = maya.cmds.joint(p=pos, n=new_joint_name)
            joint_list.append(new_joint)

    # Create tip joint
    if joint_at_tip:
        joint_index = str(len(intersect_curves_list) + int(joint_at_base) + 1)
        if len(intersect_curves_list) < (9 - int(joint_at_base)):
            joint_index = '0{}'.format(joint_index)

        pos = maya.cmds.pointOnCurve(curve, pr=max_u, p=True)
        new_joint_name = joint_name_format.format(prefix, joint_index)
        new_joint = maya.cmds.joint(p=pos, n=new_joint_name)
        joint_list.append(new_joint)

    return joint_list


def create_joint_buffer(joint, connect_inverse=True):
    """
    Creates a joint buffer on top of the given joint
    :param joint: str
    :param connect_inverse: bool, Whether to connect new buffer joint inverseScale to source joint parent node
    """

    maya.cmds.select(clear=True)

    # Create buffer joint and make sure that it has same translation and rotation than the source joint
    buffer_joint = maya.cmds.joint(n='{}_bufferJoint'.format(joint))
    maya.cmds.setAttr('{}.drawStyle'.format(buffer_joint), 2)
    transform.MatchTransform(joint, buffer_joint).translation_rotation()

    # Parent buffer joint to source joint parent node (if exists)
    parent = maya.cmds.listRelatives(joint, p=True, f=True)
    if parent:
        parent = parent[0]
        maya.cmds.parent(buffer_joint, parent)
        if connect_inverse:
            if not maya.cmds.isConnected('{}.scale'.format(parent), '{}.inverseScale'.format(buffer_joint)):
                maya.cmds.connectAttr('{}.scale'.format(parent), '{}.inverseScale'.format(buffer_joint))

    # Parent source joint to new created buffer joint
    maya.cmds.parent(joint, buffer_joint)

    return buffer_joint


@decorators.undo_chunk
def insert_joints(joints=None, joint_count=1):
    """
    Inserts joints evenly spaced along a bone
    :param list(str) joints: list of joints to insert child joints to
    :param int joint_count: Number of joints to insert
    :return: List of created joints
    :rtype: list(str)
    """

    if joints is None:
        joints = maya.cmds.ls(sl=True, type='joint')
        if not joints:
            LOGGER.warning('No joint selected')
            return
    if joint_count < 1:
        LOGGER.warning('Must insert at least 1 joint')
        return

    result = list()

    for joint in joints:
        children = maya.cmds.listRelatives(joint, children=True, type='joint')
        if not children:
            LOGGER.warning('Joint "{}" needs at least a child in order to insert joints. Skipping!'.format(joint))
            continue

        name = joint
        end_joint = children[0]
        dst = mathutils.distance_between_nodes(joint, end_joint)
        increment = dst / (joint_count + 1)
        direction = mathutils.direction_vector_between_nodes(joint, end_joint)
        direction.normalize()
        direction *= increment

        for i in range(joint_count):
            position = maya.OpenMaya.MPoint(*maya.cmds.xform(joint, query=True, worldSpace=True, translation=True))
            position += direction
            joint = maya.cmds.insertJoint(joint)
            joint = maya.cmds.rename(joint, '{}#'.format(name))
            maya.cmds.joint(joint, edit=True, component=True, position=(position.x, position.y, position.z))
            result.append(joint)

    return result


def get_joints_chain_length(list_of_joints_in_chain):
    """
    Return the total distance of a of joints chain
    :param list_of_joints_in_chain: list(str)
    :return: float
    """

    length = 0
    joint_count = len(list_of_joints_in_chain)
    for i in range(joint_count):
        if i + 1 == joint_count:
            break
        current_joint = list_of_joints_in_chain[i]
        next_joint = list_of_joints_in_chain[i + 1]
        distance = transform.get_distance(current_joint, next_joint)
        length += distance

    return length
