import math
class Guidance:
    def __init__(self, robot):
        self.robot = robot
        pass
    def get_marker(self, robot, include):
        # Copied from OG Robot
        precheck_markers = robot.camera.see() # gets all the markers it can see

        current_markers = []
        for markers in precheck_markers:
            # we only want certain markers, as to not run into walls
            if markers.id in include:
                current_markers.append(markers)
        markers = current_markers
        if not markers: # if we see no good markers, return false
            current_markers.clear()
            return False
        elif markers: # if we see markers, sort em and return closest
            target_marker = self.marker_sort(current_markers)
            if target_marker:
                return target_marker
        return False

    def marker_sort(self, current_markers):
        """sort markers by distance"""
        sorted_markers = []
        for marker in current_markers:
            position = self.markerpos(marker)
            sorted_markers.append(position)
        if sorted_markers:
            sorted_markers = sorted(sorted_markers, key=lambda x: x[3])  # element at index 3 is distance
            target_marker = current_markers[current_markers.index(sorted_markers[0][0])]
            return target_marker
        return False

    def markerpos(self,marker):
        # Spits out various info in relatiuon to visible markers, only needed for sorting so dont really care
        '''
        :param marker: sr.robot3 marker
        :return: [marker, ho, vo, distance]
        '''
        return [marker, marker.position.horizontal_angle, marker.position.vertical_angle, marker.position.distance]

    def movement_calculate(self,target):
        # converts radians to degrees
        mov_angle = math.degrees(target.position.horizontal_angle)
        return [mov_angle, target.position.distance]

    def angle_check(self,angle):
        if angle > 0:
            return 1  # 1 is right
        elif angle < 0:
            return -1  # -1 is left
        else:
            return 0

    def IRCCM(self, timeout, target):
        """
        IRCCM - Infrared Counter Countermeasure
        the thing missles have to ignore flares
        and what we will use to ignore motionblur
        hopefully

        :return:
        """
        start_time = self.robot.time()
        end_time  = start_time + timeout
        while self.robot.time() < end_time: # for the period of time
            markers = self.robot.camera.see() # scan for marker
            if markers:
                for marker in markers:
                    if marker.id == target.id: # if we find it return True
                        return True
        return False # else return False
