zone0 = [i for i in range(2, 5)]
zone1 = [i for i in range(9, 12)]
zone3 = [i for i in range(16, 19)]
zone4 = [i for i in range(23, 26)]

high_rise_0 = [195]
high_rise_1 = [196]
high_rise_2 = [197]
high_rise_3 = [198]

zone0_pallets = [i for i in range(100, 120)]
zone1_pallets = [i for i in range(121, 140)]
zone2_pallets = [i for i in range(141, 160)]
zone3_pallets = [i for i in range(160, 180)]
def zone_parse(zone: int) -> list[int]:
    """
    Checks which zone the robot is in
    :param zone: the starting zone the robot is placed in
    :return base: a list of the marker id's for the starting zone
    """

    match zone:
        case 0:
            zone_bound = zone0
            high_rise = high_rise_0
            zone_pallets = zone0_pallets
        case 1:
            zone_bound = zone1
            high_rise = high_rise_1
            zone_pallets = zone1_pallets
        case 2:
            zone_bound = zone1
            high_rise = high_rise_1
            zone_pallets = zone1_pallets
        case 3:
            zone_bound = zone1
            high_rise = high_rise_1
            zone_pallets = zone1_pallets
    return zone_bound, high_rise, zone_pallets

print(zone3 + zone4)
