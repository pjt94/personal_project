#coding:utf8
import maya.OpenMaya as om
import maya.cmds as mc

class DirectionObjects:
    """
    DirectionObjects class sets the direction and angle in the
    x, y, and z axes and returns the name, type, and position 
    value of objects within the defined range.

    Caveats:
    1.
    You must select an object to be the standard.
    2.
    After selecting the object to be the standard, you need to set the direction among "x", "y", and "z".
    3.
    Please enter the desired angle
    If you don't enter any of these 3, the api won't work.
    """
    def __init__(self):
        """
        Initialize the :class "DirectionObjects" object.
        """
        self._object = None
        self._direction = None
        self._angle = None

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, value):
        """

        Args:
            value: object = (standard_object)
                sel_object = mc.objectType(object,isType='transform')
                sel_object == True
                The type of the standard object must be 'transform'.

        Returns: 
            str:
                Invokes the object that becomes the axis.

        """
        self._object = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        """

        Args:
            value: direction = 'x' or 'y' or 'z'
                Please write in string format

        Returns: 
            str:
                Select and apply one of the x, y, and z axis directions of the selected object.

        """
        self._direction = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        """

        Args:
            value: angle = int of float

        Returns: 
            int:
                Invokes angle.

        """
        self._angle = value

    def return_direction(self):
        """

        Returns: 
            int:
                It takes a direction value and returns the values 0,1,2.
        The values 0,1,2 received are the index values of translate.

        """
        if self.direction is 'x':
            return 0
        elif self.direction is 'y':
            return 1
        elif self.direction is 'z':
            return 2
        else:
            raise ValueError("Please set correct direction.")

    def make_vector_normalize(self, b):
        """

        Args:
            b: Another object of type 'transform'

        Returns: 
            radians:
                Returns a vector value between the two using the position
        of the standard object and the position of another object.

        """
        a_translation = mc.xform(self.object, q=1,t=1,ws=1)
        if mc.objectType(b,isType='transform') == True:
            b_translation = mc.xform(b, q=1,t=1,ws=1)
            a_vector = om.MVector(*a_translation)
            b_vector = om.MVector(*b_translation)
            subtract_vector = b_vector - a_vector
            temporary_vector = a_vector + subtract_vector
        else:
            raise ValueError("Please enter the 'b' argument value in the make_vector_normalize function as an object of type 'transform'.")
        return temporary_vector

    def temporary_vector(self):
        """

        Returns: 
            radians:
                When the direction of the reference object is determined, a "transform" node is created by adding +1
        to the specified direction, and the temporary vector of the "transform" node
        and the reference object is returned.
        The reason for obtaining the temporary vector is to compare angle values using the temporary vector
        in the compare_angle function.

        """
        translation = mc.xform(self.object, q=1,t=1,ws=1)
        num = self.return_direction()
        translation[num] += 1
        temporary_transform = mc.createNode('transform', n='transform1' )
        mc.xform(temporary_transform, t=translation, ws=1)
        temporary_vector =\
            self.make_vector_normalize(temporary_transform)
        mc.delete(temporary_transform)
        return temporary_vector

    def return_sel_matrix(self):
        """

        Returns: 
            list:
                the matrix value of the standard object.

        """
        select_obj_matrix = mc.xform(self.object, q=1, ws=1, m=1)
        return select_obj_matrix
    
    def new_objects(self):
        """

        Returns: 
            list:
                All objects in the scene are leased and compared to the orientation
        value of the reference object, and the object with the higher value is output.

        """
        objects = []
        all_objects = mc.ls(typ='transform')

        for obj in all_objects:
            if obj is not self._object:
                obj_matrix = mc.xform(obj, q=1, ws=1, m=1)
                num = self.return_direction()
                directions = num + 12
                sel_obj = self.return_sel_matrix()
                if sel_obj[directions] < obj_matrix[directions]:
                    objects.append(obj)
            else:
                raise ValueError("The all_objects list contains self._object.")
        return objects
    
    def compare_angle(self):
        """

        Returns: 
            list:
                Retrieves the list of objects returned by the new_objects function.
        Get the vector value between the loaded objects and the reference object.
        Get the temporary vector created by the temporary_vector function.
        After obtaining the angle using two vectors and comparing it with the angle received through the setter,
        objects lower than the angle received through the setter are returned.

        """
        final_result = []
        objects = self.new_objects()
        for obj in objects:
            t_vector = self.make_vector_normalize(obj)
            temp_vector = self.temporary_vector()
            angle = temp_vector.angle(t_vector)
            m_angle = om.MAngle(angle)
            result_angle=m_angle.asDegrees()
            standard_angle=self.angle
            if result_angle < standard_angle:
                final_result.append(obj)
            else:
                raise ValueError("There are no objects at angles smaller than standard_angle.")

        return final_result

    def set_info(self):
        """

        Returns: 
            dict:
                The objects returned by the compare_angle function are made into a dictionary giving Name, Type,
        and Location as key values and output.

        """
        direction_info={}
        result=self.compare_angle()
        for obj in result:
            direction_info["Name"]=obj
            shape=mc.listRelatives(obj,s=1)
            shape_type=mc.objectType(shape)
            direction_info["Type"]=shape_type
            translate=mc.xform(obj, q=1,t=1,ws=1)
            direction_info["Location"]=translate
            print(direction_info)
