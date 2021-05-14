@staticmethod
def format_point(point: list):
    """ get formatted sps string from Point objects"""
    pattern = "%1s%10.2f%10.2f  %1d%2s            %2d      %9.1f%10.1f%6.1f%3d%6s"

    return pattern % (
        point[0],
        point[1],
        point[2],
        point[3],
        point[4] if point[4] is not None else '',
        point[5] if point[5] is not None else 0,
        point[6],
        point[7],
        point[8] if point[8] is not None else 0.0,
        point[9] if point[9] is not None else 0,
        point[10] if point[10] is not None else ''
    )


# @staticmethod
def format_relation(relation: list):
    """ get formatted sps string from Point objects"""
    pattern = "%1s%6s%8i%1i%1s%10.2f%10.2f%1i%5i%5i%1i%10.2f%10.2f%10.2f%1i"
    return pattern % (
        relation[0],
        relation[1] if relation[1] is not None else 0,
        relation[2],
        relation[3],
        relation[4],
        relation[5],
        relation[6],
        relation[7],
        relation[8],
        relation[9],
        relation[10],
        relation[11],
        relation[12],
        relation[13],
        relation[14]
    )
