
import re

PATTERN = re.compile(r"""(?P<lat_deg>\d+)°      # Latitude Degrees
                         (?:(?P<lat_min>\d+)')? # Latitude Minutes (Optional)
                         (?:(?P<lat_sec>\d+)")? # Latitude Seconds (Optional)
                         (?P<north_south>[NS])  # North or South
                         ,[ ]
                         (?P<lon_deg>\d+)°      # Longitude Degrees
                         (?:(?P<lon_min>\d+)')? # Longitude Minutes (Optional)
                         (?:(?P<lon_sec>\d+)")? # Longitude Seconds (Optional)
                         (?P<east_west>[EW])    # East or West
                      """, re.VERBOSE)

LAT_FIELDS = ("lat_deg", "lat_min", "lat_sec")
LON_FIELDS = ("lon_deg", "lon_min", "lon_sec")

# def parse_dms_string(s, out_type=float):
#     """
#     Convert a string of the following form to a tuple of out_type latitude, longitude.

#     Example input:
#     0°25'30"S, 91°7'W
#     """
#     values = PATTERN.match(s).groupdict()

#     return tuple(sum(out_type(values[field] or 0) / out_type(60 ** idx) for idx, field in enumerate(field_names)) for field_names in (LAT_FIELDS, LON_FIELDS))


def parse_dms_string(s, out_type=float):
    """
    Convert a string of the following form to a tuple of out_type latitude, longitude.

    Example input:
    0°25'30"S, 91°7'W
    """
    
    m_obj = PATTERN.match(s)
    print({m_obj})
    if m_obj:
        values = m_obj.groupdict()
    else:
        raise Exception(f'Input string {s} does not match pattern!')

    return tuple(sum(out_type(values[field] or 0) / out_type(60 ** idx) for idx, field in enumerate(field_names)) for field_names in (LAT_FIELDS, LON_FIELDS))


# INPUT = """0°25'30"S, 91°7'W"""
# print(parse_dms_string(INPUT)) # Prints: (0.42500000000000004, 91.11666666666666)

