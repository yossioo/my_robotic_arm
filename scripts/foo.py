def load_params_from_xacro():
    import rospkg
    import os

    params = {}
    rospack = rospkg.RosPack()
    pkg_path = rospack.get_path('my_robotic_arm')
    xacro_file_path = os.path.join(pkg_path, 'urdf', 'arm.xacro')

    properties = []
    with open(xacro_file_path) as f:
        line = f.readline()
        while line:
            if 'xacro:property' in line:
                properties.append(line)
            line = f.readline()

    prop = [i.strip() for i in properties]
    for i in prop:
        vals = i.split('"')
        name = vals[1]
        value = vals[3]
        params[name] = float(value)

    return params
